# eval-module Task Presets v1

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module Task Presets

本文档定义 eval-module 评测任务预设，对应真实文件 `eval-module/configs/task_presets/`。

## 任务类型

| Task ID | 名称 | 来源 | 场景 |
|---|---|---|---|
| `mmlu` | Massive Multitask Language Understanding | OpenCompass / lm-evaluation-harness | 知识问答 |
| `gsm8k` | Grade School Math 8K | OpenAI | 数学应用题 |
| `humaneval` | HumanEval | OpenAI / bigcode | 代码生成 |

---

## MMMU Task Preset

**对应文件：** `eval-module/configs/task_presets/mmlu.yaml`

```yaml
task_id: "mmlu"
name: "Massive Multitask Language Understanding"
description: |
  5-shot multiple choice across 57 subjects (STEM, social sciences, humanities)
  Coverage: math, physics, chemistry, biology, history, law, etc.

task_type: "multiple_choice"
num_few_shot: 5

backend: "lm-evaluation-harness"
task_config:
  model_api_format: "chat"
  model_sep: "\n"
  num_concurrent: 4

subjects:
  - "abstract_algebra"
  - "anatomy"
  - "astronomy"
  - "college_biology"
  - "college_chemistry"
  - "college_computer_science"
  - "college_mathematics"
  - "college_physics"
  - "computer_security"
  - "econometrics"
  - "electrical_engineering"
  - "machine_learning"
  - "mathematics"
  - "professional_accounting"
  - "professional_medicine"
  - "professional psychology"
  - "jurisprudence"
  - "moral_scenarios"
  - "nutrition"
  - "philosophy"
  - "prehistory"
  - "psychology"
  - "public_relations"
  - "security_studies"
  - "sociology"
  - "us_foreign_policy"

batch_size: 4
max_tokens: 64
```

---

## GSM8K Task Preset

**对应文件：** `eval-module/configs/task_presets/gsm8k.yaml`

```yaml
task_id: "gsm8k"
name: "Grade School Math 8K"
description: |
  8.5K grade school math word problems (Grade 3-5 level).
  Chain-of-thought reasoning required.
  Split: main/test (1319 problems)

task_type: "free_response"
num_few_shot: 0

backend: "lm-evaluation-harness"
task_config:
  model_api_format: "chat"
  prompt_template: |
    Question: {question}
    Answer: {answer}
  stop_strings:
    - "\n\n"
    - "Question:"

batch_size: 8
max_tokens: 512
```

---

## HumanEval Task Preset

**对应文件：** `eval-module/configs/task_presets/humaneval.yaml`

```yaml
task_id: "humaneval"
name: "HumanEval"
description: |
  164 Python programming problems from OpenAI (Codex paper).
  Tests function signature, docstring, and correctness.
  Pass@1 evaluation.

task_type: "code_generation"
num_few_shot: 0

backend: "lm-evaluation-harness"
task_config:
  model_api_format: "chat"
  prompt_template: |
    {prompt}
  stop_strings:
    - "\n\n\n"
    - "\nclass "
    - "\ndef "
    - "\n# "

batch_size: 16
max_tokens: 512
temperature: 0.0
```

---

## MMLU 运行命令

```bash
# 通过 eval-module CLI
python -m eval_module.main run \
  --task mmlu \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output-dir results/mmlu

# 对应 T813 eval-module Validation Checklist
```

---

## GSM8K 运行命令

```bash
python -m eval_module.main run \
  --task gsm8k \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output-dir results/gsm8k
```

---

## HumanEval 运行命令

```bash
python -m eval_module.main run \
  --task humaneval \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1 \
  --output-dir results/humaneval
```

---

## Task Preset 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `task_id` | string | 唯一任务标识符 |
| `task_type` | enum | `multiple_choice` / `free_response` / `code_generation` |
| `num_few_shot` | int | few-shot 样本数 |
| `backend` | string | 评测后端（目前固定 `lm-evaluation-harness`） |
| `batch_size` | int | 并发 batch size |
| `max_tokens` | int | 最大生成 token 数 |
| `task_config.model_api_format` | string | `chat` 或 `complete` |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/opencompass/opencompass — OpenCompass MMLU
3. https://github.com/openai/human-eval — HumanEval

Risk of Staleness:
- lm-evaluation-harness task definitions are stable; task IDs unchanged since v0.4
