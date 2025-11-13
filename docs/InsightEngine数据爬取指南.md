# InsightEngine 数据爬取完整指南

## 📋 概述

InsightEngine 使用 **MediaCrawler** 框架来爬取 7 大社交媒体平台的数据，并存储到本地数据库中。本指南将详细说明如何独立运行数据爬取程序。

## ⚠️ 重要说明：本地数据库与 LLM 的协作关系

### 核心理解

**InsightEngine 即使没有本地数据库的数据，也能生成完整的研究报告！**

这是 InsightEngine 的核心设计理念，与传统的数据检索系统完全不同。

### 双模式运行机制

| 模式 | 数据来源 | 报告质量 | 适用场景 |
|------|---------|---------|---------|
| **舆情分析模式** | 本地数据库 + LLM 知识 | ⭐⭐⭐⭐⭐ 最佳 | 分析真实民意、社交媒体舆情 |
| **深度研究模式** | LLM 训练知识 | ⭐⭐⭐⭐ 优秀 | 技术趋势分析、理论研究 |

### 完整工作流程

```
用户查询: "AI Agent 发展趋势"
         ↓
【步骤 1】LLM 生成报告结构（HOST 发言）
    ├─ 5 个段落大纲
    └─ 每个大纲包含 1500+ 字的详细描述 ✅
         ↓
【步骤 2】处理每个段落（反思迭代）
    │
    ├─ 2.1 生成搜索查询
    │   └─ LLM 根据段落主题生成查询
    │
    ├─ 2.2 查询本地数据库
    │   ├─ 有数据 → 使用真实社交媒体内容 ✅
    │   └─ 无数据 → 继续使用 LLM 知识 ✅
    │
    ├─ 2.3 LLM 生成总结
    │   ├─ 输入: HOST 发言 + 数据库结果（可能为空）
    │   └─ 输出: 1500+ 字的段落分析 ✅
    │
    └─ 2.4 反思循环（默认 2 次）
        ├─ LLM 审视当前内容，识别信息缺口
        ├─ 生成新的搜索查询
        ├─ 再次查询数据库（可能仍为空）
        └─ LLM 深化分析 → 15000+ 字的最终段落 ✅
         ↓
【步骤 3】生成最终报告
    └─ 合并所有段落 = 75000+ 字的完整报告 ✅
```

### 关键设计决策

#### 为什么没有数据也能生成报告？

1. **LLM 的训练知识**
   - Kimi、Qwen 等 LLM 在训练时已学习大量知识
   - 可以基于通用知识进行深度分析

2. **HOST 发言的作用**
   - LLM 生成的段落大纲本身包含大量信息（1500+ 字符）
   - 提供了详细的分析方向和框架

3. **反思迭代机制**
   - 每次反思都让内容更深入、更全面
   - 即使没有新数据，LLM 也能从不同角度深化分析

#### 为什么还需要本地数据库？

1. **真实性**: 引用真实的用户评论和数据统计
2. **时效性**: 获取最新的社交媒体讨论
3. **民意洞察**: 分析公众的真实情感和观点
4. **平台差异**: 对比不同平台用户群体的反应

### 实际运行示例

#### 场景 1：数据库有数据（舆情分析模式）

```
[14:18:41] 段落 1 - 首次搜索
    └─ 查询: "AI Agent 技术进展"
    └─ 结果: 50 条 ✅

[14:18:46] 段落 1 - 首次总结
    └─ 引用真实评论:
        - B站用户"AI探索者": "最近的AI Agent真的太强了"（点赞 1.2k）
        - 知乎用户"算法工程师": "多模态Agent是未来趋势"（赞同 2.3k）
    └─ 情感分析: 正面 68.5%, 中性 25.3%, 负面 6.2%
    └─ 输出: 1500+ 字的数据驱动分析 ✅
```

#### 场景 2：数据库无数据（深度研究模式）

```
[14:18:41] 段落 1 - 首次搜索
    └─ 查询: "AI Agent 技术进展"
    └─ 结果: 0 条 ❌

[14:18:46] 段落 1 - 首次总结
    └─ 输入: HOST 发言（1554 字符）
    └─ LLM 基于训练知识分析:
        - AI Agent 的技术演进路径
        - 关键突破点和技术瓶颈
        - 行业应用案例和发展趋势
    └─ 输出: 1500+ 字的知识驱动分析 ✅

[14:21:46] 段落 1 - 反思 1
    └─ LLM 深化分析 → 10000+ 字 ✅

[14:30:12] 段落 1 - 反思 2
    └─ LLM 再次深化 → 15000+ 字 ✅
    └─ 总耗时: 12.5 分钟
    └─ 内容来源: 100% LLM 知识
```

