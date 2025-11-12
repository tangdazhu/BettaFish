# InsightEngine 本地舆情数据库技术总结

## 📋 概述

InsightEngine 是 BettaFish 项目的核心舆情分析引擎，专门负责**本地舆情数据库的深度挖掘和智能分析**。与 MediaEngine 不同，InsightEngine 不依赖外部搜索 API，而是直接查询本地 MySQL/PostgreSQL 数据库中已爬取的社交媒体数据，实现**零成本、高速度、全掌控**的舆情分析。

**版本**: 3.0  
**最后更新**: 2025-08-23  
**核心特性**: 本地数据库查询、智能关键词优化、多语言情感分析、7大平台支持

---

## 🎯 支持的查询平台种类

InsightEngine 支持 **7 大主流社交媒体平台** + **1 个新闻聚合平台**：

### 平台支持策略说明

**重要**: InsightEngine 采用 **智能多平台并发查询** 策略：
- ✅ **默认行为**: 大部分查询工具会 **同时搜索所有平台**（除了 `search_topic_on_platform`）
- ✅ **平台选择性**: 只有 `search_topic_on_platform` 工具支持指定单个平台查询
- ✅ **数据完整性**: 所有平台的数据会被聚合、排序后统一返回
- ✅ **代码实现**: 通过 `search_configs` 字典定义所有平台配置，循环查询

#### 查询工具的平台覆盖

| 工具名称 | 平台覆盖 | 说明 |
|---------|---------|------|
| `search_hot_content` | 6个平台 | Bilibili, Douyin, Weibo, XHS, Kuaishou, Zhihu（不含Tieba和News） |
| `search_topic_globally` | 全部8个 | 所有平台 + 评论表 + 新闻 |
| `search_topic_by_date` | 7个平台 + 新闻 | 所有平台（不含评论表） |
| `get_comments_for_topic` | 7个平台的评论 | 所有平台的评论表 |
| `search_topic_on_platform` | 单个指定平台 | 用户指定的1个平台 |

#### 平台支持详情

| 平台 | 支持状态 | 支持的工具数量 | 限制说明 |
|------|---------|--------------|---------|
| **Bilibili** | ✅ 完全支持 | 5/5 | 无限制 |
| **Weibo** | ✅ 完全支持 | 5/5 | 无限制 |
| **Douyin** | ✅ 完全支持 | 5/5 | 无限制 |
| **Kuaishou** | ✅ 完全支持 | 5/5 | 无限制 |
| **XHS** | ✅ 完全支持 | 5/5 | 无限制 |
| **Zhihu** | ✅ 完全支持 | 5/5 | 无限制 |
| **Tieba** | ⚠️ 部分支持 | 4/5 | 不支持 search_hot_content（无互动数据） |
| **Daily News** | ⚠️ 部分支持 | 2/5 | 仅支持 search_topic_globally 和 search_topic_by_date |

#### 用户输入查询时的默认行为

**当您在页面上直接输入要分析的内容时**：

1. **默认查询工具**: `search_topic_globally`（全局话题搜索）
   ```python
   # 代码位置: agent.py 第 468 行
   search_tool = search_output.get("search_tool", "search_topic_globally")  # 默认工具
   ```

2. **默认搜索的平台**: **全部 8 个平台**
   - ✅ Bilibili（B站）- 视频 + 评论
   - ✅ Weibo（微博）- 微博 + 评论
   - ✅ Douyin（抖音）- 视频 + 评论
   - ✅ Kuaishou（快手）- 视频 + 评论
   - ✅ XHS（小红书）- 笔记 + 评论
   - ✅ Zhihu（知乎）- 内容 + 评论
   - ✅ Tieba（贴吧）- 帖子 + 评论
   - ✅ Daily News（新闻）- 新闻标题

3. **智能工具选择机制**:
   - LLM 会根据您的查询内容**自动选择最合适的查询工具**
   - 如果 LLM 没有明确指定工具，则使用 `search_topic_globally`
   - 如果 LLM 选择的工具缺少必要参数，会**自动降级**到 `search_topic_globally`

4. **自动降级场景**:
   ```python
   # 场景1: search_topic_by_date 缺少日期参数
   if search_tool == "search_topic_by_date":
       if not (start_date and end_date):
           search_tool = "search_topic_globally"  # 降级
   
   # 场景2: search_topic_on_platform 缺少平台参数
   if search_tool == "search_topic_on_platform":
       if not platform:
           search_tool = "search_topic_globally"  # 降级
   ```

5. **关键词优化**:
   - 您的原始查询会被 **Qwen AI 优化**为更贴近真实舆情的关键词
   - 优化后的多个关键词会**分别查询**，然后聚合去重

6. **情感分析**:
   - 默认**自动启用**情感分析（`enable_sentiment=True`）
   - 支持 22 种语言的情感倾向分析

**总结**：
- 🎯 **默认工具**: `search_topic_globally`
- 🌐 **默认平台**: 全部 8 个平台（15 个数据表）
- 🤖 **智能选择**: LLM 可根据查询内容自动选择其他工具
- 🔄 **自动降级**: 参数不足时自动降级到全局搜索
- ✨ **关键词优化**: AI 自动优化查询关键词
- 🎭 **情感分析**: 默认自动分析情感倾向

---

