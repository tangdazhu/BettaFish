# -*- coding: utf-8 -*-
"""雪球平台 API 请求客户端"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx
from playwright.async_api import BrowserContext, Page

import config
from base.base_crawler import AbstractApiClient
from tools import utils

from .exception import AuthRequiredError, DataFetchError


class XueQiuClient(AbstractApiClient):
    """封装雪球站内 API 的 httpx 客户端"""

    def __init__(
        self,
        *,
        headers: Dict[str, str],
        playwright_page: Page,
        cookie_dict: Dict[str, str],
        timeout: int = 15,
        proxy: Optional[str] = None,
    ) -> None:
        self.headers = headers
        self.cookie_dict = cookie_dict
        self.timeout = timeout
        self.proxy = proxy
        self.playwright_page = playwright_page
        self.base_url = "https://xueqiu.com"

    async def request(self, method: str, url: str, **kwargs) -> Dict:
        """统一请求入口，处理状态码与错误上报"""

        headers = kwargs.pop("headers", self.headers)
        waf_retry = 3
        for attempt in range(waf_retry):
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    **kwargs,
                )

            # 快速检测 WAF 页面
            if response.status_code == 200 and "renderData" in response.text:
                try:
                    waf_data = self._parse_waf_payload(response.text)
                except ValueError:
                    waf_data = None
                if waf_data:
                    await self._inject_waf_cookies(waf_data)
                    headers = self.headers.copy()
                    await asyncio.sleep(1)
                    continue

            break

        if response.status_code == 401:
            raise AuthRequiredError("雪球登录状态失效，请重新登录")
        if response.status_code != 200:
            raise DataFetchError(
                f"请求 {url} 失败，状态码 {response.status_code}，响应: {response.text[:200]}"
            )

        try:
            data = response.json()
        except ValueError as exc:  # noqa: B904
            snippet = response.text[:200]
            raise DataFetchError(
                f"解析雪球响应失败: {exc}，响应片段: {snippet!r}"
            ) from exc
        if isinstance(data, dict) and data.get("error_code") not in (None, 0):
            raise DataFetchError(data.get("error_description", "雪球接口返回错误"))
        return data

    def _parse_waf_payload(self, html_text: str) -> Optional[Dict[str, str]]:
        """从 WAF 页面提取 renderData 中的 JSON"""

        marker = 'id="renderData"'
        if marker not in html_text:
            return None
        start = html_text.find("<textarea")
        if start == -1:
            return None
        end = html_text.find("</textarea>", start)
        if end == -1:
            return None
        payload_start = html_text.find(">", start) + 1
        payload = html_text[payload_start:end]
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return None
        return data

    async def _inject_waf_cookies(self, waf_payload: Dict[str, str]) -> None:
        """WAF 返回 renderData 时注入必要 Cookie"""

        cookies = []
        for key, value in waf_payload.items():
            cookies.append(
                {"name": key, "value": value, "domain": ".xueqiu.com", "path": "/"}
            )
        if not cookies:
            return
        await self.playwright_page.context.add_cookies(cookies)
        cookie_str, cookie_dict = utils.convert_cookies(
            await self.playwright_page.context.cookies()
        )
        self.cookie_dict = cookie_dict
        self.headers["Cookie"] = cookie_str

    async def update_cookies(self, browser_context: BrowserContext) -> None:
        """登录成功后刷新 Cookie"""

        cookie_str, cookie_dict = utils.convert_cookies(await browser_context.cookies())
        self.cookie_dict = cookie_dict
        self.headers["Cookie"] = cookie_str

    async def pong(self) -> bool:
        """探测当前 Cookie 是否可用"""

        headers = self.headers.copy()
        headers["Referer"] = self.base_url
        try:
            res = await self.request(
                "GET",
                f"{self.base_url}/setting/user.json",
                headers=headers,
            )
            profile = res.get("profile") or res
            return bool(profile and profile.get("uid"))
        except (DataFetchError, AuthRequiredError):
            return False

    async def search_status(
        self,
        *,
        keyword: str,
        page: int,
        count: int,
    ) -> Dict:
        """关键词搜索雪球帖子"""

        headers = self.headers.copy()
        encoded_keyword = quote(keyword, safe="")
        headers["Referer"] = f"{self.base_url}/k/{encoded_keyword}?type=11"
        params = {
            "sortId": 0,
            "page": page,
            "q": keyword,
            "source": "all",
            "comment": 0,
            "hl": 0,
            "count": count,
        }
        return await self.request(
            "GET",
            f"{self.base_url}/query/v1/search/status.json",
            headers=headers,
            params=params,
        )

    async def get_status_detail(self, status_id: str) -> Dict:
        """获取雪球帖子详情"""

        params = {"id": status_id}
        return await self.request(
            "GET",
            f"{self.base_url}/statuses/show.json",
            params=params,
        )

    async def get_status_comments(
        self,
        status_id: str,
        *,
        page: int,
        size: int,
    ) -> Dict:
        """获取帖子评论"""

        params = {
            "id": status_id,
            "page": page,
            "size": size,
        }
        return await self.request(
            "GET",
            f"{self.base_url}/statuses/comments.json",
            params=params,
        )

    async def get_creator_profile(self, user_id: str) -> Dict:
        """获取创作者信息"""

        params = {"uid": user_id}
        return await self.request(
            "GET",
            f"{self.base_url}/users/show.json",
            params=params,
        )

    async def get_creator_statuses(
        self,
        user_id: str,
        *,
        page: int,
        count: int,
    ) -> Dict:
        """获取创作者近期帖子"""

        params = {
            "user_id": user_id,
            "page": page,
            "count": count,
        }
        return await self.request(
            "GET",
            f"{self.base_url}/statuses/user_timeline.json",
            params=params,
        )