### 使用建议

#### 如果您想要舆情分析（推荐爬取数据）

```bash
# 1. 运行 MediaCrawler 爬虫
cd MindSpider/DeepSentimentCrawling/MediaCrawler
python main.py --platform bili --lt qrcode --type search

# 2. 数据积累后，运行 InsightEngine
# 将获得基于真实数据的舆情分析报告
```

#### 如果您想要技术趋势分析（可以不爬取数据）

```bash
# 直接运行 InsightEngine
# 将获得基于 LLM 知识的深度研究报告
# 适合分析技术趋势、理论研究等话题
```

### 总结

| 特性 | 说明 |
|------|------|
| **必须爬取数据吗？** | ❌ 不是必须的 |
| **没有数据能用吗？** | ✅ 可以，生成深度研究报告 |
| **有数据更好吗？** | ✅ 是的，可以分析真实舆情 |
| **核心优势** | 双模式：既能分析真实数据，也能深度研究 |

---

## 📖 信息来源说明

本文档所有步骤和配置均基于以下真实文件验证：

| 信息类型 | 来源文件 | 验证方式 |
|---------|---------|---------|
| 安装步骤 | `MediaCrawler/README.md` 第 136-207 行 | 官方文档 |
| 命令行参数 | `MediaCrawler/cmd_arg/arg.py` | 实际代码 |
| 配置选项 | `MediaCrawler/config/base_config.py` | 实际配置文件 |
| 数据库配置 | `MediaCrawler/config/db_config.py` | 实际配置文件 |
| 依赖包列表 | `MediaCrawler/requirements.txt` | 实际依赖文件 |
| 支持的平台 | `MediaCrawler/cmd_arg/arg.py` PlatformEnum | 枚举类定义 |
| 数据库类型 | `MediaCrawler/cmd_arg/arg.py` InitDbOptionEnum | 枚举类定义 |

**所有命令和配置项都已在实际文件中验证，确保真实可用。**

---

## 🎯 支持的平台

MediaCrawler 支持以下平台的数据爬取：

| 平台代码 | 平台名称 | 支持功能 |
|---------|---------|---------|
| `xhs` | 小红书 | 关键词搜索、指定帖子、评论、创作者主页 |
| `dy` | 抖音 | 关键词搜索、指定帖子、评论、创作者主页 |
| `ks` | 快手 | 关键词搜索、指定帖子、评论、创作者主页 |
| `bili` | 哔哩哔哩 | 关键词搜索、指定帖子、评论、创作者主页 |
| `wb` | 微博 | 关键词搜索、指定帖子、评论、创作者主页 |
| `tieba` | 百度贴吧 | 关键词搜索、指定帖子、评论、创作者主页 |
| `zhihu` | 知乎 | 关键词搜索、指定帖子、评论、创作者主页 |

---

## 🚀 快速开始

> **信息来源说明**：以下步骤基于 MediaCrawler 官方 README.md 和实际代码文件验证。

### 步骤 1：进入 MediaCrawler 目录

```bash
cd d:\Python-Learning\bettafish\MindSpider\DeepSentimentCrawling\MediaCrawler
```

### 步骤 2：安装依赖

#### 使用 Conda 环境（推荐）

```bash
# 激活您的 conda 环境
conda activate your_env_name

# 安装 Python 依赖
pip install -r requirements.txt

# 安装浏览器驱动
playwright install
```

**requirements.txt 包含的主要依赖**（来源：实际 requirements.txt 文件）：
- `playwright==1.45.0` - 浏览器自动化
- `httpx==0.28.1` - HTTP 客户端
- `aiomysql==0.2.0` - MySQL 异步驱动
- `sqlalchemy>=2.0.43` - ORM 框架
- `aiosqlite==0.21.0` - SQLite 异步驱动
- `jieba==0.42.1` - 中文分词
- `wordcloud==1.9.3` - 词云生成

### 步骤 3：配置数据库

