# -*- coding: utf-8 -*-
"""雪球平台登录实现"""

import asyncio
import functools
import sys
from typing import Optional

from playwright.async_api import BrowserContext, Page
from tenacity import RetryError, retry, retry_if_result, stop_after_attempt, wait_fixed

import config
from base.base_crawler import AbstractLogin
from cache.cache_factory import CacheFactory
from tools import utils


class XueQiuLogin(AbstractLogin):
    """雪球平台登录器"""

    def __init__(
        self,
        login_type: str,
        browser_context: BrowserContext,
        context_page: Page,
        login_phone: Optional[str] = "",
        cookie_str: str = "",
    ) -> None:
        config.LOGIN_TYPE = login_type
        self.browser_context = browser_context
        self.context_page = context_page
        self.login_phone = login_phone or ""
        self.cookie_str = cookie_str or ""
        self.login_url = "https://xueqiu.com/"

    @retry(
        stop=stop_after_attempt(120),
        wait=wait_fixed(1),
        retry=retry_if_result(lambda value: value is False),
    )
    async def check_login_state(self, empty_token: str) -> bool:
        """轮询浏览器 Cookie，判断是否已经登录成功"""
        current_cookie = await self.browser_context.cookies()
        _, cookie_dict = utils.convert_cookies(current_cookie)
        xq_token = cookie_dict.get("xq_a_token", "")
        user_token = cookie_dict.get("u", "")
        if xq_token and user_token and (xq_token != empty_token):
            return True
        return False

    async def begin(self) -> None:
        """根据配置的登录方式启动登录流程"""
        utils.logger.info("[XueQiuLogin.begin] 开始雪球登录流程 ...")
        if config.LOGIN_TYPE == "qrcode":
            await self.login_by_qrcode()
        elif config.LOGIN_TYPE == "phone":
            await self.login_by_mobile()
        elif config.LOGIN_TYPE == "cookie":
            await self.login_by_cookies()
        else:
            raise ValueError("[XueQiuLogin.begin] 仅支持 qrcode/phone/cookie 登录方式")

    async def _open_login_dialog(self) -> None:
        """确保登录弹窗被打开，并尽量定位到弹窗容器"""
        dialog_locator = "xpath=//div[contains(@class,'login') and (contains(@class,'dialog') or contains(@class,'modal') or contains(@class,'container'))]"
        for attempt in range(3):
            dialog = await self.context_page.query_selector(dialog_locator)
            if dialog:
                return
            try:
                login_button = await self.context_page.wait_for_selector(
                    "xpath=//a[contains(@class,'login') or contains(text(),'登录')]",
                    timeout=5000,
                )
                await login_button.click()
                await self.context_page.wait_for_selector(dialog_locator, timeout=5000)
                return
            except Exception:  # noqa: BLE001
                utils.logger.info(
                    f"[XueQiuLogin._open_login_dialog] 第 {attempt + 1} 次尝试未弹出登录框，继续重试"
                )
            await asyncio.sleep(1)
        raise RuntimeError(
            "[XueQiuLogin._open_login_dialog] 未能打开登录弹窗，请检查页面结构"
        )

    async def _is_logged_in_ui(self) -> bool:
        """通过页面元素判断是否已登录"""
        selectors = [
            "xpath=//button[contains(text(),'发帖')]",
            "xpath=//a[contains(text(),'发帖')]",
            "xpath=//div[contains(@class,'user') and contains(@class,'avatar')]",
            "xpath=//a[contains(@href,'/u/') and (contains(@class,'user') or contains(@class,'menu') or contains(@class,'profile'))]",
        ]
        for selector in selectors:
            try:
                element = await self.context_page.query_selector(selector)
            except Exception:  # noqa: BLE001
                continue
            if element:
                utils.logger.info("[XueQiuLogin] 检测到页面已登录，跳过登录流程")
                return True
        return False

    async def _switch_to_qrcode_tab(self) -> None:
        """切换到二维码登录选项"""
        try:
            qr_tab = await self.context_page.wait_for_selector(
                "xpath=//*[contains(text(),'二维码登录')]",
                timeout=5000,
            )
            await qr_tab.click()
            await asyncio.sleep(0.5)
        except Exception:  # noqa: BLE001
            utils.logger.info(
                "[XueQiuLogin._switch_to_qrcode_tab] 未找到二维码登录选项，可能已在二维码模式"
            )

    async def login_by_qrcode(self) -> None:
        """通过二维码方式登录雪球"""
        await self.context_page.goto(self.login_url, wait_until="domcontentloaded")
        if await self._is_logged_in_ui():
            return
        await self._open_login_dialog()
        await self._switch_to_qrcode_tab()
        modal_qrcode_selector = (
            "xpath=(//div[contains(@class,'login') and (contains(@class,'dialog') or contains(@class,'modal') or contains(@class,'container'))]//img"
            "[contains(@src,'qrcode') or contains(@class,'qrcode')])[1]"
        )
        fallback_selectors = [
            modal_qrcode_selector,
            "xpath=//img[contains(@class,'qrcode-img') or contains(@src,'login_qrcode')]",
            "xpath=//div[contains(@class,'login')]//img[contains(@src,'qrcode')]",
        ]
        base64_qrcode_img = None
        for selector in fallback_selectors:
            base64_qrcode_img = await utils.find_login_qrcode(
                self.context_page, selector=selector
            )
            if base64_qrcode_img:
                break
        if not base64_qrcode_img:
            utils.logger.warning(
                "[XueQiuLogin.login_by_qrcode] 未能截取二维码，将使用浏览器页面上的二维码，请手动扫码"
            )

        current_cookie = await self.browser_context.cookies()
        _, cookie_dict = utils.convert_cookies(current_cookie)
        no_logged_token = cookie_dict.get("xq_a_token", "")

        if base64_qrcode_img:
            partial_show_qrcode = functools.partial(
                utils.show_qrcode, base64_qrcode_img
            )
            asyncio.get_running_loop().run_in_executor(
                executor=None, func=partial_show_qrcode
            )
            utils.logger.info("[XueQiuLogin.login_by_qrcode] 请在 120 秒内完成扫码")
        else:
            utils.logger.info(
                "[XueQiuLogin.login_by_qrcode] 请直接在浏览器页面完成扫码，系统将轮询登录态"
            )
        try:
            await self.check_login_state(no_logged_token)
        except RetryError:
            utils.logger.error("[XueQiuLogin.login_by_qrcode] 二维码登录失败或超时")
            sys.exit()
        await asyncio.sleep(5)
        utils.logger.info("[XueQiuLogin.login_by_qrcode] 登录成功")

    async def login_by_mobile(self) -> None:
        """通过短信验证码登录雪球"""
        if not self.login_phone:
            raise ValueError(
                "[XueQiuLogin.login_by_mobile] LOGIN_PHONE 未配置，无法进行手机号登录"
            )
        await self.context_page.goto(self.login_url, wait_until="domcontentloaded")
        if await self._is_logged_in_ui():
            return
        await self._open_login_dialog()
        try:
            switch_btn = await self.context_page.wait_for_selector(
                "xpath=//div[contains(@class,'phone-login') or contains(@class,'switch-phone')]",
                timeout=5000,
            )
            await switch_btn.click()
        except Exception:  # noqa: BLE001
            utils.logger.info(
                "[XueQiuLogin.login_by_mobile] 未找到切换到手机号登录的按钮，可能默认已展示"
            )

        login_container = await self.context_page.wait_for_selector(
            "xpath=//div[contains(@class,'login')]", timeout=10000
        )
        phone_input = await login_container.query_selector(
            "input[type='tel'], input[name='tel'], input[placeholder*='手机号']"
        )
        if not phone_input:
            raise RuntimeError("[XueQiuLogin.login_by_mobile] 未定位到手机号输入框")
        await phone_input.fill(self.login_phone)
        await asyncio.sleep(0.5)

        send_btn = await login_container.query_selector(
            "xpath=.//button[contains(@class,'send') or contains(text(),'验证码')]"
        )
        if not send_btn:
            raise RuntimeError("[XueQiuLogin.login_by_mobile] 未定位到发送验证码按钮")
        await send_btn.click()

        sms_input = await login_container.query_selector(
            "xpath=.//input[@type='text' or @maxlength='6']"
        )
        submit_btn = await login_container.query_selector(
            "xpath=.//button[contains(@class,'login') or contains(text(),'登录')]"
        )
        if not sms_input or not submit_btn:
            raise RuntimeError(
                "[XueQiuLogin.login_by_mobile] 未定位到验证码输入框或登录按钮"
            )

        cache_client = CacheFactory.create_cache(config.CACHE_TYPE_MEMORY)
        remain_seconds = 120
        current_cookie = await self.browser_context.cookies()
        _, cookie_dict = utils.convert_cookies(current_cookie)
        no_logged_token = cookie_dict.get("xq_a_token", "")

        while remain_seconds > 0:
            await asyncio.sleep(1)
            sms_code = cache_client.get(f"xq_{self.login_phone}")
            if not sms_code:
                remain_seconds -= 1
                continue
            await sms_input.fill(sms_code.decode())
            await asyncio.sleep(0.5)
            try:
                consent_checkbox = await login_container.query_selector(
                    "xpath=.//input[@type='checkbox']/.."
                )
                if consent_checkbox:
                    await consent_checkbox.click()
            except Exception:  # noqa: BLE001
                pass
            await submit_btn.click()
            break
        else:
            raise TimeoutError("[XueQiuLogin.login_by_mobile] 等待短信验证码超时")

        try:
            await self.check_login_state(no_logged_token)
        except RetryError:
            utils.logger.error("[XueQiuLogin.login_by_mobile] 手机号登录失败")
            sys.exit()
        await asyncio.sleep(5)
        utils.logger.info("[XueQiuLogin.login_by_mobile] 登录成功")

    async def login_by_cookies(self) -> None:
        """通过预置 Cookie 登录雪球"""
        if not self.cookie_str:
            raise ValueError("[XueQiuLogin.login_by_cookies] 未提供 COOKIE，无法注入")
        cookie_dict = utils.convert_str_cookie_to_dict(self.cookie_str)
        if not cookie_dict:
            raise ValueError("[XueQiuLogin.login_by_cookies] COOKIE 格式不正确")
        cookie_items = []
        for key, value in cookie_dict.items():
            cookie_items.append(
                {
                    "name": key,
                    "value": value,
                    "domain": ".xueqiu.com",
                    "path": "/",
                }
            )
        await self.browser_context.add_cookies(cookie_items)
        utils.logger.info("[XueQiuLogin.login_by_cookies] 已注入自定义 Cookie")
