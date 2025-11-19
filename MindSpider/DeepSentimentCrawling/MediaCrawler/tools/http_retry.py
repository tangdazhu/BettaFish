# -*- coding: utf-8 -*-
"""HTTP 请求重试工具"""

from __future__ import annotations

import asyncio
import random
from typing import Awaitable, Callable, Tuple, Type, TypeVar

import httpx

from . import utils

RetryableExceptions = Tuple[Type[BaseException], ...]
T = TypeVar("T")


async def request_with_retry(
    request_coro_factory: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 3,
    base_delay: float = 2.0,
    jitter: float = 1.0,
    log_prefix: str = "",
    retry_exceptions: RetryableExceptions = (httpx.ConnectError, httpx.HTTPError),
) -> T:
    """以指数退避方式请求 HTTP 接口，降低临时网络波动带来的失败率"""

    attempt = 1
    while True:
        try:
            return await request_coro_factory()
        except retry_exceptions as exc:  # type: ignore[misc]
            if attempt >= max_attempts:
                utils.logger.error(
                    f"{log_prefix} 连接异常已重试 {attempt} 次，仍然失败: {exc}"
                )
                raise

            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, jitter)
            utils.logger.warning(
                f"{log_prefix} 捕获 {exc.__class__.__name__}，{delay:.2f}s 后进行第 {attempt + 1} 次重试"
            )
            await asyncio.sleep(delay)
            attempt += 1
