from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Any

from finetune_demo.artifacts import build_artifact_entries
from finetune_demo.config import TrainingConfig
from finetune_demo.dataset_registry import append_dataset_registry, build_dataset_registry_entry
from finetune_demo.trainer.base import BaseTrainer

ALLOWED_CHAT_ROLES = {"system", "user", "assistant"}


class LoRATrainer(BaseTrainer):
    def __init__(self, config: TrainingConfig | dict[str, Any]) -> None:
        if isinstance(config, dict):
            self.config = TrainingConfig(**config)
        else:
            self.config = config
        self.validate()

    def validate(self) -> None:
        if self.config.method not in ("lora", "qlora"):
            raise ValueError("method must be 'lora' or 'qlora'")
        if self.config.method == "qlora" and not self.config.qlora.load_in_4bit:
            raise ValueError("QLoRA requires load_in_4bit=True")
        train_file = Path(self.config.data.train_file)
        if not train_file.exists():
            raise FileNotFoundError(f"Training dataset not found: {train_file}")
        if train_file.suffix != ".jsonl":
            raise ValueError("training dataset must be a .jsonl file")

    def train(self) -> None:
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        trainer_state = output_dir / "trainer_state.json"
        run_manifest = output_dir / "run_manifest.json"
        artifacts_manifest = output_dir / "artifacts_manifest.json"
        metrics_dir = output_dir / "metrics"
        logs_dir = output_dir / "logs"
        data_dir = output_dir / "data"
        checkpoints_dir = output_dir / "checkpoints"
        checkpoint_dir = output_dir / "checkpoint-0001"
        checkpoint_index = checkpoints_dir / "checkpoint_index.json"
        checkpoint_index_markdown = checkpoints_dir / "checkpoint_index.md"
        metrics_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        dataset_summary = self._summarize_jsonl_dataset(Path(self.config.data.train_file))
        dataset_registry_entry = build_dataset_registry_entry(
            train_file=self.config.data.train_file,
            dataset_summary=dataset_summary,
            run_output_dir=output_dir,
            method=self.config.method,
            model=self.config.model.name_or_path,
        )

        trainer_state.write_text(
            json.dumps(
                {
                    "method": self.config.method,
                    "model": self.config.model.name_or_path,
                    "train_file": self.config.data.train_file,
                    "dataset_id": dataset_registry_entry["dataset_id"],
                    "dataset_version": dataset_summary["dataset_version"],
                    "dataset_sha256": dataset_summary["dataset_sha256"],
                    "epochs": self.config.num_train_epochs,
                    "learning_rate": self.config.learning_rate,
                },
                indent=2,
            )
            + "\n"
        )
        (output_dir / "training_args.json").write_text(
            json.dumps(
                {
                    "per_device_train_batch_size": self.config.per_device_train_batch_size,
                    "num_train_epochs": self.config.num_train_epochs,
                    "learning_rate": self.config.learning_rate,
                },
                indent=2,
            )
            + "\n"
        )
        (metrics_dir / "train_metrics.json").write_text(
            json.dumps(
                {
                    "loss": 1.234,
                    "train_runtime_seconds": 12.5,
                    "train_samples_per_second": 8.0,
                },
                indent=2,
            )
            + "\n"
        )
        (logs_dir / "train.log").write_text(
            "starting mock finetune run\n"
            f"method={self.config.method}\n"
            f"model={self.config.model.name_or_path}\n"
            "checkpoint=checkpoint-0001\n"
        )
        (logs_dir / "events.jsonl").write_text(
            json.dumps({"event": "run_started", "method": self.config.method, "model": self.config.model.name_or_path})
            + "\n"
            + json.dumps({"event": "checkpoint_saved", "checkpoint": "checkpoint-0001"})
            + "\n"
            + json.dumps({"event": "run_completed", "output_dir": str(output_dir)})
            + "\n"
        )
        (data_dir / "dataset_summary.json").write_text(
            json.dumps(
                {
                    "train_file": self.config.data.train_file,
                    "detected_format": "jsonl",
                    "records": dataset_summary["records"],
                    "messages": dataset_summary["messages"],
                    "average_messages_per_record": dataset_summary["average_messages_per_record"],
                    "role_counts": dataset_summary["role_counts"],
                    "records_with_system": dataset_summary["records_with_system"],
                    "dataset_size_bytes": dataset_summary["dataset_size_bytes"],
                    "dataset_sha256": dataset_summary["dataset_sha256"],
                    "dataset_version": dataset_summary["dataset_version"],
                    "dataset_registry_entry": "dataset_registry_entry.json",
                },
                indent=2,
            )
            + "\n"
        )
        (data_dir / "dataset_registry_entry.json").write_text(json.dumps(dataset_registry_entry, indent=2) + "\n")
        (checkpoint_dir / "adapter_config.json").write_text(
            json.dumps(
                {
                    "format": "mock-peft-adapter",
                    "base_model": self.config.model.name_or_path,
                    "r": self.config.lora.r,
                    "lora_alpha": self.config.lora.lora_alpha,
                },
                indent=2,
            )
            + "\n"
        )
        (checkpoint_dir / "adapter_model.safetensors").write_text("mock checkpoint adapter weights\n")
        (checkpoint_dir / "trainer_state.json").write_text(trainer_state.read_text())
        (checkpoints_dir / "latest_checkpoint.json").write_text(
            json.dumps(
                {
                    "latest_checkpoint": "checkpoint-0001",
                    "checkpoint_dir": str(checkpoint_dir),
                    "checkpoint_index": "checkpoint_index.json",
                },
                indent=2,
            )
            + "\n"
        )
        checkpoint_index_payload = self._build_checkpoint_index(output_dir, checkpoint_dir)
        checkpoint_index.write_text(json.dumps(checkpoint_index_payload, indent=2) + "\n")
        checkpoint_index_markdown.write_text(self._render_checkpoint_index_markdown(checkpoint_index_payload))
        run_manifest.write_text(
            json.dumps(
                {
                    "method": self.config.method,
                    "model": self.config.model.name_or_path,
                    "output_dir": str(output_dir),
                    "artifacts": {
                        "trainer_state": trainer_state.name,
                        "training_args": "training_args.json",
                        "metrics": "metrics/train_metrics.json",
                        "logs": "logs/train.log",
                        "events": "logs/events.jsonl",
                        "dataset_summary": "data/dataset_summary.json",
                        "dataset_registry_entry": "data/dataset_registry_entry.json",
                        "checkpoint": "checkpoint-0001",
                        "latest_checkpoint": "checkpoints/latest_checkpoint.json",
                        "checkpoint_index": "checkpoints/checkpoint_index.json",
                    },
                    "dataset": {
                        "id": dataset_registry_entry["dataset_id"],
                        "version": dataset_summary["dataset_version"],
                        "sha256": dataset_summary["dataset_sha256"],
                        "records": dataset_summary["records"],
                        "role_counts": dataset_summary["role_counts"],
                        "registry_entry": "data/dataset_registry_entry.json",
                    },
                },
                indent=2,
            )
            + "\n"
        )
        artifact_files = sorted(
            [
                "trainer_state.json",
                "training_args.json",
                "metrics/train_metrics.json",
                "logs/train.log",
                "logs/events.jsonl",
                "data/dataset_summary.json",
                "data/dataset_registry_entry.json",
                "checkpoints/latest_checkpoint.json",
                "checkpoints/checkpoint_index.json",
                "checkpoints/checkpoint_index.md",
                "checkpoint-0001/adapter_config.json",
                "checkpoint-0001/adapter_model.safetensors",
                "checkpoint-0001/trainer_state.json",
            ]
        )
        artifacts_manifest.write_text(
            json.dumps(
                {
                    "artifact_type": "finetune_run_bundle",
                    "root": str(output_dir),
                    "files": artifact_files,
                    "file_artifacts": build_artifact_entries(output_dir, artifact_files),
                },
                indent=2,
            )
            + "\n"
        )
        append_dataset_registry(output_dir.parent / "dataset_registry.jsonl", dataset_registry_entry)
        history_path = output_dir.parent / "run_history.jsonl"
        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "method": self.config.method,
                        "model": self.config.model.name_or_path,
                        "dataset_id": dataset_registry_entry["dataset_id"],
                        "dataset_version": dataset_summary["dataset_version"],
                        "output_dir": str(output_dir),
                        "checkpoint": str(checkpoint_dir),
                        "checkpoint_index_file": str(checkpoint_index),
                    }
                )
                + "\n"
            )

    @staticmethod
    def _summarize_jsonl_dataset(path: Path) -> dict[str, Any]:
        records = 0
        messages = 0
        records_with_system = 0
        role_counts: Counter[str] = Counter()
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    record = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSONL record at {path}:{line_number}") from exc
                roles = LoRATrainer._validate_chat_record(path, line_number, record)
                records_with_system += int("system" in roles)
                messages += len(roles)
                role_counts.update(roles)
                records += 1
        if records == 0:
            raise ValueError(f"Training dataset is empty: {path}")
        dataset_digest = sha256(path.read_bytes()).hexdigest()
        return {
            "records": records,
            "messages": messages,
            "average_messages_per_record": round(messages / records, 4),
            "role_counts": dict(sorted(role_counts.items())),
            "records_with_system": records_with_system,
            "dataset_size_bytes": path.stat().st_size,
            "dataset_sha256": dataset_digest,
            "dataset_version": f"sha256:{dataset_digest[:12]}",
        }

    @staticmethod
    def _validate_chat_record(path: Path, line_number: int, record: Any) -> list[str]:
        prefix = f"Invalid dataset record at {path}:{line_number}"
        if not isinstance(record, dict):
            raise ValueError(f"{prefix}: record must be a JSON object")

        messages = record.get("messages")
        if not isinstance(messages, list) or not messages:
            raise ValueError(f"{prefix}: messages must be a non-empty list")

        roles = []
        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"{prefix}: messages[{index}] must be a JSON object")
            role = message.get("role")
            content = message.get("content")
            if role not in ALLOWED_CHAT_ROLES:
                allowed_roles = ", ".join(sorted(ALLOWED_CHAT_ROLES))
                raise ValueError(f"{prefix}: messages[{index}].role must be one of {allowed_roles}")
            if not isinstance(content, str) or not content.strip():
                raise ValueError(f"{prefix}: messages[{index}].content must be a non-empty string")
            roles.append(role)

        if "user" not in roles or "assistant" not in roles:
            raise ValueError(f"{prefix}: messages must include at least one user message and one assistant response")
        return roles

    @staticmethod
    def _build_checkpoint_index(output_dir: Path, checkpoint_dir: Path) -> dict[str, Any]:
        checkpoint_files = [
            f"{checkpoint_dir.name}/adapter_config.json",
            f"{checkpoint_dir.name}/adapter_model.safetensors",
            f"{checkpoint_dir.name}/trainer_state.json",
        ]
        file_artifacts = build_artifact_entries(output_dir, checkpoint_files)
        adapter_artifact = next(
            artifact for artifact in file_artifacts if artifact["path"].endswith("adapter_model.safetensors")
        )
        return {
            "artifact_type": "finetune_checkpoint_index",
            "checkpoint_count": 1,
            "latest_checkpoint": checkpoint_dir.name,
            "checkpoints": [
                {
                    "name": checkpoint_dir.name,
                    "checkpoint_dir": str(checkpoint_dir),
                    "files": checkpoint_files,
                    "file_artifacts": file_artifacts,
                    "adapter_model_sha256": adapter_artifact["sha256"],
                    "resumable": True,
                }
            ],
        }

    @staticmethod
    def _render_checkpoint_index_markdown(index: dict[str, Any]) -> str:
        lines = [
            "# Finetune Checkpoint Index",
            "",
            f"- Checkpoints: `{index['checkpoint_count']}`",
            f"- Latest checkpoint: `{index['latest_checkpoint']}`",
            "",
            "| Checkpoint | Resumable | Adapter SHA256 | Files |",
            "| --- | --- | --- | ---: |",
        ]
        for checkpoint in index["checkpoints"]:
            lines.append(
                "| "
                f"{checkpoint['name']} | "
                f"{str(checkpoint['resumable']).lower()} | "
                f"{checkpoint['adapter_model_sha256']} | "
                f"{len(checkpoint['files'])} |"
            )
        return "\n".join(lines) + "\n"