### 1. 哔哩哔哩 (Bilibili) ✅ 完全支持
- **数据表**: `bilibili_video`, `bilibili_video_comment`
- **支持字段**: 标题、描述、作者、点赞、评论、分享、收藏、投币、弹幕、播放量
- **时间字段**: `create_time` (秒级时间戳)
- **热度公式**: `点赞×1 + 评论×5 + (分享+收藏+投币)×10 + 弹幕×0.5 + 播放量×0.1`
- **代码验证**: ✅ 在 `search_hot_content`, `search_topic_globally`, `search_topic_by_date`, `get_comments_for_topic`, `search_topic_on_platform` 中均有配置

### 2. 微博 (Weibo) ✅ 完全支持
- **数据表**: `weibo_note`, `weibo_note_comment`
- **支持字段**: 内容、作者、点赞、评论、转发
- **时间字段**: `create_date_time` (字符串格式 'YYYY-MM-DD HH:MM:SS')
- **热度公式**: `点赞×1 + 评论×5 + 转发×10`
- **代码验证**: ✅ 在所有5个查询工具中均有配置

### 3. 抖音 (Douyin) ✅ 完全支持
- **数据表**: `douyin_aweme`, `douyin_aweme_comment`
- **支持字段**: 标题、描述、作者、点赞、评论、分享、收藏
- **时间字段**: `create_time` (毫秒级时间戳)
- **热度公式**: `点赞×1 + 评论×5 + (分享+收藏)×10`
- **代码验证**: ✅ 在所有5个查询工具中均有配置

### 4. 快手 (Kuaishou) ✅ 完全支持
- **数据表**: `kuaishou_video`, `kuaishou_video_comment`
- **支持字段**: 标题、描述、作者、点赞、观看量
- **时间字段**: `create_time` (毫秒级时间戳)
- **热度公式**: `点赞×1 + 观看量×0.1`
- **代码验证**: ✅ 在所有5个查询工具中均有配置

### 5. 小红书 (XHS) ✅ 完全支持
- **数据表**: `xhs_note`, `xhs_note_comment`
- **支持字段**: 标题、描述、标签、作者、点赞、评论、分享、收藏
- **时间字段**: `time` (毫秒级时间戳)
- **热度公式**: `点赞×1 + 评论×5 + (分享+收藏)×10`
- **特殊字段**: `tag_list` 支持标签搜索
- **代码验证**: ✅ 在所有5个查询工具中均有配置

### 6. 知乎 (Zhihu) ✅ 完全支持
- **数据表**: `zhihu_content`, `zhihu_comment`
- **支持字段**: 标题、描述、正文、作者、点赞(赞同)、评论
- **时间字段**: `created_time` (秒级时间戳字符串)
- **热度公式**: `赞同数×1 + 评论×5`
- **特殊字段**: `content_text` 支持正文全文搜索
- **代码验证**: ✅ 在所有5个查询工具中均有配置

### 7. 百度贴吧 (Tieba) ✅ 部分支持
- **数据表**: `tieba_note`, `tieba_comment`
- **支持字段**: 标题、描述、作者
- **时间字段**: `publish_time` (字符串格式)
- **热度公式**: ⚠️ 无互动数据，不参与热度排序
- **代码验证**: ✅ 在 `search_topic_globally`, `search_topic_by_date`, `get_comments_for_topic`, `search_topic_on_platform` 中有配置
- **限制**: ❌ 不支持 `search_hot_content`（因为没有互动数据）

### 8. 每日新闻 (Daily News) ✅ 部分支持
- **数据表**: `daily_news`
- **支持字段**: 标题、URL、爬取日期
- **时间字段**: `crawl_date` (日期字符串 'YYYY-MM-DD')
- **热度公式**: ⚠️ 无互动数据，不参与热度排序
- **代码验证**: ✅ 在 `search_topic_globally`, `search_topic_by_date` 中有配置
- **限制**: ❌ 不支持 `search_hot_content`, `get_comments_for_topic`, `search_topic_on_platform`


---

## 🔧 核心查询工具

InsightEngine 提供 **5 种专业的本地数据库查询工具**：

### 1. search_hot_content - 查找热点内容
```python
def search_hot_content(
    time_period: Literal['24h', 'week', 'year'] = 'week',
    limit: int = 50
) -> DBResponse
```

**功能**: 获取指定时间范围内综合热度最高的内容

**热度计算公式**:
```
热度分 = 点赞数 × 1.0 + 评论数 × 5.0 + (分享/转发/收藏/投币) × 10.0 
       + 观看量 × 0.1 + 弹幕数 × 0.5
```

**特点**:
- ✅ 智能加权算法，综合多维度互动数据
- ✅ 跨平台统一排序
- ✅ 无需指定查询关键词

**示例**:
```python
# 查找过去一周最热的50条内容
response = db.search_hot_content(time_period='week', limit=50)

# 查找过去24小时最热的10条内容
response = db.search_hot_content(time_period='24h', limit=10)
```

### 2. search_topic_globally - 全局话题搜索
```python
def search_topic_globally(topic: str, limit_per_table: int = 100) -> DBResponse
```

**功能**: 在整个数据库中全面搜索指定话题

**搜索范围**:
- ✅ 内容标题
- ✅ 内容正文/描述
- ✅ 评论内容
- ✅ 标签列表
- ✅ 来源关键词

**适用场景**:
- 全面了解某个话题的讨论情况
- 跨平台舆情监测
- 话题传播分析

