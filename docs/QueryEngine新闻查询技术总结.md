# QueryEngine 新闻查询技术总结

## 📋 概述

QueryEngine 是 BettaFish 项目的**新闻舆情查询引擎**，专门负责**实时新闻搜索和深度分析**。与 InsightEngine 不同，QueryEngine 不依赖本地数据库，而是通过 **Tavily API** 实时查询全球新闻资源，实现**实时性强、覆盖面广、深度分析**的新闻舆情研究。

**版本**: 1.5  
**最后更新**: 2025-08-22  
**核心特性**: 实时新闻搜索、深度分析、时间范围筛选、图片搜索、反思迭代

---

## 🎯 支持的查询平台种类

### 平台支持说明

QueryEngine 通过 **Tavily API** 实现**全球新闻搜索**，专注于新闻内容：

**核心特点**：
- ✅ **新闻专注**: 专门针对新闻内容优化
- ✅ **全球覆盖**: 支持多语言、多地区新闻源
- ✅ **实时更新**: 最快可获取24小时内的最新新闻
- ✅ **AI 增强**: 支持深度分析和智能摘要

QueryEngine 通过 **Tavily API** 支持 **全球新闻源**，包括但不限于：

### 1. 主流新闻媒体
- **国际媒体**: CNN, BBC, Reuters, AP, Bloomberg, The Guardian, New York Times
- **科技媒体**: TechCrunch, The Verge, Wired, Ars Technica
- **财经媒体**: Financial Times, Wall Street Journal, Forbes
- **中文媒体**: 新华网、人民网、央视新闻、澎湃新闻等

### 2. 专业领域新闻
- **科技创新**: AI、芯片、自动驾驶、量子计算
- **商业财经**: 股市、企业动态、经济政策
- **社会民生**: 教育、医疗、环境、法律
- **国际政治**: 外交、军事、地缘政治

### 3. 覆盖范围
- ✅ **全球覆盖**: 支持多语言新闻源
- ✅ **实时更新**: 最快可获取24小时内的最新新闻
- ✅ **历史查询**: 支持按日期范围查询历史新闻
- ✅ **多媒体**: 支持新闻图片搜索

---

## 🔧 核心查询工具

QueryEngine 提供 **6 种专业的新闻查询工具**：

### 1. basic_search_news - 基础新闻搜索
```python
def basic_search_news(query: str, max_results: int = 7) -> TavilyResponse
```

**功能**: 执行标准、快速的通用新闻搜索

**适用场景**:
- 常规新闻查询
- 快速了解某个话题
- 不确定需要何种特定搜索时

**特点**:
- ✅ 速度快，响应时间短
- ✅ 返回最相关的 7 条新闻
- ✅ 最常用的通用搜索工具

**示例**:
```python
# 快速搜索奥运会新闻
response = agency.basic_search_news(query="奥运会最新赛况", max_results=5)
```

### 2. deep_search_news - 深度新闻分析
```python
def deep_search_news(query: str) -> TavilyResponse
```

**功能**: 对主题进行最全面、最深入的搜索

**适用场景**:
- 全面了解事件背景
- 深度研究某个话题
- 需要 AI 生成的详细摘要

**特点**:
- ✅ 返回 AI 生成的"高级"详细摘要
- ✅ 最多返回 20 条最相关的新闻
- ✅ 搜索深度最高

**示例**:
```python
# 深度分析全球芯片竞争
response = agency.deep_search_news(query="全球芯片技术竞争")
```

### 3. search_news_last_24_hours - 24小时内新闻
```python
def search_news_last_24_hours(query: str) -> TavilyResponse
```

**功能**: 获取过去24小时内的最新动态

**适用场景**:
- 追踪突发事件
- 监测最新进展
- 实时舆情监控

**特点**:
- ✅ 只返回24小时内发布的新闻
- ✅ 时效性最强
- ✅ 返回最多 10 条结果

