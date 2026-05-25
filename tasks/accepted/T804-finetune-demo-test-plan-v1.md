# finetune-demo Test Plan v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计，准备 finetune-demo 实施前包。

---

# finetune-demo Test Plan v1

## 概述

本文档定义 finetune-demo 的测试计划，覆盖单元测试、集成测试、端到端测试。

---

## 测试分层

| 测试类型 | 覆盖范围 | Mock 程度 |
|---------|---------|----------|
| 单元测试 | Trainer、Adapter、Config | 完全 Mock 模型 |
| 集成测试 | Trainer + 模型加载 | 部分 Mock |
| 端到端测试 | 完整训练链路 | 无 Mock |

---

## 单元测试

### Trainer

#### LoRATrainer

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_init_creates_trainer` | 有效配置 | Trainer 实例 |
| `test_lora_config_validation` | 有效 lora_config | 通过 |
| `test_invalid_r_raises` | r <= 0 | 抛出 ValueError |
| `test_train_method_exists` | Trainer 实例 | 有 train 方法 |

#### QLoRATrainer

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_qlora_config_4bit` | load_in_4bit=True | 4bit 量化配置 |
| `test_bnb_config_validation` | 有效 bnb_config | 通过 |

### Adapter

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_save_adapter` | Mock trainer | adapter 文件创建 |
| `test_load_adapter` | adapter 目录 | 模型加载成功 |
| `test_get_adapter_path` | trainer | 返回路径字符串 |

### Config

| 测试用例 | 输入 | 预期输出 |
|---------|------|---------|
| `test_load_lora_config` | YAML 文件 | 正确解析 |
| `test_load_qlora_config` | YAML 文件 | 正确解析 |
| `test_default_values` | 空配置 | 使用默认值 |

---

## 集成测试

### Trainer + 模型加载

| 测试用例 | 输入 | Mock 方式 | 预期输出 |
|---------|------|----------|---------|
| `test_train_small_dataset` | 小数据集 | 使用 tiny model | Loss 下降 |
| `test_adapter_persistence` | 训练后保存 | Mock | 文件存在 |
| `test_load_trained_adapter` | adapter 目录 | Mock | 模型加载成功 |

---

## 端到端测试

### 完整训练链路

```bash
# 1. 准备数据集（小规模测试）
cat > /tmp/test_dataset.jsonl << 'EOF'
{"instruction": "What is 2+2?", "input": "", "output": "4"}
{"instruction": "What is 3+3?", "input": "", "output": "6"}
EOF

# 2. 运行 LoRA 训练（使用小模型）
finetune-demo train \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --method lora \
    --dataset /tmp/test_dataset.jsonl \
    --epochs 1 \
    --output /tmp/test_lora_output

# 3. 检查产物
ls -la /tmp/test_lora_output/
cat /tmp/test_lora_output/adapter_config.json

# 4. 保存 adapter
finetune-demo save \
    --checkpoint /tmp/test_lora_output \
    --output /tmp/test_adapter

# 5. 验证 adapter 可加载
python -c "
from peft import PeftModel, AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')
model = PeftModel.from_pretrained(model, '/tmp/test_adapter')
print('Adapter loaded successfully')
"
```

### 预期输出

| 步骤 | 预期结果 |
|------|---------|
| 训练完成 | Loss 从高到低 |
| adapter_config.json | 包含 lora_alpha, r 等 |
| Adapter 加载 | 无报错 |

---

## 测试工具建议

| 工具 | 用途 |
|------|------|
| `pytest` | 测试框架 |
| `pytest-asyncio` | 异步测试 |
| `pytest-cov` | 覆盖率 |
| `torch` | PyTorch 框架 |

---

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|----------|
| `trainer/` | 90% |
| `adapter/` | 85% |
| `config.py` | 95% |
| **总体** | **85%** |

---

## 测试数据管理

| 数据类型 | 存储位置 | 说明 |
|---------|---------|------|
| 测试数据集 | `tests/fixtures/` | 小规模 JSONL |
| Mock 模型响应 | `tests/fixtures/` | JSON 文件 |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- 测试命令可能因框架版本变化

Out of Scope Kept:
- 未写性能测试
