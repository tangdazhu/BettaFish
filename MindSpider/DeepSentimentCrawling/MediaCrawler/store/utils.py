# -*- coding: utf-8 -*-
"""存储层通用工具"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

__all__ = ["sanitize_text", "sanitize_dict_text"]


def sanitize_text(value: Optional[str]) -> Optional[str]:
    """去除数据库无法接受的控制字符（当前主要是 NUL）。"""
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    # PostgreSQL TEXT/BYTEA 字段不允许包含 NUL 字节
    return value.replace("\x00", "")


def sanitize_dict_text(
    data: Dict[str, Any], keys: Optional[Iterable[str]] = None
) -> None:
    """对指定字段或全部字符串字段执行 sanitize_text。"""
    if data is None:
        return
    target_keys = keys if keys is not None else data.keys()
    for key in target_keys:
        value = data.get(key)
        if isinstance(value, str) or value is None:
            data[key] = sanitize_text(value)
