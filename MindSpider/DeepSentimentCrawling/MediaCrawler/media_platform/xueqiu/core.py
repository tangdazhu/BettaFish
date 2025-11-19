# -*- coding: utf-8 -*-
"""雪球平台爬虫主流程"""

import asyncio
import os
from asyncio import Task
import json
import hashlib
from typing import Dict, List, Optional
from urllib.parse import urlencode, quote_plus

from playwright.async_api import (
    BrowserContext,
    BrowserType,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

import config
from base.base_crawler import AbstractCrawler
from proxy.proxy_ip_pool import IpInfoModel, create_ip_pool
from store import xueqiu as xueqiu_store
from tools import utils
from tools.cdp_browser import CDPBrowserManager
from var import crawler_type_var, source_keyword_var

from .client import XueQiuClient
from .help import extract_comment_basic, extract_creator_basic, extract_status_basic
from .login import XueQiuLogin

from config import xueqiu_config as xq_config


class XueQiuCrawler(AbstractCrawler):
    """雪球平台爬虫"""

    context_page: BrowserContext
    browser_context: BrowserContext
    xq_client: XueQiuClient
    cdp_manager: Optional[CDPBrowserManager]

    def __init__(self) -> None:
        self.index_url = "https://xueqiu.com"
        self.user_agent = utils.get_user_agent()
        self.cdp_manager = None

    async def start(self) -> None:
        """启动雪球爬虫"""

        playwright_proxy_format, httpx_proxy_format = None, None
        if config.ENABLE_IP_PROXY:
            ip_proxy_pool = await create_ip_pool(
                config.IP_PROXY_POOL_COUNT,
                enable_validate_ip=True,
            )
            ip_proxy_info: IpInfoModel = await ip_proxy_pool.get_proxy()
            playwright_proxy_format, httpx_proxy_format = utils.format_proxy_info(
                ip_proxy_info
            )

        async with async_playwright() as playwright:
            if config.ENABLE_CDP_MODE:
                utils.logger.info("[XueQiuCrawler] 使用 CDP 模式启动浏览器")
                self.browser_context = await self.launch_browser_with_cdp(
                    playwright,
                    playwright_proxy_format,
                    self.user_agent,
                    headless=config.CDP_HEADLESS,
                )
            else:
                utils.logger.info("[XueQiuCrawler] 使用标准模式启动浏览器")
                chromium = playwright.chromium
                self.browser_context = await self.launch_browser(
                    chromium,
                    playwright_proxy_format,
                    self.user_agent,
                    headless=config.HEADLESS,
                )
                await self.browser_context.add_init_script(path="libs/stealth.min.js")

            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(self.index_url, wait_until="domcontentloaded")

            self.xq_client = await self.create_xueqiu_client(httpx_proxy_format)
            if await self.xq_client.pong():
                utils.logger.info("[XueQiuCrawler] 当前浏览器已登录，直接复用 Cookie")
            else:
                utils.logger.info("[XueQiuCrawler] 检测到未登录，开始执行登录流程")
                login_obj = XueQiuLogin(
                    login_type=config.LOGIN_TYPE,
                    browser_context=self.browser_context,
                    context_page=self.context_page,
                    login_phone=config.LOGIN_PHONE,
                    cookie_str=config.COOKIES,
                )
                await login_obj.begin()
                await self.xq_client.update_cookies(self.browser_context)
                utils.logger.info("[XueQiuCrawler] 登录成功，已刷新 httpx Cookie")

            crawler_type_var.set(config.CRAWLER_TYPE)
            if config.CRAWLER_TYPE == "search":
                await self.search()
            elif config.CRAWLER_TYPE == "detail":
                await self.get_specified_status()
            elif config.CRAWLER_TYPE == "creator":
                await self.get_creators_and_notes()
            else:
                utils.logger.warning(
                    f"[XueQiuCrawler] 不支持的 CRAWLER_TYPE: {config.CRAWLER_TYPE}"
                )

    async def search(self) -> None:
        """根据关键词搜索雪球帖子"""

        utils.logger.info("[XueQiuCrawler.search] 开始搜索雪球帖子")
        max_notes = max(config.CRAWLER_MAX_NOTES_COUNT, xq_config.XUEQIU_SEARCH_COUNT)
        start_page = max(config.START_PAGE, 1)
        for keyword in config.KEYWORDS.split(","):
            keyword = keyword.strip()
            if not keyword:
                continue
            source_keyword_var.set(keyword)
            utils.logger.info(f"[XueQiuCrawler.search] 当前关键词: {keyword}")
            collected = 0
            page = start_page
            while collected < max_notes and page <= xq_config.XUEQIU_MAX_SEARCH_PAGE:
                status_list = await self._fetch_search_status_via_page(
                    keyword=keyword,
                    page=page,
                    count=xq_config.XUEQIU_SEARCH_COUNT,
                )
                if not status_list:
                    utils.logger.info("[XueQiuCrawler.search] 无更多内容，停止翻页")
                    break

                status_id_list: List[str] = []
                for status_item in status_list:
                    await self._persist_status(status_item)
                    status_id = str(status_item.get("id"))
                    if status_id:
                        status_id_list.append(status_id)
                    collected += 1
                    if collected >= max_notes:
                        break

                await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)
                await self.batch_get_comments(status_id_list)

                page += 1

    async def _fetch_search_status_via_page(
        self, keyword: str, page: int, count: int
    ) -> List[Dict]:
        """通过 DOM 解析方式获取雪球搜索结果，规避 WAF"""

        encoded_keyword = quote_plus(keyword)
        search_url = f"{self.index_url}/k?q={encoded_keyword}&page={page}"
        await self.context_page.goto(search_url, wait_until="domcontentloaded")
        await self._wait_visit_verify_resolved()
        try:
            await self.context_page.wait_for_selector(
                "div.search_type_title",
                timeout=30000,
            )
        except PlaywrightTimeoutError:
            utils.logger.warning(
                f"[XueQiuCrawler] 关键词 {keyword} 第 {page} 页未加载搜索页框架"
            )
            return []

        # 尝试点击“讨论”tab，确保加载帖子流
        try:
            discussion_tab = self.context_page.locator(
                "div.search_type_title >> text=讨论"
            )
            if await discussion_tab.count():
                await discussion_tab.first.click()
                await asyncio.sleep(1)
        except Exception:  # noqa: BLE001
            utils.logger.debug("[XueQiuCrawler] 点击讨论 tab 失败，继续尝试解析")

        await self.context_page.evaluate(
            "window.scrollTo(0, document.body.scrollHeight / 2)"
        )
        await self._wait_visit_verify_resolved()
        try:
            await self.context_page.wait_for_selector(
                "article.timeline_item",
                timeout=20000,
            )
        except PlaywrightTimeoutError:
            utils.logger.warning(
                f"[XueQiuCrawler] 关键词 {keyword} 第 {page} 页未找到讨论列表"
            )
            return []

        posts: List[Dict[str, str]] = await self.context_page.evaluate(
            """
            () => {
                const toText = (el) => (el ? el.textContent.trim() : "");
                const normalizeLink = (href) => {
                    if (!href) return "";
                    if (href.startsWith("http")) return href;
                    return `https://xueqiu.com${href}`;
                };
                return Array.from(document.querySelectorAll("article.timeline_item"))
                    .map((item) => {
                        const authorLink = item.querySelector(".user-name");
                        const authorHref = authorLink?.getAttribute("href") || "";
                        const userIdMatch = authorHref.match(/\d+/);
                        const userId = userIdMatch ? userIdMatch[0] : "";
                        const avatar = item.querySelector(".avatar img, img.avatar");
                        const detailLink = item.querySelector(".date-and-source");
                        const statusHref = detailLink?.getAttribute("href") || "";
                        const statusId = detailLink?.dataset?.id || (statusHref.match(/\d+/) || [""])[0];
                        const textContainer = item.querySelector(".timeline_item_bd") || item.querySelector(".timeline_item_ft");
                        const text = textContainer ? textContainer.innerText.trim() : "";
                        return {
                            id: statusId,
                            text,
                            created_at_text: toText(detailLink),
                            status_href: normalizeLink(statusHref),
                            user_id: userId,
                            user_name: toText(authorLink),
                            avatar: avatar ? avatar.src : "",
                        };
                    })
                    .filter((post) => post.id || post.text);
            }
        """
        )

        utils.logger.info(
            f"[XueQiuCrawler] 关键词 {keyword} 第 {page} 页解析到 {len(posts)} 条帖子"
        )
        status_list: List[Dict] = []
        for post in posts[:count]:
            status_id = (
                post.get("id")
                or hashlib.md5(
                    (post.get("status_href") or post.get("text") or keyword).encode(
                        "utf-8"
                    )
                ).hexdigest()
            )
            status = {
                "id": status_id,
                "type": "timeline",
                "title": "",
                "text": post.get("text", ""),
                "topic_desc": keyword,
                "source": "dom_search",
                "created_at": post.get("created_at_text", ""),
                "user": {
                    "id": post.get("user_id", ""),
                    "screen_name": post.get("user_name", ""),
                    "profile_image_url": post.get("avatar", ""),
                },
                "status_url": post.get("status_href", ""),
                "like_count": 0,
                "reply_count": 0,
                "retweet_count": 0,
            }
            status_list.append(status)

        return status_list

    async def _wait_visit_verify_resolved(self, timeout: int = 60000) -> None:
        """等待访问验证滑块被处理完毕"""

        candidates = [
            self.context_page.locator("text=访问验证"),
            self.context_page.locator("div.visit-verify"),
            self.context_page.locator(".visit-verify__container"),
        ]
        is_verifying = False
        for locator in candidates:
            if await locator.count():
                is_verifying = True
                break
        if not is_verifying:
            return

        utils.logger.warning(
            "[XueQiuCrawler] 检测到访问验证，请在浏览器中完成滑块操作，系统将等待其消失"
        )
        for locator in candidates:
            try:
                await locator.wait_for(state="detached", timeout=timeout)
                return
            except PlaywrightTimeoutError:
                continue
        raise RuntimeError("雪球访问验证长时间未通过，请手动刷新页面后重试")

    async def get_specified_status(self) -> None:
        """抓取配置中的指定状态"""

        if not xq_config.XUEQIU_SPECIFIED_STATUS_IDS:
            utils.logger.info("[XueQiuCrawler.get_specified_status] 未配置指定 ID")
            return

        status_ids = xq_config.XUEQIU_SPECIFIED_STATUS_IDS
        status_details = await asyncio.gather(
            *[self._get_status_detail_task(status_id) for status_id in status_ids]
        )
        need_comment_ids = []
        for detail in status_details:
            if not detail:
                continue
            await self._persist_status(detail)
            need_comment_ids.append(str(detail.get("id")))
        await self.batch_get_comments(need_comment_ids)

    async def get_creators_and_notes(self) -> None:
        """抓取创作者及其笔记"""

        if not xq_config.XUEQIU_CREATOR_ID_LIST:
            utils.logger.info("[XueQiuCrawler.get_creators_and_notes] 未配置创作者 ID")
            return

        for creator_id in xq_config.XUEQIU_CREATOR_ID_LIST:
            utils.logger.info(
                f"[XueQiuCrawler.get_creators_and_notes] 处理创作者: {creator_id}"
            )
            creator_profile = await self.xq_client.get_creator_profile(creator_id)
            creator_data = extract_creator_basic(creator_profile)
            if creator_data:
                await xueqiu_store.save_creator(creator_data)

            page = 1
            status_id_list: List[str] = []
            while page <= xq_config.XUEQIU_MAX_SEARCH_PAGE:
                timeline_res = await self.xq_client.get_creator_statuses(
                    creator_id,
                    page=page,
                    count=xq_config.XUEQIU_SEARCH_COUNT,
                )
                statuses = timeline_res.get("list", [])
                if not statuses:
                    break
                for status_item in statuses:
                    await self._persist_status(status_item)
                    status_id = str(status_item.get("id"))
                    if status_id:
                        status_id_list.append(status_id)
                page += 1
                await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)

            await self.batch_get_comments(status_id_list)

    async def batch_get_comments(self, status_id_list: List[str]) -> None:
        """批量获取评论"""

        if not config.ENABLE_GET_COMMENTS:
            utils.logger.info("[XueQiuCrawler.batch_get_comments] 评论抓取未开启")
            return
        if not status_id_list:
            return

        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        tasks: List[Task] = []
        for status_id in status_id_list:
            if not status_id:
                continue
            tasks.append(
                asyncio.create_task(
                    self._fetch_status_comments(status_id, semaphore),
                    name=status_id,
                )
            )
        await asyncio.gather(*tasks)

    async def _fetch_status_comments(
        self,
        status_id: str,
        semaphore: asyncio.Semaphore,
    ) -> None:
        """抓取单条帖子的评论"""

        async with semaphore:
            utils.logger.info(
                f"[XueQiuCrawler._fetch_status_comments] 获取状态 {status_id} 评论"
            )
            fetched = 0
            page = 1
            page_size = xq_config.XUEQIU_COMMENT_PAGE_SIZE
            max_comments = config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES
            while fetched < max_comments:
                resp = await self.xq_client.get_status_comments(
                    status_id,
                    page=page,
                    size=page_size,
                )
                comment_list = self._extract_comment_list(resp)
                if not comment_list:
                    break

                parsed_comments = [
                    extract_comment_basic(comment)
                    for comment in comment_list
                    if comment
                ]
                parsed_comments = [item for item in parsed_comments if item]

                if parsed_comments:
                    await xueqiu_store.batch_update_comments(status_id, parsed_comments)
                fetched += len(parsed_comments)

                await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)
                if len(comment_list) < page_size:
                    break
                page += 1

    async def _persist_status(self, status_item: Dict) -> None:
        """写库雪球帖子"""

        if not status_item:
            return
        status_data = extract_status_basic(status_item)
        await xueqiu_store.update_single_status(status_data)

    async def _get_status_detail_task(self, status_id: str) -> Optional[Dict]:
        """并发获取帖子详情"""

        if not status_id:
            return None
        try:
            detail = await self.xq_client.get_status_detail(status_id)
            await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)
            return detail
        except DataFetchError as exc:
            utils.logger.error(
                f"[XueQiuCrawler._get_status_detail_task] 获取 {status_id} 详情失败: {exc}"
            )
            return None

    def _extract_comment_list(self, resp: Dict) -> List[Dict]:
        """兼容不同字段的评论列表解析"""

        if not resp:
            return []
        if isinstance(resp, dict):
            if isinstance(resp.get("list"), list):
                return resp.get("list", [])
            if isinstance(resp.get("comments"), list):
                return resp.get("comments", [])
            if isinstance(resp.get("data"), dict):
                data_node = resp.get("data", {})
                if isinstance(data_node.get("list"), list):
                    return data_node.get("list", [])
                if isinstance(data_node.get("comments"), list):
                    return data_node.get("comments", [])
        return []

    async def create_xueqiu_client(
        self,
        httpx_proxy: Optional[str],
    ) -> XueQiuClient:
        """创建雪球客户端"""

        utils.logger.info("[XueQiuCrawler.create_xueqiu_client] 初始化客户端")
        cookie_str, cookie_dict = utils.convert_cookies(
            await self.browser_context.cookies()
        )
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "origin": "https://xueqiu.com",
            "referer": "https://xueqiu.com/",
            "user-agent": self.user_agent,
            "Cookie": cookie_str,
        }
        return XueQiuClient(
            headers=headers,
            playwright_page=self.context_page,
            cookie_dict=cookie_dict,
            proxy=httpx_proxy,
        )

    async def launch_browser(
        self,
        chromium: BrowserType,
        playwright_proxy: Optional[Dict],
        user_agent: Optional[str],
        headless: bool = True,
    ) -> BrowserContext:
        """创建浏览器上下文"""

        utils.logger.info("[XueQiuCrawler.launch_browser] 创建浏览器上下文")
        if config.SAVE_LOGIN_STATE:
            user_data_dir = os.path.join(
                os.getcwd(),
                "browser_data",
                config.USER_DATA_DIR % config.PLATFORM,
            )
            browser_context = await chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                accept_downloads=True,
                headless=headless,
                proxy=playwright_proxy,
                viewport={"width": 1920, "height": 1080},
                user_agent=user_agent,
            )
            return browser_context
        browser = await chromium.launch(headless=headless, proxy=playwright_proxy)
        browser_context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=user_agent,
        )
        return browser_context

    async def launch_browser_with_cdp(
        self,
        playwright: Playwright,
        playwright_proxy: Optional[Dict],
        user_agent: Optional[str],
        headless: bool = True,
    ) -> BrowserContext:
        """CDP 模式启动浏览器"""

        try:
            self.cdp_manager = CDPBrowserManager()
            browser_context = await self.cdp_manager.launch_and_connect(
                playwright=playwright,
                playwright_proxy=playwright_proxy,
                user_agent=user_agent,
                headless=headless,
            )
            return browser_context
        except Exception as exc:  # noqa: BLE001
            utils.logger.error(f"[XueQiuCrawler] CDP 启动失败，回退标准模式: {exc}")
            chromium = playwright.chromium
            return await self.launch_browser(
                chromium,
                playwright_proxy,
                user_agent,
                headless,
            )

    async def close(self) -> None:
        """关闭浏览器上下文"""

        if self.cdp_manager:
            await self.cdp_manager.cleanup()
            self.cdp_manager = None
        elif self.browser_context:
            await self.browser_context.close()
        utils.logger.info("[XueQiuCrawler] 浏览器上下文已关闭")


__all__ = ["XueQiuCrawler"]
