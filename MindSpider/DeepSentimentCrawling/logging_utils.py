# -*- coding: utf-8 -*-
"""平台日志工具模块，确保不同平台使用独立日志文件"""

from pathlib import Path
from loguru import logger

PROJECT_ROOT = Path(__file__).parent.parent

PLATFORM_NAME_MAP = {
    "xhs": "xiaohongshu",
    "dy": "douyin",
    "ks": "kuaishou",
    "bili": "bilibili",
    "wb": "weibo",
    "tieba": "tieba",
    "zhihu": "zhihu",
    "xueqiu": "xueqiu",
}


def setup_platform_logger(platform: str) -> int:
    """为指定平台创建日志文件并返回 handler id"""
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    platform_name = PLATFORM_NAME_MAP.get(platform, platform)
    log_file = logs_dir / f"{platform_name}.log"

    handler_id = logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    logger.info("=" * 60)
    logger.info(f"平台 {platform} ({platform_name}) 的日志已启用")
    logger.info(f"日志文件: {log_file}")
    logger.info("=" * 60)
    return handler_id
