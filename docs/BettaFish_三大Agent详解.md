# BettaFish 三大核心 Agent 详解

> BettaFish 微舆系统 Agent 架构说明  
> 更新时间：2025-11-11

## 📋 目录

- [1. 系统架构概览](#1-系统架构概览)
- [2. Query Engine - 新闻搜索Agent](#2-query-engine---新闻搜索agent)
- [3. Media Engine - 多模态分析Agent](#3-media-engine---多模态分析agent)
- [4. Insight Engine - 数据库挖掘Agent](#4-insight-engine---数据库挖掘agent)
- [5. 三大Agent对比](#5-三大agent对比)
- [6. 数据流转](#6-数据流转)
- [7. 常见问题](#7-常见问题)

---

## 1. 系统架构概览

### 1.1 三大Agent分工

```
用户查询："分析武汉大学的品牌声誉"
         ↓
    并行启动三个Agent
         ↓
┌────────┴────────┬────────────┐
│                 │            │
▼                 ▼            ▼
Query Engine    Media Engine  Insight Engine
国内外新闻      多模态内容    私有数据库
广度搜索        深度分析      深度挖掘
│                 │            │
└────────┬────────┴────────────┘
         ↓
    Forum Engine
    (协调讨论)
         ↓
    Report Agent
    (生成报告)
```

---

### 1.2 核心特点

| Agent | 核心功能 | 数据来源 | 特点 |
|-------|---------|---------|------|
| **Query Engine** | 新闻搜索 | 外部网站 | 广度覆盖 |
| **Media Engine** | 多模态分析 | 社交媒体 | 深度理解 |
| **Insight Engine** | 数据挖掘 | 私有数据库 | 历史洞察 |

---

## 2. Query Engine - 新闻搜索Agent

### 2.1 功能定位

**国内外新闻广度搜索Agent**

- 🌐 搜索国内外主流新闻网站
- 📰 获取最新热点资讯
- 🔍 多维度信息覆盖
- 📊 快速概览舆情态势

---

### 2.2 工作原理

```
用户查询
    ↓
生成报告结构
    ↓
初步搜索 (Tavily/Bocha)
    ↓
生成初始总结
    ↓
反思循环 (2轮)
  - 发现盲点
  - 深入搜索
  - 更新总结
    ↓
输出分析结果
```

---

### 2.3 搜索工具

**支持的搜索引擎**：

1. **Tavily Search**
   - 专业的新闻搜索API
   - 支持时间范围过滤
   - 高质量结果

2. **Bocha Search**
   - 国内搜索引擎
   - 中文内容优化
   - 实时新闻

**搜索类型**：
- `search_news_last_24_hours` - 最近24小时
- `search_news_last_week` - 最近一周
- `basic_search_news` - 基础新闻搜索
- `search_news_by_date` - 按日期搜索

---

### 2.4 数据来源

**外部新闻网站**：
- 国内：新华网、人民网、中新网等
- 国际：BBC、CNN、路透社等
- 社交媒体：微博热搜、知乎热榜等

**特点**：
- ✅ 实时性强
- ✅ 覆盖面广
- ⚠️ 可能触发内容审核（敏感话题）

---

### 2.5 配置说明

```bash
# .env 配置
QUERY_ENGINE_API_KEY=your_api_key
QUERY_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QUERY_ENGINE_MODEL_NAME=qwen-max

# 搜索工具配置
TAVILY_API_KEY=your_tavily_key
BOCHA_WEB_SEARCH_API_KEY=your_bocha_key
```

---

### 2.6 使用场景

**适合**：
- ✅ 最新热点事件分析
- ✅ 突发事件追踪
- ✅ 国际舆情监测
- ✅ 新闻趋势分析

**不适合**：
- ❌ 历史数据分析
- ❌ 深度用户画像
- ❌ 情感细节分析

---

## 3. Media Engine - 多模态分析Agent

### 3.1 功能定位

**强大的多模态理解Agent**

- 🖼️ 图像内容分析
- 🎥 视频内容理解
- 📱 社交媒体内容
- 🎨 视觉传播分析

---

### 3.2 工作原理

```
用户查询
    ↓
多模态搜索
  - 图片搜索
  - 视频搜索
  - 文本搜索
    ↓
内容理解
  - 视觉元素识别
  - 情感色彩分析
  - 传播效果评估
    ↓
综合分析
    ↓
输出洞察
```

---

### 3.3 支持的平台

**社交媒体**：
- 抖音 (Douyin)
- 快手 (Kuaishou)
- B站 (Bilibili)
- 小红书 (Xiaohongshu)
- Instagram
- YouTube

**分析维度**：
- 视觉内容（画面、色彩、构图）
- 音频内容（背景音乐、旁白）
- 文本内容（标题、描述、评论）
- 传播数据（播放量、点赞、转发）

---

### 3.4 多模态能力

**图像理解**：
```python
# 分析图片内容
- 识别主体对象
- 分析情感色彩
- 提取文字信息
- 评估视觉冲击力
```

**视频分析**：
```python
# 分析视频内容
- 关键帧提取
- 场景识别
- 人物识别
- 情感倾向分析
```

---

### 3.5 配置说明

```bash
# .env 配置
MEDIA_ENGINE_API_KEY=your_api_key
MEDIA_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MEDIA_ENGINE_MODEL_NAME=qwen-vl-max  # 多模态模型
```

**推荐模型**：
- `qwen-vl-max` - 阿里云多模态模型
- `gemini-2.0-flash-exp` - Google 多模态模型
- `gpt-4o` - OpenAI 多模态模型

---

### 3.6 使用场景

**适合**：
- ✅ 短视频传播分析
- ✅ 品牌视觉形象评估
- ✅ 网红营销效果分析
- ✅ 视觉内容趋势研究

**不适合**：
- ❌ 纯文本新闻分析
- ❌ 历史数据挖掘

---

## 4. Insight Engine - 数据库挖掘Agent

### 4.1 功能定位

**私有数据库深度挖掘Agent**

- 💾 查询历史舆情数据
- 📈 分析趋势变化
- 💬 深度评论分析
- 🎯 精准用户画像

---

### 4.2 什么是"私有数据库"？

**数据来源**：

```
MindSpider 爬虫系统
       ↓
  自动爬取数据
  - 微博
  - 小红书
  - 抖音
  - 快手
  - B站
       ↓
  存储到 PostgreSQL
       ↓
  Insight Engine 查询分析
```

**数据库表结构**：
```sql
-- 每日新闻表
daily_news
  - news_id (新闻ID)
  - title (标题)
  - source_platform (来源平台)
  - crawl_date (爬取日期)

-- 话题表
daily_topics
  - topic_id (话题ID)
  - topic_name (话题名称)
  - keywords (关键词)

-- 微博内容表
weibo_note
  - note_id (微博ID)
  - content (内容)
  - like_count (点赞数)
  - comment_count (评论数)

-- 评论表
comments
  - comment_id (评论ID)
  - content (评论内容)
  - sentiment (情感倾向)
```

---

### 4.3 工作原理

```
用户查询
    ↓
关键词优化 (Qwen)
    ↓
数据库搜索
  - 搜索相关内容
  - 获取评论数据
  - 统计分析
    ↓
情感分析
  - 正面/负面/中性
  - 情感强度
  - 情感趋势
    ↓
深度洞察
  - 热点话题
  - 用户画像
  - 传播路径
    ↓
输出报告
```

---

### 4.4 核心功能

#### 功能 1：关键词优化

```python
# 使用小参数 Qwen 模型优化搜索关键词
用户输入: "武汉大学"
优化后: ["武汉大学", "武大", "WHU", "珞珈山"]
```

#### 功能 2：数据库查询

```python
# 搜索相关内容
search_topic_globally(
    keywords=["武汉大学"],
    limit=200
)

# 获取评论
get_comments(
    note_ids=[...],
    limit=500
)
```

#### 功能 3：情感分析

**支持多种模型**：
- BERT 中文模型
- 多语言情感模型
- Qwen 微调模型
- 传统机器学习模型

```python
# 情感分析结果
{
    "positive": 65%,
    "neutral": 30%,
    "negative": 5%
}
```

---

### 4.5 数据获取方式

#### 方式 1：运行爬虫（本地）

```bash
# 进入爬虫目录
cd MindSpider

# 初始化数据库
python main.py --setup

# 运行话题提取
python main.py --broad-topic

# 运行深度爬取
python main.py --deep-sentiment --platforms xhs dy wb

# 完整流程
python main.py --complete --date 2024-11-11
```

**注意**：
- 需要配置爬虫相关设置
- 爬取需要时间
- 详见 `MindSpider/README.md`

---

#### 方式 2：云数据库服务（推荐）

**项目提供免费云数据库**：
- 📧 联系：670939375@qq.com
- 📊 数据：日均 10万+ 真实舆情
- ✅ 实时更新
- ✅ 多维度标签

**注意**：自 2025年10月1日起暂停新申请

---

### 4.6 配置说明

```bash
# .env 配置
INSIGHT_ENGINE_API_KEY=your_api_key
INSIGHT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
INSIGHT_ENGINE_MODEL_NAME=qwen-max

# 关键词优化器
KEYWORD_OPTIMIZER_API_KEY=your_api_key
KEYWORD_OPTIMIZER_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_USER=bettafish
DB_PASSWORD=your_password
DB_NAME=bettafish
DB_DIALECT=postgresql
```

---

### 4.7 使用场景

**适合**：
- ✅ 历史趋势分析
- ✅ 深度用户画像
- ✅ 情感细节研究
- ✅ 传播路径追踪

**不适合**：
- ❌ 最新突发事件（数据有延迟）
- ❌ 国际舆情（主要是国内数据）

**前提条件**：
- ⚠️ 需要有数据（运行爬虫或使用云数据库）
- ⚠️ 数据库为空时无法工作

---

## 5. 三大Agent对比

### 5.1 功能对比

| 维度 | Query Engine | Media Engine | Insight Engine |
|------|-------------|--------------|----------------|
| **数据来源** | 外部新闻网站 | 社交媒体平台 | 私有数据库 |
| **实时性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **覆盖广度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **分析深度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **历史数据** | ❌ | ❌ | ✅ |
| **多模态** | ❌ | ✅ | ⚠️ 部分 |
| **情感分析** | ⚠️ 基础 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **用户画像** | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

### 5.2 技术栈对比

| 组件 | Query Engine | Media Engine | Insight Engine |
|------|-------------|--------------|----------------|
| **LLM模型** | qwen-max | qwen-vl-max | qwen-max |
| **搜索工具** | Tavily, Bocha | 社交媒体API | SQL查询 |
| **特殊能力** | 网页搜索 | 多模态理解 | 情感分析 |
| **中间件** | - | - | 关键词优化器 |

---

### 5.3 适用场景对比

#### 场景 1：突发热点事件

```
最佳选择: Query Engine
理由: 实时性强，覆盖面广

示例: "某明星突发事件"
- Query Engine: 搜索最新新闻报道 ✅
- Media Engine: 分析社交媒体反应 ✅
- Insight Engine: 历史数据对比 ⚠️
```

---

#### 场景 2：品牌视觉形象分析

```
最佳选择: Media Engine
理由: 多模态分析能力强

示例: "某品牌广告效果"
- Query Engine: 搜索新闻评价 ⚠️
- Media Engine: 分析视频传播 ✅
- Insight Engine: 历史数据对比 ✅
```

---

#### 场景 3：深度舆情研究

```
最佳选择: Insight Engine
理由: 历史数据丰富，分析深入

示例: "某话题长期趋势"
- Query Engine: 最新动态 ⚠️
- Media Engine: 视觉传播 ⚠️
- Insight Engine: 趋势分析 ✅
```

---

### 5.4 内容安全对比

| Agent | 触发审核风险 | 原因 | 解决方案 |
|-------|-------------|------|---------|
| **Query Engine** | ⚠️ 高 | 搜索外部敏感新闻 | 更换模型/过滤内容 |
| **Media Engine** | ⚠️ 中 | 分析社交媒体内容 | 较少触发 |
| **Insight Engine** | ✅ 低 | 私有数据库可控 | 基本不触发 |

---

## 6. 数据流转

### 6.1 完整分析流程

```
用户输入查询
       ↓
┌──────┴──────┬──────────┐
│             │          │
▼             ▼          ▼
Query       Media     Insight
Engine      Engine    Engine
│             │          │
│ 搜索新闻    │ 分析视频  │ 查询数据库
│ 外部网站    │ 社交媒体  │ 历史数据
│             │          │
└──────┬──────┴──────────┘
       ↓
  Forum Engine
  (协调讨论)
       ↓
  各Agent阅读论坛
  调整研究方向
       ↓
  循环迭代 2-3 轮
       ↓
  Report Agent
  (整合报告)
       ↓
  最终分析报告
```

---

### 6.2 数据交互

**Agent 之间的协作**：

```python
# Query Engine 发现
"微博热搜显示武汉大学樱花季讨论量激增"

# Media Engine 补充
"抖音相关视频播放量达500万，主要是校园风景"

# Insight Engine 深入
"历史数据显示，每年3-4月是讨论高峰期
 今年正面情感比例比去年提升10%"

# Forum Host 总结
"综合三方分析，武汉大学品牌传播主要依赖自然景观
 建议加强学术成果的社交媒体传播"
```

---

## 7. 常见问题

### Q1: 为什么 Query Engine 报内容安全错误？

**原因**：Query Engine 搜索外部新闻，结果可能包含敏感内容

**解决**：
1. 使用更中性的查询词
2. 更换为审核宽松的模型（DeepSeek/OpenAI）
3. 部署 One API 配置多模型备选

---

### Q2: Insight Engine 无法工作怎么办？

**原因**：数据库为空，没有数据可查询

**解决**：
1. 运行爬虫爬取数据：`python main.py --complete`
2. 申请云数据库服务
3. 暂时只使用 Query 和 Media Engine

---

### Q3: 如何选择使用哪个 Agent？

**建议**：
- 最新热点 → Query Engine
- 视觉内容 → Media Engine
- 历史趋势 → Insight Engine
- 综合分析 → 三个都用（推荐）

---

### Q4: 三个 Agent 可以单独使用吗？

**可以**！每个 Agent 都有独立的 Streamlit 应用：

```bash
# 单独启动 Query Engine
streamlit run SingleEngineApp/query_engine_streamlit_app.py --server.port 8503

# 单独启动 Media Engine
streamlit run SingleEngineApp/media_engine_streamlit_app.py --server.port 8502

# 单独启动 Insight Engine
streamlit run SingleEngineApp/insight_engine_streamlit_app.py --server.port 8501
```

---

### Q5: 如何优化分析效果？

**建议**：
1. **Query Engine**: 使用精准的搜索关键词
2. **Media Engine**: 选择多模态能力强的模型
3. **Insight Engine**: 确保数据库数据充足且更新
4. **Forum Engine**: 让三个 Agent 充分讨论（多轮迭代）

---

## 8. 配置示例

### 8.1 完整 .env 配置

```bash
# ====================== 数据库配置 ======================
DB_HOST=localhost
DB_PORT=5432
DB_USER=bettafish
DB_PASSWORD=bettafish_2024
DB_NAME=bettafish
DB_CHARSET=utf8mb4
DB_DIALECT=postgresql

# ====================== Query Engine ======================
QUERY_ENGINE_API_KEY=sk-your-key
QUERY_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QUERY_ENGINE_MODEL_NAME=qwen-max

# ====================== Media Engine ======================
MEDIA_ENGINE_API_KEY=sk-your-key
MEDIA_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MEDIA_ENGINE_MODEL_NAME=qwen-vl-max

# ====================== Insight Engine ======================
INSIGHT_ENGINE_API_KEY=sk-your-key
INSIGHT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
INSIGHT_ENGINE_MODEL_NAME=qwen-max

# ====================== 关键词优化器 ======================
KEYWORD_OPTIMIZER_API_KEY=sk-your-key
KEYWORD_OPTIMIZER_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo

# ====================== 搜索工具 ======================
TAVILY_API_KEY=your-tavily-key
BOCHA_WEB_SEARCH_API_KEY=your-bocha-key
```

---

### 8.2 推荐模型组合

#### 组合 1：全阿里云（成本优化）

```bash
QUERY_ENGINE_MODEL_NAME=qwen-plus       # 快速搜索
MEDIA_ENGINE_MODEL_NAME=qwen-vl-max     # 多模态
INSIGHT_ENGINE_MODEL_NAME=qwen-max      # 深度分析
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo # 轻量优化
```

---

#### 组合 2：混合方案（效果优先）

```bash
QUERY_ENGINE_MODEL_NAME=deepseek-chat   # 避免审核
MEDIA_ENGINE_MODEL_NAME=gemini-2.0-flash-exp  # 多模态强
INSIGHT_ENGINE_MODEL_NAME=qwen-max      # 深度分析
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo # 轻量优化
```

---

#### 组合 3：国际模型（无审核限制）

```bash
QUERY_ENGINE_MODEL_NAME=gpt-4o-mini     # OpenAI
MEDIA_ENGINE_MODEL_NAME=gpt-4o          # 多模态
INSIGHT_ENGINE_MODEL_NAME=claude-3-opus # 深度分析
KEYWORD_OPTIMIZER_MODEL_NAME=gpt-4o-mini # 优化
```

---

## 9. 总结

### 核心要点

1. **Query Engine** = 新闻搜索 + 外部数据 + 实时性强
2. **Media Engine** = 多模态分析 + 视觉理解 + 社交媒体
3. **Insight Engine** = 数据库挖掘 + 历史分析 + 深度洞察

### 协作机制

三个 Agent 通过 **Forum Engine** 协作：
- 独立分析 → 发布发现 → 主持人总结 → 调整方向 → 深入研究

### 使用建议

- ✅ **完整分析**：三个 Agent 都启用
- ✅ **快速测试**：只用 Query + Media
- ✅ **深度研究**：重点用 Insight（需要数据）

---

**BettaFish 的强大之处在于三个 Agent 的协同工作，通过 Forum Engine 的协调，产生超越单一 Agent 的分析质量！**

---

## 参考资源

- 项目地址：https://github.com/666ghj/BettaFish
- 完整文档：[README.md](../README.md)
- Forum Engine：[ForumEngine_简明指南.md](./ForumEngine_简明指南.md)
- AI 网关对比：[AI_Gateway_Comparison.md](./AI_Gateway_Comparison.md)

---

**文档维护**：BettaFish 项目组 | 更新：2025-11-11
