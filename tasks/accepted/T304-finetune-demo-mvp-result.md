Task ID: T304
Title: finetune-demo MVP 目录与边界设计
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T173、T174，定义 finetune-demo MVP 的边界和目录结构，聚焦 LoRA/QLoRA/Unsloth 路径。

Result:

## 一、定位说明

**finetune-demo** 是 AI Infra 项目中负责**模型微调演示**的模块。它的核心职责：

- 提供 LoRA/QLoRA 微调的最小可运行流程
- 支持使用 Unsloth 加速的微调演示
- 产出可用于 inference-service 部署的微调模型（adapter权重）

**finetune-demo 不做的事**：
- 完整训练平台（全参数微调、分布式训练）
- 模型预训练
- 多节点 GPU 集群管理

## 二、目录结构（最小骨架）

```
finetune-demo/
├── README.md                      # 模块说明、快速启动
├── pyproject.toml                 # Python 依赖定义
├── scripts/
│   ├── train_lora.py            # LoRA 微调脚本
│   ├── train_qwen_lora.py       # Qwen 模型 LoRA 微调示例
│   └── export_adapter.py         # 导出 adapter 权重
├── configs/
│   └── lora_config_example.yaml  # LoRA 配置示例
├── data/
│   └── example_dataset.json      # 示例数据集格式
├── models/                       # 微调产物（adapter权重，不上传）
│   └── .gitkeep
└── tests/
    └── test_train.py             # 基本训练逻辑测试
```

## 三、核心接口（提案接口）

**注意**：以下接口为提案接口，不是仓库现有实现。

### Python API（提案）

```python
from finetune_demo import LoRATrainer

# 提案接口：创建 LoRA 微调训练器
trainer = LoRATrainer(
    model="Qwen/Qwen2.5-7B-Instruct",
    method="lora",  # or "qwen"
    output_dir="./models/qwen-lora"
)

# 提案接口：启动微调
trainer.train(
    dataset="path/to/dataset.jsonl",
    epochs=3,
    batch_size=4,
    learning_rate=2e-4
)

# 提案接口：导出 adapter
trainer.export_adapter()
```

### CLI 接口（提案）

```bash
# 提案接口：运行 LoRA 微调
finetune-demo train \
    --model Qwen/Qwen2.5-7B-Instruct \
    --method lora \
    --dataset data/example_dataset.jsonl \
    --epochs 3 \
    --output ./models/qwen-lora

# 提案接口：使用 Unsloth 加速（提案）
finetune-demo train \
    --model Qwen/Qwen2.5-7B-Instruct \
    --method unsloth \
    --dataset data/example_dataset.jsonl \
    --epochs 3 \
    --output ./models/qwen-lora
```

## 四、依赖关系

```
finetune-demo（本案）
    ↓
├── Hugging Face PEFT（LoRA/QLoRA 接口）
├── Unsloth（训练加速，可选）
├── TRL（Hugging Face 训练框架，SFT/DPO）
├── vLLM（推理服务，微调后部署）
└── inference-service（部署微调产物）
```

- **下游**：微调产出的 adapter 权重由 inference-service 加载部署
- **平行**：使用 Unsloth 加速时，底层调用 PEFT + Unsloth kernel

## 五、与 inference-service 的交接边界

```
finetune-demo                    inference-service
     |                                    |
     |-- 微调训练（PEFT/Unsloth）          |
     |-- 导出 adapter 权重                 |
     |                                    |-- 加载 adapter（PEFT）
     |                                    |-- 启动推理服务
```

微调产物（adapter权重）由 finetune-demo 导出，通过 inference-service 部署为推理 API。

## 六、最小可运行路径（提案）

**目标**：使用 Unsloth 加速的 LoRA 微调，训练一个 Qwen 小模型的 adapter，并在本地验证。

**注意**：以下为提案接口，不是仓库现有实现。

```bash
# 提案接口：安装（实际不存在 pip install finetune-demo）
# pip install finetune-demo[unsloth]

# 1. 准备数据集（JSONL 格式）
# {"instruction": "...", "input": "...", "output": "..."}

# 2. 提案接口：运行 LoRA 微调（使用 Unsloth）
# finetune-demo train \
#     --model Qwen/Qwen2.5-3B-Instruct \
#     --method unsloth \
#     --dataset data/example_dataset.jsonl \
#     --epochs 3 \
#     --output ./models/qwen-lora-3b

# 3. 提案接口：导出 adapter
# finetune-demo export \
#     --checkpoint ./models/qwen-lora-3b \
#     --output ./models/qwen-lora-3b/adapter

# 4. 部署到 inference-service（由 inference-service 模块定义）
# inference-service serve \
#     --engine vllm \
#     --model Qwen/Qwen2.5-3B-Instruct \
#     --lora ./models/qwen-lora-3b/adapter \
#     --port 8000
```

实际可参考 Unsloth 官方 Notebooks：
来源：https://github.com/unslothai/notebooks

## 七、微调方法说明

```python
# 提案：LoRA 配置
LoraConfig = {
    "r": 8,              # rank
    "lora_alpha": 16,    # scaling factor
    "target_modules": ["q_proj", "v_proj"],
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM"
}

# 提案：QLoRA 配置（在 LoRA 基础上加量化）
QLoRAConfig = {
    **LoraConfig,
    "quantization_config": {
        "load_in_4bit": True,
        "bnb_4bit_compute_dtype": "float16"
    }
}
```

Sources:
1. https://github.com/huggingface/peft — PEFT（LoRA/QLoRA 接口）
2. https://github.com/unslothai/unsloth — Unsloth（训练加速）
3. https://github.com/huggingface/trl — TRL（SFT/DPO 训练器）
4. https://github.com/unslothai/notebooks — Unsloth Notebooks（参考训练流程）
5. https://arxiv.org/abs/2305.14314 — QLoRA 论文

Risk of Staleness:
- PEFT 和 Unsloth 版本更新快，API 以实际安装版本为准
- QLoRA 配置参数可能随版本变化

Out of Scope Kept:
- 未写完整训练平台
- 未写多节点分布式训练
- 未写全参数微调