**示例**:
```python
# 全局搜索"人工智能"相关内容
response = db.search_topic_globally(topic="人工智能", limit_per_table=100)
```

### 3. search_topic_by_date - 按日期搜索话题
```python
def search_topic_by_date(
    topic: str,
    start_date: str,  # 'YYYY-MM-DD'
    end_date: str,    # 'YYYY-MM-DD'
    limit_per_table: int = 100
) -> DBResponse
```

**功能**: 在指定历史时间段内搜索话题

**适用场景**:
- 历史舆情回溯
- 事件时间线分析
- 周期性趋势研究

**示例**:
```python
# 搜索2024年春节期间关于"春晚"的讨论
response = db.search_topic_by_date(
    topic="春晚",
    start_date="2024-02-09",
    end_date="2024-02-11",
    limit_per_table=100
)
```

### 4. get_comments_for_topic - 获取话题评论
```python
def get_comments_for_topic(topic: str, limit: int = 500) -> DBResponse
```

**功能**: 专门提取公众对某一话题的评论数据

**适用场景**:
- 分析公众真实态度
- 提取用户观点
- 评论情感分析

**示例**:
```python
# 获取关于"电动汽车"的500条评论
response = db.get_comments_for_topic(topic="电动汽车", limit=500)
```

### 5. search_topic_on_platform - 平台定向搜索
```python
def search_topic_on_platform(
    platform: Literal['bilibili', 'weibo', 'douyin', 'kuaishou', 'xhs', 'zhihu', 'tieba'],
    topic: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 20
) -> DBResponse
```

**功能**: 在指定单一平台上精确搜索话题

**适用场景**:
- 平台特定舆情分析
- 对比不同平台的讨论差异
- 平台用户画像研究

**示例**:
```python
# 在B站搜索"游戏"相关内容
response = db.search_topic_on_platform(
    platform='bilibili',
    topic="游戏",
    limit=50
)

# 在微博搜索特定日期的"明星"话题
response = db.search_topic_on_platform(
    platform='weibo',
    topic="明星",
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=100
)
```

---

## 💻 多平台查询的代码实现

### 核心实现机制

InsightEngine 通过 **配置驱动的循环查询** 实现多平台支持：

#### 1. 平台配置字典 (search_configs)

每个查询工具都定义了一个 `search_configs` 字典，包含所有支持平台的配置：

```python
# 示例：search_topic_globally 的配置
search_configs = {
    'bilibili_video': {
        'fields': ['title', 'desc', 'source_keyword'],
        'type': 'video'
    },
    'bilibili_video_comment': {
        'fields': ['content'],
        'type': 'comment'
    },
    'douyin_aweme': {
        'fields': ['title', 'desc', 'source_keyword'],
        'type': 'video'
    },
    'douyin_aweme_comment': {
        'fields': ['content'],
        'type': 'comment'
    },
    # ... 其他平台配置
    'xhs_note': {
        'fields': ['title', 'desc', 'tag_list', 'source_keyword'],
        'type': 'note'
    },
    'zhihu_content': {
        'fields': ['title', 'desc', 'content_text', 'source_keyword'],
        'type': 'content'
    },
    'tieba_note': {
        'fields': ['title', 'desc', 'source_keyword'],
        'type': 'note'
    },
    'daily_news': {
        'fields': ['title'],
        'type': 'news'
    }
}
```

#### 2. 循环查询所有平台

```python
# 遍历所有平台配置
for table, config in search_configs.items():
    # 构建 WHERE 子句
    where_clauses = []
    for field in config['fields']:
        where_clauses.append(f"`{field}` LIKE %s")
    where_clause = " OR ".join(where_clauses)
    
    # 执行查询
    query = f"SELECT * FROM `{table}` WHERE {where_clause} LIMIT %s"
    raw_results = self._execute_query(query, params)
    
    # 将结果添加到总结果列表
    all_results.extend(raw_results)
```

#### 3. 统一数据结构

所有平台的查询结果都被转换为统一的 `QueryResult` 对象：

```python
@dataclass
class QueryResult:
    platform: str              # 平台名称 (bilibili, weibo, douyin...)
    content_type: str          # 内容类型 (video, note, comment...)
    title_or_content: str      # 标题或内容
    author_nickname: Optional[str]
    url: Optional[str]
    publish_time: Optional[datetime]
    engagement: Dict[str, int]  # 互动数据 {likes, comments, shares...}
    hotness_score: Optional[float]
    source_keyword: Optional[str]
    source_table: str          # 来源表名
```

#### 4. 热度计算 (search_hot_content)

不同平台使用不同的热度计算公式：

```python
hotness_formulas = {
    'bilibili_video': (
        "点赞×1 + 评论×5 + (分享+收藏+投币)×10 + 弹幕×0.5 + 播放量×0.1"
    ),
    'douyin_aweme': (
        "点赞×1 + 评论×5 + (分享+收藏)×10"
    ),
    'weibo_note': (
        "点赞×1 + 评论×5 + 转发×10"
    ),
    'xhs_note': (
        "点赞×1 + 评论×5 + (分享+收藏)×10"
    ),
    'kuaishou_video': (
        "点赞×1 + 观看量×0.1"
    ),
    'zhihu_content': (
        "赞同数×1 + 评论×5"
    )
}

# 使用 UNION ALL 合并所有平台的查询
final_query = f"""
    (SELECT ... FROM bilibili_video WHERE ...)
    UNION ALL
    (SELECT ... FROM douyin_aweme WHERE ...)
    UNION ALL
    (SELECT ... FROM weibo_note WHERE ...)
    ...
    ORDER BY hotness_score DESC
    LIMIT {limit}
"""
```

