# Integration Test Matrix v1

## Task ID: T805
## Task Title: Cross-Project Integration Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801-T804 validation checklist，准备跨项目集成测试矩阵。

---

# Integration Test Matrix v1

## 概述

本文档定义四个核心模块之间的集成测试矩阵，覆盖模块两两之间的集成验证。

---

## 集成测试矩阵

| 测试 ID | 上游模块 | 下游模块 | 测试场景 | 验证内容 | 优先级 |
|--------|----------|----------|---------|---------|--------|
| IT-01 | ai-gateway | inference-service | 请求透传 | 推理请求正确转发和响应 | P0 |
| IT-02 | ai-gateway | inference-service | 多后端路由 | 不同 model 路由到不同后端 | P1 |
| IT-03 | ai-gateway | inference-service | Fallback | 后端故障时切换 | P1 |
| IT-04 | eval-module | inference-service | lm-eval backend | benchmark 正常执行 | P0 |
| IT-05 | eval-module | inference-service | Token 计量 | usage 字段正确 | P0 |
| IT-06 | finetune-demo | inference-service | Adapter 加载 | 微调后模型推理 | P0 |
| IT-07 | finetune-demo | eval-module | 训练+评测串联 | 微调效果可评测 | P0 |
| IT-08 | ai-gateway | eval-module | 代理到 backend | eval 请求透传 | P1 |
| IT-09 | ai-gateway | finetune-demo | 代理到 backend | 微调请求透传 | P1 |
| IT-10 | eval-module | finetune-demo | 评测微调模型 | 加载微调 adapter 评测 | P1 |

---

## IT-01：ai-gateway → inference-service 请求透传

### 测试步骤

```bash
# 1. 启动 inference-service
inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 启动 ai-gateway
ai-gateway serve --port 8080 &

# 3. 通过 gateway 请求
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-test-key" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"Hello"}]}'
```

### 验证内容

- [ ] 请求成功返回
- [ ] 响应格式与直接调用 inference-service 一致
- [ ] 延迟在可接受范围

---

## IT-04：eval-module → inference-service lm-eval backend

### 测试步骤

```bash
# 1. 启动 inference-service
inference-service serve --engine vllm --model Qwen/Qwen2.5-0.5B-Instruct &

# 2. 运行 MMLU 评测
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu \
    --limit 10
```

### 验证内容

- [ ] 评测成功完成
- [ ] accuracy 分数正常返回
- [ ] usage 字段正确

---

## IT-06：finetune-demo → inference-service Adapter 加载

### 测试步骤

```bash
# 1. 训练 LoRA adapter（参考 T804）

# 2. 加载 adapter 到 inference-service
# vLLM 加载 adapter（如果有支持）
# 或使用 PEFT 加载后重新启动服务

# 3. 推理请求
curl -X POST http://localhost:8000/v1/chat/completions \
  -d '{"model":"Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Hello"}]}'
```

### 验证内容

- [ ] 微调后模型推理正常
- [ ] 推理结果与 base model 有差异（验证 adapter 生效）

---

## IT-07：finetune-demo → eval-module 训练+评测串联

### 测试步骤

```bash
# 1. 微调训练
finetune-demo train --method lora --model Qwen/Qwen2.5-0.5B-Instruct \
    --dataset /data/train.jsonl --epochs 1 --output /tmp/lora

# 2. 保存 adapter
finetune-demo save --checkpoint /tmp/lora --output /tmp/adapter

# 3. 加载到 inference-service（重启服务加载 adapter）

# 4. 运行评测
lm_eval --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu
```

### 验证内容

- [ ] 训练完成，adapter 产出
- [ ] 评测可运行
- [ ] 评测结果与 base model 可对比

---

## 优先级说明

| 优先级 | 说明 | 必须验证 |
|--------|------|---------|
| P0 | MVP 必须 | 是 |
| P1 | 增强功能 | 否 |

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- 集成测试可能因版本更新需要调整

Out of Scope Kept:
- 未写完整自动化集成测试