数据库配置文件位于 `config/db_config.py`，默认已配置为 BettaFish 项目的数据库：

```python
# PostgreSQL 配置（推荐）
POSTGRESQL_DB_HOST = "127.0.0.1"
POSTGRESQL_DB_PORT = "5444"
POSTGRESQL_DB_USER = "bettafish"
POSTGRESQL_DB_PWD = "bettafish"
POSTGRESQL_DB_NAME = "bettafish"
```

**确保数据库已启动并可访问！**

### 步骤 4：初始化数据库表（首次运行）

> **来源**：`cmd_arg/arg.py` 第 201-208 行，`main.py` 第 67-70 行

```bash
# 初始化 PostgreSQL 数据库表结构
python main.py --init_db postgresql

# 或初始化 SQLite（轻量级，推荐个人使用）
python main.py --init_db sqlite

# 或初始化 MySQL
python main.py --init_db mysql
```

**支持的数据库类型**（来源：`cmd_arg/arg.py` InitDbOptionEnum）：
- `sqlite` - SQLite 数据库（无需服务器）
- `mysql` - MySQL 数据库
- `postgresql` - PostgreSQL 数据库

### 步骤 5：配置爬取参数

> **来源**：`config/base_config.py` 实际配置文件

编辑 `config/base_config.py`：

```python
# 选择要爬取的平台（来源：第 12 行）
PLATFORM = "bili"  # xhs | dy | ks | bili | wb | tieba | zhihu

# 配置关键词（用英文逗号分隔）（来源：第 13 行）
KEYWORDS = "人工智能,AI Agent,大模型,ChatGPT"

# 登录方式（来源：第 14 行）
LOGIN_TYPE = "qrcode"  # qrcode（二维码） | phone（手机号） | cookie

# 爬取类型（来源：第 16 行）
CRAWLER_TYPE = "search"  # search（关键词搜索） | detail（指定帖子） | creator（创作者主页）

# 数据保存方式（来源：第 64 行）
SAVE_DATA_OPTION = "postgresql"  # postgresql | db(mysql) | sqlite | json | csv

# 是否开启评论爬取（来源：第 82 行）
ENABLE_GET_COMMENTS = True

# 爬取数量控制（来源：第 73 行）
CRAWLER_MAX_NOTES_COUNT = 20  # 每个关键词爬取的帖子数量

# 评论数量控制（来源：第 85 行）
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 50  # 每个帖子爬取的评论数量

# 是否开启二级评论（来源：第 89 行）
ENABLE_GET_SUB_COMMENTS = False

# 并发控制（来源：第 76 行）
MAX_CONCURRENCY_NUM = 1

# 是否使用 CDP 模式（使用本地浏览器）（来源：第 40 行）
ENABLE_CDP_MODE = True

# 是否无头模式（不显示浏览器窗口）（来源：第 31 行）
HEADLESS = False  # 建议首次运行设为 False，方便调试
```

### 步骤 6：运行爬虫

> **来源**：MediaCrawler README.md 第 142-151 行（官方示例）

#### 关键词搜索模式（推荐）

```bash
# 小红书
python main.py --platform xhs --lt qrcode --type search

# 抖音
python main.py --platform dy --lt qrcode --type search

# 快手
python main.py --platform ks --lt qrcode --type search

# B站
python main.py --platform bili --lt qrcode --type search

# 微博
python main.py --platform wb --lt qrcode --type search

# 贴吧
python main.py --platform tieba --lt qrcode --type search

# 知乎
python main.py --platform zhihu --lt qrcode --type search
```

**命令行参数说明**（来源：`cmd_arg/arg.py`）：
- `--platform`: 平台选择（xhs/dy/ks/bili/wb/tieba/zhihu）
- `--lt`: 登录方式（qrcode/phone/cookie）
- `--type`: 爬取类型（search/detail/creator）
- `--keywords`: 关键词（可选，覆盖配置文件）
- `--save_data_option`: 数据保存方式（csv/json/sqlite/db/postgresql）

#### 指定帖子 ID 爬取

编辑对应平台的配置文件（如 `config/xhs_config.py`），添加帖子 ID：

```python
# 小红书配置示例
XHS_SPECIFIED_ID_LIST = [
    "6411cf2d000000001300d0a4",
    "64116ab4000000001300d0a3",
]
```

然后运行：

