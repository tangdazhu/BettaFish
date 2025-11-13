"""
Unified OpenAI-compatible LLM client for the Report Engine, with retry support.
"""

import os
import sys
from typing import Any, Dict, Optional

from openai import OpenAI
from loguru import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
utils_dir = os.path.join(project_root, "utils")
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

try:
    from retry_helper import with_retry, LLM_RETRY_CONFIG
except ImportError:
    def with_retry(config=None):
        def decorator(func):
            return func
        return decorator

    LLM_RETRY_CONFIG = None


class LLMClient:
    """Minimal wrapper around the OpenAI-compatible chat completion API."""

    def __init__(self, api_key: str, model_name: str, base_url: Optional[str] = None):
        if not api_key:
            raise ValueError("Report Engine LLM API key is required.")
        if not model_name:
            raise ValueError("Report Engine model name is required.")

        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.provider = model_name
        timeout_fallback = os.getenv("LLM_REQUEST_TIMEOUT") or os.getenv("REPORT_ENGINE_REQUEST_TIMEOUT") or "3000"
        try:
            self.timeout = float(timeout_fallback)
        except ValueError:
            self.timeout = 3000.0

        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "max_retries": 0,
        }
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    @with_retry(LLM_RETRY_CONFIG)
    def invoke(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        allowed_keys = {"temperature", "top_p", "presence_penalty", "frequency_penalty", "stream", "max_tokens"}
        extra_params = {key: value for key, value in kwargs.items() if key in allowed_keys and value is not None}
        
        # 如果没有指定 max_tokens，为 qwen-long 设置合理的默认值
        if "max_tokens" not in extra_params:
            # qwen-long 支持 32768 tokens 输出，设置为 16000 以生成长报告（约 11200-12800 字）
            extra_params["max_tokens"] = 16000
        
        # 记录实际使用的 max_tokens
        logger.info(f"LLM调用参数 - max_tokens: {extra_params.get('max_tokens')}, model: {self.model_name}")

        timeout = kwargs.pop("timeout", self.timeout)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            timeout=timeout,
            **extra_params,
        )

        if response.choices and response.choices[0].message:
            content = self.validate_response(response.choices[0].message.content)
            logger.info(f"LLM响应长度: {len(content)} 字符, finish_reason: {response.choices[0].finish_reason}")
            return content
        return ""

    @staticmethod
    def validate_response(response: Optional[str]) -> str:
        if response is None:
            return ""
        return response.strip()

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model_name,
            "api_base": self.base_url or "default",
        }
