# 各个模型价格说明URL
1. kimi
https://platform.moonshot.cn/docs/pricing/chat#%E8%AE%A1%E8%B4%B9%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5

2. deepseek
https://api-docs.deepseek.com/zh-cn/quick_start/pricing

3. qwen
https://help.aliyun.com/zh/model-studio/model-pricing?spm=a2c4g.11186623.help-menu-2400256.d_0_0_3.bdd429da8xmWhz&scm=20140722.H_2987148._.OR_help-T_cn~zh-V_1


# Kimi vs DeepSeek vs 通义千问 价格对比分析

> BettaFish 项目 LLM 成本优化指南  
> 更新时间：2025-11-14  
> ⚠️ **重要更新**：
> - Kimi K2 于2025年4月7日大幅降价
> - DeepSeek 于2025年2月9日结束优惠期，价格上调
> - 通义千问 Qwen3 系列全面升级，采用阶梯定价

## 📋 目录

- [价格总览](#价格总览)
- [BettaFish 推荐配置](#bettafish-推荐配置)
- [成本计算示例](#成本计算示例)
- [推荐方案](#推荐方案)
- [总结建议](#总结建议)

---

## ⚠️ 价格变更重要说明

### DeepSeek 价格调整历史

**调整前（2024年优惠期）**：
- deepseek-chat: ¥1.0/M 输入, ¥2.0/M 输出

**2025年2月调整**：
- deepseek-chat: ¥2.0/M 输入, ¥8.0/M 输出

**当前价格（2025年11月）**：
- deepseek-chat: ¥0.2/M 输入（缓存命中）, ¥2.0/M 输入（缓存未命中）, ¥3.0/M 输出

**影响**：
- 相比2月价格，输出价格**下降62.5%**（从¥8降至¥3）
- 支持缓存后，输入成本可降低90%
- 总体成本相比2月**大幅下降**

**参考资料**：
- [DeepSeek官方定价页面](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)

---

## 价格总览

### 三家LLM提供商价格对比表（2025年11月）

#### Moonshot Kimi 模型价格

| 模型 | 计费单位 | 输入价格<br>（缓存命中） | 输入价格<br>（缓存未命中） | 输出价格 | 模型上下文长度 |
|------|---------|---------|---------|---------|----------|
| kimi-k2-0905-preview | 1M tokens | ¥1.00 | ¥4.00 | ¥16.00 | 262,144 tokens |
| kimi-k2-0711-preview | 1M tokens | ¥1.00 | ¥4.00 | ¥16.00 | 131,072 tokens |
| kimi-k2-turbo-preview | 1M tokens | ¥1.00 | ¥8.00 | ¥58.00 | 262,144 tokens |
| kimi-k2-thinking | 1M tokens | ¥1.00 | ¥4.00 | ¥16.00 | 262,144 tokens |
| kimi-k2-thinking-turbo | 1M tokens | ¥1.00 | ¥8.00 | ¥58.00 | 262,144 tokens |

**数据来源**：[Kimi官方定价](https://platform.moonshot.cn/docs/pricing/chat)  
**价格说明**：价格单位为人民币/百万tokens

---

#### DeepSeek 模型价格

| 模型 | 计费单位 | 输入价格<br>（缓存命中） | 输入价格<br>（缓存未命中） | 输出价格 | 模型上下文长度 |
|------|---------|---------|---------|---------|----------|
| deepseek-chat | 1M tokens | ¥0.2 | ¥2.0 | ¥3.0 | 128K tokens |
| deepseek-reasoner | 1M tokens | ¥0.2 | ¥2.0 | ¥3.0 | 128K tokens |

**数据来源**：[DeepSeek官方定价](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)  
**价格说明**：价格单位为人民币/百万tokens

---

#### 通义千问 Qwen 模型价格（中国大陆-北京）

**文本生成模型**

| 模型 | 计费单位 | 输入价格 | 输出价格 | 模型上下文长度 | 免费额度 |
|------|---------|---------|---------|----------|----------|
| qwen-turbo | 1M tokens | ¥0.3 | ¥0.6 | 1M tokens | 各100万 |
| qwen-plus | 1M tokens | ¥0.8 | ¥2.0 | 1M tokens | 各100万 |
| qwen-max | 1M tokens | ¥2.4 | ¥9.6 | 32K tokens | 各100万 |
| qwen-long | 1M tokens | ¥0.5 | ¥2.0 | 10M tokens | 各100万 |
| qwen3-max | 1M tokens | ¥3.2 | ¥12.8 | 262K tokens | 各100万 |

**多模态模型**

| 模型 | 计费单位 | 输入价格 | 输出价格 | 模型上下文长度 | 免费额度 |
|------|---------|---------|---------|----------|----------|
| qwen-vl-max | 1M tokens | ¥1.6 | ¥4.0 | 131K tokens | 各100万 |
| qwen-vl-plus | 1M tokens | ¥0.8 | ¥2.0 | 131K tokens | 各100万 |
| qwen3-vl-flash | 1M tokens | ¥0.15 | ¥1.5 | 262K tokens | 各100万 |

**数据来源**：[通义千问官方定价](https://help.aliyun.com/zh/model-studio/model-pricing)  
**价格说明**：
- 价格单位为人民币/百万tokens（已从官方的“每千Token”转换）
- 免费额度有效期为开通后90天
- Qwen3系列支持阶梯定价，上表为最低档价格（0<Token≤32K）

---

## 核心对比

### 通用对话模型对比（2025年11月最新）

| 维度 | Kimi-K2 | DeepSeek-Chat | Qwen-Turbo | Qwen-Plus | Qwen-Max |
|------|---------|--------------|-----------|-----------|----------|
| **输入价格** | ¥1.05/M | ¥0.2/M（缓存）<br>¥2.0/M（普通） | ¥0.31/M | ¥0.81/M | ¥2.4/M |
| **输出价格** | ¥17.5/M | ¥3.0/M | ¥0.61/M | ¥2.0/M | ¥9.6/M |
| **上下文** | 128K | 128K | 1M | 1M | 32K |
| **免费额度** | ❌ | ❌ | ✅ 各100万 | ✅ 各100万 | ✅ 各100万 |
| **内容审核** | ⚠️ 宽松 | ⚠️ 较宽松 | ⚠️⚠️ 严格 | ⚠️⚠️ 严格 | ⚠️⚠️⚠️ 非常严格 |
| **能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **特色** | 1T参数 | 缓存优化 | 最便宜 | 均衡 | 最强 |

**结论**：
- **输入成本最优**：DeepSeek-Chat（¥0.2/M，缓存命中）
- **输出成本最优**：Qwen-Turbo（¥0.61/M）
- **性价比最高**：DeepSeek-Chat（缓存优化后）和 Qwen-Plus
- **审核最宽松**：Kimi-K2 和 DeepSeek-Chat
- **能力最强**：Kimi-K2（1T参数）和 Qwen-Max

---

## BettaFish 推荐配置

### 方案 A：极致成本优先（¥15-30/月）

```bash
# Query Engine - DeepSeek-Chat（审核宽松）
QUERY_ENGINE_API_KEY=your_deepseek_key
QUERY_ENGINE_BASE_URL=https://api.deepseek.com
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen-Turbo（最便宜）
MEDIA_ENGINE_API_KEY=your_qwen_key
MEDIA_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MEDIA_ENGINE_MODEL_NAME=qwen-turbo

# Insight Engine - Qwen-Turbo
INSIGHT_ENGINE_API_KEY=your_qwen_key
INSIGHT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
INSIGHT_ENGINE_MODEL_NAME=qwen-turbo

# Report Engine - Qwen-Plus
REPORT_ENGINE_API_KEY=your_qwen_key
REPORT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
REPORT_ENGINE_MODEL_NAME=qwen-plus

# Forum Host - Qwen-Plus
FORUM_HOST_API_KEY=your_qwen_key
FORUM_HOST_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
FORUM_HOST_MODEL_NAME=qwen-plus

# Keyword Optimizer - Qwen-Turbo
KEYWORD_OPTIMIZER_API_KEY=your_qwen_key
KEYWORD_OPTIMIZER_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo
```

**优点**：成本最低，充分利用通义千问免费额度  
**缺点**：Qwen审核较严格，能力相对较弱  
**月成本**：前90天几乎免费，之后约¥15-30/月

---

### 方案 B：性价比优先（¥20-50/月）⭐推荐

```bash
# Query Engine - DeepSeek-Chat（审核宽松）
QUERY_ENGINE_API_KEY=your_deepseek_key
QUERY_ENGINE_BASE_URL=https://api.deepseek.com
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen-Plus（能力强）
MEDIA_ENGINE_API_KEY=your_qwen_key
MEDIA_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MEDIA_ENGINE_MODEL_NAME=qwen-plus

# Insight Engine - Kimi-K2（1T参数，能力最强）
INSIGHT_ENGINE_API_KEY=your_kimi_key
INSIGHT_ENGINE_BASE_URL=https://api.moonshot.cn/v1
INSIGHT_ENGINE_MODEL_NAME=kimi-k2

# Report Engine - Qwen-Long（超长上下文）
REPORT_ENGINE_API_KEY=your_qwen_key
REPORT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
REPORT_ENGINE_MODEL_NAME=qwen-long

# Forum Host - Qwen-Plus
FORUM_HOST_API_KEY=your_qwen_key
FORUM_HOST_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
FORUM_HOST_MODEL_NAME=qwen-plus

# Keyword Optimizer - Qwen-Turbo
KEYWORD_OPTIMIZER_API_KEY=your_qwen_key
KEYWORD_OPTIMIZER_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo
```

**优点**：性价比最高，能力均衡，Insight使用最强模型  
**缺点**：Kimi输出成本较高（但输入便宜）  
**月成本**：约¥20-50/月（DeepSeek降价后）

---

### 方案 C：能力优先（¥60-120/月）

```bash
# Query Engine - DeepSeek-Chat（审核宽松）
QUERY_ENGINE_API_KEY=your_deepseek_key
QUERY_ENGINE_BASE_URL=https://api.deepseek.com
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen3-Max（最新旗舰）
MEDIA_ENGINE_API_KEY=your_qwen_key
MEDIA_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MEDIA_ENGINE_MODEL_NAME=qwen3-max

# Insight Engine - Kimi-K2-Thinking（推理能力最强）
INSIGHT_ENGINE_API_KEY=your_kimi_key
INSIGHT_ENGINE_BASE_URL=https://api.moonshot.cn/v1
INSIGHT_ENGINE_MODEL_NAME=kimi-k2-thinking

# Report Engine - Qwen3-Max（能力最强）
REPORT_ENGINE_API_KEY=your_qwen_key
REPORT_ENGINE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
REPORT_ENGINE_MODEL_NAME=qwen3-max

# Forum Host - Qwen-Max
FORUM_HOST_API_KEY=your_qwen_key
FORUM_HOST_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
FORUM_HOST_MODEL_NAME=qwen-max

# Keyword Optimizer - Qwen-Plus
KEYWORD_OPTIMIZER_API_KEY=your_qwen_key
KEYWORD_OPTIMIZER_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-plus
```

**优点**：能力最强，分析质量最高，使用最新模型  
**缺点**：成本较高，Qwen审核严格  
**月成本**：约¥60-120/月（DeepSeek降价后）

---

## 成本计算示例

### 单次查询成本（方案B：性价比优先）

```
Query Engine (deepseek-chat):
  输入: 2000 tokens × ¥2.0/M = ¥0.004
  输出: 1000 tokens × ¥3.0/M = ¥0.003
  小计: ¥0.007

Media Engine (qwen-plus):
  输入: 3000 tokens × ¥0.81/M = ¥0.0024
  输出: 1500 tokens × ¥2.0/M = ¥0.003
  小计: ¥0.0054

Insight Engine (kimi-k2):
  输入: 5000 tokens × ¥1.05/M = ¥0.0053
  输出: 2000 tokens × ¥17.5/M = ¥0.035
  小计: ¥0.0403

Forum Host (qwen-plus):
  输入: 10000 tokens × ¥0.81/M = ¥0.0081
  输出: 3000 tokens × ¥2.0/M = ¥0.006
  小计: ¥0.0141

Report Engine (qwen-long):
  输入: 15000 tokens × ¥0.5/M = ¥0.0075
  输出: 5000 tokens × ¥2.0/M = ¥0.01
  小计: ¥0.0175

总成本: ¥0.0793 ≈ ¥0.08/次
```

**月成本估算**（每天10次）：
- 日成本：¥0.08 × 10 = ¥0.8
- 月成本：¥0.8 × 30 = **¥24/月**

**注意**：
- DeepSeek输出成本大幅下降（从¥8降至¥3）
- Kimi输出成本较高，但输入便宜
- Qwen系列前90天有免赹额度
- 实际成本取决于输入输出比例

---

## 免费额度利用策略

### 通义千问免费额度（开通后90天）

每个模型：
- 输入：100万 tokens
- 输出：100万 tokens

**总价值估算**：
```
Qwen-Max: ¥2.4 + ¥9.6 = ¥12
Qwen-Plus: ¥0.8 + ¥2.0 = ¥2.8
Qwen-VL-Plus: ¥0.8 + ¥2.0 = ¥2.8
Qwen-Turbo: ¥0.3 + ¥0.6 = ¥0.9

总价值: ¥50-100
```

**使用策略**：
1. 优先使用有免费额度的模型
2. 90天内可免费测试和开发
3. 免费额度用完后再考虑降级

---

## 总结建议

### 核心建议

#### 1. 2025年11月最新价格变化

**重要变化**：
- ✅ **Kimi K2 大幅降价**：输入¥1.05/M，性价比大幅提升
- ✅ **DeepSeek 再次降价**：输出从¥8 → ¥3，缓存输入仅需¥0.2/M
- ✅ **Qwen3 系列升级**：新增qwen3-max，能力更强
- ✅ **Qwen 免费额度**：每个模型各100万tokens，90天有效期

---

#### 2. 按引擎特点选择模型（2025年11月推荐）

| Agent | 推荐模型 | 原因 | 月成本估算 |
|-------|---------|------|----------|
| **Query Engine** | DeepSeek-Chat | 审核宽松，成本极低 | ¥3-6 |
| **Media Engine** | Qwen-Plus | 性价比高，能力均衡 | ¥3-8 |
| **Insight Engine** | **DeepSeek-Chat** ⭐ | 缓存优化，成本极低 | ¥5-10 |
| **Report Engine** | Qwen-Long | 超长上下文，成本低 | ¥5-10 |
| **Forum Host** | Qwen-Plus | 中文理解强，性价比高 | ¥3-8 |
| **Keyword Optimizer** | Qwen-Turbo | 轻量任务，最便宜 | ¥1-3 |

**关键洞察**：
- **DeepSeek 再次降价后成为性价比之王**（缓存输入¥0.2/M，输出¥3/M）
- **Qwen系列适合大部分场景**（免费额度+性价比）
- **Kimi K2 适合高要求场景**（1T参数，能力最强）

---

#### 3. 成本对比总结（2025年11月）

| 方案 | 月成本 | 能力 | 审核 | 适用 | 核心优势 |
|------|-------|------|------|------|----------|
| **极致成本** | ¥10-25 | ⭐⭐⭐ | 宽松 | 学习测试 | DeepSeek缓存+Qwen免费 |
| **性价比优先** | ¥20-50 | ⭐⭐⭐⭐ | 宽松 | 日常使用⭐ | DeepSeek+Qwen黄金组合 |
| **能力优先** | ¥60-120 | ⭐⭐⭐⭐⭐ | 较严格 | 企业项目 | Kimi+Qwen3-Max顶配 |

---

#### 4. 充分利用免费额度策略

**Qwen免费额度（90天）**：
- 每个模型：输入100万 + 输出100万 tokens
- 总价值：约¥50-100
- **策略**：前90天优先使用Qwen系列，免费期结束后再调整

**Kimi无免费额度，但**：
- 输入价格极低（¥1.05/M）
- 适合输入多、输出少的场景（如Insight Engine）
- 支持上下文缓存，缓存命中更便宜

---

### 最终推荐（2025年11月）

**个人/学习**：方案A（极致成本）  
- DeepSeek缓存优化 + Qwen免费额度
- 前90天几乎免费，之后仅¥10-25/月

**中小项目**：方案B（性价比优先）⭐⭐⭐  
- **强烈推荐**：DeepSeek + Qwen组合
- DeepSeek缓存优化后性价比极高
- 月成本¥20-50，能力均衡

**企业/高质量**：方案C（能力优先）  
- 使用Kimi-K2-Thinking + Qwen3-Max
- 分析质量最高，1T参数模型
- 月成本¥60-120

**敏感话题**：
- Query Engine必须用DeepSeek或国际模型
- 其他引擎可用Kimi（审核相对宽松）

---

## 参考链接

- **Kimi定价**：https://platform.moonshot.cn/docs/pricing/chat
- **DeepSeek定价**：https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- **通义千问定价**：https://help.aliyun.com/zh/model-studio/models
- **BettaFish项目**：https://github.com/666ghj/BettaFish

---

## 价格变化时间线

| 日期 | 事件 | 影响 |
|------|------|------|
| 2024-08 | DeepSeek降价至¥0.1/¥2 | 极致性价比时代 |
| 2025-02-09 | DeepSeek结束优惠，涨至¥2/¥8 | 成本增加3-4倍 |
| 2025-02-26 | DeepSeek推出错峰优惠 | 夜间5折/2.5折 |
| 2025-11 | DeepSeek再次降价至¥0.2/¥3 | 输出降62.5%，缓存优化 |
| 2025-04-07 | Kimi K2大幅降价 | 降幅50-90% |
| 2025-07 | Qwen3系列发布 | 能力大幅提升 |
| 2025-11 | 当前状态 | DeepSeek性价比之王 |

---

**文档维护**：BettaFish 项目组 | 更新：2025-11-14