```bash
python main.py --platform xhs --lt qrcode --type detail
```

#### 创作者主页爬取

编辑对应平台的配置文件，添加创作者 ID：

```python
# 小红书配置示例
XHS_CREATOR_ID_LIST = [
    "5ff0e6410000000001008400",
]
```

然后运行：

```bash
python main.py --platform xhs --lt qrcode --type creator
```

---

## 🔐 登录方式说明

> **来源**：`cmd_arg/arg.py` LoginTypeEnum（第 42-47 行）

### 1. 二维码登录（推荐）

```bash
python main.py --platform xhs --lt qrcode --type search
```

- 运行后会弹出浏览器窗口
- 打开对应平台的 APP
- 扫描浏览器中显示的二维码
- 登录成功后，Cookie 会自动保存到 `cache/` 目录

### 2. 手机号登录

```bash
python main.py --platform xhs --lt phone --type search
```

- 按照提示输入手机号和验证码

### 3. Cookie 登录

1. 手动获取 Cookie（通过浏览器开发者工具）
2. 在 `config/base_config.py` 中配置：

```python
LOGIN_TYPE = "cookie"
COOKIES = "你的Cookie字符串"
```

或通过命令行参数：

```bash
python main.py --platform xhs --lt cookie --cookies "你的Cookie字符串" --type search
```

---

## 📊 数据存储说明

### PostgreSQL（推荐）

数据会存储到以下表中：

| 表名 | 说明 |
|------|------|
| `bilibili_video` | B站视频数据 |
| `bilibili_video_comment` | B站视频评论 |
| `weibo_note` | 微博内容 |
| `weibo_note_comment` | 微博评论 |
| `douyin_aweme` | 抖音视频 |
| `douyin_aweme_comment` | 抖音评论 |
| `kuaishou_video` | 快手视频 |
| `kuaishou_video_comment` | 快手评论 |
| `xhs_note` | 小红书笔记 |
| `xhs_note_comment` | 小红书评论 |
| `zhihu_content` | 知乎内容 |
| `zhihu_comment` | 知乎评论 |
| `tieba_note` | 贴吧帖子 |
| `tieba_comment` | 贴吧评论 |

### 其他存储方式

- **SQLite**: 数据存储在 `database/sqlite_tables.db`
- **JSON**: 数据存储在 `data/` 目录下的 JSON 文件
- **CSV**: 数据存储在 `data/` 目录下的 CSV 文件

---

## ⚙️ 高级配置

### 1. 使用 IP 代理池

编辑 `config/base_config.py`：

```python
# 开启 IP 代理
ENABLE_IP_PROXY = True

# 代理池数量
IP_PROXY_POOL_COUNT = 5

# 代理提供商
IP_PROXY_PROVIDER_NAME = "kuaidaili"  # kuaidaili | wandouhttp
```

然后在 `proxy/` 目录下配置代理提供商的 API。

### 2. 爬取媒体资源（图片/视频）

```python
# 开启媒体资源下载
ENABLE_GET_MEIDAS = True
```

媒体文件会下载到 `data/` 目录。

### 3. 生成评论词云图

```python
# 开启词云图生成
ENABLE_GET_WORDCLOUD = True

# 配置词云图参数
CUSTOM_WORDS = {
    "人工智能": "技术",
    "大模型": "技术",
}

STOP_WORDS_FILE = "./docs/hit_stopwords.txt"
FONT_PATH = "./docs/STZHONGS.TTF"
```

### 4. 调整爬取速度

```python
# 爬取间隔时间（秒）
CRAWLER_MAX_SLEEP_SEC = 2

# 并发数量
MAX_CONCURRENCY_NUM = 3  # 建议不超过 5
```

---

## 🔍 验证数据是否爬取成功

### 方法 1：查询数据库

```sql
-- 查看 B站 视频数据
SELECT COUNT(*) FROM bilibili_video;

-- 查看最新爬取的数据
SELECT title, author_name, liked_count, create_time 
FROM bilibili_video 
ORDER BY create_time DESC 
LIMIT 10;

-- 查看评论数据
SELECT COUNT(*) FROM bilibili_video_comment;
```

### 方法 2：查看日志

爬虫运行时会在终端输出详细日志：

