# MindSpider 完整使用指南

> **最后更新**: 2025-11-17  
> **版本**: v2.0  
> **维护**: BettaFish 项目组

---

## 📑 目录

1. [快速开始](#快速开始)
2. [话题管理](#话题管理)
3. [数据管理](#数据管理)
4. [常见问题排查](#常见问题排查)
5. [平台特定问题](#平台特定问题)
6. [最佳实践](#最佳实践)

---

## 快速开始

### 基本使用流程

```bash
# 1. 添加自定义话题
python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,雷军,电动车"

# 2. 运行爬虫（测试模式）
python main.py --deep-sentiment --platforms bili --test

# 3. 查看数据
python check_crawled_data.py --platform bili

# 4. 查看日志
Get-Content logs\bilibili.log -Encoding UTF8 -Tail 50
```

### 三种话题管理方式

| 方式 | 命令 | 适用场景 | 推荐度 |
|------|------|---------|--------|
| **AI自动提取** | `python main.py --broad-topic` | 日常热点监测 | ⭐⭐⭐⭐ |
| **脚本工具** | `python add_custom_topic.py "话题" "关键词"` | 快速添加特定话题 | ⭐⭐⭐⭐⭐ |
| **SQL插入** | 直接操作数据库 | 批量导入 | ⭐⭐⭐ |

---

## 话题管理

### 添加话题

#### 使用脚本工具（推荐）

```bash
# 基本用法
python add_custom_topic.py "话题名称" "关键词1,关键词2,关键词3"

# 带描述
python add_custom_topic.py "话题名称" "关键词1,关键词2" "话题描述"

# 实际示例
python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,雷军,电动车,新能源"
python add_custom_topic.py "AI技术趋势" "人工智能,ChatGPT,Claude,大模型"
python add_custom_topic.py "A股投资" "A股,股票,投资,牛市,基金"
```

**输出示例**：
```
✅ 成功添加自定义话题：小米汽车分析
   话题ID: custom_20251117_140530
   关键词: 小米汽车, 小米SU7, 雷军, 电动车, 新能源
   日期: 2025-11-17

📌 下一步：运行爬虫
   python main.py --deep-sentiment --platforms bili --test
```

#### 使用AI自动提取

```bash
# 完整流程（一键运行）
python main.py --complete --test

# 分步运行
python main.py --broad-topic  # Step 1: 提取话题
python main.py --deep-sentiment --test  # Step 2: 爬取数据
```

### 查看话题

```bash
# 查看所有话题
python add_custom_topic.py --list
```

**输出示例**：
```
================================================================================
话题列表
================================================================================

1. 小米汽车分析
   ID: custom_20251117_140530
   关键词: 小米汽车, 小米SU7, 雷军, 电动车
   日期: 2025-11-17
   状态: pending

2. AI技术趋势
   ID: custom_20251117_141205
   关键词: 人工智能, ChatGPT, 大模型, AI应用
   日期: 2025-11-17
   状态: completed

================================================================================
总计: 2 个话题
================================================================================
```

### 删除话题

```bash
# 按名称删除
python add_custom_topic.py --delete "小米汽车分析"

# 按ID删除
python add_custom_topic.py --delete-id "custom_20251117_140530"
```

### 关键词选择建议

**推荐格式**：
- ✅ 使用 3-7 个关键词
- ✅ 包含核心词和相关词
- ✅ 考虑不同表达方式
- ✅ 避免过于宽泛的词

**示例**：
```bash
# ❌ 不好：关键词太少
python add_custom_topic.py "汽车" "汽车"

# ✅ 好：关键词丰富
python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,雷军,电动车,新能源,智能驾驶"
```

---

## 数据管理

### 查看数据统计

```bash
# 查看所有平台数据
python check_crawled_data.py

# 查看特定平台
python check_crawled_data.py --platform bili
python check_crawled_data.py --platform weibo
python check_crawled_data.py --platform kuaishou
```

**输出示例**：
```
============================================================
B站数据统计
============================================================

总视频数量: 36 条
总评论数量: 520 条

============================================================
最新爬取的视频（前5条）
============================================================

ID: 115557571494414
标题: 炸裂！11.16凤凰晚报硬刚雷军！...
点赞: 399 | 评论: 67

============================================================
关键词覆盖情况
============================================================
小米汽车: 20 条视频
小米SU7: 8 条视频

============================================================
总计: 36 条视频, 520 条评论
============================================================
```

### 清空数据

#### 清空所有数据

```bash
python check_crawled_data.py --clear
```

**执行流程**：
1. 显示当前数据量
2. 要求输入 `yes` 确认
3. 删除所有视频和评论
4. 显示删除结果

#### 按关键词清空

```bash
python check_crawled_data.py --clear --keyword "小米汽车"
```

**示例**：
```bash
$ python check_crawled_data.py --clear --keyword "小米汽车"

正在清空包含关键词 '小米汽车' 的数据...
找到 18 条相关视频
确认删除这 18 条视频及其评论吗？(yes/no): yes

删除成功!
- 删除视频: 18 条
- 删除评论: 245 条
```

### 数据管理场景

#### 场景1：测试爬虫

```bash
# 1. 测试爬取
python main.py --deep-sentiment --platforms bili --test

# 2. 查看结果
python check_crawled_data.py

# 3. 清空测试数据
python check_crawled_data.py --clear
```

#### 场景2：更新特定主题

```bash
# 1. 清空旧数据
python check_crawled_data.py --clear --keyword "小米汽车"

# 2. 重新爬取
python main.py --deep-sentiment --platforms bili --test
```

---

## 常见问题排查

### 日志查看

#### Windows PowerShell（推荐）

```powershell
# 查看最后100行
Get-Content logs\kuaishou.log -Encoding UTF8 -Tail 100

# 实时监控日志
Get-Content logs\kuaishou.log -Encoding UTF8 -Wait

# 搜索特定内容
Select-String -Path logs\kuaishou.log -Pattern "comments count"
Select-String -Path logs\kuaishou.log -Pattern "ERROR"
```

#### 避免中文乱码

日志文件使用 UTF-8 编码保存。如果在 Windows CMD 中看到乱码，请使用以下方法：

1. **使用 PowerShell**（推荐）：
   ```powershell
   Get-Content logs\kuaishou.log -Encoding UTF8 -Tail 100
   ```

2. **使用文本编辑器**：
   - 用 VS Code、Notepad++ 等编辑器打开日志文件
   - 确保编码设置为 UTF-8

3. **使用 Python 查看**：
   ```bash
   python -c "with open('logs/kuaishou.log', 'r', encoding='utf-8') as f: print(f.read())"
   ```

### 数据库连接失败

**错误信息**：
```
connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**解决方案**：
1. 检查 `.env` 文件配置
2. 确认数据库服务已启动
3. 验证用户名和密码
4. 运行系统状态检查：
   ```bash
   python main.py --status
   ```

### 没有数据

**输出**：
```
总视频数量: 0 条
总评论数量: 0 条
```

**原因**：
- 还未运行爬虫
- 爬虫失败未保存数据
- 数据已被清空

**解决**：
```bash
# 运行爬虫
python main.py --deep-sentiment --platforms bili --test
```

---

## 平台特定问题

### 微博 HTTP 432 错误

#### 问题描述

```
MediaCrawler ERROR (client.py:63) - [WeiboClient.request] HTTP 432
media_platform.weibo.exception.DataFetchError: HTTP 432
```

**错误原因**：
- ❌ Cookie已过期或无效
- ❌ 请求频率过快
- ❌ IP被限制
- ❌ 需要验证码验证
- ❌ 账号风控

#### 解决方案

**方案1：重新登录（推荐）**

```bash
# 1. 删除旧Cookie
del DeepSentimentCrawling\MediaCrawler\cookies\weibo_cookies.json

# 2. 重新扫码登录
python main.py --deep-sentiment --platforms wb --test
```

**方案2：降低爬取频率**

编辑 `DeepSentimentCrawling/MediaCrawler/config/base_config.py`：
```python
CRAWLER_MAX_NOTES_COUNT = 5  # 从默认的10改为5
ENABLE_GET_COMMENTS = False  # 暂时禁用评论爬取
```

**方案3：使用其他平台**

```bash
# B站（最稳定，无需登录）
python main.py --deep-sentiment --platforms bili --test

# 小红书
python main.py --deep-sentiment --platforms xhs --test
```

### 快手登录点击超时

#### 问题描述

```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
waiting for locator("//p[text()='登录']")
  - <div></div> from <div>…</div> subtree intercepts pointer events
```

**错误原因**：登录按钮被遮挡元素拦截点击事件

#### 解决方案

**已修复**：在 `media_platform/kuaishou/login.py` 第74行使用 `force=True` 强制点击：

```python
await login_button_ele.click(force=True)
```

**测试验证**：
```bash
python main.py --deep-sentiment --platforms ks --test
```

### 快手评论为0

#### 问题描述

```
快手:
  内容: 40 条
  评论: 0 条
```

#### 诊断步骤

**步骤1：检查日志**

```bash
python main.py --deep-sentiment --platforms ks --test
```

查看日志中的关键信息：
```
[KuaiShouClient.get_video_all_comments] photo_id:xxx, comments_res keys:...
[KuaiShouClient.get_video_all_comments] photo_id:xxx, pcursor:xxx, comments count:0
```

**步骤2：检查登录状态**

```bash
# 删除旧的 Cookie
rmdir /s /q MindSpider\DeepSentimentCrawling\MediaCrawler\browser_data\ks_user_data_dir

# 重新登录
python main.py --deep-sentiment --platforms ks --test
```

**步骤3：检查配置**

确认 `config/base_config.py` 中：
```python
ENABLE_GET_COMMENTS = True  # 必须为 True
```

#### 可能原因

1. **快手 API 未返回评论数据**（最可能）
2. **评论数据类型不匹配**（已修复）
3. **评论爬取被禁用**
4. **快手反爬虫机制**

### 知乎数据类型错误

#### 问题描述

```
asyncpg.exceptions.DataError: invalid input for query argument $8: 1763364305 (expected str, got int)
```

**错误原因**：数据库中 `created_time`、`updated_time`、`publish_time` 字段定义为 `String` 类型，但爬虫传入的是整数时间戳。

#### 解决方案

**已修复**：在 `store/zhihu/_store_impl.py` 中添加类型转换：

```python
# 内容存储
if "created_time" in content_item and isinstance(content_item["created_time"], int):
    content_item["created_time"] = str(content_item["created_time"])
if "updated_time" in content_item and isinstance(content_item["updated_time"], int):
    content_item["updated_time"] = str(content_item["updated_time"])

# 评论存储
if "publish_time" in comment_item and isinstance(comment_item["publish_time"], int):
    comment_item["publish_time"] = str(comment_item["publish_time"])
```

**测试验证**：
```bash
python main.py --deep-sentiment --platforms zhihu --test
```

---

## 最佳实践

### 平台选择建议

| 话题类型 | 推荐平台 | 原因 |
|---------|---------|------|
| 科技产品 | 小红书、知乎、B站 | 用户评测和深度讨论多 |
| 娱乐八卦 | 微博、抖音 | 传播速度快，讨论热烈 |
| 专业技术 | 知乎、B站 | 专业用户多，内容深度好 |
| 生活消费 | 小红书、抖音 | 用户体验分享多 |
| 时事热点 | 微博、知乎 | 实时性强，观点多元 |

### 平台稳定性

| 平台 | 状态 | 说明 |
|------|------|------|
| B站 (bili) | ✅ 正常 | 无需登录，最稳定 |
| 小红书 (xhs) | ✅ 正常 | 需要登录 |
| 知乎 (zhihu) | ✅ 正常 | 需要登录，已修复类型错误 |
| 抖音 (dy) | ✅ 正常 | 需要登录 |
| 快手 (ks) | ⚠️ 部分问题 | 评论可能为0，已修复登录问题 |
| 微博 (wb) | ⚠️ 问题 | HTTP 432错误，建议重新登录 |
| 贴吧 (tieba) | ✅ 正常 | 部分支持 |

### 日常使用推荐流程

```bash
# 每天早上：AI 自动提取热点
python main.py --broad-topic

# 添加特定关注话题
python add_custom_topic.py "行业话题" "关键词..."

# 运行爬虫（推荐使用稳定平台）
python main.py --deep-sentiment --platforms bili xhs zhihu --test

# 查看数据
python check_crawled_data.py
```

### 关键词优化建议

- **核心词**：话题的主要名称（如"小米汽车"）
- **相关词**：相关产品、人物、事件（如"小米SU7"、"雷军"）
- **行业词**：行业通用术语（如"电动车"、"新能源"）
- **热点词**：当前热门词汇（如"智能驾驶"、"自动驾驶"）

### 数据管理建议

```bash
# 测试前清空旧数据
python check_crawled_data.py --clear
python main.py --deep-sentiment --platforms bili --test

# 按主题管理数据
python add_custom_topic.py "主题A" "关键词A1,关键词A2"
python main.py --deep-sentiment --platforms bili --test
python check_crawled_data.py --clear --keyword "关键词A1"

# 定期清理历史数据（保留最近30天）
# 使用 SQL 或数据库管理工具
```

### 数据备份

在清空重要数据前，建议先备份数据库：

```bash
# PostgreSQL备份
pg_dump -U bettafish -d bettafish > backup.sql

# 清空数据
python check_crawled_data.py --clear

# 如需恢复
psql -U bettafish -d bettafish < backup.sql
```

---

## 常用命令速查

### 话题管理

```bash
# 添加话题
python add_custom_topic.py "话题名称" "关键词1,关键词2"

# 查看话题
python add_custom_topic.py --list

# 删除话题
python add_custom_topic.py --delete "话题名称"
```

### 爬虫运行

```bash
# 测试模式（单平台）
python main.py --deep-sentiment --platforms bili --test

# 测试模式（多平台）
python main.py --deep-sentiment --platforms bili xhs zhihu --test

# 完整流程
python main.py --complete --test

# AI提取话题
python main.py --broad-topic
```

### 数据管理

```bash
# 查看数据
python check_crawled_data.py
python check_crawled_data.py --platform bili

# 清空数据
python check_crawled_data.py --clear
python check_crawled_data.py --clear --keyword "关键词"
```

### 日志查看

```bash
# PowerShell
Get-Content logs\kuaishou.log -Encoding UTF8 -Tail 100
Get-Content logs\kuaishou.log -Encoding UTF8 -Wait
Select-String -Path logs\kuaishou.log -Pattern "ERROR"

# Python
python -c "with open('logs/kuaishou.log', 'r', encoding='utf-8') as f: print(f.read())"
```

### 系统检查

```bash
# 检查系统状态
python main.py --status

# 查看帮助
python main.py --help
python add_custom_topic.py --help
python check_crawled_data.py --help
```

---

## 故障排查流程图

```
遇到问题
    ↓
查看日志（logs/*.log）
    ↓
确定问题类型
    ├─ 数据库连接问题 → 检查 .env 配置 → 运行 python main.py --status
    ├─ 登录问题 → 删除 Cookie → 重新登录
    ├─ 数据类型错误 → 检查是否已修复 → 更新代码
    ├─ 评论为0 → 检查日志 → 重新登录 → 检查配置
    └─ 其他问题 → 查看本文档对应章节 → 尝试解决方案
```

---

## 获取帮助

如果问题仍然存在：

1. **查看日志**：
   ```bash
   Get-Content logs\*.log -Encoding UTF8 -Tail 100
   ```

2. **检查系统状态**：
   ```bash
   python main.py --status
   ```

3. **查看数据**：
   ```bash
   python check_crawled_data.py
   ```

4. **参考文档**：
   - [MindSpider README](../MindSpider/README.md)
   - 本文档各章节

---

## 附录：错误码对照表

### 微博错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| HTTP 432 | 反爬虫拦截 | 重新登录或使用代理 |
| HTTP 403 | 访问被拒绝 | Cookie无效，重新登录 |
| HTTP 418 | 请求频率过快 | 降低爬取速度 |
| HTTP 429 | 请求过多 | 等待一段时间后重试 |

### 快手错误信息

| 错误信息 | 含义 | 解决方案 |
|---------|------|----------|
| No Login | 未登录 | 重新扫码登录 |
| Rate limit exceeded | 接口限流 | 增加延迟时间 |
| visionCommentList: null | 视频不存在 | 跳过该视频 |

---

---

## 平台爬取技术方案

### 技术架构概览

MindSpider 基于 **MediaCrawler** 框架，采用 Playwright + 反爬虫技术实现对7大社交媒体平台的数据爬取。

**核心技术栈**:
- **浏览器自动化**: Playwright (真实浏览器环境)
- **反检测**: stealth.min.js (防止网站检测爬虫)
- **登录管理**: Cookie持久化 + 二维码/手机号登录
- **请求签名**: 各平台专用签名算法
- **数据存储**: PostgreSQL/MySQL
- **情感分析**: 22种语言支持

### 平台测试状态

| 平台 | 状态 | 登录方式 | 反爬虫难度 | 稳定性 |
|------|------|---------|-----------|--------|
| B站 (bili) | ✅ 正常 | 二维码/Cookie | ⭐⭐ 低 | ⭐⭐⭐⭐⭐ |
| 快手 (ks) | ✅ 正常 | 二维码/Cookie | ⭐⭐⭐ 中 | ⭐⭐⭐⭐ |
| 知乎 (zhihu) | ✅ 正常 | 二维码/Cookie | ⭐⭐⭐ 中 | ⭐⭐⭐⭐ |
| 微博 (wb) | ✅ 正常 | 二维码/Cookie | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ |
| 抖音 (dy) | ✅ 正常 | 二维码/Cookie | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ |
| 小红书 (xhs) | ❌ 问题 | 二维码/手机号/Cookie | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐ |
| 贴吧 (tieba) | ⚠️ 部分 | Cookie | ⭐⭐ 低 | ⭐⭐⭐ |

---

## 各平台技术方案详解

### 1. B站 (Bilibili) - 最稳定平台

**技术特点**:
- ✅ 无需登录即可爬取公开内容
- ✅ WBI签名机制（已破解）
- ✅ 反爬虫强度低
- ✅ API稳定性高

**登录方式**:
```python
# 1. 二维码登录（推荐）
config.LOGIN_TYPE = "qrcode"

# 2. Cookie登录
config.LOGIN_TYPE = "cookie"
config.COOKIES = "SESSDATA=xxx; DedeUserID=xxx"
```

**核心技术**:
1. **WBI签名**: 从localStorage获取wbi_img_urls，计算请求签名
2. **Stealth.min.js**: 防止浏览器指纹检测
3. **Cookie管理**: SESSDATA + DedeUserID

**爬取流程**:
```
启动浏览器 → 加载stealth.js → 访问首页 → 检查登录状态 
→ 执行搜索/详情/创作者爬取 → 获取评论 → 存储数据库
```

**优势**:
- 无需登录即可爬取
- API响应速度快
- 数据结构清晰
- 很少触发反爬虫

**注意事项**:
- 长视频需要更长的超时时间（60秒）
- 建议使用CDP模式提升稳定性

---

### 2. 快手 (Kuaishou) - 稳定可用

**技术特点**:
- ✅ GraphQL API
- ✅ 登录按钮需force点击
- ⚠️ 评论可能为0（已知问题）
- ✅ 整体稳定

**登录方式**:
```python
# 二维码登录（推荐）
config.LOGIN_TYPE = "qrcode"
# 使用force=True强制点击登录按钮
await login_button_ele.click(force=True)
```

**核心技术**:
1. **GraphQL查询**: 使用预定义的GraphQL查询模板
2. **强制点击**: 登录按钮被遮挡，需force=True
3. **Cookie验证**: 检查passToken

**已修复问题**:
- ✅ 登录点击超时 → 使用force=True
- ⚠️ 评论数为0 → 仍在调查

**爬取示例**:
```bash
python main.py --deep-sentiment --platforms ks --test
```

---

### 3. 知乎 (Zhihu) - 稳定可用

**技术特点**:
- ✅ 需要先访问搜索页面获取Cookie
- ✅ Canvas二维码登录
- ✅ 数据类型已修复
- ✅ 稳定性好

**登录方式**:
```python
# 二维码登录（Canvas渲染）
config.LOGIN_TYPE = "qrcode"
# 从Canvas元素提取二维码
base64_qrcode_img = await utils.find_qrcode_img_from_canvas(
    page, canvas_selector="canvas.Qrcode-qrcode"
)
```

**核心技术**:
1. **Canvas二维码**: 从Canvas元素提取base64图片
2. **Cookie预热**: 访问搜索页面获取完整Cookie
3. **类型转换**: 时间戳转字符串（已修复）

**特殊流程**:
```python
# 1. 访问首页并登录
await page.goto("https://www.zhihu.com")
await login()

# 2. 访问搜索页面获取搜索Cookie（重要！）
await page.goto("https://www.zhihu.com/search?q=python")
await asyncio.sleep(5)
await client.update_cookies()

# 3. 开始爬取
await search()
```

**已修复问题**:
- ✅ 数据类型错误 → created_time/updated_time转字符串

---

### 4. 微博 (Weibo) - 反爬虫较强

**技术特点**:
- ⚠️ HTTP 432反爬虫拦截
- ⚠️ Cookie容易过期
- ✅ 移动端API相对稳定
- ⚠️ 需要频繁重新登录

**登录方式**:
```python
# 二维码登录（移动端）
config.LOGIN_TYPE = "qrcode"
# 登录后重定向到移动端
await page.goto("https://m.weibo.cn")
```

**核心技术**:
1. **移动端API**: 使用m.weibo.cn接口
2. **Cookie双端同步**: PC端登录后同步到移动端
3. **错误处理**: 详细的HTTP 432错误提示

**常见问题**:
```python
# HTTP 432 错误处理
if response.status_code == 432:
    logger.error("微博反爬虫拦截 (HTTP 432)")
    logger.error("可能原因：")
    logger.error("  1. Cookie已过期，需要重新登录")
    logger.error("  2. 请求频率过快")
    logger.error("  3. IP被限制")
```

**解决方案**:
1. 删除Cookie重新登录
2. 降低爬取频率
3. 使用代理IP
4. 改用其他平台（推荐B站）

---

### 5. 抖音 (Douyin) - 反爬虫较强

**技术特点**:
- ⚠️ a-bogus签名（JS版本）
- ⚠️ 滑块验证码
- ✅ localStorage登录状态
- ⚠️ 需要处理验证码中间页

**登录方式**:
```python
# 二维码登录
config.LOGIN_TYPE = "qrcode"
# 可能需要滑动验证码
await check_page_display_slider(move_step=3, slider_level="hard")
```

**核心技术**:
1. **a-bogus签名**: 动态生成请求签名
2. **滑块验证**: 自动识别并滑动验证码
3. **localStorage检查**: HasUserLogin=1

**验证码处理**:
```python
# 检查是否有滑动验证码
await check_page_display_slider(move_step=10, slider_level="easy")

# 如果重定向到验证码中间页
if "验证码中间页" in await page.title():
    await check_page_display_slider(move_step=3, slider_level="hard")
```

**注意事项**:
- 滑块验证准确率不高
- 建议使用Cookie登录
- 需要更长的超时时间（60秒）

---

### 6. 小红书 (XHS) - 反爬虫极强 ❌

**技术特点**:
- ❌ 反爬虫机制最强
- ❌ 频繁更新检测规则
- ❌ 需要手动验证码
- ❌ 当前不建议使用

**登录方式**:
```python
# 1. 二维码登录
config.LOGIN_TYPE = "qrcode"

# 2. 手机号登录（需要短信验证码）
config.LOGIN_TYPE = "phone"
config.LOGIN_PHONE = "your_phone"

# 3. Cookie登录
config.LOGIN_TYPE = "cookie"
```

**核心技术**:
1. **web_session验证**: 检查Cookie中的web_session
2. **xsec_token**: 每个笔记都有独立的安全令牌
3. **验证码检测**: "请通过验证"提示

**主要问题**:
- 登录过程中频繁出现验证码
- API返回数据结构不稳定
- Cookie容易失效
- 搜索结果可能为空

**建议**:
- ❌ 不建议使用小红书爬取
- ✅ 改用B站、知乎等稳定平台
- ⚠️ 如必须使用，建议手动获取Cookie

---

### 7. 贴吧 (Tieba) - 部分支持

**技术特点**:
- ⚠️ 部分功能支持
- ✅ Cookie登录
- ⚠️ 数据结构简单

**状态**: 部分支持，功能有限

---

## 反爬虫技术对比

### 核心反爬虫技术

| 技术 | B站 | 快手 | 知乎 | 微博 | 抖音 | 小红书 |
|------|-----|------|------|------|------|--------|
| **请求签名** | WBI | GraphQL | 无 | 无 | a-bogus | xsec |
| **浏览器指纹** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Cookie验证** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **滑块验证码** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **频率限制** | 低 | 中 | 中 | 高 | 高 | 极高 |
| **IP封禁** | 少 | 少 | 少 | 多 | 多 | 极多 |

### 破解方案

**1. Playwright真实浏览器**
```python
# 使用真实浏览器环境，绕过浏览器指纹检测
chromium = playwright.chromium
browser_context = await chromium.launch(
    headless=config.HEADLESS,
    proxy=proxy_config
)
```

**2. stealth.min.js反检测**
```python
# 加载反检测脚本
await browser_context.add_init_script(path="libs/stealth.min.js")
```

**3. Cookie持久化**
```python
# 保存登录状态
await browser_context.storage_state(path="cookies/platform_cookies.json")

# 恢复登录状态
await browser_context.add_cookies(saved_cookies)
```

**4. 请求签名**
```python
# B站WBI签名
img_key, sub_key = await get_wbi_keys()
signed_params = BilibiliSign(img_key, sub_key).sign(params)

# 抖音a-bogus签名
a_bogus = await get_a_bogus(uri, query_string, post_data, user_agent)
```

**5. 频率控制**
```python
# 每页爬取后休眠
await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)
```

**6. IP代理池**
```python
if config.ENABLE_IP_PROXY:
    ip_proxy_pool = await create_ip_pool(
        config.IP_PROXY_POOL_COUNT,
        enable_validate_ip=True
    )
```

---

## 最佳实践建议

### 平台选择策略

**优先级排序**:
1. **B站** - 最稳定，无需登录，推荐首选
2. **知乎** - 稳定可靠，内容质量高
3. **快手** - 基本稳定，下沉市场数据
4. **微博** - 需要注意Cookie过期
5. **抖音** - 需要处理验证码
6. **小红书** - 不推荐使用

### 爬取配置建议

```python
# 推荐配置
CRAWLER_MAX_NOTES_COUNT = 20  # 每次爬取数量
CRAWLER_MAX_SLEEP_SEC = 2     # 页面间隔时间
MAX_CONCURRENCY_NUM = 1        # 并发数（建议为1）
ENABLE_GET_COMMENTS = True     # 启用评论爬取
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20  # 每条内容的评论数

# 登录方式
LOGIN_TYPE = "qrcode"  # 推荐二维码登录
# LOGIN_TYPE = "cookie"  # 或使用Cookie登录

# 代理设置（可选）
ENABLE_IP_PROXY = False  # 一般情况下不需要
```

### 错误处理建议

```python
# 1. Cookie过期 → 重新登录
if "HTTP 432" in error or "未登录" in error:
    # 删除旧Cookie
    os.remove("cookies/platform_cookies.json")
    # 重新运行爬虫
    python main.py --deep-sentiment --platforms wb --test

# 2. 验证码 → 手动处理或切换平台
if "验证码" in error:
    # 建议切换到B站或知乎
    python main.py --deep-sentiment --platforms bili --test

# 3. 频率限制 → 降低爬取速度
if "频率" in error or "限制" in error:
    # 增加休眠时间
    CRAWLER_MAX_SLEEP_SEC = 5
```

### 日常维护建议

1. **定期检查Cookie**:
   ```bash
   # 每周检查一次登录状态
   python main.py --deep-sentiment --platforms bili --test
   ```

2. **监控日志**:
   ```bash
   # 查看错误日志
   Get-Content logs\bilibili.log -Encoding UTF8 -Tail 100 | Select-String "ERROR"
   ```

3. **数据备份**:
   ```bash
   # 定期备份数据库
   pg_dump -U bettafish -d bettafish > backup_$(date +%Y%m%d).sql
   ```

---

**文档维护**: BettaFish 项目组  
**最后更新**: 2025-11-17  
**版本**: v2.1
