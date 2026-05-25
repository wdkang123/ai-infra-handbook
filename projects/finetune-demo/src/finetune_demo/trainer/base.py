from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTrainer(ABC):
    @abstractmethod
    def validate(self) -> None: ...

    @abstractmethod
    def train(self) -> None: ...