#### 5. 平台定向查询 (search_topic_on_platform)

只有这个工具支持指定单个平台：

```python
def search_topic_on_platform(
    self,
    platform: Literal['bilibili', 'weibo', 'douyin', 'kuaishou', 'xhs', 'zhihu', 'tieba'],
    topic: str,
    ...
):
    # 所有平台的配置
    all_configs = {
        'bilibili': [
            {'table': 'bilibili_video', 'fields': [...], 'type': 'video'},
            {'table': 'bilibili_video_comment', 'fields': [...], 'type': 'comment'}
        ],
        'weibo': [...],
        'douyin': [...],
        # ... 其他平台
    }
    
    # 只查询用户指定的平台
    if platform not in all_configs:
        return DBResponse(error_message=f"不支持的平台: {platform}")
    
    platform_configs = all_configs[platform]  # 只获取指定平台的配置
    
    # 只循环查询该平台的表
    for config in platform_configs:
        # 执行查询...
```

### 查询流程总结

```
用户查询请求
    ↓
选择查询工具
    ↓
┌─────────────────────────────────────────┐
│ 是否为 search_topic_on_platform?       │
├─────────────────────────────────────────┤
│ 是 → 只查询指定的单个平台              │
│ 否 → 查询所有支持的平台                │
└─────────────────────────────────────────┘
    ↓
遍历平台配置字典 (search_configs)
    ↓
对每个平台:
    ├─ 构建 SQL 查询
    ├─ 执行数据库查询
    ├─ 转换为统一数据结构
    └─ 添加到结果列表
    ↓
聚合所有平台的结果
    ↓
按热度/时间排序
    ↓
返回统一的 DBResponse
```

### 代码验证结果

通过分析 `InsightEngine/tools/search.py` 的代码，确认：

1. ✅ **search_hot_content**: 查询 6 个平台（Bilibili, Douyin, Weibo, XHS, Kuaishou, Zhihu）
   - 代码位置: 第 152-159 行定义 `hotness_formulas`
   - 不包含 Tieba 和 Daily News（因为它们没有互动数据）

2. ✅ **search_topic_globally**: 查询全部 8 个平台 + 所有评论表
   - 代码位置: 第 208 行定义 `search_configs`
   - 包含 15 个表（7个平台主表 + 7个评论表 + 1个新闻表）

3. ✅ **search_topic_by_date**: 查询 7 个平台 + 新闻
   - 代码位置: 第 258-263 行定义 `search_configs`
   - 不包含评论表

4. ✅ **get_comments_for_topic**: 查询 7 个平台的评论表
   - 代码位置: 第 305-319 行构建评论表的 UNION 查询
   - 不包含 Daily News（新闻没有评论表）

5. ✅ **search_topic_on_platform**: 只查询用户指定的 1 个平台
   - 代码位置: 第 352 行定义 `all_configs`，第 354-358 行验证和选择平台
   - 支持 7 个社交平台（不包含 Daily News）

---

## 🛡️ 如何突破安全访问限制

### 核心策略：本地数据库 + 预先爬取

**与 MediaEngine 的本质区别**:
- ❌ **MediaEngine**: 实时调用外部 API，受限于 API 提供商
- ✅ **InsightEngine**: 查询本地数据库，**完全自主可控**

### 1. 数据预先爬取

**实现方式**: 使用 **MediaCrawler** 框架预先爬取数据

MediaCrawler 是一个专业的社交媒体爬虫框架，通过以下 **7 大核心技术** 突破平台的反爬虫限制：

#### 1.1 使用 Playwright 模拟真实浏览器

**核心技术**: 使用 Playwright 驱动真实的 Chromium 浏览器

```python
async with async_playwright() as playwright:
    chromium = playwright.chromium
    self.browser_context = await chromium.launch(
        headless=config.HEADLESS,  # 可选无头模式
        proxy=playwright_proxy_format,
        args=['--disable-blink-features=AutomationControlled']
    )
```

**突破原理**:
- ✅ **真实浏览器环境**: 不是简单的 HTTP 请求，而是完整的浏览器
- ✅ **完整 JavaScript 执行**: 可以执行页面的所有 JS 代码
- ✅ **真实用户行为**: 模拟鼠标、键盘、滚动等操作

#### 1.2 反爬虫检测规避 (stealth.min.js)

**核心技术**: 注入 stealth.min.js 脚本隐藏自动化特征

```python
# 注入反检测脚本
await self.browser_context.add_init_script(path="libs/stealth.min.js")
```

**突破原理**:
- ✅ **隐藏 WebDriver 标识**: 移除 `navigator.webdriver` 等自动化特征
- ✅ **伪造浏览器指纹**: 修改 `navigator.plugins`、`navigator.languages` 等
- ✅ **绕过 CDP 检测**: 隐藏 Chrome DevTools Protocol 痕迹
- ✅ **修改权限查询**: 伪造 `navigator.permissions.query` 结果

