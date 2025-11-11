"""
独立重新生成报告脚本
使用已有的三个引擎报告和论坛日志，重新生成最终报告
"""

import os
import sys
from pathlib import Path
from loguru import logger

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ReportEngine.agent import ReportAgent
from config import settings


def find_latest_reports():
    """查找最新的三个引擎报告"""
    reports_dirs = {
        'query': 'query_engine_streamlit_reports',
        'media': 'media_engine_streamlit_reports',
        'insight': 'insight_engine_streamlit_reports'
    }
    
    latest_files = {}
    
    for engine, dir_name in reports_dirs.items():
        dir_path = project_root / dir_name
        if not dir_path.exists():
            logger.warning(f"目录不存在: {dir_path}")
            continue
        
        # 查找 .md 文件
        md_files = list(dir_path.glob('*.md'))
        if md_files:
            # 按修改时间排序，获取最新的
            latest = max(md_files, key=lambda p: p.stat().st_mtime)
            latest_files[engine] = latest
            logger.info(f"找到 {engine} 最新报告: {latest.name}")
        else:
            logger.warning(f"未找到 {engine} 报告")
    
    return latest_files


def load_report_content(file_path: Path) -> str:
    """加载报告内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"已加载报告: {file_path.name}, 长度: {len(content)} 字符")
        return content
    except Exception as e:
        logger.error(f"加载报告失败 {file_path}: {str(e)}")
        return ""


def load_forum_logs() -> str:
    """加载论坛日志"""
    forum_log_path = project_root / 'logs' / 'forum.log'
    
    if not forum_log_path.exists():
        logger.warning(f"论坛日志不存在: {forum_log_path}")
        return ""
    
    try:
        with open(forum_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"已加载论坛日志，长度: {len(content)} 字符")
        return content
    except Exception as e:
        logger.error(f"加载论坛日志失败: {str(e)}")
        return ""


def main():
    """主函数"""
    print("=" * 60)
    print("独立重新生成报告工具")
    print("=" * 60)
    print()
    
    # 1. 查找最新的报告文件
    print("[1/5] 查找最新的引擎报告...")
    latest_reports = find_latest_reports()
    
    if len(latest_reports) < 3:
        print(f"❌ 错误: 需要3个引擎报告，但只找到 {len(latest_reports)} 个")
        print("请确保已经运行过 Query Engine, Media Engine 和 Insight Engine")
        return
    
    print(f"✓ 找到 {len(latest_reports)} 个引擎报告")
    print()
    
    # 2. 加载报告内容
    print("[2/5] 加载报告内容...")
    query_report = load_report_content(latest_reports.get('query'))
    media_report = load_report_content(latest_reports.get('media'))
    insight_report = load_report_content(latest_reports.get('insight'))
    
    if not all([query_report, media_report, insight_report]):
        print("❌ 错误: 部分报告内容加载失败")
        return
    
    print("✓ 所有报告内容已加载")
    print()
    
    # 3. 加载论坛日志
    print("[3/5] 加载论坛日志...")
    forum_logs = load_forum_logs()
    print(f"✓ 论坛日志已加载 ({len(forum_logs)} 字符)")
    print()
    
    # 4. 提取查询主题
    print("[4/5] 准备生成报告...")
    # 从文件名中提取查询主题
    query_file = latest_reports.get('query')
    query_name = query_file.stem.replace('deep_search_report_', '').replace('state_', '')
    # 移除时间戳部分
    import re
    query = re.sub(r'_\d{8}_\d{6}$', '', query_name)
    
    print(f"查询主题: {query}")
    print()
    
    # 5. 初始化 ReportAgent 并生成报告
    print("[5/5] 生成最终报告...")
    print("注意: 这可能需要几分钟时间...")
    print()
    
    try:
        # 初始化 ReportAgent
        agent = ReportAgent()
        
        # 生成报告
        reports = [query_report, media_report, insight_report]
        html_content = agent.generate_report(
            query=query,
            reports=reports,
            forum_logs=forum_logs,
            custom_template="",
            save_report=True
        )
        
        print()
        print("=" * 60)
        print("✅ 报告生成成功！")
        print("=" * 60)
        print()
        print(f"报告已保存到: final_reports/")
        print(f"HTML 长度: {len(html_content)} 字符")
        print()
        
        # 显示保存的文件
        final_reports_dir = project_root / 'final_reports'
        if final_reports_dir.exists():
            html_files = sorted(final_reports_dir.glob('final_report_*.html'), 
                              key=lambda p: p.stat().st_mtime, 
                              reverse=True)
            if html_files:
                latest_html = html_files[0]
                print(f"最新报告: {latest_html.name}")
                print(f"完整路径: {latest_html.absolute()}")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 报告生成失败")
        print("=" * 60)
        logger.exception(f"生成报告时出错: {str(e)}")
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
