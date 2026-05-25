# finetune-demo Risk Checklist v1

## Task ID: T1204
## Title: finetune-demo Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo Risk & Blocker Checklist

本文档定义 finetune-demo 实现过程中的风险点与阻塞检查项。

## P0 阻塞风险

| Risk | 描述 | 缓解方案 |
|---|---|---|
| **GPU 显存不足** | QLoRA 需要足够显存加载 base model | P0 阶段用 `Qwen2.5-0.5B-Instruct`，确保 GPU >= 16GB |
| **bitsandbytes 安装失败** | QLoRA 依赖 `bitsandbytes` | `pip install bitsandbytes`，确认 import 成功 |
| **PEFT 版本不兼容** | `PeftModel.merge_and_unload()` API 变化 | 锁定 `peft>=0.7,<0.8` |

---

## P1 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **trl 版本变化** | `SFTTrainer` 参数 API 变化 | `python -c "from trl import SFTTrainer"` 失败 | 查看 trl 文档，对齐版本 |
| **JSONL 格式不一致** | 不同来源 JSONL 字段名不同（messages vs instruction） | F03/F04 失败 | 统一使用 `messages` 格式，alpaca 格式做兼容 |
| **model_name_or_path 不存在** | HuggingFace 下载慢或模型不存在 | 直接测 `Qwen2.5-0.5B-Instruct`（国内可访问） | 从 Qwen2.5-0.5B-Instruct 开始 |
| **adapter merge 路径错误** | checkpoint 目录结构与预期不符 | F09 失败 | 先 `ls outputs/qlora_qwen_05b/checkpoint-3/` 确认结构 |

---

## P2 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **LoRA rank 选择不当** | `lora_r=16` 对小模型效果差 | 观察 loss 收敛曲线 | 使用 `lora_r=64`（T1104 fixture 默认） |
| **checkpoint 保存频率** | `save_steps=100` 在小数据集上永远不触发 | F08 失败 | 训练时加 `--save-steps 1` 或 `--save-steps 3` |
| **merge 后模型无法加载** | merge 产物格式问题 | merge 后 `AutoModelForCausalLM.from_pretrained(output)` | 先用 `merge_and_unload().save_pretrained()` |

---

## P3 风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **dataset text_field 不匹配** | `dataset_text_field="text"` 但数据没有 text 字段 | SFTTrainer 报错 | 使用 `formatting_func` 或 `dataset_text_field="messages"` |
| **max_seq_length 截断** | 过长序列被截断影响质量 | 观察训练日志 | 设置 `max_seq_length=512`（MVP 默认） |

---

## 测试阶段风险

| Risk | 描述 | 检测方式 | 缓解 |
|---|---|---|---|
| **mock trainer 依赖 GPU** | P2 mock 测试仍然尝试加载模型 | `pytest tests/test_trainer.py` 报错 | P2 用纯 mock，不 import transformers |
| **pytest-asyncio 冲突** | trainer 是普通函数不是 async | `pytest tests/` 无需 asyncio | 不需要 pytest-asyncio |

---

## Blocker Checklist

- [ ] Python ≥ 3.10
- [ ] GPU ≥ 16GB 可用（或使用 QLoRA + 0.5B 模型）
- [ ] `peft>=0.7,<0.8` 已安装：`python -c "import peft; print(peft.__version__)"`
- [ ] `trl>=0.7,<0.9` 已安装：`python -c "from trl import SFTTrainer; print('OK')"`
- [ ] `bitsandbytes` 已安装：`python -c "import bitsandbytes; print('OK')"`
- [ ] `datasets>=3.0` 已安装：`python -c "from datasets import load_dataset; print('OK')"`
- [ ] `pyproject.toml` 依赖已安装：`pip install -e finetune-demo`

---

Sources:
- T304: finetune-demo MVP design
- T703: finetune training map v3 (QLoRA decision)
- T1104: finetune fixture manifest (LoRA/QLoRA configs, adapter artifacts)

Risk of Staleness:
- PEFT/TRL API stable; bitsandbytes Windows compatibility is the main known issue