**stealth.min.js 做的事情**:
```javascript
// 隐藏 webdriver 属性
Object.defineProperty(navigator, 'webdriver', { get: () => undefined })

// 伪造 Chrome 对象
window.chrome = { runtime: {} }

// 修改插件列表
Object.defineProperty(navigator, 'plugins', { get: () => [/* 伪造的插件 */] })

// 绕过权限检测
const originalQuery = window.navigator.permissions.query
window.navigator.permissions.query = (parameters) => (
  parameters.name === 'notifications' 
    ? Promise.resolve({ state: Notification.permission })
    : originalQuery(parameters)
)
```

#### 1.3 Cookie 和登录状态管理

**核心技术**: 多种登录方式 + Cookie 持久化

```python
class XiaoHongShuLogin(AbstractLogin):
    async def begin(self):
        if config.LOGIN_TYPE == "qrcode":
            await self.login_by_qrcode()  # 二维码登录
        elif config.LOGIN_TYPE == "phone":
            await self.login_by_mobile()  # 手机号登录
        elif config.LOGIN_TYPE == "cookie":
            await self.login_by_cookies()  # Cookie 登录
```

**突破原理**:
- ✅ **真实用户登录**: 使用真实账号登录，获取合法 Cookie
- ✅ **Cookie 复用**: 保存 Cookie 到本地，下次直接使用
- ✅ **登录状态检测**: 自动检测登录是否失效
- ✅ **自动重新登录**: 登录失效时自动重新登录

**Cookie 管理流程**:
```python
# 1. 检查登录状态
if not await self.xhs_client.pong():
    # 2. 登录失效，重新登录
    login_obj = XiaoHongShuLogin(...)
    await login_obj.begin()
    # 3. 更新 Cookie
    await self.xhs_client.update_cookies(browser_context=self.browser_context)
```

#### 1.4 请求签名和加密 (X-S, X-T)

**核心技术**: 模拟平台的请求签名算法

```python
async def _pre_headers(self, url: str, data=None) -> Dict:
    """请求头参数签名"""
    # 1. 使用 Playwright 执行平台的签名 JS
    x_s = await seccore_signv2_playwright(self.playwright_page, url, data)
    
    # 2. 获取本地存储的参数
    local_storage = await self.playwright_page.evaluate("() => window.localStorage")
    
    # 3. 生成签名
    signs = sign(
        a1=self.cookie_dict.get("a1", ""),
        b1=local_storage.get("b1", ""),
        x_s=x_s,
        x_t=str(int(time.time())),
    )
    
    # 4. 添加签名到请求头
    headers = {
        "X-S": signs["x-s"],
        "X-T": signs["x-t"],
        "x-S-Common": signs["x-s-common"],
        "X-B3-Traceid": signs["x-b3-traceid"],
    }
    return headers
```

**突破原理**:
- ✅ **动态签名**: 每个请求都有唯一的签名，无法伪造
- ✅ **时间戳验证**: X-T 包含时间戳，防止重放攻击
- ✅ **参数加密**: X-S 对请求参数进行加密
- ✅ **调用平台 JS**: 直接在浏览器中执行平台的签名代码

#### 1.5 IP 代理池

**核心技术**: 动态 IP 代理轮换

```python
if config.ENABLE_IP_PROXY:
    # 创建 IP 代理池
    ip_proxy_pool = await create_ip_pool(
        config.IP_PROXY_POOL_COUNT, 
        enable_validate_ip=True
    )
    # 获取可用代理
    ip_proxy_info = await ip_proxy_pool.get_proxy()
    playwright_proxy_format, httpx_proxy_format = utils.format_proxy_info(ip_proxy_info)
```

**突破原理**:
- ✅ **IP 轮换**: 每次请求使用不同的 IP
- ✅ **代理验证**: 使用前验证代理是否可用
- ✅ **自动切换**: IP 被封时自动切换到下一个
- ✅ **分布式爬取**: 多个 IP 并发爬取

#### 1.6 请求频率控制

**核心技术**: 智能延迟和并发控制

```python
# 1. 并发控制
semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)

# 2. 页面间延迟
await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)

# 3. 随机延迟
await asyncio.sleep(random.uniform(1, 3))
```

**突破原理**:
- ✅ **限制并发**: 控制同时请求的数量
- ✅ **模拟人类**: 添加随机延迟，模拟真实用户行为
- ✅ **避免触发限流**: 合理控制请求频率
- ✅ **分批爬取**: 分页爬取，避免一次性大量请求

#### 1.7 验证码和异常处理

**核心技术**: 自动检测和人工介入

```python
# 1. 检测验证码
if response.status_code == 471 or response.status_code == 461:
    verify_type = response.headers["Verifytype"]
    verify_uuid = response.headers["Verifyuuid"]
    utils.logger.error(f"出现验证码: {verify_type}, {verify_uuid}")
    raise Exception("需要人工处理验证码")

# 2. 检测 IP 封禁
if data["code"] == self.IP_ERROR_CODE:
    raise IPBlockError("IP 被封禁")

# 3. 重试机制
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def request(self, method, url, **kwargs):
    # 自动重试 3 次
    pass
```

**突破原理**:
- ✅ **验证码检测**: 自动识别验证码出现
- ✅ **人工介入**: 暂停爬取，等待人工处理
- ✅ **异常恢复**: IP 被封时自动切换代理
- ✅ **重试机制**: 网络错误时自动重试

