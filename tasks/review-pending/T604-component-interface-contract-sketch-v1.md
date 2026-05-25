Task ID: T604
Task Title: Cross-Project Systemization Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
整理提案级接口，不写成"已实现接口"。

Result:

# Component Interface Contract Sketch v1

## 概述

本文档整理各模块间的提案级接口，明确输入/输出，不写成仓库已实现接口。

---

## inference-service 接口

### 对 ai-gateway 提供

```python
# 提案接口
class InferenceService:
    def chat_completions(self, model: str, messages: list) -> dict:
        """
        代理到 vLLM/SGLang
        返回: {"id": "...", "choices": [...], "usage": {...}}
        """
        pass

    def list_models(self) -> list[str]:
        """返回可用模型列表"""
        pass

    def health(self) -> bool:
        """健康检查"""
        pass
```

### 对 eval-module 提供

```python
# 提案接口（lm-eval backend 兼容）
class InferenceServiceBackend:
    def generate(self, prompt: str, **kwargs) -> str:
        """
        lm-eval backend 接口
        返回生成的文本
        """
        pass
```

来源：https://docs.vllm.ai/

---

## ai-gateway 接口

### 对客户端提供

```python
# 提案接口
class AIGateway:
    def chat_completions(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        代理到 inference-service
        额外功能：鉴权、限流、计量
        """
        pass

    def get_metrics(self) -> dict:
        """gateway 自身 metrics"""
        pass
```

### 对 inference-service 调用

```python
# 内部接口
class GatewayBackend:
    def call_inference(self, request: dict) -> dict:
        """
        转发到 inference-service
        返回: {"status": "success", "response": {...}}
        """
        pass
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## eval-module 接口

### 对 finetune-demo 提供

```python
# 提案接口
class EvalModule:
    def evaluate(self, model: str, tasks: list[str], backend: str = "vllm") -> dict:
        """
        运行 benchmark 评测
        model: 模型名称或路径
        tasks: benchmark 任务列表，如 ["mmlu", "gsm8k"]
        backend: 推理后端，如 "vllm"
        返回: {"task": {"acc_norm": 0.xx, ...}}
        """
        pass

    def load_results(self, path: str) -> dict:
        """加载历史评测结果"""
        pass

    def compare(self, result_a: dict, result_b: dict) -> dict:
        """对比两个评测结果"""
        pass
```

### 对 Langfuse 上报（可选）

```python
    def report_to_langfuse(self, eval_result: dict) -> None:
        """评测结果上报 Langfuse（可选）"""
        pass
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

---

## finetune-demo 接口

### 对 eval-module 提供

```python
# 提案接口
class FinetuneDemo:
    def train(self, config: FinetuneConfig, dataset: Dataset) -> TrainResult:
        """
        执行微调训练
        config: 训练配置（方法、路径、参数等）
        dataset: 训练数据集
        返回: {"adapter_path": "...", "metrics": {...}}
        """
        pass

    def save_adapter(self, path: str) -> None:
        """保存 LoRA adapter"""
        pass

    def load_adapter(self, path: str) -> None:
        """加载 LoRA adapter"""
        pass

    def get_adapter_path(self) -> str:
        """获取当前 adapter 路径"""
        pass
```

### 对 inference-service 提供

```python
# 内部接口
class AdapterManager:
    def register_to_inference(self, adapter_path: str, inference_url: str) -> None:
        """
        将 adapter 注册到 inference-service
        用于微调后推理验证
        """
        pass
```

来源：https://github.com/huggingface/peft

---

## 接口依赖总览

```
ai-gateway
    ├── chat_completions(request) → inference-service.chat_completions()
    └── get_metrics()

eval-module
    ├── evaluate(model, tasks) → lm-eval
    └── report_to_langfuse(result)

finetune-demo
    ├── train(config, dataset) → adapter
    ├── save_adapter(path)
    ├── load_adapter(path)
    └── register_to_inference(adapter_path, inference_url)
```

---

## 约束与说明

- 所有接口为**提案级**，不是仓库已实现
- 具体接口以实际代码实现为准
- 接口版本管理在后续迭代中完善

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
3. https://github.com/huggingface/peft — PEFT

Risk of Staleness:
- 具体接口以实际实现为准

Out of Scope Kept:
- 未写代码实现
- 未写 API 错误码规范
- 未写接口版本管理
