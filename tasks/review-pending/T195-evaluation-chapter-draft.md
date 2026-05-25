# LLM Evaluation

## 1. 这是什么

LLM Evaluation（评测）关注模型输出的质量评估，目标是回答"模型回答得好不好"。核心方法包括：基于标准数据集的 Benchmark 评测、LLM-as-Judge 主观评估、Heuristic 规则评测。

**与 Observability 的边界**：Observability 关注"系统行为"（做了什么、耗时多久），Evaluation 关注"输出质量"（回答得好不好）。两者互补，Observability 高点后需要 Evaluation 向下钻取质量。

## 2. 为什么重要

在 AI Infra 推理服务中，评测是模型迭代和选型的基础：

1. **模型选型**：通过 Benchmark 在标准数据集上对比不同模型能力
2. **版本验证**：通过 Replay 用真实流量验证新版本模型质量
3. **质量监控**：通过 LLM-as-Judge 持续监控生产环境输出质量
4. **能力边界**：通过评测了解模型在特定任务（数学、代码、推理）上的表现

## 3. 核心原理

### Benchmark Eval（标准数据集评测）
在标准数据集（MMLU、GSM8K、HumanEval 等）上评估模型能力，关注"模型懂不懂、会不会"。不关注推理速度、成本、并发。

来源：https://github.com/EleutherAI/lm-evaluation-harness

### LLM-as-Judge
用强模型（如 GPT-4）评估弱模型输出的质量，适合无法用规则定义正确答案的开放式任务。

来源：https://github.com/EleutherAI/lm-evaluation-harness

### Heuristic Eval
基于规则的评测（Rouge、BLEU、准确率），适合有标准答案的任务。

来源：https://github.com/EleutherAI/lm-evaluation-harness

### Replay / 回放
用真实流量重放，验证新版本模型在相同输入下的输出质量变化。

来源：https://crfm.stanford.edu/helm/

## 4. 常见方案 / 组件

| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **LM-Eval Harness** | 标准 benchmark 评测工具，支持 70+ 标准数据集 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Stanford HELM** | 全面评测框架，覆盖 50+ 场景 | https://crfm.stanford.edu/helm/ |
| **BigCode Eval Harness** | 代码模型专用评测工具 | https://github.com/bigcode-project/bigcode-eval-harness |
| **LMSYS Chatbot Arena** | 基于人类盲评的模型排名 | https://chat.lmsys.org/ |
| **Open LLM Leaderboard** | Hugging Face 官方开源模型排行榜 | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://crfm.stanford.edu/helm/

## 5. 关键指标

| 指标 | 全称 | 说明 | 来源 |
|------|------|------|------|
| **Accuracy** | 准确率 | 正确答案比例 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Rouge-L** | Rouge-L | 生成文本与参考答案的 n-gram 重叠度 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Pass@K** | Pass at K | K 次采样中至少一次通过的比例（代码评测） | https://github.com/bigcode-project/bigcode-eval-harness |
| **MMLU** | Massive Multitask Language Understanding | 57 个学科选择题综合评测 | https://github.com/EleutherAI/lm-evaluation-harness |
| **Elo** | Elo Rating | 人类盲评胜率换算的相对评分 | https://chat.lmsys.org/ |

## 6. 常见误区

1. **"Benchmark 等于模型能力唯一标准"**：Benchmark 只覆盖特定任务，模型在真实场景的表现可能与 Benchmark 结果不一致
2. **"Evaluation 和 Observability 是同一件事"**：Observability 描述系统行为，Evaluation 评估输出质量，两者互补但不等同
3. **"Benchmark 分高就一定好"**：不同 Benchmark 评测维度不同，应根据实际任务场景选择合适的评测集

## 7. 与项目关系

在 AI Infra 学习路径中，Evaluation 是模型质量保障的环节：

- eval-module 提供评测抽象，是 Observability → Evaluation 协作的典型场景
- 评测结果指导模型选型和版本发布决策
- 与 inference-service 的关系：评测在推理层之上评估输出质量

## 8. 最小实践任务

**目标**：使用 LM-Eval Harness 对本地 vLLM 推理服务做一次 benchmark 评测，验证评测工具正常运行。

```bash
# 1. 安装 LM-Eval Harness
pip install lm-eval

# 2. 启动 vLLM（本地推理服务）
# vllm serve Qwen/Qwen2.5-0.5B-Instruct --host 0.0.0.0 --port 8000

# 3. 运行评测（示例：MMLU 5-shot）
lm_eval \
  --model vllm \
  --model_args pretrained=Qwen/Qwen2.5-0.5B-Instruct,tensor_parallel_size=1 \
  --tasks mmlu \
  --num_fewshot 5 \
  --batch_size 8

# 4. 查看输出
# 评测完成后输出各任务准确率
```

来源：https://github.com/EleutherAI/lm-evaluation-harness
来源：https://docs.vllm.ai/

## 9. 输出物

- LM-Eval Harness 安装完成
- vLLM 推理服务运行中（端口 8000）
- 至少一个标准任务（MMLU 或其他）的评测结果输出

## 10. 延伸阅读

1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
2. https://crfm.stanford.edu/helm/ — Stanford HELM 评测框架
3. https://chat.lmsys.org/ — LMSYS Chatbot Arena（人类盲评排名）
4. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
5. https://github.com/bigcode-project/bigcode-eval-harness — BigCode 评测工具

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
2. https://crfm.stanford.edu/helm/ — Stanford HELM 官网
3. https://chat.lmsys.org/ — LMSYS Chatbot Arena
4. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
5. https://github.com/bigcode-project/bigcode-eval-harness — BigCode 评测工具

Risk of Staleness:
- LM-Eval Harness 版本更新影响 benchmark 兼容性，具体 API 以实际安装版本为准
- LMSYS Arena 和 Open LLM Leaderboard 按季度更新，排名变化较快
- 各 benchmark 数据集版本可能影响结果可比性

Out of Scope Kept:
- 未写完整评测手册
- 未做 leaderboard 设计
- 未写分布式训练相关