**示例**:
```python
# 追踪 GTC 大会最新消息
response = agency.search_news_last_24_hours(query="Nvidia GTC大会 最新发布")
```

### 4. search_news_last_week - 本周新闻
```python
def search_news_last_week(query: str) -> TavilyResponse
```

**功能**: 获取过去一周内的主要新闻报道

**适用场景**:
- 周度舆情总结
- 一周回顾
- 趋势分析

**特点**:
- ✅ 返回过去7天的新闻
- ✅ 适合周报制作
- ✅ 返回最多 10 条结果

**示例**:
```python
# 查找自动驾驶本周新闻
response = agency.search_news_last_week(query="自动驾驶商业化落地")
```

### 5. search_images_for_news - 新闻图片搜索
```python
def search_images_for_news(query: str) -> TavilyResponse
```

**功能**: 搜索与新闻主题相关的图片

**适用场景**:
- 为报告配图
- 可视化新闻内容
- 多媒体报道

**特点**:
- ✅ 返回图片链接和描述
- ✅ 图片与新闻主题高度相关
- ✅ 返回最多 5 张图片

**示例**:
```python
# 查找韦伯望远镜新闻图片
response = agency.search_images_for_news(query="韦伯太空望远镜最新发现")
```

### 6. search_news_by_date - 按日期范围搜索
```python
def search_news_by_date(
    query: str, 
    start_date: str,  # 'YYYY-MM-DD'
    end_date: str     # 'YYYY-MM-DD'
) -> TavilyResponse
```

**功能**: 在指定历史时间段内搜索新闻

**适用场景**:
- 历史事件分析
- 特定时期研究
- 时间线梳理

**特点**:
- ✅ 精确的时间范围控制
- ✅ 唯一需要详细时间参数的工具
- ✅ 返回最多 15 条结果

**示例**:
```python
# 研究2025年Q1的AI法规新闻
response = agency.search_news_by_date(
    query="人工智能法规",
    start_date="2025-01-01",
    end_date="2025-03-31"
)
```

---

## 📍 用户输入查询时的默认行为

**当您在页面上直接输入要分析的内容时**：

1. **默认查询工具**: `basic_search_news`（基础新闻搜索）
   ```python
   # 代码位置: agent.py 第 244 行
   search_tool = search_output.get("search_tool", "basic_search_news")  # 默认工具
   ```

2. **默认搜索范围**: **全球新闻源**（无平台限制）
   - 🌐 全球主流新闻媒体
   - 📰 国际新闻网站（CNN, BBC, Reuters等）
   - 💼 财经媒体（Bloomberg, WSJ等）
   - 🔬 科技媒体（TechCrunch, The Verge等）
   - 🇨🇳 中文新闻媒体（新华网、人民网等）
   - 🌍 多语言新闻源

3. **智能工具选择机制**:
   - LLM 会根据查询内容**自动选择最合适的新闻搜索工具**
   - 如果 LLM 没有明确指定工具，则使用默认的 `basic_search_news`
   - 如果 LLM 选择的工具缺少必要参数，会**自动降级**到 `basic_search_news`

4. **自动降级场景**:
   ```python
   # 场景: search_news_by_date 缺少日期参数
   if search_tool == "search_news_by_date":
       if not (start_date and end_date):
           search_tool = "basic_search_news"  # 降级到基础搜索
   ```

5. **默认返回内容**:
   - ✅ **新闻标题**: 最多 7 条新闻（可配置）
   - ✅ **新闻链接**: 原始新闻 URL
   - ✅ **新闻摘要**: 内容概要
   - ✅ **发布日期**: 新闻发布时间
   - ✅ **相关性评分**: 搜索相关性得分

