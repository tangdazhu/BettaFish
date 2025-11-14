"""
报告格式化节点
负责将最终研究结果格式化为美观的Markdown报告
"""

import json
from typing import List, Dict, Any
from loguru import logger

from .base_node import BaseNode
from ..prompts import SYSTEM_PROMPT_REPORT_FORMATTING
from ..utils.text_processing import remove_reasoning_from_output, clean_markdown_tags


class ReportFormattingNode(BaseNode):
    """格式化最终报告的节点"""

    def __init__(self, llm_client):
        """
        初始化报告格式化节点

        Args:
            llm_client: LLM客户端
        """
        super().__init__(llm_client, "ReportFormattingNode")

    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据"""
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                return isinstance(data, list) and all(
                    isinstance(item, dict)
                    and "title" in item
                    and "paragraph_latest_state" in item
                    for item in data
                )
            except:
                return False
        elif isinstance(input_data, list):
            return all(
                isinstance(item, dict)
                and "title" in item
                and "paragraph_latest_state" in item
                for item in input_data
            )
        return False

    def run(self, input_data: Any, **kwargs) -> str:
        """
        调用LLM生成Markdown格式报告

        Args:
            input_data: 包含所有段落信息的列表
            **kwargs: 额外参数

        Returns:
            格式化的Markdown报告
        """
        try:
            if not self.validate_input(input_data):
                raise ValueError(
                    "输入数据格式错误，需要包含title和paragraph_latest_state的列表"
                )

            # 准备输入数据
            if isinstance(input_data, str):
                message = input_data
            else:
                message = json.dumps(input_data, ensure_ascii=False)

            # 记录输入长度
            input_length = len(message)
            logger.info(f"正在格式化最终报告 - 输入长度: {input_length} 字符")
            if input_length > 100000:
                logger.warning(
                    f"输入数据过长({input_length}字符)，可能导致LLM输出被截断"
                )

            # 调用LLM生成Markdown格式（设置大的 max_tokens 以支持长报告）
            # qwen3-max 支持 65536 tokens 输出，262K 上下文
            response = self.llm_client.invoke(
                SYSTEM_PROMPT_REPORT_FORMATTING,
                message,
                max_tokens=32000,  # qwen3-max 支持超大输出，32000 tokens ≈ 22000-25000 字中文
            )

            # 处理响应
            processed_response = self.process_output(response)

            # 记录输出长度
            output_length = len(processed_response)
            logger.info(f"成功生成格式化报告 - 输出长度: {output_length} 字符")

            # 如果报告过短，使用备用方法
            if output_length < 5000:
                logger.warning(
                    f"报告内容过短({output_length}字符)，未达到预期的一万字要求，使用备用格式化方法"
                )
                # 使用备用方法：直接将所有段落内容拼接成完整报告
                if isinstance(input_data, list):
                    backup_report = self._format_report_with_full_content(input_data)
                    logger.info(f"备用方法生成报告长度: {len(backup_report)} 字符")
                    return backup_report

            return processed_response

        except Exception as e:
            logger.exception(f"报告格式化失败: {str(e)}")
            raise e

    def process_output(self, output: str) -> str:
        """
        处理LLM输出，清理Markdown格式

        Args:
            output: LLM原始输出

        Returns:
            清理后的Markdown报告
        """
        try:
            # 清理响应文本
            cleaned_output = remove_reasoning_from_output(output)
            cleaned_output = clean_markdown_tags(cleaned_output)

            # 确保报告有基本结构
            if not cleaned_output.strip():
                return "# 报告生成失败\n\n无法生成有效的报告内容。"

            # 如果没有标题，添加一个默认标题
            if not cleaned_output.strip().startswith("#"):
                cleaned_output = "# 深度研究报告\n\n" + cleaned_output

            return cleaned_output.strip()

        except Exception as e:
            logger.exception(f"处理输出失败: {str(e)}")
            return "# 报告处理失败\n\n报告格式化过程中发生错误。"

    def format_report_manually(
        self, paragraphs_data: List[Dict[str, str]], report_title: str = "深度研究报告"
    ) -> str:
        """
        手动格式化报告（备用方法）

        Args:
            paragraphs_data: 段落数据列表
            report_title: 报告标题

        Returns:
            格式化的Markdown报告
        """
        try:
            logger.info("使用手动格式化方法")

            # 构建报告
            report_lines = [f"# {report_title}", "", "---", ""]

            # 添加各个段落
            for i, paragraph in enumerate(paragraphs_data, 1):
                title = paragraph.get("title", f"段落 {i}")
                content = paragraph.get("paragraph_latest_state", "")

                if content:
                    report_lines.extend([f"## {title}", "", content, "", "---", ""])

            # 添加结论
            if len(paragraphs_data) > 1:
                report_lines.extend(
                    [
                        "## 结论",
                        "",
                        "本报告通过深度搜索和研究，对相关主题进行了全面分析。"
                        "以上各个方面的内容为理解该主题提供了重要参考。",
                        "",
                    ]
                )

            return "\n".join(report_lines)

        except Exception as e:
            logger.exception(f"手动格式化失败: {str(e)}")
            return "# 报告生成失败\n\n无法完成报告格式化。"

    def _format_report_with_full_content(
        self, paragraphs_data: List[Dict[str, str]]
    ) -> str:
        """
        使用完整内容生成报告（当LLM输出过短时的备用方法）

        Args:
            paragraphs_data: 段落数据列表

        Returns:
            包含所有段落完整内容的Markdown报告
        """
        try:
            logger.info("使用完整内容备用格式化方法")

            # 构建报告
            report_lines = [
                "# 【全景解析】阿里巴巴港股多维度融合分析报告",
                "",
                "---",
                "",
            ]

            # 添加各个段落的完整内容
            for i, paragraph in enumerate(paragraphs_data, 1):
                title = paragraph.get("title", f"段落 {i}")
                content = paragraph.get("paragraph_latest_state", "")

                if content:
                    report_lines.extend(
                        [f"## {i}. {title}", "", content, "", "---", ""]
                    )

            # 添加综合结论
            report_lines.extend(
                [
                    "## 综合结论",
                    "",
                    "本报告通过多维度、多模态的深度分析，全面解析了阿里巴巴港股的基本面、财务表现、行业环境、股价走势及未来展望。",
                    "报告整合了文字、数据、视觉等多种信息源，为投资者提供了立体化的决策参考。",
                    "",
                ]
            )

            final_report = "\n".join(report_lines)
            logger.info(f"完整内容报告生成完成，总长度: {len(final_report)} 字符")
            return final_report

        except Exception as e:
            logger.exception(f"完整内容格式化失败: {str(e)}")
            # 如果备用方法也失败，使用最基础的格式化
            return self.format_report_manually(paragraphs_data, "深度研究报告")
