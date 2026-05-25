# finetune-demo lora_trainer.py Blueprint v1

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold（pyproject / sample-config catalog），产出 `lora_trainer.py` 蓝图。

---

# finetune-demo lora_trainer.py Blueprint v1

## 概述

本文档定义 `src/finetune_demo/trainer/lora_trainer.py` 的蓝图——LoRA/QLoRA 训练器，基于 PEFT 和 TRL SFTTrainer。

## `src/finetune_demo/trainer/lora_trainer.py` 模板

```python
# src/finetune_demo/trainer/lora_trainer.py
"""
LoRA and QLoRA trainer for finetune-demo.

Wraps PEFT + TRL SFTTrainer for easy training.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import torch
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoTokenizer, AutoModelForCausalLM


@dataclass
class TrainingConfig:
    """Training configuration dataclass."""
    method: str = "lora"
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"
    output_dir: str = "./models"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    warmup_steps: int = 100
    logging_steps: int = 10
    save_steps: int = 500
    max_seq_length: int = 512
    fp16: bool = True
    gradient_checkpointing: bool = True

    # LoRA params
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: list[str] = field(
        default_factory=lambda: ["q_proj", "v_proj"]
    )

    # QLoRA params
    load_in_4bit: bool = False
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_quant_type: str = "nf4"

    def validate(self) -> None:
        """Validate config parameters."""
        if self.method not in ("lora", "qlora"):
            raise ValueError(f"method must be 'lora' or 'qlora', got '{self.method}'")
        if self.method == "qlora" and not self.load_in_4bit:
            raise ValueError("load_in_4bit must be True for QLoRA")
        if self.lora_r <= 0:
            raise ValueError(f"lora_r must be positive, got {self.lora_r}")


class LoRATrainer:
    """
    LoRA/QLoRA trainer.

    Uses PEFT for LoRA config and TRL SFTTrainer for training loop.
    """

    def __init__(self, config: TrainingConfig | dict[str, Any]) -> None:
        """
        Args:
            config: TrainingConfig instance or dict.
        """
        if isinstance(config, dict):
            self.config = TrainingConfig(**config)
        else:
            self.config = config
        self.config.validate()
        self._model = None
        self._tokenizer = None

    def _build_peft_config(self) -> LoraConfig:
        """Build PEFT LoraConfig from self.config."""
        task_type = TaskType.CAUSAL_LM
        target_modules = self.config.lora_target_modules

        if isinstance(target_modules, str):
            target_modules = target_modules.split(",")

        return LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            lora_dropout=self.config.lora_dropout,
            target_modules=target_modules,
            bias="none",
            task_type=task_type,
        )

    def _setup_model(self) -> tuple[Any, Any]:
        """
        Load model and tokenizer, apply LoRA.

        Returns:
            (model, tokenizer)
        """
        cfg = self.config

        # [PLACEHOLDER] 真实实现：
        # from transformers import AutoTokenizer, AutoModelForCausalLM
        # from peft import get_peft_model, prepare_model_for_kbit_training
        #
        # tokenizer = AutoTokenizer.from_pretrained(
        #     cfg.model_name,
        #     trust_remote_code=True,
        # )
        # tokenizer.pad_token = tokenizer.eos_token
        #
        # load_in_4bit = cfg.load_in_4bit and cfg.method == "qlora"
        #
        # model = AutoModelForCausalLM.from_pretrained(
        #     cfg.model_name,
        #     trust_remote_code=True,
        #     torch_dtype=torch.float16 if not load_in_4bit else None,
        #     device_map="auto",
        #     load_in_4bit=load_in_4bit,
        # )
        #
        # if load_in_4bit:
        #     model = prepare_model_for_kbit_training(model)
        #
        # peft_config = self._build_peft_config()
        # model = get_peft_model(model, peft_config)
        # model.print_trainable_parameters()
        #
        # return model, tokenizer
        return None, None  # [PLACEHOLDER]

    def train(
        self,
        train_dataset: Any,
        eval_dataset: Any | None = None,
    ) -> None:
        """
        Run the training loop.

        Args:
            train_dataset: HuggingFace Dataset for training.
            eval_dataset: Optional HuggingFace Dataset for evaluation.
        """
        # [PLACEHOLDER] 真实实现：
        # from trl import SFTTrainer
        # from transformers import TrainingArguments
        #
        # model, tokenizer = self._setup_model()
        # self._model = model
        # self._tokenizer = tokenizer
        #
        # training_args = TrainingArguments(
        #     output_dir=self.config.output_dir,
        #     num_train_epochs=self.config.num_train_epochs,
        #     per_device_train_batch_size=self.config.per_device_train_batch_size,
        #     gradient_accumulation_steps=self.config.gradient_accumulation_steps,
        #     learning_rate=self.config.learning_rate,
        #     warmup_steps=self.config.warmup_steps,
        #     logging_steps=self.config.logging_steps,
        #     save_steps=self.config.save_steps,
        #     fp16=self.config.fp16,
        #     gradient_checkpointing=self.config.gradient_checkpointing,
        #     report_to=["tensorboard"],
        # )
        #
        # trainer = SFTTrainer(
        #     model=model,
        #     train_dataset=train_dataset,
        #     eval_dataset=eval_dataset,
        #     args=training_args,
        #     tokenizer=tokenizer,
        #     dataset_text_field="text",
        #     max_seq_length=self.config.max_seq_length,
        # )
        #
        # trainer.train()
        pass

    def save_adapter(self, output_dir: Path | str) -> None:
        """
        Save the trained LoRA adapter.

        Args:
            output_dir: Directory to save adapter files.
        """
        if self._model is None:
            raise RuntimeError("Model not trained yet. Call train() first.")
        # [PLACEHOLDER]
        # self._model.save_pretrained(output_dir)
        pass
```

## 显存需求参考

| 模型大小 | LoRA | QLoRA |
|---------|------|-------|
| 7B | ~16GB | ~5GB |
| 13B | ~28GB | ~10GB |
| 0.5B | ~4GB | ~2GB |

## LoRA adapter 产物结构

```
{output_dir}/
├── adapter_config.json    # PEFT 配置
├── adapter_model.safetensors  # adapter 权重
└── README.md
```

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://arxiv.org/abs/2305.14314 — QLoRA paper