6. **工具选择示例**:
   ```python
   # 查询: "人工智能最新进展"
   # LLM 选择: basic_search_news
   # 返回: 7条相关新闻
   
   # 查询: "深度分析AI对教育的影响"
   # LLM 选择: deep_search_news
   # 返回: AI生成的深度摘要 + 20条新闻
   
   # 查询: "今天的科技新闻"
   # LLM 选择: search_news_last_24_hours
   # 返回: 24小时内的最新科技新闻
   
   # 查询: "2025年1月的AI新闻"
   # LLM 选择: search_news_by_date
   # 参数: start_date="2025-01-01", end_date="2025-01-31"
   # 返回: 指定时间范围内的新闻
   ```

**总结**：
- 🎯 **默认工具**: `basic_search_news`（基础新闻搜索）
- 🌐 **默认范围**: 全球新闻源（无平台限制）
- 🤖 **智能选择**: LLM 根据查询内容自动选择工具
- 🔄 **自动降级**: 参数不足时自动降级到基础搜索
- 📰 **新闻专注**: 只返回新闻内容，不包含其他类型网页
- ⏰ **时间灵活**: 支持24小时、一周、自定义日期范围

---

## 🛡️ 如何突破安全访问限制

### 核心策略：使用 Tavily API + 重试机制

**与 InsightEngine 的本质区别**:
- ❌ **InsightEngine**: 查询本地数据库，数据需预先爬取
- ✅ **QueryEngine**: 调用 Tavily API，**实时获取全球新闻**

### 1. 使用 Tavily 专业 API

**实现方式**: 通过 Tavily API 访问全球新闻资源

```python
from tavily import TavilyClient

class TavilyNewsAgency:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("TAVILY_API_KEY")
        self._client = TavilyClient(api_key=api_key)
```

**Tavily API 的优势**:
- ✅ **合法授权**: Tavily 与新闻源有合作协议
- ✅ **无反爬虫**: API 调用不会触发反爬虫机制
- ✅ **全球覆盖**: 覆盖全球主流新闻源
- ✅ **实时更新**: 新闻数据实时同步

**Tavily 如何解决安全访问问题**:
1. **商业合作**: Tavily 与新闻媒体有商业合作协议
2. **API 授权**: 通过 API Key 进行身份验证
3. **合规爬取**: Tavily 后端使用合规的爬虫技术
4. **数据缓存**: Tavily 维护新闻数据缓存，减少实时请求

### 2. 智能重试机制

**实现方式**: 使用装饰器实现带停止事件的重试

```python
from retry_helper import with_graceful_retry, SEARCH_API_RETRY_CONFIG

def _search_internal(self, **kwargs) -> TavilyResponse:
    """内部通用的搜索执行器"""
    @with_graceful_retry(
        SEARCH_API_RETRY_CONFIG, 
        default_return=TavilyResponse(query="搜索失败"), 
        stop_event=self.stop_event
    )
    def _do_search():
        try:
            api_params = {k: v for k, v in kwargs.items() if v is not None}
            response_dict = self._client.search(**api_params)
            return self._parse_response(response_dict)
        except Exception as e:
            print(f"搜索时发生错误: {str(e)}")
            raise e  # 让重试机制捕获并处理
    
    return _do_search()
```

**重试配置**:
```python
SEARCH_API_RETRY_CONFIG = RetryConfig(
    max_retries=3,              # 最大重试3次
    initial_delay=1.0,          # 初始延迟1秒
    backoff_factor=2.0,         # 指数退避
    max_delay=60.0,             # 最大延迟60秒
    retry_on_exceptions=(       # 需要重试的异常类型
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        ConnectionError,
        TimeoutError,
        Exception
    )
)
```

**优势**:
- ✅ **自动重试**: 网络错误时自动重试
- ✅ **指数退避**: 避免频繁请求
- ✅ **优雅中断**: 支持用户主动停止
- ✅ **默认返回**: 失败时返回默认值，不中断流程

### 3. 统一数据结构

**数据结构设计**:

