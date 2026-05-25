# eval-module Validation Checklist v1 (Revised)

## Task ID: T813
## Task Title: eval-module Validation Checklist Tighten
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803-review.md，修复 shell 命令可执行性问题。

---

# eval-module Validation Checklist v1 (Revised)

## 概述

本文档定义 eval-module 的验收清单，供 Codex 执行后快速验证。

---

## 验收清单总览

| 类别 | 检查项数 | 必须项 |
|------|---------|-------|
| Runner | 4 | 4 |
| Dataset | 3 | 3 |
| Result Store | 3 | 3 |
| Comparator | 2 | 2 |
| CLI | 3 | 3 |
| **合计** | **15** | **15** |

---

## Runner 验收

- [ ] `LmEvalRunner` 可实例化
- [ ] `run("mmlu")` 返回 EvalResult
- [ ] `list_tasks()` 返回非空列表
- [ ] 无效 task 抛出 ValueError

---

## Dataset 验收

- [ ] MMLU 数据集可下载
- [ ] GSM8K 数据集可下载
- [ ] 指定 num_fewshot 生效

---

## Result Store 验收

- [ ] `save()` 保存 JSON 成功
- [ ] `load()` 加载 JSON 成功
- [ ] 加载不存在的文件抛出 FileNotFoundError

---

## Comparator 验收

- [ ] `compare()` 返回 diff
- [ ] diff 计算正确

---

## CLI 验收

- [ ] `eval-module run --help` 可执行
- [ ] `eval-module compare --help` 可执行
- [ ] 命令参数正确解析

---

## 快速验证命令

### 完整评测验证

```bash
# 1. 确保 inference-service 运行
curl http://localhost:8000/health

# 2. 安装 lm-eval（如未安装）
pip install "lm-eval[vllm]>=0.4.0"

# 3. 运行 MMLU 评测（少量样本）
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu \
    --num_fewshot 5 \
    --limit 10

# 4. 运行完整 MMLU 评测
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks mmlu \
    --num_fewshot 5

# 5. 运行 GSM8K 评测
lm_eval \
    --model vllm \
    --model_args "base_url=http://localhost:8000/v1,pretrained=Qwen/Qwen2.5-0.5B-Instruct" \
    --tasks gsm8k \
    --num_fewshot 5
```

### 预期输出

| 步骤 | 预期结果 |
|------|---------|
| MMLU | `{"mmlu": {"acc": 0.XX}}` |
| GSM8K | `{"gsm8k": {"acc": 0.XX}}` |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval 命令可能因版本更新变化

Out of Scope Kept:
- 未写自动化验收脚本
