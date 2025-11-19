# -*- coding: utf-8 -*-
"""雪球平台异常定义"""


class XueQiuError(Exception):
    """雪球爬虫基础异常"""


class DataFetchError(XueQiuError):
    """调用雪球接口失败"""


class AuthRequiredError(XueQiuError):
    """雪球登录状态失效"""