```python
@dataclass
class SearchResult:
    """网页搜索结果数据类"""
    title: str
    url: str
    content: str
    score: Optional[float] = None
    raw_content: Optional[str] = None
    published_date: Optional[str] = None  # 新闻发布日期

@dataclass
class ImageResult:
    """图片搜索结果数据类"""
    url: str
    description: Optional[str] = None

@dataclass
class TavilyResponse:
    """封装Tavily API的完整返回结果"""
    query: str
    answer: Optional[str] = None           # AI生成的摘要
    results: List[SearchResult] = field(default_factory=list)
    images: List[ImageResult] = field(default_factory=list)
    response_time: Optional[float] = None
```

**优势**:
- ✅ **类型安全**: 使用 dataclass 确保类型正确
- ✅ **易于处理**: 统一接口便于后续分析
- ✅ **包含元数据**: 保留发布日期、评分等信息

### 4. API 参数优化

**实现方式**: 针对不同场景优化 API 参数

```python
# 基础搜索: 快速、通用
self._search_internal(
    query=query,
    max_results=7,
    search_depth="basic",      # 基础搜索深度
    include_answer=False       # 不生成AI摘要
)

# 深度搜索: 全面、详细
self._search_internal(
    query=query,
    search_depth="advanced",   # 高级搜索深度
    max_results=20,            # 更多结果
    include_answer="advanced"  # 生成高级AI摘要
)

# 时间范围搜索: 精确控制
self._search_internal(
    query=query,
    time_range='d',            # 'd'=24小时, 'w'=一周
    max_results=10
)

# 图片搜索: 多媒体
self._search_internal(
    query=query,
    include_images=True,              # 包含图片
    include_image_descriptions=True,  # 包含图片描述
    max_results=5
)
```

**优势**:
- ✅ **场景优化**: 不同工具使用不同参数组合
- ✅ **性能平衡**: 在速度和质量之间取得平衡
- ✅ **成本控制**: 合理控制 API 调用成本

### 5. 错误处理和降级

**实现方式**: 多层错误处理机制

```python
def _search_internal(self, **kwargs) -> TavilyResponse:
    @with_graceful_retry(...)
    def _do_search():
        try:
            # 1. 执行搜索
            response_dict = self._client.search(**api_params)
            
            # 2. 解析响应
            search_results = [...]
            return TavilyResponse(...)
            
        except Exception as e:
            # 3. 记录错误
            print(f"搜索时发生错误: {str(e)}")
            # 4. 抛出异常让重试机制处理
            raise e
    
    # 5. 返回结果或默认值
    return _do_search()
```

**错误处理层次**:
1. **API 层**: Tavily SDK 内部错误处理
2. **重试层**: 自动重试机制
3. **降级层**: 返回默认值，不中断流程
4. **日志层**: 记录所有错误信息

**优势**:
- ✅ **健壮性强**: 多层保护机制
- ✅ **用户友好**: 错误不会中断整个流程
- ✅ **可追溯**: 完整的错误日志

---

## 💡 技术创新点

### 1. 实时新闻获取
- ✅ 通过 Tavily API 实时查询全球新闻
- ✅ 最快可获取24小时内的最新新闻
- ✅ 无需维护本地数据库

### 2. AI 深度分析
- ✅ 支持 AI 生成的新闻摘要
- ✅ 自动提取关键信息
- ✅ 智能相关性评分

### 3. 灵活时间控制
- ✅ 支持24小时、一周、自定义日期范围
- ✅ 精确到日的时间筛选
- ✅ 历史新闻回溯

### 4. 多媒体支持
- ✅ 新闻文本搜索
- ✅ 新闻图片搜索
- ✅ 图片描述生成

### 5. 反思迭代机制
- ✅ 自动识别信息缺口
- ✅ 迭代补充查询
- ✅ 最多 3 轮优化

### 6. 智能工具选择
- ✅ LLM 自动选择最合适的查询工具
- ✅ 根据任务意图动态调整
- ✅ 参数自动优化

---

## 🔄 深度研究工作流程

### 工作流程图

