"""
Unified OpenAI-compatible LLM client for the Media Engine, with retry support.
"""

import os
import sys
import threading
from datetime import datetime
from typing import Any, Dict, Optional

from openai import OpenAI

# Ensure project-level retry helper is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
utils_dir = os.path.join(project_root, "utils")
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

try:
    from retry_helper import with_retry, LLM_RETRY_CONFIG, InterruptedError
except ImportError:
    def with_retry(config=None, stop_event=None):
        def decorator(func):
            return func
        return decorator

    LLM_RETRY_CONFIG = None
    
    class InterruptedError(Exception):
        pass


class LLMClient:
    """
    Minimal wrapper around the OpenAI-compatible chat completion API.
    """

    def __init__(self, api_key: str, model_name: str, base_url: Optional[str] = None, stop_event: Optional[threading.Event] = None):
        if not api_key:
            raise ValueError("Media Engine LLM API key is required.")
        if not model_name:
            raise ValueError("Media Engine model name is required.")

        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.provider = model_name
        self.stop_event = stop_event
        timeout_fallback = os.getenv("LLM_REQUEST_TIMEOUT") or os.getenv("MEDIA_ENGINE_REQUEST_TIMEOUT") or "1800"
        try:
            self.timeout = float(timeout_fallback)
        except ValueError:
            self.timeout = 1800.0

        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "max_retries": 0,
        }
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    def invoke(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        @with_retry(LLM_RETRY_CONFIG, stop_event=self.stop_event)
        def _invoke_with_retry():
            if self.stop_event and self.stop_event.is_set():
                raise InterruptedError("用户请求停止")
            return self._do_invoke(system_prompt, user_prompt, **kwargs)
        return _invoke_with_retry()
    
    def _do_invoke(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        current_time = datetime.now().strftime("%Y年%m月%d日%H时%M分")
        time_prefix = f"今天的实际时间是{current_time}"
        if user_prompt:
            user_prompt = f"{time_prefix}\n{user_prompt}"
        else:
            user_prompt = time_prefix
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        allowed_keys = {"temperature", "top_p", "presence_penalty", "frequency_penalty", "stream"}
        extra_params = {key: value for key, value in kwargs.items() if key in allowed_keys and value is not None}

        timeout = kwargs.pop("timeout", self.timeout)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            timeout=timeout,
            **extra_params,
        )

        if response.choices and response.choices[0].message:
            return self.validate_response(response.choices[0].message.content)
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
