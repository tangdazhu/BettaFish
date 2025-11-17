# MindSpider 更新日志

## [2025-11-17] - 配置管理优化与工具增强

### ⚠️ 已知问题

#### 微博爬取问题
- **问题**：微博爬虫出现JSON解析错误
- **原因**：MediaCrawler的微博爬虫模块与微博API不兼容
- **状态**：等待MediaCrawler库更新
- **临时方案**：使用B站等其他平台（B站最稳定，无需登录）
- **详细文档**：参见 `docs/MindSpider微博爬取问题排查.md`

#### 平台状态

| 平台 | 状态 | 说明 |
|------|------|------|
| B站 | ✅ 正常 | 无需登录，最稳定 |
| 微博 | ⚠️ 问题 | API不兼容 |
| 小红书 | ✅ 可用 | 需要登录 |
| 抖音 | ✅ 可用 | 需要登录 |
| 快手 | ✅ 可用 | 需要登录 |
| 知乎 | ✅ 可用 | 需要登录 |
| 贴吧 | ✅ 可用 | 需要登录 |

### 新增功能

#### 1. 统一配置管理
- ✅ 实现了统一的环境变量配置管理
- ✅ 所有配置项从 `.env` 文件读取
- ✅ MindSpider主项目和MediaCrawler子项目共享配置
- ✅ 支持MySQL和PostgreSQL两种数据库

#### 2. 自定义话题管理工具 (`add_custom_topic.py`)
- ✅ **添加话题**：命令行快速添加自定义话题
- ✅ **查看话题**：列出所有话题及其详细信息
- ✅ **删除话题**：支持按名称或ID删除（需确认）
- ✅ 支持多个关键词（逗号分隔）
- ✅ 自动生成话题ID
- ✅ 可选添加话题描述
- ✅ 直接保存到数据库

**使用示例**：
```bash
# 添加话题
python add_custom_topic.py "小米汽车分析" "小米汽车,小米SU7,电动车"

# 查看所有话题
python add_custom_topic.py --list

# 删除话题
python add_custom_topic.py --delete "小米汽车分析"
```

#### 3. 数据检查和管理工具 (`check_crawled_data.py`)
- ✅ **多平台支持**：B站、微博、小红书、抖音、快手
- ✅ **所有平台统计**：一键查看所有平台数据汇总
- ✅ **单平台详情**：查看指定平台的详细数据
- ✅ 显示最新内容详情（前5条）
- ✅ **动态关键词统计**：自动从 `daily_topics` 表读取
- ✅ **智能关键词解析**：支持中文逗号、英文逗号、顿号
- ✅ 数据质量概览
- ✅ **清空所有数据**（需确认）
- ✅ **按关键词清空数据**（精确删除）

**使用示例**：
```bash
# 查看所有平台数据
python check_crawled_data.py

# 查看指定平台数据
python check_crawled_data.py --platform bili
python check_crawled_data.py --platform weibo

# 清空指定平台所有数据
python check_crawled_data.py --platform bili --clear

# 清空特定关键词数据
python check_crawled_data.py --platform bili --clear --keyword "阿里巴巴"
```

### 优化改进

#### 配置管理
- ✅ 删除了90多行的临时配置同步代码
- ✅ `configure_mediacrawler_db()` 从100行简化到15行
- ✅ 修改 `db_config.py` 从环境变量读取配置
- ✅ 统一环境变量命名（`DB_HOST`, `DB_PORT` 等）

#### 代码质量
- ✅ 修复了 `base_config.py` 的语法错误
- ✅ 优化了数据库连接管理
- ✅ 改进了错误处理和日志记录
- ✅ 添加了 `psycopg2-binary` 依赖

#### 文档更新
- ✅ 更新 `README.md` 添加新工具说明
- ✅ 新增 `docs/数据库配置统一说明.md`
- ✅ 完善配置管理章节
- ✅ 添加快速开始工作流

### Bug修复

- ✅ 修复了B站爬虫的浏览器页面关闭问题
- ✅ 修复了配置文件语法错误
- ✅ 修复了控制台GBK编码错误
- ✅ 修复了数据库表名不匹配问题

### 技术改进

#### 配置架构
```
项目根目录/.env
    ↓
    ├─→ MindSpider主项目 (config.py + pydantic-settings)
    └─→ MediaCrawler子项目 (db_config.py + os.getenv)
```

#### 依赖更新
- 新增 `psycopg2-binary>=2.9.0` 用于PostgreSQL同步操作
- 保留 `psycopg[binary]>=3.1.0` 用于异步操作

### 配置示例

```bash
# .env 文件配置示例
DB_HOST=localhost
DB_PORT=5432
DB_USER=bettafish
DB_PASSWORD=bettafish_2024
DB_NAME=bettafish
DB_CHARSET=utf8mb4
DB_DIALECT=postgresql
```

### 使用建议

1. **配置管理**：
   - 只修改 `.env` 文件
   - 不要修改 `db_config.py` 或 `base_config.py`
   - 使用 `python main.py --status` 验证配置

2. **数据库切换**：
   ```bash
   # PostgreSQL
   DB_DIALECT=postgresql
   DB_PORT=5432
   
   # MySQL
   DB_DIALECT=mysql
   DB_PORT=3306
   ```

3. **工作流程**：
   ```bash
   # 1. 添加自定义话题
   python add_custom_topic.py "话题名" "关键词1,关键词2"
   
   # 2. 运行爬虫
   python main.py --deep-sentiment --platforms bili --test
   
   # 3. 检查数据
   python check_crawled_data.py
   ```

### 已知问题

- CDP模式在某些环境下可能启动失败，已默认禁用
- 小红书平台存在账号风控问题，需要等待24小时恢复
- 控制台输出需避免使用emoji字符（GBK编码限制）

### 下一步计划

- [ ] 支持更多平台的数据检查
- [ ] 添加数据导出功能
- [ ] 优化爬虫稳定性
- [ ] 增强错误恢复机制
- [ ] 添加数据可视化功能

---

## 贡献者

感谢所有为MindSpider项目做出贡献的开发者！

## 参考资料

- [The Twelve-Factor App - Config](https://12factor.net/config)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [MediaCrawler Project](https://github.com/NanmiCoder/MediaCrawler)