```
用户查询
    ↓
1. 生成报告结构
    ↓
2. 对每个段落:
    ├─ 2.1 首次搜索
    │   ├─ LLM 生成搜索查询
    │   ├─ 选择 Tavily 查询工具
    │   └─ 执行实时新闻搜索
    │
    ├─ 2.2 首次总结
    │   └─ 基于查询结果生成初始内容
    │
    └─ 2.3 反思循环 (最多3次)
        ├─ 反思分析
        ├─ 补充查询
        └─ 反思总结
    ↓
3. 格式化最终报告
    ↓
4. 保存报告
```

### 关键特性

#### 1. 智能工具选择
```python
# LLM 自动选择最合适的查询工具
{
    "search_query": "Nvidia GTC大会最新发布",
    "search_tool": "search_news_last_24_hours",
    "reasoning": "需要追踪最新动态，选择24小时内新闻搜索"
}
```

#### 2. 动态参数生成
```python
# LLM 自动生成日期参数
{
    "search_query": "2025年第一季度AI法规",
    "search_tool": "search_news_by_date",
    "reasoning": "需要查询特定时期的新闻",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31"
}
```

---

## 🔐 安全性与合规性总结

### API 访问
1. ✅ **合法授权**: 使用 Tavily 官方 API
2. ✅ **身份验证**: API Key 认证机制
3. ✅ **速率限制**: 遵守 API 调用限制
4. ✅ **数据合规**: Tavily 确保数据来源合法

### 数据来源
1. ✅ **授权新闻源**: Tavily 与新闻媒体有合作协议
2. ✅ **实时同步**: 新闻数据实时更新
3. ✅ **全球覆盖**: 支持多语言、多地区新闻

### 稳定性保障
1. ✅ **重试机制**: 自动重试失败的请求
2. ✅ **优雅降级**: 失败时返回默认值
3. ✅ **错误处理**: 完善的异常捕获
4. ✅ **用户中断**: 支持用户主动停止

---

## 📚 技术栈

### 核心依赖
- **Tavily Python SDK**: 官方 API 客户端
- **OpenAI SDK**: LLM 调用（兼容多种模型）
- **loguru**: 日志记录
- **dataclasses**: 数据结构定义

### API 服务
- **Tavily API**: 新闻搜索服务
- **LLM API**: 通义千问等大语言模型

### 设计模式
- **装饰器模式**: 重试机制
- **工厂模式**: Agent 创建
- **状态模式**: 研究状态管理
- **策略模式**: 多种查询工具

---

## 🎯 使用示例

### 基本使用
```python
from QueryEngine import DeepSearchAgent

# 创建 Agent
agent = DeepSearchAgent()

# 执行深度研究
report = agent.research("分析Nvidia GTC大会的最新发布")
```

### 直接使用查询工具
```python
from QueryEngine.tools import TavilyNewsAgency

agency = TavilyNewsAgency(api_key="your_api_key")

# 基础搜索
response = agency.basic_search_news(query="奥运会最新赛况", max_results=5)

# 深度分析
response = agency.deep_search_news(query="全球芯片技术竞争")

# 24小时内新闻
response = agency.search_news_last_24_hours(query="Nvidia GTC大会")

# 按日期搜索
response = agency.search_news_by_date(
    query="人工智能法规",
    start_date="2025-01-01",
    end_date="2025-03-31"
)
```

---

## 📖 参考资料

### 项目文件
- `QueryEngine/agent.py`: 主 Agent 实现
- `QueryEngine/tools/search.py`: Tavily 查询工具集
- `QueryEngine/nodes/search_node.py`: 搜索节点实现
- `QueryEngine/prompts/prompts.py`: 提示词定义

### 相关文档
- [Tavily API 文档](https://docs.tavily.com/)
- [通义千问 API](https://help.aliyun.com/zh/model-studio/)

### 对比文档
- `InsightEngine本地舆情数据库技术总结.md`: 本地数据库查询方案
- `MediaEngine多模态搜索技术总结.md`: 多模态搜索方案

---

**文档维护**: BettaFish 项目组  
**最后更新**: 2025-11-12  
**版本**: v1.0
