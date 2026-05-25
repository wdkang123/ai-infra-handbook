from __future__ import annotations

from typing import Protocol

from eval_module.runners.lm_eval_runner import EvalResult


class EvalRunner(Protocol):
    def list_tasks(self) -> list[str]: ...

    def run(
        self,
        task: str,
        model: str,
        num_fewshot: int = 5,
        limit: int | None = None,
    ) -> EvalResult: ...
