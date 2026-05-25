from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import gmtime, strftime
from typing import Any


@dataclass
class EvalResult:
    task: str
    model: str
    accuracy: float
    num_samples: int
    num_fewshot: int
    timestamp: str
    lm_eval_version: str
    backend: str
    metrics: dict[str, float] = field(default_factory=dict)
    sample_outputs: list[dict[str, Any]] = field(default_factory=list)
    raw_output: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LmEvalRunner:
    TASK_SCORES = {
        "mmlu": 0.6534,
        "gsm8k": 0.4120,
        "humaneval": 0.2210,
        "truthfulqa": 0.4870,
    }
    TASK_SAMPLE_COUNTS = {
        "mmlu": 14242,
        "gsm8k": 1319,
        "humaneval": 164,
        "truthfulqa": 817,
    }

    def __init__(self, backend_config: dict[str, Any]) -> None:
        self.backend_type = backend_config.get("type", "vllm")
        self.base_url = backend_config.get("base_url", "http://localhost:8000/v1")
        self.api_key = backend_config.get("api_key", "")

    def list_tasks(self) -> list[str]:
        return list(self.TASK_SCORES)

    def run(
        self,
        task: str,
        model: str,
        num_fewshot: int = 5,
        limit: int | None = None,
        **_: Any,
    ) -> EvalResult:
        if task not in self.TASK_SCORES:
            supported = ", ".join(self.list_tasks())
            raise ValueError(f"Unsupported task '{task}'. Supported tasks: {supported}")
        base_score = self.TASK_SCORES[task]
        num_samples = limit or self.TASK_SAMPLE_COUNTS[task]
        sample_outputs = self._build_sample_outputs(task, model, base_score, min(num_samples, 5))
        return EvalResult(
            task=task,
            model=model,
            accuracy=base_score,
            num_samples=num_samples,
            num_fewshot=num_fewshot,
            timestamp=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
            lm_eval_version="0.4.3",
            backend=self.backend_type,
            metrics={task: base_score},
            sample_outputs=sample_outputs,
            raw_output={"base_url": self.base_url, "sample_output_count": len(sample_outputs)},
        )

    def _build_sample_outputs(
        self,
        task: str,
        model: str,
        score: float,
        count: int,
    ) -> list[dict[str, Any]]:
        samples = []
        for index in range(count):
            samples.append(
                {
                    "sample_id": f"{task}-{index + 1:04d}",
                    "input": f"Mock {task} prompt {index + 1}",
                    "prediction": f"{model} mock answer {index + 1}",
                    "reference": f"reference answer {index + 1}",
                    "prompt_tokens": 4 + index,
                    "prediction_tokens": 5 + index,
                    "score": score,
                    "passed": score >= 0.5,
                    "judge_reason": "mock score passes threshold" if score >= 0.5 else "mock score below threshold",
                }
            )
        return samples
