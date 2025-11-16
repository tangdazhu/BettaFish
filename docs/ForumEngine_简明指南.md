# Forum Engine 工作原理简明指南

> BettaFish 微舆系统核心创新功能

## 🎯 什么是 Forum Engine？

**Forum Engine（论坛引擎）** 充当"论坛主持人"角色，协调多个 AI Agent 之间的交流和协作。

## 🤔 为什么需要它？

### 单一 LLM 的问题
- ❌ 思维固化
- ❌ 观点重复
- ❌ 视角单一
- ❌ 缺乏批判性

### Forum Engine 的优势
- ✅ 多视角分析
- ✅ 观点碰撞
- ✅ 主持引导
- ✅ 集体智能

## 🏗️ 工作架构

```
用户提问
    ↓
并行启动 3 个 Agent
    ↓
┌─────────┬─────────┬─────────┐
│ Query   │ Media   │ Insight │
│ Agent   │ Agent   │ Agent   │
└────┬────┴────┬────┴────┬────┘
     │         │         │
     └────────┬┴─────────┘
              ↓
      Forum Engine
      (主持人监控)
              ↓
      生成总结和引导
              ↓
      Agent 调整方向
              ↓
      循环迭代深化
              ↓
      Report Agent
      生成最终报告
```

## 🔄 工作流程

### 1. 初始阶段
- 3个 Agent 并行启动
- 各自使用专属工具搜索
- 发布初步发现到论坛

### 2. 论坛协作（循环）
- **Forum Engine 监控**：实时监控各 Agent 日志
- **提取关键信息**：识别重要发现
- **主持人总结**：LLM 分析并生成引导
- **Agent 调整**：根据引导深入研究

### 3. 最终整合
- Report Agent 收集论坛讨论
- 生成综合分析报告

## 💬 实际案例

### 用户输入
```
"分析武汉大学的品牌声誉"
```

### 第一轮发现

**Query Agent**:
```
发现微博热搜 #武汉大学樱花季#
讨论量10万+，主要关注校园美景
```

**Media Agent**:
```
抖音相关视频500万播放
内容类型：风景70%、生活20%、学术10%
```

**Insight Agent**:
```
数据库查询：近7天2000+条
情感分析：正面65%、中性30%、负面5%
```

### 主持人总结

```
📊 综合分析：

发现：
1. 传播热点集中在校园美景（樱花季）
2. 学术内容传播较少（仅10%）
3. 整体舆情正面，但有5%负面声音

🎯 建议深入调研：
1. 负面舆情的具体来源？
2. 学术成果为何传播效果不佳？
3. 不同平台用户画像差异？
4. 与竞品高校的对比？
```

### 第二轮深入

**Query Agent**（根据引导）:
```
搜索"武汉大学 学术成果"
发现：学术新闻主要在官方渠道
```

**Media Agent**（根据引导）:
```
分析B站学术视频
发现：播放量低，用户觉得"太硬核"
```

**Insight Agent**（根据引导）:
```
分析负面评论：
40%校园管理、30%学费住宿、30%就业
```

### 最终报告
整合所有发现，生成深度分析报告

## 🔧 技术实现

### 代码结构
```
ForumEngine/
├── monitor.py     # 监控Agent日志
└── llm_host.py    # 主持人LLM
```

### 核心逻辑

**monitor.py** - 监控器
- 读取各 Agent 日志
- 提取关键信息
- 发布到论坛
- 触发主持人总结

**llm_host.py** - 主持人
- 分析论坛讨论
- 生成综合总结
- 提出引导建议

**forum_reader.py** - Agent工具
- 读取主持人总结
- 读取其他Agent发现
- 调整研究策略

## ⚙️ 配置说明

### .env 配置
```bash
# Forum Host LLM配置
FORUM_HOST_API_KEY=sk-your-key
FORUM_HOST_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
FORUM_HOST_MODEL_NAME=qwen-max
```

### 推荐模型
- **qwen-max**: 中文理解强（推荐）
- **gpt-4**: 综合能力强
- **claude-3-opus**: 长文本处理好

## 📊 效果对比

| 指标 | 单一LLM | Forum Engine | 提升 |
|------|---------|--------------|------|
| 分析深度 | ⭐⭐ | ⭐⭐⭐⭐⭐ | +150% |
| 覆盖面 | ⭐⭐ | ⭐⭐⭐⭐ | +80% |
| 发现盲点 | ⭐ | ⭐⭐⭐⭐⭐ | +200% |
| 报告质量 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +60% |

