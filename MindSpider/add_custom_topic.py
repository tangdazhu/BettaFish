# -*- coding: utf-8 -*-
"""
管理自定义话题：添加、查看、删除话题
使用方法：
python add_custom_topic.py "话题" "关键词1,关键词2,关键词3"     # 添加
python add_custom_topic.py --list              # 查看
python add_custom_topic.py --delete "话题"     # 删除（按名称）
python add_custom_topic.py --delete-id "ID"    # 删除（按ID）
python add_custom_topic.py --help              # 帮助

使用示例:
  # 添加话题
  python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,电动车"
  python add_custom_topic.py "AI技术趋势" "人工智能,ChatGPT,大模型" "AI技术发展趋势分析"

  # 查看所有话题
  python add_custom_topic.py --list

  # 删除话题（按名称）
  python add_custom_topic.py --delete "小米汽车分析"

  # 删除话题（按ID）
  python add_custom_topic.py --delete-id "custom_20251117_140530"
"""

import sys
import json
import argparse
from datetime import date, datetime
from sqlalchemy import create_engine, text
from config import settings


def get_db_engine():
    """获取数据库引擎"""
    if settings.DB_DIALECT == "postgresql":
        url = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    else:
        url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset={settings.DB_CHARSET}"
    return create_engine(url, future=True)


def add_custom_topic(topic_name: str, keywords_str: str, description: str = ""):
    """
    添加自定义话题到数据库

    Args:
        topic_name: 话题名称
        keywords_str: 关键词，用逗号分隔
        description: 话题描述（可选）
    """
    # 解析关键词
    keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]

    if not keywords:
        print("❌ 错误：至少需要一个关键词")
        return False

    engine = get_db_engine()

    # 生成话题ID
    topic_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    today = date.today()
    current_ts = int(datetime.now().timestamp())

    # 插入话题
    insert_sql = text(
        """
        INSERT INTO daily_topics (
            topic_id, topic_name, topic_description, keywords,
            extract_date, relevance_score, news_count, processing_status,
            add_ts, last_modify_ts
        ) VALUES (
            :topic_id, :topic_name, :topic_description, :keywords,
            :extract_date, :relevance_score, :news_count, :processing_status,
            :add_ts, :last_modify_ts
        )
    """
    )

    try:
        with engine.connect() as conn:
            conn.execute(
                insert_sql,
                {
                    "topic_id": topic_id,
                    "topic_name": topic_name,
                    "topic_description": description or f"自定义话题：{topic_name}",
                    "keywords": json.dumps(keywords, ensure_ascii=False),
                    "extract_date": today,
                    "relevance_score": 1.0,
                    "news_count": 0,
                    "processing_status": "pending",
                    "add_ts": current_ts,
                    "last_modify_ts": current_ts,
                },
            )
            conn.commit()

        print(f"✅ 成功添加自定义话题：{topic_name}")
        print(f"   话题ID: {topic_id}")
        print(f"   关键词: {', '.join(keywords)}")
        print(f"   日期: {today}")
        print(f"\n📌 下一步：运行爬虫")
        print(f"   python main.py --deep-sentiment --platforms xhs --test")

        return True

    except Exception as e:
        print(f"❌ 添加话题失败: {e}")
        return False
    finally:
        engine.dispose()


def list_topics():
    """列出所有话题"""
    engine = get_db_engine()

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT topic_id, topic_name, keywords, extract_date, processing_status
                    FROM daily_topics
                    ORDER BY extract_date DESC, add_ts DESC
                """
                )
            )
            topics = result.fetchall()

            if not topics:
                print("数据库中没有话题")
                return

            print("=" * 80)
            print("话题列表")
            print("=" * 80)

            for i, topic in enumerate(topics, 1):
                topic_id, topic_name, keywords_json, extract_date, status = topic
                keywords = json.loads(keywords_json) if keywords_json else []

                print(f"\n{i}. {topic_name}")
                print(f"   ID: {topic_id}")
                print(f"   关键词: {', '.join(keywords)}")
                print(f"   日期: {extract_date}")
                print(f"   状态: {status}")

            print("\n" + "=" * 80)
            print(f"总计: {len(topics)} 个话题")
            print("=" * 80)

    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        engine.dispose()


def delete_topic(topic_name: str = None, topic_id: str = None):
    """
    删除话题

    Args:
        topic_name: 话题名称
        topic_id: 话题ID（可选，如果提供则优先使用）
    """
    if not topic_name and not topic_id:
        print("错误: 必须提供话题名称或话题ID")
        return False

    engine = get_db_engine()

    try:
        with engine.connect() as conn:
            # 查找话题
            if topic_id:
                query = text(
                    "SELECT topic_id, topic_name, keywords FROM daily_topics WHERE topic_id = :topic_id"
                )
                result = conn.execute(query, {"topic_id": topic_id})
            else:
                query = text(
                    "SELECT topic_id, topic_name, keywords FROM daily_topics WHERE topic_name = :topic_name"
                )
                result = conn.execute(query, {"topic_name": topic_name})

            topic = result.fetchone()

            if not topic:
                search_key = topic_id if topic_id else topic_name
                print(f"未找到话题: {search_key}")
                return False

            tid, tname, keywords_json = topic
            keywords = json.loads(keywords_json) if keywords_json else []

            # 显示话题信息
            print("\n即将删除以下话题:")
            print(f"  话题名称: {tname}")
            print(f"  话题ID: {tid}")
            print(f"  关键词: {', '.join(keywords)}")

            # 确认删除
            confirm = input("\n确认删除该话题吗？(yes/no): ")
            if confirm.lower() != "yes":
                print("已取消删除操作")
                return False

            # 删除话题
            delete_sql = text("DELETE FROM daily_topics WHERE topic_id = :topic_id")
            conn.execute(delete_sql, {"topic_id": tid})
            conn.commit()

            print(f"\n删除成功!")
            print(f"已删除话题: {tname}")

            return True

    except Exception as e:
        print(f"删除失败: {e}")
        return False
    finally:
        engine.dispose()


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="管理自定义话题",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 添加话题
  python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,电动车"
  python add_custom_topic.py "AI技术趋势" "人工智能,ChatGPT,大模型" "AI技术发展趋势分析"
  
  # 查看所有话题
  python add_custom_topic.py --list
  
  # 删除话题（按名称）
  python add_custom_topic.py --delete "小米汽车分析"
  
  # 删除话题（按ID）
  python add_custom_topic.py --delete-id "custom_20251117_140530"
        """,
    )

    parser.add_argument(
        "topic_name",
        nargs="?",
        help="话题名称",
    )

    parser.add_argument(
        "keywords",
        nargs="?",
        help="关键词，用逗号分隔",
    )

    parser.add_argument(
        "description",
        nargs="?",
        default="",
        help="话题描述（可选）",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有话题",
    )

    parser.add_argument(
        "--delete",
        type=str,
        metavar="TOPIC_NAME",
        help="删除指定名称的话题",
    )

    parser.add_argument(
        "--delete-id",
        type=str,
        metavar="TOPIC_ID",
        help="删除指定ID的话题",
    )

    args = parser.parse_args()

    # 处理不同的操作
    if args.list:
        list_topics()
    elif args.delete:
        delete_topic(topic_name=args.delete)
    elif args.delete_id:
        delete_topic(topic_id=args.delete_id)
    elif args.topic_name and args.keywords:
        add_custom_topic(args.topic_name, args.keywords, args.description)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
