Task ID: T303
Task Title: eval-module MVP 目录与边界设计
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T162、T175、T301、T302，定义 eval-module MVP 的边界和目录结构。eval-module 通过调用已有推理入口做评测，不重新实现推理服务。

Result:

## 一、定位说明

**eval-module** 是 AI Infra 项目中负责**模型输出质量评测**的模块。它的核心职责：

- 调用推理服务（inference-service 或外部 API）获取模型输出
- 在标准数据集或自定义测试集上评估输出质量
- 记录评测结果，支持版本间对比

**eval-module 不做的事**：
- 模型推理本身（委托给 inference-service）
- 推理流量的透传和路由（属于 ai-gateway）
- 训练和微调（属于 finetune-demo）

## 二、目录结构（最小骨架）

```
eval-module/
├── README.md                      # 模块说明、快速启动
├── pyproject.toml                 # Python 依赖定义
├── src/
│   └── eval_module/
│       ├── __init__.py
│       ├── evaluator.py         # 评测器基类
│       ├── llm_judge.py         # LLM-as-Judge 评测实现
│       ├── heuristic_eval.py     # 规则评测（Rouge/BLEU/准确率）
│       ├── dataset.py           # 数据集加载和管理
│       ├── runner.py            # 评测任务运行器
│       └── results.py           # 结果记录和对比
├── tests/
│   └── test_eval.py             # 基本评测逻辑测试
└── examples/
    └── quickstart.py             # 快速启动示例（调用 vLLM）
```

## 三、核心接口（提案接口）

**注意**：以下接口为提案接口，不是仓库现有实现。

### Python API（提案）

```python
from eval_module import Evaluator, LLmasJudge

# 提案接口：创建 LLM-as-Judge 评测器
evaluator = LLMasJudge(
    judge_model="gpt-4",
    api_key="replace-with-openai-api-key",
    inference_endpoint="http://localhost:8000/v1"  # 对接 inference-service
)

# 提案接口：运行评测
result = evaluator.evaluate(
    dataset="GSM8K",
    metric="accuracy",
    target_model="Qwen/Qwen2.5-7B-Instruct"
)
print(result.summary())
```

### CLI 接口（提案）

```bash
# 提案接口：运行评测任务
eval-module run \
    --judge gpt-4 \
    --target http://localhost:8000/v1 \
    --dataset GSM8K \
    --metric accuracy \
    --output results.json

# 提案接口：对比两个版本的评测结果
eval-module compare \
    --baseline results_v1.json \
    --candidate results_v2.json
```

## 四、依赖关系

```
ai-gateway（可选，上层调用）
    ↓ 推理请求
eval-module（本案）
    ↓ 调用
inference-service（提供推理服务）
    ↓ 或直接调用
外部模型 API（OpenAI GPT-4 等）
```

- **上游**：被 ai-gateway 调用，或直接被应用层调用
- **下游**：通过 inference-service 或外部 API 发送推理请求，不自己实现推理

## 五、边界说明

| 边界 | 说明 |
|------|------|
| vs inference-service | eval-module 调用 inference-service 的 API 做评测，不自己实现推理逻辑 |
| vs ai-gateway | ai-gateway 做流量透传，eval-module 做质量评测；两者可以组合使用 |
| vs benchmark | eval-module 侧重模型输出质量评测，benchmark 侧重标准数据集上的能力评测 |
| vs finetune-demo | finetune-demo 负责训练，eval-module 负责评测训练产出的模型 |

## 六、最小可运行路径（提案）

**目标**：通过 eval-module 对 Qwen 模型做 GSM8K 准确率评测。

**注意**：以下为提案接口，不是仓库现有实现。

```bash
# 提案接口：安装（实际不存在 pip install eval-module）
# pip install eval-module

# 1. 准备 inference-service（已由 inference-service 模块定义）
# inference-service serve --engine vllm --model Qwen/Qwen2.5-7B-Instruct --port 8000 &

# 2. 提案接口：运行评测
# eval-module run \
#     --judge gpt-4 \
#     --target http://localhost:8000/v1 \
#     --dataset examples/datasets/gsm8k_test.json \
#     --metric accuracy \
#     --output result.json

# 实际可使用 LM-Eval Harness（已开源）做类似事情：
# pip install lm-eval
# lm_eval --model vllm \
#     --model_args model=Qwen/Qwen2.5-7B-Instruct \
#     --tasks gsm8k \
#     --limit 10
```

来源：https://github.com/EleutherAI/lm-evaluation-harness

## 七、评测方法说明

```python
# 提案：Evaluator 抽象基类
class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, dataset: Dataset, target_model: str, **kwargs) -> EvalResult: ...

# 提案：LLM-as-Judge 评测
class LLMasJudge(Evaluator):
    def evaluate(self, dataset, target_model, **kwargs):
        # 1. 调用 target_model 获取输出
        response = call_model(target_model, prompt)
        # 2. 调用 judge_model 评分
        score = self.judge(response, reference)
        return EvalResult(score=score, response=response)

# 提案：规则评测
class HeuristicEval(Evaluator):
    def evaluate(self, dataset, target_model, **kwargs):
        # Rouge/BLEU/精确匹配等规则指标
        ...
```

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness（参考评测工具）
2. https://crfm.stanford.edu/helm/ — Stanford HELM（参考评测框架）
3. https://github.com/tensorzero/tensorzero — TensorZero（参考 evaluation 集成）
4. https://github.com/Arize-AI/phoenix — Phoenix（参考 observability 集成）

Risk of Staleness:
- LM-Eval Harness 版本更新影响 benchmark 兼容性
- 具体 API 以实际实现版本为准

Out of Scope Kept:
- 未写完整 benchmark 系统
- 未做 Leaderboard 平台
- 未写多供应商评测对比
