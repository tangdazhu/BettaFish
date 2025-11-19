# -*- coding: utf-8 -*-
"""雪球平台数据存储工厂与写库入口"""

from typing import Dict, List

import config
from base.base_crawler import AbstractStore
from tools import utils
from var import source_keyword_var

from ._store_impl import (
    XueQiuCsvStoreImplement,
    XueQiuDbStoreImplement,
    XueQiuJsonStoreImplement,
    XueQiuSqliteStoreImplement,
)


class XueQiuStoreFactory:
    """雪球存储工厂"""

    STORES = {
        "csv": XueQiuCsvStoreImplement,
        "json": XueQiuJsonStoreImplement,
        "db": XueQiuDbStoreImplement,
        "sqlite": XueQiuSqliteStoreImplement,
        "postgresql": XueQiuDbStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = XueQiuStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[XueQiuStoreFactory] 不支持的存储方式，请选择 csv/db/json/sqlite/postgresql"
            )
        return store_class()


async def batch_update_status_list(status_list: List[Dict]) -> None:
    """批量写入雪球帖子"""

    if not status_list:
        return
    for status_item in status_list:
        await update_single_status(status_item)


async def update_single_status(status_item: Dict) -> None:
    """写入单条雪球帖子"""

    if not status_item:
        return

    status_item.setdefault("source_keyword", source_keyword_var.get())
    status_item.setdefault("add_ts", utils.get_current_timestamp())
    status_item["last_modify_ts"] = utils.get_current_timestamp()

    utils.logger.info(
        f"[store.xueqiu.update_single_status] status_id: {status_item.get('status_id')}, title: {status_item.get('title', '')[:24]}"
    )
    await XueQiuStoreFactory.create_store().store_content(status_item)


async def batch_update_comments(status_id: str, comments: List[Dict]) -> None:
    """批量写入雪球评论"""

    if not comments:
        return
    for comment in comments:
        await update_single_comment(status_id, comment)


async def update_single_comment(status_id: str, comment: Dict) -> None:
    """写入单条雪球评论"""

    if not comment:
        return

    comment["status_id"] = status_id
    comment.setdefault("add_ts", utils.get_current_timestamp())
    comment["last_modify_ts"] = utils.get_current_timestamp()
    await XueQiuStoreFactory.create_store().store_comment(comment)


async def save_creator(creator: Dict) -> None:
    """写入雪球创作者信息"""

    if not creator:
        return

    creator.setdefault("add_ts", utils.get_current_timestamp())
    creator["last_modify_ts"] = utils.get_current_timestamp()
    await XueQiuStoreFactory.create_store().store_creator(creator)


__all__ = [
    "XueQiuStoreFactory",
    "batch_update_status_list",
    "update_single_status",
    "batch_update_comments",
    "update_single_comment",
    "save_creator",
]
