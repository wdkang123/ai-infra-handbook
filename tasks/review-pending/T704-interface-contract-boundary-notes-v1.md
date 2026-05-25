Task ID: T704
Task Title: Cross-Project Deep-Research Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
重点解释哪些接口是提案、哪些是依赖外部工具、哪些只适合后续阶段。

Result:

# Interface Contract Boundary Notes v1

## 概述

本文档说明各模块接口的边界，哪些是提案级、哪些依赖外部工具、哪些只适合后续阶段。

---

## 接口分类

| 类别 | 说明 | 约束 |
|------|------|------|
| **提案接口** | 描述输入/输出，不等于已实现 | 需要 Codex 确认方向 |
| **外部依赖接口** | 依赖外部工具（vLLM/lm-eval 等） | 需要确认版本 |
| **后续阶段接口** | MVP 后才实现的功能 | MVP 阶段不实现 |

---

## inference-service 接口边界

### 提案接口

```python
class InferenceService:
    def chat_completions(self, model: str, messages: list) -> dict:
        """
        代理到 vLLM/SGLang
        返回: {"id": "...", "choices": [...], "usage": {...}}
        状态: 提案接口
        """
        pass
```

### 外部依赖

| 依赖 | 说明 | 版本建议 |
|------|------|---------|
| vLLM | 推理引擎 | v0.5.x 稳定版 |
| SGLang | 备选推理引擎 | 最新 release |
| OpenAI API 兼容 | 兼容 OpenAI 接口规范 | — |

### 后续阶段接口

| 接口 | 说明 |
|------|------|
| Triton IS 集成 | 多模型编排，MVP 后引入 |
| TensorRT-LLM backend | 高性能推理，MVP 后引入 |

来源：https://docs.vllm.ai/

---

## ai-gateway 接口边界

### 提案接口

```python
class AIGateway:
    def chat_completions(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        代理到 inference-service
        额外功能：鉴权、限流、计量
        状态: 提案接口
        """
        pass
```

### 外部依赖

| 依赖 | 说明 |
|------|------|
| inference-service | 上游推理服务 |

### 后续阶段接口

| 接口 | 说明 |
|------|------|
| 多后端负载均衡 | v2，后续引入 |
| 流量调度策略 | v2，后续引入 |

---

## eval-module 接口边界

### MVP 必须接口

```python
class EvalModule:
    def evaluate(self, model: str, tasks: list[str]) -> dict:
        """
        运行 benchmark 评测
        model: 模型名称或路径
        tasks: benchmark 任务列表，如 ["mmlu", "gsm8k"]
        返回: {"task": {"acc_norm": 0.xx, ...}}
        状态: MVP 必须
        """
        pass

    def load_results(self, path: str) -> dict:
        """
        加载历史评测结果
        状态: MVP 必须
        """
        pass

    def compare(self, result_a: dict, result_b: dict) -> dict:
        """
        对比两个评测结果
        状态: MVP 必须
        """
        pass
```

### 后续阶段接口

```python
    def report_to_langfuse(self, eval_result: dict) -> None:
        """
        评测结果上报 Langfuse
        状态: MVP 不包含，后续迭代
        """
        pass

    def judge_with_llm(self, prompt: str, response: str) -> dict:
        """
        LLM-as-Judge 主观评测
        状态: MVP 不包含，后续迭代（需要外部 Judge 模型）
        """
        pass
```

### 外部依赖

| 依赖 | 说明 | 版本建议 |
|------|------|---------|
| lm-eval | 评测执行 | v0.4.3 稳定版 |
| inference-service | 推理 backend | — |

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## finetune-demo 接口边界

### MVP 必须接口

```python
class FinetuneDemo:
    def train(self, config: FinetuneConfig, dataset: Dataset) -> TrainResult:
        """
        执行微调训练
        config: 训练配置（方法、路径、参数等）
        dataset: 训练数据集
        返回: {"adapter_path": "...", "metrics": {...}}
        状态: MVP 必须
        """
        pass

    def save_adapter(self, path: str) -> None:
        """
        保存 LoRA adapter
        状态: MVP 必须
        """
        pass

    def load_adapter(self, path: str) -> None:
        """
        加载 LoRA adapter
        状态: MVP 必须
        """
        pass

    def get_adapter_path(self) -> str:
        """
        获取当前 adapter 路径
        状态: MVP 必须
        """
        pass
```

### 后续阶段接口

```python
    def train_dpo(self, config: DPOConfig, dataset: Dataset) -> TrainResult:
        """
        DPO 偏好优化训练
        状态: MVP 不包含，后续迭代（需要偏好数据）
        """
        pass

    def report_metrics_to_langfuse(self, metrics: dict) -> None:
        """
        训练 metrics 上报 Langfuse
        状态: MVP 可选，后续建议
        """
        pass
```

### 外部依赖

| 依赖 | 说明 | 版本建议 |
|------|------|---------|
| PEFT | adapter 管理 | 最新 release |
| TRL | SFT/DPO 训练 | 最新 release |
| Unsloth | 加速（可选） | 按需 |

来源：https://github.com/huggingface/peft
来源：https://github.com/huggingface/trl

---

## 接口约束总结

| 模块 | 提案接口 | 外部依赖 | 后续阶段 |
|------|---------|---------|---------|
| inference-service | chat_completions | vLLM/SGLang | Triton/TensorRT-LLM |
| ai-gateway | chat_completions | inference-service | 多后端负载均衡 |
| eval-module | evaluate/load_results/compare | lm-eval | Langfuse 上报/LLM-as-Judge |
| finetune-demo | train/save_adapter/load_adapter | PEFT/TRL | DPO/Langfuse 上报 |

---

## 约束与说明

- 所有接口为**提案级**，不是仓库已实现
- 具体接口以实际代码实现为准
- MVP 阶段只实现"必须"接口
- 后续阶段接口在 v2/v3 中逐步实现

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT
4. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- 具体接口以实际实现为准

Out of Scope Kept:
- 未写代码实现
- 未写 API 错误码规范
- 未写接口版本管理