## 🌟 核心价值

1. **突破单一LLM局限** - 多Agent协作产生集体智能
2. **模拟专家组讨论** - 还原真实的专家会议过程
3. **动态优化路径** - 根据讨论调整研究方向
4. **提升分析质量** - 多维度、深层次、全覆盖

## 🎓 最佳实践

### 配置建议
```bash
# 主持人使用大参数模型
FORUM_HOST_MODEL_NAME=qwen-max

# 各Agent使用特长模型
QUERY_ENGINE_MODEL_NAME=deepseek-chat  # 快速
MEDIA_ENGINE_MODEL_NAME=qwen-vl-max    # 多模态
INSIGHT_ENGINE_MODEL_NAME=qwen-max     # 深度
```

### 使用技巧
1. 合理设置触发阈值
2. 保持日志清晰
3. 定期清理历史
4. 监控总结质量

## 🔮 未来展望

- 更智能的主持人（识别矛盾、主动质疑）
- 更丰富的协作模式（Agent直接对话）
- 可视化论坛（实时展示讨论过程）
- 扩展到其他领域（金融、医疗、法律）

---

## 🔬 深度解析：ForumEngine 协同指导机制

> 本章节详细剖析 ForumEngine 如何指导三个 Engine 协同工作

### ⚠️ 重要说明：工作模式

**ForumEngine 采用"异步并行 + 非阻塞协同"模式，而非串行模式**

#### 核心特征

- ✅ **并行启动**：三个 Engine 同时启动，互不等待
- ✅ **独立执行**：各 Engine 完成一个段落后立即开始下一个，不等待主持人指导
- ✅ **累积触发**：主持人累积 5 条发言后才分析一次（不是每条都触发）
- ✅ **机会主义读取**：Agent 在反思阶段"如果有就用"地读取指导，没有也继续
- ❌ **不是串行**：不是"Insight完成 → Forum指导 → Insight继续"的串行等待模式

#### 与串行模式的对比

| 维度 | ❌ 串行模式（误解） | ✅ 实际的异步并行模式 |
|------|----------------|------------------|
| **启动方式** | Insight 先启动，其他等待 | 三个 Engine 同时启动 |
| **执行方式** | 完成一个段落后等待指导 | 完成后立即开始下一个段落 |
| **触发条件** | 每次完成就触发 Forum | 累积 5 条发言才触发 |
| **指导对象** | 专门指导刚完成的 Engine | 指导所有正在运行的 Engine |
| **读取时机** | 收到指导后立即读取 | 在反思阶段才尝试读取 |
| **总耗时** | 串行累加（60-90分钟） | 并行重叠（25-35分钟） |

#### 实际时间线示例

```
时间    Insight              Media               Query               Forum
────────────────────────────────────────────────────────────────────────────
00:00   启动，搜索段落1      启动，搜索段落1      启动，搜索段落1      Monitor启动
        ↓                   ↓                   ↓
03:00   完成段落1 ──────────→ forum.log [1]
        立即开始段落2        继续搜索段落1        继续搜索段落1        累积1条
        ↓
05:00   完成段落2 ──────────→ forum.log [2]
        立即开始段落3        完成段落1 ─────────→ forum.log [3]       累积3条
        ↓                   立即开始段落2        继续搜索段落1
                            ↓
07:00   完成段落3 ──────────→ forum.log [4]
        立即开始段落4        继续搜索段落2        完成段落1 ─────────→ forum.log [5]
                                                立即开始段落2        累积5条！
                                                                    ↓
08:00                                                              【触发HOST】
                                                                    分析5条发言
                                                                    生成引导
                                                                    ↓
08:30                                                              写入 forum.log
                                                                    [HOST] 综合分析...
        ↓                   ↓                   ↓
        继续段落4           继续段落2           继续段落2            等待下一个5条
        (如果进入反思阶段)   (如果进入反思阶段)   (如果进入反思阶段)
        会读取HOST指导      会读取HOST指导      会读取HOST指导
```

#### 为什么要这样设计？