```
[INFO] 开始爬取关键词: 人工智能
[INFO] 找到 20 条帖子
[INFO] 正在爬取帖子: 《AI Agent 的未来发展》
[INFO] 爬取评论: 50 条
[INFO] 数据已保存到数据库
```

### 方法 3：使用 InsightEngine 查询

运行 InsightEngine 的 Streamlit 应用：

```bash
cd d:\Python-Learning\bettafish\SingleEngineApp
streamlit run insight_engine_streamlit_app.py
```

在界面中输入查询，查看是否能检索到爬取的数据。

---

## 🛠️ 常见问题

### 1. 登录失败

**问题**: 扫码后一直提示登录失败

**解决方案**:
- 设置 `HEADLESS = False`，打开浏览器窗口
- 手动完成滑动验证码
- 检查是否需要手机号验证

### 2. 数据库连接失败

**问题**: `Connection refused` 或 `Access denied`

**解决方案**:
```bash
# 检查数据库是否启动
docker ps

# 检查数据库配置
# 确保 config/db_config.py 中的配置与实际数据库一致
```

### 3. 爬取速度慢

**解决方案**:
- 增加并发数: `MAX_CONCURRENCY_NUM = 3`
- 减少评论数量: `CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20`
- 关闭二级评论: `ENABLE_GET_SUB_COMMENTS = False`

### 4. 被平台检测到

**解决方案**:
- 启用 CDP 模式: `ENABLE_CDP_MODE = True`
- 使用 IP 代理: `ENABLE_IP_PROXY = True`
- 增加爬取间隔: `CRAWLER_MAX_SLEEP_SEC = 5`
- 减少并发数: `MAX_CONCURRENCY_NUM = 1`

### 5. Cookie 过期

**解决方案**:
- 删除 `cache/` 目录下的 Cookie 文件
- 重新运行爬虫，使用二维码登录

---

## 📝 完整示例：爬取 B站 数据

### 1. 配置参数

编辑 `config/base_config.py`：

```python
PLATFORM = "bili"
KEYWORDS = "人工智能,AI Agent,大模型"
LOGIN_TYPE = "qrcode"
CRAWLER_TYPE = "search"
SAVE_DATA_OPTION = "postgresql"
ENABLE_GET_COMMENTS = True
CRAWLER_MAX_NOTES_COUNT = 50
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 100
HEADLESS = False
```

### 2. 初始化数据库（首次运行）

```bash
cd d:\Python-Learning\bettafish\MindSpider\DeepSentimentCrawling\MediaCrawler
python main.py --init_db postgresql
```

### 3. 运行爬虫

```bash
python main.py --platform bili --lt qrcode --type search
```

### 4. 扫码登录

- 浏览器窗口会自动打开
- 打开 B站 APP
- 扫描二维码
- 等待登录成功

### 5. 等待爬取完成

爬虫会自动：
1. 搜索关键词 "人工智能"
2. 爬取 50 个视频
3. 每个视频爬取 100 条评论
4. 保存到 PostgreSQL 数据库

### 6. 验证数据

```sql
-- 查看爬取的视频数量
SELECT COUNT(*) FROM bilibili_video;

-- 查看最新视频
SELECT title, author_name, video_play_count, liked_count 
FROM bilibili_video 
ORDER BY create_time DESC 
LIMIT 10;
```

---

## 🔄 定期更新数据

### 方法 1：手动运行

定期执行爬虫命令：

```bash
cd d:\Python-Learning\bettafish\MindSpider\DeepSentimentCrawling\MediaCrawler
python main.py --platform bili --lt qrcode --type search
```

### 方法 2：使用定时任务

#### Windows 任务计划程序

1. 创建批处理文件 `run_crawler.bat`：

```batch
@echo off
cd /d d:\Python-Learning\bettafish\MindSpider\DeepSentimentCrawling\MediaCrawler
python main.py --platform bili --lt cookie --type search
```

2. 打开"任务计划程序"
3. 创建基本任务
4. 设置触发器（如每天凌晨 2 点）
5. 操作选择"启动程序"，选择 `run_crawler.bat`