---

### MediaCrawler 突破反爬虫的完整流程

```
1. 启动真实浏览器 (Playwright + Chromium)
    ↓
2. 注入反检测脚本 (stealth.min.js)
    ↓
3. 使用代理 IP (可选)
    ↓
4. 真实用户登录 (二维码/手机号/Cookie)
    ↓
5. 保存 Cookie 和登录状态
    ↓
6. 访问目标页面
    ↓
7. 执行平台的签名 JS，生成请求签名
    ↓
8. 发送带签名的 API 请求
    ↓
9. 解析响应数据
    ↓
10. 检测异常 (验证码/IP封禁)
    ├─ 正常: 继续爬取
    └─ 异常: 切换代理/人工介入
    ↓
11. 控制请求频率 (延迟 + 并发限制)
    ↓
12. 保存数据到本地数据库
```

---

**优势总结**:
- ✅ **零实时访问**: InsightEngine 查询本地数据库，不直接访问平台
- ✅ **无反爬风险**: 数据已在本地，查询时无任何反爬虫限制
- ✅ **无频率限制**: 查询速度只受数据库性能限制
- ✅ **完全合规**: 查询自己的数据库，符合数据使用规范
- ✅ **成本可控**: 爬取一次，多次使用，无 API 调用费用

### 2. 异步数据库连接

**实现方式**: 使用 SQLAlchemy 2.x 异步引擎

```python
from sqlalchemy.ext.asyncio import create_async_engine

def get_async_engine() -> AsyncEngine:
    database_url = _build_database_url()
    return create_async_engine(
        database_url,
        pool_pre_ping=True,      # 连接池心跳检测
        pool_recycle=1800,       # 连接回收时间
    )

async def fetch_all(query: str, params: Optional[Dict] = None):
    engine = get_async_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text(query), params or {})
        return [dict(row) for row in result.mappings().all()]
```

**优势**:
- ✅ **高性能**: 异步IO，不阻塞主线程
- ✅ **连接复用**: 连接池管理
- ✅ **自动重连**: pool_pre_ping 检测失效连接
- ✅ **跨数据库**: 支持 MySQL 和 PostgreSQL

### 3. 智能关键词优化中间件

**核心问题**: Agent 生成的查询词往往过于专业，不符合网民真实表达

**解决方案**: 使用 LLM 优化关键词

```python
class KeywordOptimizer:
    """使用 Qwen 模型优化搜索关键词"""
    
    def optimize_keywords(self, original_query: str) -> KeywordOptimizationResponse:
        """
        将专业查询词转换为网民常用词汇
        
        示例:
        输入: "武汉大学舆情管理 未来展望 发展趋势"
        输出: ["武大", "武汉大学", "学校管理", "大学", "教育"]
        """
        system_prompt = """
        你是舆情数据挖掘专家。将查询优化为网民常用词汇：
        1. 贴近网民语言
        2. 避免专业术语
        3. 简洁具体
        4. 情感丰富
        5. 10-20个关键词
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"优化查询: {original_query}"}
            ]
        )
        
        return self._parse_keywords(response)
```

**优化效果**:
```
原始查询: "人工智能技术发展趋势与未来展望"
优化后:   ["AI", "人工智能", "ChatGPT", "机器学习", "智能助手", 
          "科技", "未来", "技术", "创新", "自动化"]

原始查询: "新能源汽车市场竞争态势分析"
优化后:   ["电动车", "新能源车", "特斯拉", "比亚迪", "充电桩",
          "续航", "电池", "汽车", "环保", "绿牌"]
```

**优势**:
- ✅ **提高召回率**: 使用网民真实用词
- ✅ **降低噪音**: 避免过于宽泛的词汇
- ✅ **优雅降级**: API 失败时使用备用方案
- ✅ **重试机制**: 自动处理网络错误

### 4. 多语言情感分析

**实现方式**: 使用 WeiboMultilingualSentiment 模型

```python
class WeiboMultilingualSentimentAnalyzer:
    """
    基于 tabularisai/multilingual-sentiment-analysis 模型
    支持 22 种语言的情感分析
    """
    
    def __init__(self):
        self.sentiment_map = {
            0: "非常负面", 1: "负面", 2: "中性", 
            3: "正面", 4: "非常正面"
        }
    
    def initialize(self) -> bool:
        """加载模型到本地"""
        local_model_path = "SentimentAnalysisModel/WeiboMultilingualSentiment/model"
        
        if os.path.exists(local_model_path):
            # 从本地加载
            self.tokenizer = AutoTokenizer.from_pretrained(local_model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
        else:
            # 首次下载并保存
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.tokenizer.save_pretrained(local_model_path)
            self.model.save_pretrained(local_model_path)
        
        # 自动选择设备: CUDA > MPS > CPU
        self.device = self._select_device()
        self.model.to(self.device)
        self.model.eval()
        
        return True
```

**支持语言** (22种):
中文、英文、西班牙文、阿拉伯文、日文、韩文、德文、法文、意大利文、葡萄牙文、俄文、荷兰文、波兰文、土耳其文、丹麦文、希腊文、芬兰文、瑞典文、挪威文、匈牙利文、捷克文、保加利亚文

**优势**:
- ✅ **本地推理**: 模型在本地运行，无需外部 API
- ✅ **自动设备选择**: GPU > MPS > CPU
- ✅ **批量处理**: 高效处理大量文本
- ✅ **可选功能**: 可通过配置开关禁用