**优势**：
1. **效率高**：三个 Engine 并行工作，总耗时约为最慢 Engine 的耗时，而非三者之和
2. **容错强**：某个 Engine 慢了不影响其他 Engine 继续工作
3. **灵活性**：主持人的建议是给所有 Engine 的，各自理解和应用
4. **可扩展**：未来可以轻松增加更多 Engine，不需要修改协同逻辑

**如果是串行模式的问题**：
1. ❌ 效率低：总耗时 = Insight耗时 + Media耗时 + Query耗时（60-90分钟）
2. ❌ 容错差：一个 Engine 卡住，整个系统停滞
3. ❌ 僵化：每个 Engine 必须等待专门的指导才能继续

**核心理念**：让 AI Agents 像真实的专家组一样工作——各自独立研究，定期交流，而不是排队等待发言权。

---

### 🏁 交互结束机制

#### 3 种结束条件

ForumEngine 和其他 3 个 Engine 的交互有 **3 种结束方式**：

**1. 日志文件缩短（正常结束）⭐**

```python
# monitor.py - 检测到日志文件变小
if any_shrink:  # 日志文件缩短
    self.is_searching = False
    self.write_to_forum_log(f"=== ForumEngine 论坛结束 - {end_time} ===", "SYSTEM")
```

- **触发时机**：某个 Engine 的日志文件被清空或重置
- **发生场景**：
  - ✅ Engine 完成所有段落，准备生成最终报告（**最常见**）
  - ✅ 系统重启或重新运行
- **特点**：立即结束，写入结束标记

**2. 长时间无活动（超时结束）**

```python
# monitor.py - 15分钟无新日志
if self.search_inactive_count >= 900:  # 900秒 = 15分钟
    logger.info("ForumEngine: 长时间无活动，结束论坛")
    self.is_searching = False
    self.write_to_forum_log(f"=== ForumEngine 论坛结束 - {end_time} ===", "SYSTEM")
```

- **触发时机**：连续 15 分钟没有任何 Engine 产生新日志
- **发生场景**：
  - 所有 Engine 都已完成工作
  - 某个 Engine 卡住或崩溃
  - 网络问题导致长时间无响应
- **特点**：自动检测，防止 Monitor 永久运行

**3. 手动停止（外部结束）**

```python
# monitor.py - 用户主动停止
def stop_monitoring(self):
    self.is_monitoring = False
    self.monitor_thread.join(timeout=5)
```

- **触发时机**：用户在前端点击"停止"按钮
- **特点**：立即响应，最多等待 5 秒

#### 结束方式对比

| 结束方式 | 触发条件 | 等待时间 | 写入标记 | 使用场景 |
|---------|---------|---------|---------|---------|
| **日志缩短** | 日志文件变小 | 立即 | ✅ 是 | ⭐ Engine 正常完成（最常见） |
| **超时结束** | 15分钟无活动 | 15分钟 | ✅ 是 | 所有 Engine 完成或异常 |
| **手动停止** | 外部调用 | 最多5秒 | ❌ 否 | 用户主动中断 |

#### 完整生命周期

```
┌─────────────────────────────────────────────────────────┐
│  1. 启动阶段                                             │
│  - 用户提交查询                                          │
│  - 三个 Engine 同时启动                                  │
│  - ForumEngine Monitor 启动                             │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  2. 等待阶段（is_searching = False）                     │
│  - Monitor 每秒检查日志                                  │
│  - 等待检测到 FirstSummaryNode                           │
└────────────────────┬────────────────────────────────────┘
                     ↓
              检测到 FirstSummaryNode
                     ↓
┌─────────────────────────────────────────────────────────┐
│  3. 活跃阶段（is_searching = True）                      │
│  - 清空 forum.log，写入开始标记                          │
│  - 实时监控三个 Engine 的日志                            │
│  - 捕获 SummaryNode 输出                                │
│  - 累积 5 条发言触发 HOST                                │
│  - 循环迭代 2-3 轮                                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
              满足结束条件之一
                     ↓
┌─────────────────────────────────────────────────────────┐
│  4. 结束阶段                                             │
│  - 写入结束标记（条件1或2）                              │
│  - 重置所有状态变量                                      │
│  - 回到等待阶段，准备下次运行                            │
└─────────────────────────────────────────────────────────┘
```

#### 正常结束的实际案例

