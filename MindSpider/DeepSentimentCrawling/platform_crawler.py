#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSentimentCrawling模块 - 平台爬虫管理器
负责配置和调用MediaCrawler进行多平台爬取
"""

import os
import re
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json
from loguru import logger

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import config
except ImportError:
    raise ImportError("无法导入config.py配置文件")

from platforms_config import SUPPORTED_PLATFORMS
from logging_utils import setup_platform_logger


class PlatformCrawler:
    """平台爬虫管理器"""

    def __init__(self):
        """初始化平台爬虫管理器"""
        self.mediacrawler_path = Path(__file__).parent / "MediaCrawler"
        self.supported_platforms = SUPPORTED_PLATFORMS
        self.crawl_stats = {}

        # 确保MediaCrawler目录存在
        if not self.mediacrawler_path.exists():
            raise FileNotFoundError(f"MediaCrawler目录不存在: {self.mediacrawler_path}")

        logger.info(f"初始化平台爬虫管理器，MediaCrawler路径: {self.mediacrawler_path}")

    def configure_mediacrawler_db(self):
        """
        配置MediaCrawler使用MindSpider的数据库

        注意：MediaCrawler的db_config.py已经配置为自动从.env读取数据库配置，
        因此这个函数现在只需要验证配置是否正确。
        """
        try:
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            db_type = (
                "PostgreSQL" if db_dialect in ("postgresql", "postgres") else "MySQL"
            )
            logger.info(f"已配置MediaCrawler使用MindSpider {db_type}数据库")
            return True

        except Exception as e:
            logger.exception(f"配置MediaCrawler数据库失败: {e}")
            return False

    def create_base_config(
        self,
        platform: str,
        keywords: List[str],
        crawler_type: str = "search",
        max_notes: int = 50,
    ) -> bool:
        """
        创建MediaCrawler的基础配置

        Args:
            platform: 平台名称
            keywords: 关键词列表
            crawler_type: 爬取类型
            max_notes: 最大爬取数量

        Returns:
            是否配置成功
        """
        try:
            # 判断数据库类型，确定 SAVE_DATA_OPTION
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            is_postgresql = db_dialect in ("postgresql", "postgres")
            save_data_option = "postgresql" if is_postgresql else "db"

            base_config_path = self.mediacrawler_path / "config" / "base_config.py"

            # 将关键词列表转换为逗号分隔的字符串
            sanitized_keywords = [
                kw.replace('"', "").replace("'", "").strip() for kw in keywords
            ]
            keywords_str = ",".join(sanitized_keywords)

            # 读取原始配置文件
            with open(base_config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 把旧的多行 CRAWLER_TYPE 块清理掉，避免残留缩进
            content = re.sub(
                r"^CRAWLER_TYPE\s*=\s*\(\s*\r?\n.*?^\)\s*$",
                "",
                content,
                flags=re.MULTILINE | re.DOTALL,
            )

            def replace_or_append(pattern: str, replacement: str) -> None:
                nonlocal content
                if re.search(pattern, content, flags=re.MULTILINE):
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                else:
                    if not content.endswith("\n"):
                        content += "\n"
                    content += replacement

            replace_or_append(
                r"^PLATFORM\s*=.*$",
                f'PLATFORM = "{platform}"  # 平台，xhs | dy | ks | bili | wb | tieba | zhihu',
            )
            replace_or_append(
                r"^KEYWORDS\s*=.*$",
                f'KEYWORDS = "{keywords_str}"  # 关键词搜索配置，以英文逗号分隔',
            )
            replace_or_append(
                r"^CRAWLER_TYPE\s*=.*$",
                f'CRAWLER_TYPE = "{crawler_type}"  # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据)',
            )
            replace_or_append(
                r"^SAVE_DATA_OPTION\s*=.*$",
                f'SAVE_DATA_OPTION = "{save_data_option}"  # csv or db or json or sqlite or postgresql',
            )
            replace_or_append(
                r"^CRAWLER_MAX_NOTES_COUNT\s*=.*$",
                f"CRAWLER_MAX_NOTES_COUNT = {max_notes}",
            )
            replace_or_append(
                r"^ENABLE_GET_COMMENTS\s*=.*$",
                "ENABLE_GET_COMMENTS = True",
            )
            replace_or_append(
                r"^CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES\s*=.*$",
                "CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20",
            )

            # HEADLESS 支持 .env 开关，默认为配置文件原值
            headless_match = re.search(
                r"^HEADLESS\s*=\s*(True|False)", content, flags=re.MULTILINE
            )
            existing_headless_value = (
                headless_match.group(1) if headless_match else "True"
            )
            headless_env = os.getenv("MEDIACRAWLER_HEADLESS")
            if headless_env is not None:
                env_lower = headless_env.strip().lower()
                new_headless_value = (
                    "True" if env_lower in ("1", "true", "yes", "on") else "False"
                )
            else:
                new_headless_value = existing_headless_value

            replace_or_append(
                r"^HEADLESS\s*=.*$",
                f"HEADLESS = {new_headless_value}  # 运行模式由配置或 MEDIACRAWLER_HEADLESS 控制",
            )

            # 写入新配置
            with open(base_config_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(
                f"已配置 {platform} 平台，爬取类型: {crawler_type}，关键词数量: {len(keywords)}，最大爬取数量: {max_notes}，保存数据方式: {save_data_option}"
            )
            return True

        except Exception as e:
            logger.exception(f"创建基础配置失败: {e}")
            return False

    def run_crawler(
        self,
        platform: str,
        keywords: List[str],
        login_type: str = "qrcode",
        max_notes: int = 50,
    ) -> Dict:
        """
        运行爬虫

        Args:
            platform: 平台名称
            keywords: 关键词列表
            login_type: 登录方式
            max_notes: 最大爬取数量

        Returns:
            爬取结果统计
        """
        if platform not in self.supported_platforms:
            raise ValueError(f"不支持的平台: {platform}")

        if not keywords:
            raise ValueError("关键词列表不能为空")

        handler_id = setup_platform_logger(platform)

        start_message = f"\n开始爬取平台: {platform}"
        start_message += f"\n关键词: {keywords[:5]}{'...' if len(keywords) > 5 else ''} (共{len(keywords)}个)"
        logger.info(start_message)

        start_time = datetime.now()

        try:
            # 配置数据库
            if not self.configure_mediacrawler_db():
                return {"success": False, "error": "数据库配置失败"}

            # 创建基础配置
            if not self.create_base_config(platform, keywords, "search", max_notes):
                return {"success": False, "error": "基础配置创建失败"}

            # 判断数据库类型，确定 save_data_option
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            is_postgresql = db_dialect in ("postgresql", "postgres")
            save_data_option = "postgresql" if is_postgresql else "db"

            # 构建命令
            cmd = [
                sys.executable,
                "main.py",
                "--platform",
                platform,
                "--lt",
                login_type,
                "--type",
                "search",
                "--save_data_option",
                save_data_option,
            ]

            logger.info(f"执行命令: {' '.join(cmd)}")

            # 使用 Popen 实时捕获输出
            # 注意：不指定 text=True 和 encoding，以二进制模式读取
            process = subprocess.Popen(
                cmd,
                cwd=self.mediacrawler_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,  # 行缓冲
            )

            # 实时读取并记录输出，智能处理编码
            for line in process.stdout:
                # 尝试多种编码解码
                decoded_line = None
                for encoding in ["utf-8", "gbk", "gb2312"]:
                    try:
                        decoded_line = line.decode(encoding).rstrip()
                        break
                    except (UnicodeDecodeError, AttributeError):
                        continue

                # 如果所有编码都失败，使用 utf-8 并替换错误字符
                if decoded_line is None:
                    decoded_line = line.decode("utf-8", errors="replace").rstrip()

                if decoded_line:  # 跳过空行
                    logger.info(f"[MediaCrawler] {decoded_line}")

            # 等待进程结束
            return_code = process.wait(timeout=3600)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # 创建统计信息
            crawl_stats = {
                "platform": platform,
                "keywords_count": len(keywords),
                "duration_seconds": duration,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "return_code": return_code,
                "success": return_code == 0,
                "notes_count": 0,
                "comments_count": 0,
                "errors_count": 0,
            }

            # 保存统计信息
            self.crawl_stats[platform] = crawl_stats

            if return_code == 0:
                logger.info(f"✅ {platform} 爬取完成，耗时: {duration:.1f}秒")
            else:
                logger.error(f"❌ {platform} 爬取失败，返回码: {return_code}")

            return crawl_stats

        except subprocess.TimeoutExpired:
            logger.exception(f"❌ {platform} 爬取超时")
            return {"success": False, "error": "爬取超时", "platform": platform}
        except Exception as e:
            logger.exception(f"❌ {platform} 爬取异常: {e}")
            return {"success": False, "error": str(e), "platform": platform}
        finally:
            logger.remove(handler_id)

    def _parse_crawl_output(
        self, output_lines: List[str], error_lines: List[str]
    ) -> Dict:
        """解析爬取输出，提取统计信息"""
        stats = {
            "notes_count": 0,
            "comments_count": 0,
            "errors_count": 0,
            "login_required": False,
        }

        # 解析输出行
        for line in output_lines:
            if "条笔记" in line or "条内容" in line:
                try:
                    # 提取数字
                    import re

                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        stats["notes_count"] = int(numbers[0])
                except:
                    pass
            elif "条评论" in line:
                try:
                    import re

                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        stats["comments_count"] = int(numbers[0])
                except:
                    pass
            elif "登录" in line or "扫码" in line:
                stats["login_required"] = True

        # 解析错误行
        for line in error_lines:
            if "error" in line.lower() or "异常" in line:
                stats["errors_count"] += 1

        return stats

    def run_multi_platform_crawl_by_keywords(
        self,
        keywords: List[str],
        platforms: List[str],
        login_type: str = "qrcode",
        max_notes_per_keyword: int = 50,
    ) -> Dict:
        """
        基于关键词的多平台爬取 - 每个关键词在所有平台上都进行爬取

        Args:
            keywords: 关键词列表
            platforms: 平台列表
            login_type: 登录方式
            max_notes_per_keyword: 每个关键词在每个平台的最大爬取数量

        Returns:
            总体爬取统计
        """

        start_message = f"\n🚀 开始全平台关键词爬取"
        start_message += f"\n   关键词数量: {len(keywords)}"
        start_message += f"\n   平台数量: {len(platforms)}"
        start_message += f"\n   登录方式: {login_type}"
        start_message += (
            f"\n   每个关键词在每个平台的最大爬取数量: {max_notes_per_keyword}"
        )
        start_message += f"\n   总爬取任务: {len(keywords)} × {len(platforms)} = {len(keywords) * len(platforms)}"
        logger.info(start_message)

        total_stats = {
            "total_keywords": len(keywords),
            "total_platforms": len(platforms),
            "total_tasks": len(keywords) * len(platforms),
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_notes": 0,
            "total_comments": 0,
            "keyword_results": {},
            "platform_summary": {},
        }

        # 初始化平台统计
        for platform in platforms:
            total_stats["platform_summary"][platform] = {
                "successful_keywords": 0,
                "failed_keywords": 0,
                "total_notes": 0,
                "total_comments": 0,
            }

        # 对每个平台一次性爬取所有关键词
        for platform in platforms:
            logger.info(f"\n📝 在 {platform} 平台爬取所有关键词")
            logger.info(
                f"   关键词: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}"
            )

            try:
                # 一次性传递所有关键词给平台
                result = self.run_crawler(
                    platform, keywords, login_type, max_notes_per_keyword
                )

                if result.get("success"):
                    total_stats["successful_tasks"] += len(keywords)
                    total_stats["platform_summary"][platform]["successful_keywords"] = (
                        len(keywords)
                    )

                    notes_count = result.get("notes_count", 0)
                    comments_count = result.get("comments_count", 0)

                    total_stats["total_notes"] += notes_count
                    total_stats["total_comments"] += comments_count
                    total_stats["platform_summary"][platform][
                        "total_notes"
                    ] = notes_count
                    total_stats["platform_summary"][platform][
                        "total_comments"
                    ] = comments_count

                    # 为每个关键词记录结果
                    for keyword in keywords:
                        if keyword not in total_stats["keyword_results"]:
                            total_stats["keyword_results"][keyword] = {}
                        total_stats["keyword_results"][keyword][platform] = result

                    logger.info(
                        f"   ✅ 成功: {notes_count} 条内容, {comments_count} 条评论"
                    )
                else:
                    total_stats["failed_tasks"] += len(keywords)
                    total_stats["platform_summary"][platform]["failed_keywords"] = len(
                        keywords
                    )

                    # 为每个关键词记录失败结果
                    for keyword in keywords:
                        if keyword not in total_stats["keyword_results"]:
                            total_stats["keyword_results"][keyword] = {}
                        total_stats["keyword_results"][keyword][platform] = result

                    logger.error(f"   ❌ 失败: {result.get('error', '未知错误')}")

            except Exception as e:
                total_stats["failed_tasks"] += len(keywords)
                total_stats["platform_summary"][platform]["failed_keywords"] = len(
                    keywords
                )
                error_result = {"success": False, "error": str(e)}

                # 为每个关键词记录异常结果
                for keyword in keywords:
                    if keyword not in total_stats["keyword_results"]:
                        total_stats["keyword_results"][keyword] = {}
                    total_stats["keyword_results"][keyword][platform] = error_result

                logger.error(f"   ❌ 异常: {e}")

        # 打印详细统计
        finish_message = f"\n📊 全平台关键词爬取完成!"
        finish_message += f"\n   总任务: {total_stats['total_tasks']}"
        finish_message += f"\n   成功: {total_stats['successful_tasks']}"
        finish_message += f"\n   失败: {total_stats['failed_tasks']}"
        finish_message += f"\n   成功率: {total_stats['successful_tasks']/total_stats['total_tasks']*100:.1f}%"
        finish_message += f"\n   总内容: {total_stats['total_notes']} 条"
        finish_message += f"\n   总评论: {total_stats['total_comments']} 条"
        logger.info(finish_message)

        platform_summary_message = f"\n� 各平台统计:"
        for platform, stats in total_stats["platform_summary"].items():
            success_rate = (
                stats["successful_keywords"] / len(keywords) * 100 if keywords else 0
            )
            platform_summary_message += f"\n   {platform}: {stats['successful_keywords']}/{len(keywords)} 关键词成功 ({success_rate:.1f}%), "
            platform_summary_message += f"{stats['total_notes']} 条内容"
        logger.info(platform_summary_message)

        return total_stats

    def get_crawl_statistics(self) -> Dict:
        """获取爬取统计信息"""
        return {
            "platforms_crawled": list(self.crawl_stats.keys()),
            "total_platforms": len(self.crawl_stats),
            "detailed_stats": self.crawl_stats,
        }

    def save_crawl_log(self, log_path: str = None):
        """保存爬取日志"""
        if not log_path:
            log_path = f"crawl_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(self.crawl_stats, f, ensure_ascii=False, indent=2)
            logger.info(f"爬取日志已保存到: {log_path}")
        except Exception as e:
            logger.exception(f"保存爬取日志失败: {e}")


if __name__ == "__main__":
    # 测试平台爬虫管理器
    crawler = PlatformCrawler()

    # 测试配置
    test_keywords = ["科技", "AI", "编程"]
    result = crawler.run_crawler("xhs", test_keywords, max_notes=5)

    logger.info(f"测试结果: {result}")
    logger.info("平台爬虫管理器测试完成！")
