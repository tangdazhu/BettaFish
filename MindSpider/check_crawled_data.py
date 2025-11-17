# -*- coding: utf-8 -*-
"""
检查和管理已爬取的数据
支持查看统计、清空数据等操作
  # 查看所有平台数据统计
  python check_crawled_data.py

  # 查看指定平台数据
  python check_crawled_data.py --platform bili

  # 清空B站所有数据
  python check_crawled_data.py --platform bili --clear

  # 清空包含特定关键词的数据
  python check_crawled_data.py --platform bili --clear --keyword "小米汽车"
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import settings
import psycopg2
import json
from datetime import datetime


# 平台配置
PLATFORM_CONFIG = {
    "bili": {
        "name": "B站",
        "video_table": "bilibili_video",
        "comment_table": "bilibili_video_comment",
        "id_field": "video_id",
        "title_field": "title",
        "liked_field": "liked_count",
        "comment_count_field": "video_comment",
    },
    "weibo": {
        "name": "微博",
        "video_table": "weibo_note",
        "comment_table": "weibo_note_comment",
        "id_field": "note_id",
        "title_field": "note_content",
        "liked_field": "liked_count",
        "comment_count_field": "comments_count",
    },
    "xhs": {
        "name": "小红书",
        "video_table": "xhs_note",
        "comment_table": "xhs_note_comment",
        "id_field": "note_id",
        "title_field": "note_title",
        "liked_field": "liked_count",
        "comment_count_field": "comments_count",
    },
    "douyin": {
        "name": "抖音",
        "video_table": "douyin_aweme",
        "comment_table": "douyin_aweme_comment",
        "id_field": "aweme_id",
        "title_field": "aweme_title",
        "liked_field": "liked_count",
        "comment_count_field": "comments_count",
    },
    "kuaishou": {
        "name": "快手",
        "video_table": "kuaishou_video",
        "comment_table": "kuaishou_video_comment",
        "id_field": "video_id",
        "title_field": "video_title",
        "liked_field": "liked_count",
        "comment_count_field": "comments_count",
    },
    "tieba": {
        "name": "贴吧",
        "video_table": "tieba_note",
        "comment_table": "tieba_comment",
        "id_field": "note_id",
        "title_field": "title",
        "liked_field": "liked_count",
        "comment_count_field": "comments_count",
    },
    "zhihu": {
        "name": "知乎",
        "video_table": "zhihu_content",
        "comment_table": "zhihu_comment",
        "id_field": "content_id",
        "title_field": "title",
        "liked_field": "voteup_count",
        "comment_count_field": "comment_count",
    },
}


def check_all_platforms():
    """检查所有平台的数据统计"""
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME,
        )
        cursor = conn.cursor()

        print("=" * 60)
        print("所有平台数据统计")
        print("=" * 60)

        total_content = 0
        total_comments = 0

        for platform_key, config in PLATFORM_CONFIG.items():
            # 检查内容数量
            cursor.execute(f"SELECT COUNT(*) FROM {config['video_table']}")
            content_count = cursor.fetchone()[0]

            # 检查评论数量
            cursor.execute(f"SELECT COUNT(*) FROM {config['comment_table']}")
            comment_count = cursor.fetchone()[0]

            if content_count > 0 or comment_count > 0:
                print(f"\n{config['name']}:")
                print(f"  内容: {content_count} 条")
                print(f"  评论: {comment_count} 条")

                total_content += content_count
                total_comments += comment_count

        print("\n" + "=" * 60)
        print(f"总计: {total_content} 条内容, {total_comments} 条评论")
        print("=" * 60)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"检查失败: {e}")


def check_platform_data(platform_key):
    """检查指定平台的数据"""
    if platform_key not in PLATFORM_CONFIG:
        print(f"不支持的平台: {platform_key}")
        print(f"支持的平台: {', '.join(PLATFORM_CONFIG.keys())}")
        return

    config = PLATFORM_CONFIG[platform_key]
    try:
        # 连接数据库
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME,
        )
        cursor = conn.cursor()

        print("=" * 60)
        print(f"{config['name']}数据统计")
        print("=" * 60)

        # 检查内容数量
        cursor.execute(f"SELECT COUNT(*) FROM {config['video_table']}")
        content_count = cursor.fetchone()[0]
        print(f"\n总内容数量: {content_count} 条")

        # 检查评论数量
        cursor.execute(f"SELECT COUNT(*) FROM {config['comment_table']}")
        comment_count = cursor.fetchone()[0]
        print(f"总评论数量: {comment_count} 条")

        # 显示最新的5条内容
        if content_count > 0:
            print("\n" + "=" * 60)
            print("最新爬取的内容（前5条）")
            print("=" * 60)
            cursor.execute(
                f"""
                SELECT {config['id_field']}, {config['title_field']}, 
                       {config['liked_field']}, {config['comment_count_field']}
                FROM {config['video_table']}
                ORDER BY add_ts DESC 
                LIMIT 5
            """
            )
            for row in cursor.fetchall():
                print(f"\nID: {row[0]}")
                title = str(row[1])[:50] if row[1] else "(无标题)"
                print(f"标题: {title}...")
                print(f"点赞: {row[2]} | 评论: {row[3]}")

        # 显示关键词统计
        # 从daily_topics表获取所有关键词
        cursor.execute(
            """
            SELECT keywords 
            FROM daily_topics
            WHERE keywords IS NOT NULL AND keywords != ''
            ORDER BY extract_date DESC
        """
        )
        topics = cursor.fetchall()

        # 解析所有关键词
        all_keywords = set()
        for topic_row in topics:
            keywords_json = topic_row[0]
            try:
                if keywords_json:
                    keywords_list = json.loads(keywords_json)
                    # 进一步拆分每个关键词（处理中文逗号和英文逗号）
                    for kw in keywords_list:
                        if isinstance(kw, str):
                            # 同时支持中文逗号、英文逗号和顿号分隔
                            sub_keywords = (
                                kw.replace("，", ",").replace("、", ",").split(",")
                            )
                            for sub_kw in sub_keywords:
                                cleaned = sub_kw.strip().strip('"').strip("'")
                                if cleaned:
                                    all_keywords.add(cleaned)
                        else:
                            all_keywords.add(str(kw))
            except (json.JSONDecodeError, TypeError):
                # 如果不是JSON格式，尝试按逗号分隔
                if isinstance(keywords_json, str):
                    keywords_list = [
                        k.strip()
                        for k in keywords_json.replace("，", ",").split(",")
                        if k.strip()
                    ]
                    all_keywords.update(keywords_list)

        # 获取所有内容标题
        cursor.execute(
            f"""
            SELECT {config['id_field']}, {config['title_field']}
            FROM {config['video_table']}
        """
        )
        videos = cursor.fetchall()

        if videos and all_keywords:
            print("\n" + "=" * 60)
            print("关键词覆盖情况")
            print("=" * 60)

            # 统计每个关键词的覆盖情况
            keyword_stats = []
            for keyword in all_keywords:
                count = sum(1 for v in videos if v[1] and keyword in str(v[1]))
                if count > 0:  # 只显示有数据的关键词
                    keyword_stats.append((keyword, count))

            # 按数量降序排序
            keyword_stats.sort(key=lambda x: x[1], reverse=True)

            if keyword_stats:
                for keyword, count in keyword_stats:
                    print(f"{keyword}: {count} 条内容")
            else:
                print("未找到匹配的关键词数据")
        elif videos:
            print("\n" + "=" * 60)
            print("关键词覆盖情况")
            print("=" * 60)
            print("数据库中没有配置关键词，请先使用 add_custom_topic.py 添加话题")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print(f"总计: {content_count} 条内容, {comment_count} 条评论")
        print("=" * 60)

    except Exception as e:
        print(f"检查失败: {e}")


def clear_bilibili_data(keyword=None):
    """
    清空B站爬取的数据

    Args:
        keyword: 可选，指定关键词只清空包含该关键词的数据
    """
    try:
        # 连接数据库
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME,
        )
        cursor = conn.cursor()

        if keyword:
            # 清空包含特定关键词的数据
            print(f"\n正在清空包含关键词 '{keyword}' 的数据...")

            # 先获取要删除的视频ID
            cursor.execute(
                """
                SELECT video_id FROM bilibili_video 
                WHERE title LIKE %s OR note_url LIKE %s
                """,
                (f"%{keyword}%", f"%{keyword}%"),
            )
            video_ids = [row[0] for row in cursor.fetchall()]

            if not video_ids:
                print(f"未找到包含关键词 '{keyword}' 的数据")
                cursor.close()
                conn.close()
                return

            print(f"找到 {len(video_ids)} 条相关视频")

            # 确认删除
            confirm = input(f"确认删除这 {len(video_ids)} 条视频及其评论吗？(yes/no): ")
            if confirm.lower() != "yes":
                print("已取消删除操作")
                cursor.close()
                conn.close()
                return

            # 删除评论
            cursor.execute(
                """
                DELETE FROM bilibili_video_comment 
                WHERE video_id = ANY(%s)
                """,
                (video_ids,),
            )
            comment_deleted = cursor.rowcount

            # 删除视频
            cursor.execute(
                """
                DELETE FROM bilibili_video 
                WHERE video_id = ANY(%s)
                """,
                (video_ids,),
            )
            video_deleted = cursor.rowcount

            conn.commit()
            print(f"\n删除成功!")
            print(f"- 删除视频: {video_deleted} 条")
            print(f"- 删除评论: {comment_deleted} 条")

        else:
            # 清空所有B站数据
            print("\n警告: 即将清空所有B站数据!")

            # 先统计数量
            cursor.execute("SELECT COUNT(*) FROM bilibili_video")
            video_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM bilibili_video_comment")
            comment_count = cursor.fetchone()[0]

            if video_count == 0 and comment_count == 0:
                print("数据库中没有B站数据")
                cursor.close()
                conn.close()
                return

            print(f"当前数据: {video_count} 条视频, {comment_count} 条评论")
            confirm = input("确认清空所有B站数据吗？(yes/no): ")

            if confirm.lower() != "yes":
                print("已取消清空操作")
                cursor.close()
                conn.close()
                return

            # 清空评论表
            cursor.execute("DELETE FROM bilibili_video_comment")
            comment_deleted = cursor.rowcount

            # 清空视频表
            cursor.execute("DELETE FROM bilibili_video")
            video_deleted = cursor.rowcount

            conn.commit()
            print(f"\n清空成功!")
            print(f"- 删除视频: {video_deleted} 条")
            print(f"- 删除评论: {comment_deleted} 条")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"清空失败: {e}")
        if conn:
            conn.rollback()


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="检查和管理爬取数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查看所有平台数据统计
  python check_crawled_data.py
  
  # 查看指定平台数据
  python check_crawled_data.py --platform bili
  python check_crawled_data.py --platform weibo
  
  # 清空指定平台所有数据
  python check_crawled_data.py --platform bili --clear
  
  # 清空包含特定关键词的数据
  python check_crawled_data.py --platform bili --clear --keyword "阿里巴巴"
        """,
    )

    parser.add_argument(
        "--platform",
        type=str,
        choices=list(PLATFORM_CONFIG.keys()),
        help=f"指定平台 ({', '.join(PLATFORM_CONFIG.keys())})",
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="清空数据（需要确认）",
    )

    parser.add_argument(
        "--keyword",
        type=str,
        help="指定关键词，只清空包含该关键词的数据",
    )

    args = parser.parse_args()

    if args.clear:
        # 清空数据（目前只支持B站）
        if args.platform and args.platform != "bili":
            print(f"暂不支持清空{PLATFORM_CONFIG[args.platform]['name']}数据")
            print("目前只支持清空B站数据")
            return
        clear_bilibili_data(keyword=args.keyword)
    else:
        if args.keyword:
            print("提示: --keyword 参数需要配合 --clear 使用")
            print("使用 --help 查看帮助信息")
        elif args.platform:
            check_platform_data(args.platform)
        else:
            check_all_platforms()


if __name__ == "__main__":
    main()