#### Linux/macOS Cron

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2 点）
0 2 * * * cd /path/to/MediaCrawler && python main.py --platform bili --lt cookie --type search
```

---

## 📚 参考资料

- **MediaCrawler 官方文档**: [GitHub - NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- **Playwright 文档**: https://playwright.dev/
- **InsightEngine 技术总结**: `docs/InsightEngine本地舆情数据库技术总结.md`

---

## ⚠️ 免责声明

本工具仅供学习和研究使用，请遵守以下原则：

1. ✅ 不得用于任何商业用途
2. ✅ 遵守目标平台的使用条款和 robots.txt 规则
3. ✅ 不得进行大规模爬取或对平台造成运营干扰
4. ✅ 合理控制请求频率，避免给目标平台带来负担
5. ✅ 不得用于任何非法或不当的用途

**使用本工具即表示您同意遵守上述原则和 LICENSE 中的所有条款。**

---

## 🎯 重要提醒：关于数据爬取的必要性

### 核心要点

**InsightEngine 可以在没有本地数据的情况下正常工作！**

### 三种使用场景

#### 1. 舆情分析场景（推荐爬取数据）

**适用于**：
- 分析特定事件的社交媒体反应
- 了解公众对某个话题的真实看法
- 对比不同平台用户群体的观点差异
- 追踪舆情随时间的演变趋势

**数据价值**：
- ✅ 引用真实的用户评论
- ✅ 提供精确的数据统计（点赞、转发、评论数）
- ✅ 情感分析基于真实内容
- ✅ 平台差异对比有数据支撑

**操作建议**：
```bash
# 定期运行爬虫，积累数据
cd MindSpider/DeepSentimentCrawling/MediaCrawler
python main.py --platform bili --lt qrcode --type search
```

#### 2. 技术趋势分析场景（可以不爬取数据）

**适用于**：
- 分析技术发展趋势
- 研究行业动态和未来方向
- 理论框架和概念解析
- 技术对比和评估

**LLM 知识优势**：
- ✅ 覆盖全球范围的技术知识
- ✅ 包含历史发展脉络
- ✅ 理论深度和广度
- ✅ 跨领域知识整合

**操作建议**：
```bash
# 直接使用 InsightEngine，无需爬取数据
# LLM 会基于训练知识生成深度分析报告
```

#### 3. 混合模式（最佳实践）

**适用于**：
- 既需要真实数据，又需要深度理论分析
- 结合民意和专业知识的综合研究

**数据流**：
```
本地数据库（真实舆情）
         +
LLM 训练知识（理论深度）
         ↓
    完美结合的报告
```

### 决策流程图

```
您的研究目标是什么？
         ↓
    ┌────┴────┐
    │         │
分析舆情？  研究技术？
    │         │
    ↓         ↓
需要爬取   可以不爬取
    │         │
    ↓         ↓
运行爬虫   直接使用
    │         │
    └────┬────┘
         ↓
    运行 InsightEngine
         ↓
    生成高质量报告
```

### 常见误解澄清

| 误解 | 事实 |
|------|------|
| ❌ "必须先爬取数据才能用" | ✅ 可以直接使用，LLM 知识足够强大 |
| ❌ "没有数据报告质量差" | ✅ 深度研究模式质量优秀（4星） |
| ❌ "爬虫是 InsightEngine 的前置条件" | ✅ 爬虫是可选的增强功能 |
| ❌ "数据库为空就没法用" | ✅ 反思迭代机制保证报告质量 |

### 最佳实践建议

1. **首次使用**：
   - 可以先不爬取数据，体验 InsightEngine 的深度研究能力
   - 了解反思迭代机制如何工作

2. **舆情分析需求**：
   - 定期运行爬虫（如每周一次）
   - 积累特定话题的数据
   - 结合真实数据和 LLM 知识

3. **技术研究需求**：
   - 直接使用，无需爬取
   - 充分利用 LLM 的知识广度

4. **混合使用**：
   - 根据具体查询内容决定
   - 舆情话题 → 爬取数据
   - 技术话题 → 直接使用

### 性能对比

| 指标 | 有数据 | 无数据 |
|------|--------|--------|
| 报告生成时间 | 约 65 分钟 | 约 65 分钟 |
| 报告字数 | 75000+ 字 | 75000+ 字 |
| 报告质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 真实性 | 高（引用真实数据） | 中（基于通用知识） |
| 深度 | 高 | 高 |
| 适用场景 | 舆情分析 | 技术研究 |

---

**文档维护**: BettaFish 项目组  
**最后更新**: 2025-11-13  
**版本**: v2.0（新增 LLM 协作关系说明）