### 5. 统一数据结构

**数据结构设计**:

```python
@dataclass
class QueryResult:
    """统一的查询结果数据类"""
    platform: str                    # 平台名称
    content_type: str                # 内容类型 (video/note/comment)
    title_or_content: str            # 标题或内容
    author_nickname: Optional[str]   # 作者昵称
    url: Optional[str]               # 内容链接
    publish_time: Optional[datetime] # 发布时间
    engagement: Dict[str, int]       # 互动数据
    source_keyword: Optional[str]    # 来源关键词
    hotness_score: float             # 热度分数
    source_table: str                # 来源表名

@dataclass
class DBResponse:
    """封装工具的完整返回结果"""
    tool_name: str                   # 工具名称
    parameters: Dict[str, Any]       # 查询参数
    results: List[QueryResult]       # 查询结果列表
    results_count: int               # 结果数量
    error_message: Optional[str]     # 错误信息
```

**优势**:
- ✅ **跨平台统一**: 不同平台数据结构一致
- ✅ **类型安全**: 使用 dataclass 确保类型正确
- ✅ **易于处理**: 统一接口便于后续分析

### 6. 智能互动数据提取

**问题**: 不同平台的互动指标字段名不一致

**解决方案**: 智能字段映射

```python
def _extract_engagement(self, row: Dict[str, Any]) -> Dict[str, int]:
    """从数据行中提取并统一互动指标"""
    engagement = {}
    
    # 字段映射表
    mapping = {
        'likes': ['liked_count', 'like_count', 'voteup_count', 'comment_like_count'],
        'comments': ['video_comment', 'comments_count', 'comment_count'],
        'shares': ['video_share_count', 'shared_count', 'share_count'],
        'views': ['video_play_count', 'viewd_count'],
        'favorites': ['video_favorite_count', 'collected_count'],
        'coins': ['video_coin_count'],
        'danmaku': ['video_danmaku'],
    }
    
    # 自动匹配字段
    for key, potential_cols in mapping.items():
        for col in potential_cols:
            if col in row and row[col] is not None:
                engagement[key] = int(row[col])
                break
    
    return engagement
```

**优势**:
- ✅ **自动适配**: 无需手动处理每个平台
- ✅ **容错性强**: 缺失字段不影响其他数据
- ✅ **可扩展**: 易于添加新平台

### 7. 时间格式统一处理

**问题**: 不同平台使用不同的时间格式

**解决方案**: 智能时间转换

```python
@staticmethod
def _to_datetime(ts: Any) -> Optional[datetime]:
    """统一时间格式转换"""
    if not ts:
        return None
    
    try:
        # 已经是 datetime 对象
        if isinstance(ts, datetime):
            return ts
        
        # 时间戳 (秒或毫秒)
        if isinstance(ts, (int, float)) or str(ts).isdigit():
            val = float(ts)
            # 判断是毫秒还是秒
            if val > 1_000_000_000_000:  # 毫秒级
                return datetime.fromtimestamp(val / 1000)
            else:  # 秒级
                return datetime.fromtimestamp(val)
        
        # ISO 格式字符串
        if isinstance(ts, str):
            return datetime.fromisoformat(ts.split('+')[0].strip())
    
    except (ValueError, TypeError):
        return None
```

**支持格式**:
- ✅ 秒级时间戳 (Bilibili, Zhihu)
- ✅ 毫秒级时间戳 (Douyin, Kuaishou, XHS)
- ✅ ISO 字符串 (Weibo, Tieba)
- ✅ datetime 对象
- ✅ date 对象

---

## 💡 技术创新点

### 1. 零成本舆情分析
- ❌ 不依赖外部 API
- ✅ 查询本地数据库
- ✅ 无调用费用
- ✅ 无频率限制

### 2. 智能关键词优化
- ✅ LLM 自动优化查询词
- ✅ 提高召回率
- ✅ 贴近网民语言
- ✅ 优雅降级

### 3. 多语言情感分析
- ✅ 支持 22 种语言
- ✅ 本地模型推理
- ✅ GPU 加速
- ✅ 批量处理

### 4. 跨平台统一查询
- ✅ 一次查询覆盖 7 大平台
- ✅ 统一数据结构
- ✅ 智能字段映射
- ✅ 时间格式自动转换

### 5. 智能热度算法
- ✅ 多维度加权计算
- ✅ 跨平台可比
- ✅ 无需人工指定排序字段

### 6. 反思迭代优化
- ✅ 自动识别信息缺口
- ✅ 迭代补充查询
- ✅ 最多 3 轮优化

---

## 🔐 安全性与合规性总结

### 数据访问
1. ✅ **本地数据库**: 查询自己的数据，无外部访问
2. ✅ **异步连接**: 连接池管理，自动重连
3. ✅ **参数化查询**: 防止 SQL 注入
4. ✅ **权限控制**: 数据库用户权限管理

### 数据来源
1. ✅ **预先爬取**: 使用 MediaCrawler 框架
2. ✅ **合规存储**: 存储在自己的数据库
3. ✅ **定期更新**: 定时任务更新数据
4. ✅ **数据清洗**: 去除敏感信息