```
21:30:00  [SYSTEM] === ForumEngine 监控开始 - 2025-11-16 21:30:00 ===
21:35:00  [INSIGHT] ## 核心发现概述\n当前港股科技板块舆情...
21:40:00  [MEDIA] ## 多模态内容传播分析\n小米汽车相关视频...
21:45:00  [QUERY] ## 全球新闻动态追踪\n路透社报道显示...
21:50:00  [HOST] **一、事件梳理与时间线分析**\n综合三位专家...
...（多轮迭代，每个 Engine 完成 4-5 个段落）
22:15:00  [INSIGHT] ## 最终总结\n综合以上分析...（段落5，最后一个）
22:20:00  [MEDIA] ## 传播效果总结\n...（段落5，最后一个）
22:25:00  [QUERY] ## 全球视角总结\n...（段落5，最后一个）
22:30:00  【检测到 insight.log 缩短】
          ↓ InsightEngine 完成所有段落，开始生成最终报告
          ↓ 清空 insight.log，准备写入报告内容
22:30:01  [SYSTEM] === ForumEngine 论坛结束 - 2025-11-16 22:30:01 ===
          ↓ Monitor 检测到日志缩短，立即结束
          ↓ 重置状态，等待下次分析任务
```

#### 关键要点

1. **正常结束标志**：日志文件缩短是 Engine 完成工作的信号
2. **为什么会缩短**：Engine 完成段落分析后，会清空日志准备写入最终报告
3. **立即响应**：Monitor 每秒检查一次，检测到缩短后立即结束
4. **可重复运行**：结束后所有状态重置，可以立即开始新的分析任务
5. **异常保护**：15分钟超时机制防止 Monitor 永久运行

---

### 📋 核心数据流转

#### forum.log 文件格式

```
[时间戳] [发言者] 内容
```

**示例**：
```
[21:32:30] [SYSTEM] === ForumEngine 监控开始 - 2025-11-15 21:32:30 ===
[21:41:32] [INSIGHT] ## 核心发现概述\n当前港股科技板块舆情呈现显著分化...
[21:58:25] [MEDIA] ## 多模态内容传播分析\n小米汽车相关视频在抖音平台获得...
[22:01:17] [QUERY] ## 全球新闻动态追踪\n路透社报道显示，小米印度市场...
[22:05:30] [HOST] **一、事件梳理与时间线分析**\n综合三位专家的发言...
```

#### 监控触发机制

**monitor.py 核心逻辑**：

```python
# 每 1 秒检查一次日志文件
for app_name, log_file in monitored_logs.items():
    new_lines = read_new_lines(log_file, app_name)
    
    # 检测到 FirstSummaryNode 输出 → 开始监控
    if 'FirstSummaryNode' in line:
        is_searching = True
        clear_forum_log()  # 清空论坛，开始新会话
    
    # 提取 SummaryNode 的 JSON 输出
    captured_contents = process_lines_for_json(new_lines, app_name)
    
    # 写入 forum.log
    for content in captured_contents:
        write_to_forum_log(content, app_name.upper())
        agent_speeches_buffer.append(log_line)
        
        # 每 5 条发言触发主持人
        if len(agent_speeches_buffer) >= 5:
            _trigger_host_speech()
```

---

### 🎯 与 InsightEngine 的交互细节

#### InsightEngine 特点
- **数据源**：本地舆情数据库（7大社交媒体平台）
- **专长**：历史数据分析、情感分析、热度算法
- **工具**：search_topic_globally、search_topic_by_date、get_comments_for_topic 等

#### 交互流程

**步骤 1：InsightEngine 发布初始发现**

```python
# InsightEngine/nodes/summary_node.py - FirstSummaryNode
# 输出示例（写入 insight.log）
"""
## 核心发现概述
当前港股科技板块舆情呈现显著分化态势，小米集团1810.HK与阿里巴巴09988.HK
在2025年Q3财报周期形成鲜明对比...

## 详细数据分析
从量化舆情指标看，过去30天内小米相关讨论量达12.3万条，远超阿里的7.8万条...
"""
```

**Monitor 捕获并写入 forum.log**：
```
[21:41:32] [INSIGHT] ## 核心发现概述\n当前港股科技板块舆情呈现显著分化...
```

**步骤 2：主持人分析并提出引导**

