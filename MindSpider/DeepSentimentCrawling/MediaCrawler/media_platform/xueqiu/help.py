# -*- coding: utf-8 -*-
"""雪球辅助工具函数"""

from typing import Dict, Any


def extract_status_basic(status: Dict[str, Any]) -> Dict[str, Any]:
    """提取雪球状态的核心字段，用于存储"""
    user = status.get("user", {})
    status_id = str(status.get("id"))
    return {
        "status_id": status_id,
        "status_type": status.get("type", ""),
        "title": status.get("title", ""),
        "text": status.get("text", ""),
        "target_text": status.get("target", {}).get("text", ""),
        "topic_desc": status.get("topic_desc", ""),
        "source": status.get("source", ""),
        "status_url": f"https://xueqiu.com/{user.get('id', '')}/{status_id}",
        "like_count": status.get("like_count", 0),
        "reply_count": status.get("reply_count", 0),
        "retweet_count": status.get("retweet_count", 0),
        "reward_count": status.get("reward_count", 0),
        "created_at": status.get("created_at", 0),
        "user_id": user.get("id", ""),
        "screen_name": user.get("screen_name", ""),
        "profile_image": user.get("profile_image_url", ""),
        "verified_description": user.get("verified_description", ""),
    }


def extract_comment_basic(comment: Dict[str, Any]) -> Dict[str, Any]:
    user = comment.get("user", {})
    return {
        "comment_id": str(comment.get("id")),
        "status_id": str(comment.get("status_id")),
        "user_id": user.get("id", ""),
        "nickname": user.get("screen_name", ""),
        "avatar": user.get("profile_image_url", ""),
        "content": comment.get("text", ""),
        "like_count": comment.get("like_count", 0),
        "parent_comment_id": comment.get("in_reply_to_status_id", ""),
        "reply_to_user": comment.get("in_reply_to_screen_name", ""),
        "created_at": comment.get("created_at", 0),
    }


def extract_creator_basic(user: Dict[str, Any]) -> Dict[str, Any]:
    """提取雪球创作者核心字段"""

    if not user:
        return {}

    return {
        "user_id": str(user.get("id", "")),
        "screen_name": user.get("screen_name", ""),
        "description": user.get("description", ""),
        "city": user.get("city", ""),
        "province": user.get("province", ""),
        "profile_image": user.get("profile_image_url", ""),
        "followers_count": user.get("followers_count", ""),
        "friends_count": user.get("friends_count", ""),
        "statuses_count": user.get("statuses_count", ""),
        "verified_type": user.get("verified_type", ""),
        "verified_description": user.get("verified_description", ""),
    }
