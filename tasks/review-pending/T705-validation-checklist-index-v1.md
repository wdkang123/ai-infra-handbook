# Validation Checklist Index v1

## Task ID: T705
## Task Title: Execution Decomposition Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
把后续实施拆成若干工作流，便于 Codex 继续分发。

---

# Validation Checklist Index v1

## 概述

本文档为每个模块提供验收清单索引，便于 Codex 执行后快速验证。

---

## 清单总览

| 模块 | 清单项数 | 关键清单 |
|------|---------|---------|
| inference-service | 5 | 服务启动 / API 调用 / 健康检查 / metrics / 模型加载 |
| ai-gateway | 4 | 路由 / 鉴权 / 限流 / 端到端 |
| eval-module | 5 | lm-eval / MMLU / GSM8K / 持久化 / 对比 |
| finetune-demo | 4 | LoRA 训练 / 保存加载 / 串联验证 / QLoRA（可选） |
| 基础设施 | 3 | 仓库 / CI / 文档 |

---

## inference-service 验收清单

### vLLM 服务启动
- [ ] `vllm serve` 命令可执行
- [ ] 模型加载无报错
- [ ] 服务监听端口可访问

### OpenAI 兼容 API
- [ ] POST /v1/chat/completions 可调用
- [ ] 返回格式符合 OpenAI 规范
- [ ] 流式输出（可选）正常

### 健康检查
- [ ] GET /health 返回 200
- [ ] 响应包含服务状态

### Prometheus metrics
- [ ] GET /metrics 返回 Prometheus 格式
- [ ] 包含请求数、延迟、GPU 指标

### 模型加载
- [ ] Base model 可加载
- [ ] LoRA adapter 可动态加载
- [ ] 推理结果正常返回

---

## ai-gateway 验收清单

### 路由功能
- [ ] 请求可路由到 inference-service
- [ ] 路由路径正确
- [ ] 错误响应正确代理

### 鉴权中间件
- [ ] 有效 Token 可通过
- [ ] 无效 Token 返回 401
- [ ] Token 解析正确

### 限流中间件
- [ ] QPS 限制生效
- [ ] 超限返回 429
- [ ] 配置可调整

### 端到端串联
- [ ] 请求从 gateway → inference 全链路可跑
- [ ] 响应格式正确
- [ ] 延迟在可接受范围

---

## eval-module 验收清单

### lm-eval 集成
- [ ] lm-eval 命令可执行
- [ ] 评测任务可配置
- [ ] 结果格式正确

### MMLU benchmark
- [ ] MMLU 数据集可下载
- [ ] 评测分数正常返回（0-100）
- [ ] 结果可复现

### GSM8K benchmark
- [ ] GSM8K 数据集可下载
- [ ] 评测分数正常返回（0-100）
- [ ] 结果可复现

### 结果持久化
- [ ] 评测结果保存为 JSON
- [ ] 文件路径可配置
- [ ] 历史结果不覆盖

### 历史结果对比
- [ ] 可加载两个历史结果
- [ ] 对比视图正确显示
- [ ] 差异可量化

---

## finetune-demo 验收清单

### LoRA 训练
- [ ] 训练任务可启动
- [ ] Loss 下降正常
- [ ] Adapter 生成成功

### Adapter 保存/加载
- [ ] Adapter 持久化到文件
- [ ] 可重新加载
- [ ] 加载后推理结果一致

### 训练+评测串联
- [ ] 微调后模型可评测
- [ ] MMLU/GSM8K 分数返回
- [ ] 全流程可复现

### QLoRA（可选）
- [ ] 4-bit 量化训练可启动
- [ ] 显存占用降低可验证
- [ ] 训练结果质量可接受

---

## 基础设施验收清单

### 仓库骨架
- [ ] 目录结构符合设计
- [ ] 必要配置文件存在
- [ ] Git 仓库初始化

### CI 基础
- [ ] lint 检查可运行
- [ ] 单元测试可运行
- [ ] CI 配置正确

### 文档
- [ ] README.md 存在
- [ ] 模块文档结构清晰
- [ ] 接口文档存在

---

## 快速验证命令

### inference-service
```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/metrics
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"hello"}]}'
```

### ai-gateway
```bash
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{"model":"default","messages":[{"role":"user","content":"hello"}]}'
```

### eval-module
```bash
lm_eval --model vllm --tasks mmlu --model_args pretrained=model/path
lm_eval --model vllm --tasks gsm8k --model_args pretrained=model/path
```

### finetune-demo
```bash
python train.py --method lora --rank 8 --alpha 16
python train.py --method qlora --rank 8 --alpha 16 --load_in_4bit
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 验证命令可能因版本更新变化

Out of Scope Kept:
- 未写自动化测试脚本
- 未写详细错误排查指南