### 隐私保护
1. ✅ **本地处理**: 情感分析在本地进行
2. ✅ **无数据上传**: 不向外部服务发送数据
3. ✅ **匿名化**: 可选的数据脱敏处理

### 稳定性保障
1. ✅ **连接池**: 复用数据库连接
2. ✅ **重试机制**: 关键词优化 API 失败重试
3. ✅ **优雅降级**: 各模块失败不影响主流程
4. ✅ **错误处理**: 完善的异常捕获

---

## 📚 技术栈

### 核心依赖
- **SQLAlchemy 2.x**: 异步 ORM 框架
- **aiomysql / asyncpg**: 异步数据库驱动
- **transformers**: Hugging Face 模型库
- **torch**: PyTorch 深度学习框架
- **OpenAI SDK**: LLM 调用（兼容多种模型）
- **loguru**: 日志记录

### 数据库支持
- **MySQL**: 使用 aiomysql 驱动
- **PostgreSQL**: 使用 asyncpg 驱动

### AI 模型
- **关键词优化**: Qwen 系列模型
- **情感分析**: tabularisai/multilingual-sentiment-analysis

### 设计模式
- **装饰器模式**: 重试机制
- **工厂模式**: Agent 创建
- **状态模式**: 研究状态管理
- **策略模式**: 多种查询工具

---

## 🎯 使用示例

### 基本使用
```python
from InsightEngine import DeepSearchAgent

# 创建 Agent
agent = DeepSearchAgent()

# 执行深度研究
report = agent.research("分析最近一周电动汽车的舆情")
```

### 直接使用查询工具
```python
from InsightEngine.tools import MediaCrawlerDB

db = MediaCrawlerDB()

# 查找热点
response = db.search_hot_content(time_period='week', limit=50)

# 全局搜索
response = db.search_topic_globally(topic="人工智能", limit_per_table=100)

# 平台定向搜索
response = db.search_topic_on_platform(
    platform='bilibili',
    topic="游戏",
    start_date='2024-01-01',
    end_date='2024-01-31'
)
```

### 情感分析
```python
from InsightEngine.tools import multilingual_sentiment_analyzer

# 初始化模型
analyzer = multilingual_sentiment_analyzer
analyzer.initialize()

# 分析单个文本
result = analyzer.analyze_single_text("今天天气真好！")
print(f"情感: {result.sentiment_label}, 置信度: {result.confidence}")

# 批量分析
texts = ["很棒的产品", "服务太差了", "一般般"]
batch_result = analyzer.analyze_batch(texts)
```

### 关键词优化
```python
from InsightEngine.tools import keyword_optimizer

# 优化查询词
result = keyword_optimizer.optimize_keywords(
    original_query="人工智能技术发展趋势分析",
    context="分析AI行业的最新动态"
)

print(f"原始查询: {result.original_query}")
print(f"优化后: {result.optimized_keywords}")
print(f"理由: {result.reasoning}")
```

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
    │   ├─ 关键词优化中间件处理
    │   ├─ 选择数据库查询工具
    │   └─ 执行本地数据库查询
    │
    ├─ 2.2 自动情感分析 (可选)
    │   ├─ 提取查询结果文本
    │   ├─ 批量情感分析
    │   └─ 生成情感分布统计
    │
    ├─ 2.3 首次总结
    │   └─ 基于查询结果生成初始内容
    │
    └─ 2.4 反思循环 (最多3次)
        ├─ 反思分析
        ├─ 补充查询
        ├─ 情感分析
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
    "search_query": "最近一周的热点话题",
    "search_tool": "search_hot_content",
    "reasoning": "需要发现热点，选择热点内容查询工具",
    "time_period": "week",
    "enable_sentiment": true
}
```

#### 2. 关键词优化流程
```python
# 原始查询
original_query = "人工智能技术发展趋势分析"

# 关键词优化
optimized = keyword_optimizer.optimize_keywords(original_query)
# 结果: ["AI", "人工智能", "ChatGPT", "技术", "发展"]

# 使用优化后的关键词查询
for keyword in optimized.optimized_keywords:
    results = db.search_topic_globally(topic=keyword)
```

#### 3. 自动情感分析
```python
# 执行查询
response = db.search_topic_globally(topic="电动汽车", limit_per_table=100)

# 自动情感分析 (默认启用)
if response.parameters.get("sentiment_analysis"):
    sentiment_data = response.parameters["sentiment_analysis"]
    print(f"情感分布: {sentiment_data['sentiment_distribution']}")
    print(f"平均置信度: {sentiment_data['average_confidence']}")
```

---

## 📖 参考资料

### 项目文件
- `InsightEngine/agent.py`: 主 Agent 实现
- `InsightEngine/tools/search.py`: 数据库查询工具集
- `InsightEngine/tools/keyword_optimizer.py`: 关键词优化中间件
- `InsightEngine/tools/sentiment_analyzer.py`: 情感分析工具
- `InsightEngine/utils/db.py`: 数据库连接工具

### 相关文档
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/)
- [Transformers 文档](https://huggingface.co/docs/transformers/)
- [通义千问 API](https://help.aliyun.com/zh/model-studio/)

### 对比文档
- `MediaEngine多模态搜索技术总结.md`: 外部 API 搜索方案
- `Windows编码问题修复总结.md`: Windows 环境配置

---

**文档维护**: BettaFish 项目组  
**最后更新**: 2025-11-12  
**版本**: v1.0