```python
# 主持人输出示例
"""
**一、事件梳理与时间线分析**
综合三位专家的发言，我们发现：
1. InsightEngine 提供了详实的本地舆情数据（12.3万条讨论）
2. 但数据时间范围不明确，需要补充具体的时间段分析
3. 情感分析数据（正面42%、负面35%）很有价值，但缺少情感演变趋势

**四、问题引导与讨论方向**
建议 InsightEngine 深入探讨：
1. 负面舆情的具体来源和传播路径？
2. 不同平台（微博、知乎、B站）用户群体的观点差异？
3. 情感倾向在时间维度上的变化趋势（按周/按月）？
"""
```

**步骤 3：InsightEngine 读取主持人引导**

```python
# InsightEngine/nodes/summary_node.py - ReflectionSummaryNode
def run(self, input_data: Any, **kwargs) -> str:
    data = input_data.copy()
    
    # 【关键】从 forum.log 读取最新的 HOST 发言
    from utils.forum_reader import get_latest_host_speech
    
    host_speech = get_latest_host_speech()
    if host_speech:
        data['host_speech'] = host_speech
        logger.info(f"已读取HOST发言，长度: {len(host_speech)}字符")
    
    # 格式化 HOST 发言并添加到 Prompt 前面
    message = json.dumps(data, ensure_ascii=False)
    if 'host_speech' in data:
        formatted_host = format_host_speech_for_prompt(data['host_speech'])
        message = formatted_host + "\n" + message
    
    # LLM 会看到主持人的引导，并据此调整分析方向
    response = self.llm_client.invoke(SYSTEM_PROMPT_REFLECTION_SUMMARY, message)
```

**步骤 4：InsightEngine 调整搜索方向**

```python
# InsightEngine/nodes/search_node.py - ReflectionSearchNode

# 调整后的搜索策略
{
  "search_query": "小米su7 故障 刹车 异响 提车等了多久",
  "search_tool": "search_topic_on_platform",
  "reasoning": "根据主持人建议，需要补充负面舆情的具体来源。微博是消费者投诉的主要阵地。",
  "platform": "weibo",
  "start_date": "2025-10-15",
  "end_date": "2025-11-15",
  "enable_sentiment": true
}
```

**关键变化**：
- ✅ 从泛泛的"小米股票"改为具体的"小米su7 故障"
- ✅ 从全局搜索改为平台定向搜索（微博）
- ✅ 增加了时间范围（最近1个月）
- ✅ 启用情感分析以量化负面情绪

---

### 🌐 与 MediaEngine 的交互细节

#### MediaEngine 特点
- **数据源**：全网搜索（Bocha AI Search API）
- **专长**：多模态内容分析、视频图片传播
- **工具**：comprehensive_search、web_search_only、search_last_24_hours 等

#### 交互流程

**主持人引导 MediaEngine**：

```python
"""
**二、观点整合与对比分析**
- MEDIA 提供了视频传播数据（500万播放），但缺少具体的用户评论分析
- INSIGHT 的数据显示负面情绪占35%，但 MEDIA 的视频内容似乎偏正面
- 需要 MEDIA 深入分析视频评论区的真实舆情

**四、问题引导与讨论方向**
建议 MediaEngine：
1. 分析视频评论区的情感倾向，是否与 INSIGHT 的数据一致？
2. 对比官方内容与 UGC 内容的评论差异
3. 关注"翻车"、"避坑"等负面关键词的视频内容
"""
```

**MediaEngine 调整搜索策略**：

```python
# 调整后的搜索查询
{
  "search_query": "小米su7翻车 小米汽车避坑 提车后悔",
  "search_tool": "comprehensive_search",
  "reasoning": "根据主持人建议，需要平衡正面内容，搜索负面关键词以获取真实的用户吐槽。",
  "include_images": true,
  "include_videos": true
}
```

---

### 📰 与 QueryEngine 的交互细节

#### QueryEngine 特点
- **数据源**：全球新闻（Tavily API）
- **专长**：权威媒体报道、实时新闻
- **工具**：basic_search_news、deep_search_news、search_news_by_date 等

#### 交互流程

**主持人引导 QueryEngine**：

```python
"""
**二、观点整合与对比分析**
- QUERY 提供了权威媒体的负面报道（印度监管、盈利困境）
- 但 INSIGHT 和 MEDIA 的数据显示国内舆情偏正面
- 存在"国内外舆情分化"现象，需要深入分析原因

**四、问题引导与讨论方向**
建议 QueryEngine：
1. 搜索小米在其他海外市场（欧洲、东南亚）的新闻报道
2. 对比国内外媒体对小米汽车业务的评价差异
3. 关注分析师对小米股价的最新预测和目标价
"""
```

