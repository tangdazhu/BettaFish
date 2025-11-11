"""
Streamlit Web界面
为Query Agent提供友好的Web界面
"""

import os
import sys
import time
import threading
import streamlit as st
from datetime import datetime
import json
import locale
from loguru import logger

# 设置UTF-8编码环境
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# 设置系统编码
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except locale.Error:
        pass

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from QueryEngine import DeepSearchAgent, Settings
from config import settings
from utils.github_issues import error_with_issue_link


def main():
    """主函数"""
    st.set_page_config(
        page_title="Query Agent",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Query Agent")
    st.markdown("具备强大网页搜索能力的AI代理")
    st.markdown("广度爬取官方报道与新闻，注重国内外资源相结合理解舆情")
    
    # 初始化停止事件和运行状态
    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = threading.Event()
    
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    
    if 'task_thread' not in st.session_state:
        st.session_state.task_thread = None
    
    if 'task_result' not in st.session_state:
        st.session_state.task_result = None
    
    if 'task_error' not in st.session_state:
        st.session_state.task_error = None

    # 检查URL参数
    try:
        # 尝试使用新版本的query_params
        query_params = st.query_params
        auto_query = query_params.get('query', '')
        auto_search = query_params.get('auto_search', 'false').lower() == 'true'
    except AttributeError:
        # 兼容旧版本
        query_params = st.experimental_get_query_params()
        auto_query = query_params.get('query', [''])[0]
        auto_search = query_params.get('auto_search', ['false'])[0].lower() == 'true'

    # ----- 配置被硬编码 -----
    # 强制使用 DeepSeek
    model_name = settings.QUERY_ENGINE_MODEL_NAME or "deepseek-chat"
    # 默认高级配置
    max_reflections = 2
    max_content_length = 20000

    # 简化的研究查询展示区域

    # 如果有自动查询，使用它作为默认值，否则显示占位符
    display_query = auto_query if auto_query else "等待从主页面接收分析内容..."

    # 查询展示区域和停止按钮
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.text_area(
            "当前查询",
            value=display_query,
            height=100,
            disabled=True,
            help="查询内容由主页面的搜索框控制",
            label_visibility="hidden"
        )
    
    with col2:
        st.write("")  # 添加一些垂直空间
        st.write("")  # 对齐按钮位置
        if st.session_state.is_running:
            if st.button("⏹️ 停止", type="secondary", use_container_width=True, key="stop_button"):
                logger.info("=" * 50)
                logger.info("用户点击了停止按钮")
                st.session_state.stop_event.set()
                logger.info(f"停止事件已设置: {st.session_state.stop_event.is_set()}")
                logger.info("=" * 50)
                st.warning("⏹️ 正在停止任务，请稍候...")
        else:
            st.button("⏹️ 停止", type="secondary", use_container_width=True, disabled=True, key="stop_button_disabled")

    # 自动搜索逻辑
    start_research = False
    query = auto_query

    if auto_search and auto_query and 'auto_search_executed' not in st.session_state:
        st.session_state.auto_search_executed = True
        start_research = True
    elif auto_query and not auto_search:
        st.warning("等待搜索启动信号...")

    # 验证配置
    if start_research:
        if not query.strip():
            st.error("请输入研究查询")
            return

        # 由于强制使用DeepSeek，检查相关的API密钥
        if not settings.QUERY_ENGINE_API_KEY:
            st.error("请在您的环境变量中设置QUERY_ENGINE_API_KEY")
            return
        if not settings.TAVILY_API_KEY:
            st.error("请在您的环境变量中设置TAVILY_API_KEY")
            return

        # 自动使用配置文件中的API密钥
        engine_key = settings.QUERY_ENGINE_API_KEY
        tavily_key = settings.TAVILY_API_KEY

        # 创建配置
        config = Settings(
            QUERY_ENGINE_API_KEY=engine_key,
            QUERY_ENGINE_BASE_URL=settings.QUERY_ENGINE_BASE_URL,
            QUERY_ENGINE_MODEL_NAME=model_name,
            TAVILY_API_KEY=tavily_key,
            MAX_REFLECTIONS=max_reflections,
            SEARCH_CONTENT_MAX_LENGTH=max_content_length,
            OUTPUT_DIR="query_engine_streamlit_reports"
        )

        # 执行研究
        execute_research(query, config)


def _run_research_in_thread(query: str, config: Settings, stop_event: threading.Event, result_container: dict):
    """在后台线程中运行研究任务"""
    try:
        # 初始化Agent
        agent = DeepSearchAgent(config, stop_event=stop_event)
        result_container['agent'] = agent
        result_container['task_result'] = {"status": "初始化完成", "progress": 10}

        # 生成报告结构
        result_container['task_result'] = {"status": "生成报告结构", "progress": 20}
        agent._generate_report_structure(query)

        # 处理段落
        total_paragraphs = len(agent.state.paragraphs)
        for i in range(total_paragraphs):
            # 检查停止信号
            if stop_event.is_set():
                result_container['task_result'] = {"status": "已停止", "progress": 0}
                result_container['task_error'] = "用户请求停止"
                return
            
            result_container['task_result'] = {
                "status": f"处理段落 {i + 1}/{total_paragraphs}: {agent.state.paragraphs[i].title}",
                "progress": 20 + int((i + 0.5) / total_paragraphs * 60)
            }

            # 初始搜索和总结
            agent._initial_search_and_summary(i)

            # 反思循环
            agent._reflection_loop(i)
            agent.state.paragraphs[i].research.mark_completed()

            result_container['task_result'] = {
                "status": f"完成段落 {i + 1}/{total_paragraphs}",
                "progress": 20 + int((i + 1) / total_paragraphs * 60)
            }

        # 生成最终报告
        result_container['task_result'] = {"status": "生成最终报告", "progress": 90}
        final_report = agent._generate_final_report()

        # 保存报告
        result_container['task_result'] = {"status": "保存报告", "progress": 95}
        agent._save_report(final_report)

        result_container['task_result'] = {
            "status": "完成",
            "progress": 100,
            "final_report": final_report
        }

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        # 检查是否是用户中断
        if "InterruptedError" in error_traceback or "用户请求停止" in str(e):
            result_container['task_result'] = {"status": "已停止", "progress": 0}
            result_container['task_error'] = "用户请求停止"
            logger.info("任务被用户停止")
        else:
            result_container['task_error'] = error_traceback
            logger.error(f"研究过程中发生错误: {str(e)}")
    finally:
        result_container['is_running'] = False


def execute_research(query: str, config: Settings):
    """执行研究（启动后台线程并轮询）"""
    try:
        # 重置停止事件和状态
        st.session_state.stop_event.clear()
        st.session_state.is_running = True
        st.session_state.task_result = {"status": "启动中", "progress": 0}
        st.session_state.task_error = None
        
        # 创建结果容器（用于线程间通信）
        result_container = {
            'agent': None,
            'task_result': None,
            'task_error': None,
            'is_running': True
        }
        st.session_state.result_container = result_container
        
        # 启动后台线程
        task_thread = threading.Thread(
            target=_run_research_in_thread,
            args=(query, config, st.session_state.stop_event, result_container),
            daemon=True
        )
        task_thread.start()
        st.session_state.task_thread = task_thread
        
        # 创建进度条和状态显示
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 轮询任务状态
        while result_container['is_running']:
            # 从 result_container 同步到 session_state（用于显示）
            if result_container['task_result']:
                st.session_state.task_result = result_container['task_result']
                result = result_container['task_result']
                status_text.text(result.get("status", "运行中"))
                progress_bar.progress(result.get("progress", 0))
                
                # 检查是否完成
                if result.get("status") == "完成":
                    status_text.text("研究完成！")
                    st.session_state.agent = result_container['agent']
                    display_results(result_container['agent'], result.get("final_report"))
                    st.session_state.is_running = False
                    break
                elif result.get("status") == "已停止":
                    status_text.text("任务已被用户停止")
                    st.warning("✋ 任务已停止")
                    st.session_state.is_running = False
                    break
            
            # 检查是否有错误
            if result_container['task_error']:
                st.session_state.task_error = result_container['task_error']
                if result_container['task_error'] == "用户请求停止":
                    st.warning("✋ 任务已被用户停止")
                    logger.info("任务被用户停止")
                else:
                    error_display = error_with_issue_link(
                        f"研究过程中发生错误",
                        result_container['task_error'],
                        app_name="Query Engine Streamlit App"
                    )
                    st.error(error_display, icon="🚨")
                    logger.error(f"错误详情:\n{result_container['task_error']}")
                st.session_state.is_running = False
                break
            
            # 短暂延迟后刷新
            time.sleep(0.5)
            st.rerun()

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        error_display = error_with_issue_link(
            f"启动研究任务时发生错误: {str(e)}",
            error_traceback,
            app_name="Query Engine Streamlit App"
        )
        st.error(error_display, icon="🚨")
        logger.error(f"错误详情:\n{error_traceback}")
        st.session_state.is_running = False


def display_results(agent: DeepSearchAgent, final_report: str):
    """显示研究结果"""
    st.header("研究结果")

    # 结果标签页（已移除下载选项）
    tab1, tab2 = st.tabs(["研究小结", "引用信息"])

    with tab1:
        st.markdown(final_report)

    with tab2:
        # 段落详情
        st.subheader("段落详情")
        for i, paragraph in enumerate(agent.state.paragraphs):
            with st.expander(f"段落 {i + 1}: {paragraph.title}"):
                st.write("**预期内容:**", paragraph.content)
                st.write("**最终内容:**", paragraph.research.latest_summary[:300] + "..."
                if len(paragraph.research.latest_summary) > 300
                else paragraph.research.latest_summary)
                st.write("**搜索次数:**", paragraph.research.get_search_count())
                st.write("**反思次数:**", paragraph.research.reflection_iteration)

        # 搜索历史
        st.subheader("搜索历史")
        all_searches = []
        for paragraph in agent.state.paragraphs:
            all_searches.extend(paragraph.research.search_history)

        if all_searches:
            for i, search in enumerate(all_searches):
                with st.expander(f"搜索 {i + 1}: {search.query}"):
                    st.write("**URL:**", search.url)
                    st.write("**标题:**", search.title)
                    st.write("**内容预览:**",
                             search.content[:200] + "..." if len(search.content) > 200 else search.content)
                    if search.score:
                        st.write("**相关度评分:**", search.score)


if __name__ == "__main__":
    main()
