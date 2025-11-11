# DeepSeek vs 通义千问 价格对比分析

> BettaFish 项目 LLM 成本优化指南  
> 更新时间：2025-11-11

## 📋 目录

- [价格总览](#价格总览)
- [BettaFish 推荐配置](#bettafish-推荐配置)
- [成本计算示例](#成本计算示例)
- [推荐方案](#推荐方案)
- [总结建议](#总结建议)

---

## 价格总览

### DeepSeek 模型价格

| 模型名称 | 输入价格 | 输出价格 | 上下文 | 特点 |
|---------|---------|---------|--------|------|
| **deepseek-chat** | ¥1.0/M | ¥2.0/M | 64K | 通用对话，审核宽松 |
| **deepseek-reasoner** | ¥4.0/M | ¥16.0/M | 64K | 推理模型（含思考链） |

**注**：价格单位为 人民币/百万tokens

---

### 通义千问模型价格（中国大陆-北京）

#### 文本生成模型

| 模型 | 输入 | 输出 | 上下文 | 免费额度 | 特点 |
|------|-----|------|--------|---------|------|
| **qwen-turbo** | ¥0.3/M | ¥0.6/M | 1M | 各100万 | 最便宜 |
| **qwen-plus** | ¥0.8/M | ¥2.0/M | 1M | 各100万 | 性价比高 |
| **qwen-max** | ¥2.4/M | ¥9.6/M | 32K | 各100万 | 能力最强 |
| **qwen-long** | ¥0.5/M | ¥2.0/M | 10M | 各100万 | 超长上下文 |

#### 多模态模型

| 模型 | 输入 | 输出 | 上下文 | 免费额度 | 特点 |
|------|-----|------|--------|---------|------|
| **qwen-vl-max** | ¥1.6/M | ¥4.0/M | 131K | 各100万 | 视觉-最强 |
| **qwen-vl-plus** | ¥0.8/M | ¥2.0/M | 131K | 各100万 | 视觉-均衡 |
| **qwen3-vl-flash** | ¥0.15/M | ¥1.5/M | 262K | 各100万 | 视觉-快速 |

**注**：免费额度有效期为开通后90天

---

## 核心对比

### 通用对话模型对比

| 维度 | DeepSeek-Chat | Qwen-Turbo | Qwen-Plus | Qwen-Max |
|------|--------------|-----------|-----------|----------|
| **输入价格** | ¥1.0/M | ¥0.3/M | ¥0.8/M | ¥2.4/M |
| **输出价格** | ¥2.0/M | ¥0.6/M | ¥2.0/M | ¥9.6/M |
| **上下文** | 64K | 1M | 1M | 32K |
| **免费额度** | ❌ | ✅ 各100万 | ✅ 各100万 | ✅ 各100万 |
| **内容审核** | ⚠️ 较宽松 | ⚠️⚠️ 严格 | ⚠️⚠️ 严格 | ⚠️⚠️⚠️ 非常严格 |
| **能力** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**结论**：
- **成本最优**：Qwen-Turbo（¥0.3/M）
- **性价比最高**：DeepSeek-Chat（能力强+无审核）
- **能力最强**：Qwen-Max（但审核严格）

---

## BettaFish 推荐配置

### 方案 A：成本优先（¥15-30/月）

```bash
# Query Engine - DeepSeek（避免审核）
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen3-VL-Flash（最便宜多模态）
MEDIA_ENGINE_MODEL_NAME=qwen3-vl-flash

# Insight Engine - DeepSeek
INSIGHT_ENGINE_MODEL_NAME=deepseek-chat

# Report Engine - Qwen-Plus
REPORT_ENGINE_MODEL_NAME=qwen-plus

# Forum Host - Qwen-Plus
FORUM_HOST_MODEL_NAME=qwen-plus

# Keyword Optimizer - Qwen-Turbo
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo
```

**优点**：成本最低，DeepSeek无审核  
**缺点**：Insight能力相对较弱

---

### 方案 B：性价比优先（¥30-60/月）⭐推荐

```bash
# Query Engine - DeepSeek
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen-VL-Plus
MEDIA_ENGINE_MODEL_NAME=qwen-vl-plus

# Insight Engine - Qwen-Plus
INSIGHT_ENGINE_MODEL_NAME=qwen-plus

# Report Engine - Qwen-Plus
REPORT_ENGINE_MODEL_NAME=qwen-plus

# Forum Host - Qwen-Plus
FORUM_HOST_MODEL_NAME=qwen-plus

# Keyword Optimizer - Qwen-Turbo
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo
```

**优点**：性价比最高，能力均衡  
**缺点**：Insight不是最强模型

---

### 方案 C：能力优先（¥80-150/月）

```bash
# Query Engine - DeepSeek（避免审核）
QUERY_ENGINE_MODEL_NAME=deepseek-chat

# Media Engine - Qwen-VL-Max
MEDIA_ENGINE_MODEL_NAME=qwen-vl-max

# Insight Engine - Qwen-Max
INSIGHT_ENGINE_MODEL_NAME=qwen-max

# Report Engine - Qwen-Max
REPORT_ENGINE_MODEL_NAME=qwen-max

# Forum Host - Qwen-Max
FORUM_HOST_MODEL_NAME=qwen-max

# Keyword Optimizer - Qwen-Turbo
KEYWORD_OPTIMIZER_MODEL_NAME=qwen-turbo
```

**优点**：能力最强，分析质量最高  
**缺点**：成本较高，Qwen-Max审核严格

---

## 成本计算示例

### 单次查询成本（方案B：性价比优先）

```
Query Engine (deepseek-chat):
  输入: 2000 tokens × ¥1.0/M = ¥0.002
  输出: 1000 tokens × ¥2.0/M = ¥0.002
  小计: ¥0.004

Media Engine (qwen-vl-plus):
  输入: 3000 tokens × ¥0.8/M = ¥0.0024
  输出: 1500 tokens × ¥2.0/M = ¥0.003
  小计: ¥0.0054

Insight Engine (qwen-plus):
  输入: 5000 tokens × ¥0.8/M = ¥0.004
  输出: 2000 tokens × ¥2.0/M = ¥0.004
  小计: ¥0.008

Forum Host (qwen-plus):
  输入: 10000 tokens × ¥0.8/M = ¥0.008
  输出: 3000 tokens × ¥2.0/M = ¥0.006
  小计: ¥0.014

Report Engine (qwen-plus):
  输入: 15000 tokens × ¥0.8/M = ¥0.012
  输出: 5000 tokens × ¥2.0/M = ¥0.01
  小计: ¥0.022

总成本: ¥0.0534 ≈ ¥0.05/次
```

**月成本估算**（每天10次）：
- 日成本：¥0.05 × 10 = ¥0.5
- 月成本：¥0.5 × 30 = **¥15/月**

**加上免费额度**：前90天基本免费！

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

#### 1. Query Engine 必须避免审核

**推荐**：DeepSeek-Chat 或国际模型（OpenAI/Claude）

**原因**：
- Query Engine搜索外部新闻，易触发审核
- DeepSeek审核宽松
- 国际模型基本无审核

---

#### 2. 充分利用免费额度

**策略**：
- 前90天优先使用Qwen-Plus、Qwen-VL-Plus
- 总价值¥50-100，足够2-3个月使用
- 免费期结束后再考虑降级

---

#### 3. 按Agent特点选择模型

| Agent | 推荐 | 原因 |
|-------|------|------|
| **Query Engine** | DeepSeek | 避免审核 |
| **Media Engine** | Qwen-VL-Plus | 多模态性价比高 |
| **Insight Engine** | Qwen-Plus/Max | 需要强分析能力 |
| **Report Engine** | Qwen-Plus | 综合报告 |
| **Forum Host** | Qwen-Plus | 中文理解强 |
| **Keyword Optimizer** | Qwen-Turbo | 轻量任务 |

---

#### 4. 成本对比总结

| 方案 | 月成本 | 能力 | 审核 | 适用 |
|------|-------|------|------|------|
| **成本优先** | ¥15-30 | ⭐⭐⭐ | 宽松 | 学习测试 |
| **性价比优先** | ¥30-60 | ⭐⭐⭐⭐ | 宽松 | 日常使用⭐ |
| **能力优先** | ¥80-150 | ⭐⭐⭐⭐⭐ | 严格 | 企业项目 |

---

### 最终推荐

**个人/学习**：方案A（成本优先）  
**中小项目**：方案B（性价比优先）⭐  
**企业/高质量**：方案C（能力优先）  
**敏感话题**：使用国际模型（OpenAI/Claude）

---

## 参考链接

- DeepSeek定价：https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- 通义千问定价：https://help.aliyun.com/zh/model-studio/getting-started/models
- BettaFish项目：https://github.com/666ghj/BettaFish

---

**文档维护**：BettaFish 项目组 | 更新：2025-11-11