**QueryEngine 调整搜索方向**：

```python
# 调整后的搜索查询
{
  "search_query": "Xiaomi Europe market expansion electric vehicle analyst price target",
  "search_tool": "deep_search_news",
  "reasoning": "根据主持人建议，需要扩展海外市场分析。搜索欧洲市场的英文新闻。",
  "max_results": 10,
  "include_domains": ["reuters.com", "bloomberg.com", "ft.com"]
}
```

**关键变化**：
- ✅ 从"小米印度"扩展到"小米欧洲市场"
- ✅ 使用英文关键词搜索国际媒体
- ✅ 关注分析师观点和股价预测

---

### 🔄 反思迭代循环机制

#### 循环流程图

```
第1轮：初始搜索 → 首次总结 → 写入论坛
         ↓
      累积5条发言
         ↓
      主持人分析 → 提出引导 → 写入论坛
         ↓
第2轮：读取引导 → 调整搜索 → 反思总结 → 写入论坛
         ↓
      累积5条发言
         ↓
      主持人分析 → 深化引导 → 写入论坛
         ↓
第3轮：读取引导 → 精准搜索 → 最终总结 → 写入论坛
```

#### 每轮的变化对比

| 轮次 | InsightEngine | MediaEngine | QueryEngine |
|------|---------------|-------------|-------------|
| **第1轮** | 全局话题搜索 | 综合搜索 | 基础新闻搜索 |
| **第2轮** | 平台定向搜索 | 负面内容搜索 | 深度新闻分析 |
| **第3轮** | 评论深度挖掘 | 评论区情感分析 | 分析师观点汇总 |

#### 配置参数

```python
# config.py
MAX_REFLECTIONS = 2  # 反思次数（2次 = 3轮总结）
```

**建议配置**：
- **快速分析**：`MAX_REFLECTIONS = 1`（2轮，15-20分钟）
- **标准分析**：`MAX_REFLECTIONS = 2`（3轮，25-30分钟）
- **深度分析**：`MAX_REFLECTIONS = 3`（4轮，35-40分钟）

---

### 🎨 主持人引导策略详解

#### 四大引导维度

**1. 事件梳理与时间线分析**
- 识别关键事件、人物、时间节点
- 按时间顺序整理事件脉络
- 指出关键转折点和重要节点
- 发现时间线上的空白和矛盾

**2. 观点整合与对比分析**
- 综合三个 Agent 的视角和发现
- 指出不同数据源之间的共识与分歧
- 分析每个 Agent 的信息价值和互补性
- 发现事实错误或逻辑矛盾

**3. 深层次分析与趋势预测**
- 分析舆情的深层原因和影响因素
- 预测舆情发展趋势
- 指出可能的风险点和机遇
- 提出需要特别关注的方面

**4. 问题引导与讨论方向**
- 提出2-3个值得进一步探讨的关键问题
- 为后续研究提出具体建议和方向
- 引导各 Agent 关注特定的数据维度

---

### 💡 协同效果对比

#### 单一 Agent vs 协同模式

| 维度 | 单一 Agent | 协同模式 | 提升 |
|------|-----------|---------|------|
| **数据覆盖** | 单一数据源 | 三个数据源互补 | +200% |
| **视角多样性** | 单一视角 | 三个专业视角 | +300% |
| **分析深度** | 2-3层 | 5-6层（经过引导） | +150% |
| **发现盲点** | 容易遗漏 | 主持人指出盲点 | +200% |
| **错误纠正** | 难以自我纠正 | 主持人发现并纠正 | +100% |
| **报告质量** | 中等 | 高质量 | +60% |

---

### 🛠️ 技术实现要点

#### 1. 日志监控的关键技术

```python
# monitor.py - 核心技术点

# ① ERROR 块过滤机制
if log_level == 'ERROR':
    in_error_block[app_name] = True
    capturing_json[app_name] = False  # 停止 JSON 捕获
elif log_level == 'INFO':
    in_error_block[app_name] = False  # 退出 ERROR 块

# ② 多行 JSON 捕获（状态机模式）
if is_json_start_line(line):
    capturing_json[app_name] = True
    json_buffer[app_name] = [line]
elif capturing_json[app_name]:
    json_buffer[app_name].append(line)
    if is_json_end_line(line):
        content = extract_json_content(json_buffer[app_name])
        write_to_forum_log(content, app_name.upper())

# ③ 线程安全写入
with write_lock:
    with open(forum_log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] [{source}] {content}\n")
```

