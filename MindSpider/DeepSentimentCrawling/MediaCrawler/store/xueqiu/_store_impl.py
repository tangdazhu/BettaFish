# -*- coding: utf-8 -*-
"""雪球平台数据存储实现"""

from typing import Dict

import config
from base.base_crawler import AbstractStore
from database.db_session import get_session
from database.models import XueqiuStatus, XueqiuComment, XueqiuCreator
from sqlalchemy import select
from tools import utils
from tools.async_file_writer import AsyncFileWriter
from var import crawler_type_var


class XueQiuCsvStoreImplement(AbstractStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.writer = AsyncFileWriter(
            platform="xueqiu", crawler_type=crawler_type_var.get()
        )

    async def store_content(self, content_item: Dict):
        await self.writer.write_to_csv(item_type="contents", item=content_item)

    async def store_comment(self, comment_item: Dict):
        await self.writer.write_to_csv(item_type="comments", item=comment_item)

    async def store_creator(self, creator: Dict):
        await self.writer.write_to_csv(item_type="creators", item=creator)


class XueQiuJsonStoreImplement(AbstractStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.writer = AsyncFileWriter(
            platform="xueqiu", crawler_type=crawler_type_var.get()
        )

    async def store_content(self, content_item: Dict):
        await self.writer.write_single_item_to_json(
            item_type="contents", item=content_item
        )

    async def store_comment(self, comment_item: Dict):
        await self.writer.write_single_item_to_json(
            item_type="comments", item=comment_item
        )

    async def store_creator(self, creator: Dict):
        await self.writer.write_single_item_to_json(item_type="creators", item=creator)


class XueQiuDbStoreImplement(AbstractStore):
    async def store_content(self, content_item: Dict):
        status_id = content_item.get("status_id")
        if not status_id:
            return

        async with get_session() as session:
            stmt = select(XueqiuStatus).where(XueqiuStatus.status_id == status_id)
            res = await session.execute(stmt)
            db_status = res.scalar_one_or_none()
            if db_status:
                db_status.last_modify_ts = utils.get_current_timestamp()
                for key, value in content_item.items():
                    if hasattr(db_status, key):
                        setattr(db_status, key, value)
            else:
                content_item["add_ts"] = utils.get_current_timestamp()
                content_item["last_modify_ts"] = utils.get_current_timestamp()
                db_status = XueqiuStatus(**content_item)
                session.add(db_status)
            await session.commit()

    async def store_comment(self, comment_item: Dict):
        comment_id = comment_item.get("comment_id")
        if not comment_id:
            return

        async with get_session() as session:
            stmt = select(XueqiuComment).where(XueqiuComment.comment_id == comment_id)
            res = await session.execute(stmt)
            db_comment = res.scalar_one_or_none()
            if db_comment:
                db_comment.last_modify_ts = utils.get_current_timestamp()
                for key, value in comment_item.items():
                    if hasattr(db_comment, key):
                        setattr(db_comment, key, value)
            else:
                comment_item["add_ts"] = utils.get_current_timestamp()
                comment_item["last_modify_ts"] = utils.get_current_timestamp()
                db_comment = XueqiuComment(**comment_item)
                session.add(db_comment)
            await session.commit()

    async def store_creator(self, creator: Dict):
        user_id = creator.get("user_id")
        if not user_id:
            return

        async with get_session() as session:
            stmt = select(XueqiuCreator).where(XueqiuCreator.user_id == user_id)
            res = await session.execute(stmt)
            db_creator = res.scalar_one_or_none()
            if db_creator:
                db_creator.last_modify_ts = utils.get_current_timestamp()
                for key, value in creator.items():
                    if hasattr(db_creator, key):
                        setattr(db_creator, key, value)
            else:
                creator["add_ts"] = utils.get_current_timestamp()
                creator["last_modify_ts"] = utils.get_current_timestamp()
                db_creator = XueqiuCreator(**creator)
                session.add(db_creator)
            await session.commit()


class XueQiuSqliteStoreImplement(XueQiuDbStoreImplement):
    """SQLite 与 DB 实现复用相同逻辑"""

    pass


class XueQiuStoreFactory:
    STORES = {
        "csv": XueQiuCsvStoreImplement,
        "json": XueQiuJsonStoreImplement,
        "db": XueQiuDbStoreImplement,
        "postgresql": XueQiuDbStoreImplement,
        "sqlite": XueQiuSqliteStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = XueQiuStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[XueQiuStoreFactory] 不支持的存储方式，请选择 csv/db/json/sqlite/postgresql"
            )
        return store_class()