#### 2. 主持人触发策略

```python
# monitor.py - 当前实现

# 固定阈值触发
if len(agent_speeches_buffer) >= 5:
    _trigger_host_speech()

# 未来优化方向：
# - 动态阈值（根据发言质量）
# - 关键词触发（检测到"矛盾"、"错误"立即触发）
# - 时间触发（超过N分钟无主持人发言则触发）
```

#### 3. Agent 读取的容错机制

```python
# 所有 Engine 的 summary_node.py

try:
    host_speech = get_latest_host_speech()
    if host_speech:
        data['host_speech'] = host_speech
except Exception as e:
    # 读取失败不影响主流程
    logger.exception(f"读取HOST发言失败: {str(e)}")
    # 继续执行，不抛出异常
```

---

### 📊 性能优化建议

#### 1. 模型选择策略

```bash
# 主持人：使用大参数模型（需要强大的综合分析能力）
FORUM_HOST_MODEL_NAME=qwen3-max  # 推荐

# 各 Agent：根据任务特点选择
INSIGHT_ENGINE_MODEL_NAME=kimi-k2-0905-preview  # 平衡速度与质量
MEDIA_ENGINE_MODEL_NAME=qwen3-max               # 多模态能力强
QUERY_ENGINE_MODEL_NAME=deepseek-chat           # 速度快
```

#### 2. 触发阈值调优

```python
# monitor.py - 根据场景调整

# 快速分析模式（20分钟内完成）
host_speech_threshold = 10  # 每10条发言触发一次
MAX_REFLECTIONS = 1         # 只反思1次

# 标准分析模式（30分钟）
host_speech_threshold = 5   # 每5条发言触发一次（当前默认）
MAX_REFLECTIONS = 2         # 反思2次

# 深度分析模式（45分钟）
host_speech_threshold = 3   # 每3条发言触发一次
MAX_REFLECTIONS = 3         # 反思3次
```

#### 3. 日志清理策略

```python
# 定期清理历史日志，避免文件过大

# 方案 1：每次运行前清空（当前实现）
clear_forum_log()  # monitor.py 中已实现

# 方案 2：保留最近 N 次运行
keep_recent_logs(n=10)

# 方案 3：按日期归档
archive_logs_by_date()
```

---

### 🎯 实际应用案例

#### 案例：分析"小米vs阿里巴巴投资价值"

**单一 Agent（InsightEngine）**：
- 数据范围：国内7大平台
- 分析维度：讨论量、情感倾向
- 耗时：15分钟
- 报告长度：5000字
- **问题**：缺少全网视角和国际新闻，视角单一

**协同模式（ForumEngine + 3 Engines）**：
- InsightEngine：本地社交媒体舆情（12.3万条讨论）
- MediaEngine：全网视频图片传播（500万播放）
- QueryEngine：全球新闻权威报道（路透社、彭博社）
- 主持人：整合观点、发现矛盾、引导深化
- 数据范围：国内外全覆盖
- 分析维度：10+维度（舆情、传播、新闻、财务、国际化等）
- 耗时：30分钟
- 报告长度：15000字
- **优势**：多维度、深层次、全覆盖，发现单一 Agent 遗漏的关键信息

**主持人的关键贡献**：
1. 发现 InsightEngine 和 MediaEngine 的数据矛盾（负面35% vs 正面视频）
2. 引导 QueryEngine 扩展海外市场分析（从印度到欧洲）
3. 促使 MediaEngine 关注视频评论区的真实舆情
4. 指出"国内外舆情分化"现象，深化分析

---

## 📚 参考资源

- 项目地址：https://github.com/666ghj/BettaFish
- 完整文档：[README.md](../README.md)
- AI网关对比：[AI_Gateway_Comparison.md](./AI_Gateway_Comparison.md)

---

**Forum Engine 让 AI 从"单打独斗"变成"团队协作"，这正是 BettaFish 的核心创新！**

---

文档维护：BettaFish 项目组 | 最后更新：2025-11-16
