from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest
from finetune_demo.artifacts import file_artifact_entry
from finetune_demo.config import load_config, load_config_from_cli
from finetune_demo.dataset_registry import (
    append_dataset_registry,
    build_dataset_registry_diff,
    build_dataset_registry_report,
    render_dataset_registry_diff_markdown,
    render_dataset_registry_markdown,
    save_dataset_registry_diff,
    save_dataset_registry_diff_markdown,
    save_dataset_registry_markdown,
    save_dataset_registry_report,
)
from finetune_demo.export.adapter_exporter import (
    build_export_history_report,
    export_adapter,
    render_export_history_markdown,
    save_export_history_markdown,
    save_export_history_report,
)
from finetune_demo.run_history import (
    build_run_history_report,
    render_run_history_markdown,
    save_run_history_markdown,
    save_run_history_report,
)
from finetune_demo.trainer.lora_trainer import LoRATrainer


def test_load_config_from_yaml() -> None:
    cfg = load_config("configs/lora/lora_config_qwen_05b.yaml")
    assert cfg.method == "lora"
    assert cfg.lora.r == 16


def test_load_config_from_cli() -> None:
    cfg = load_config_from_cli(
        method="qlora",
        model="Qwen/Qwen2.5-0.5B-Instruct",
        dataset="./data/train.jsonl",
        output="./outputs/test_trial",
        epochs=1,
        per_device_batch_size=4,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32,
        load_in_4bit=True,
        config=None,
    )
    assert cfg.method == "qlora"
    assert cfg.qlora.load_in_4bit is True


def test_config_file_keeps_qlora_4bit_when_cli_flag_omitted() -> None:
    cfg = load_config_from_cli(
        method=None,
        model=None,
        dataset=None,
        output=None,
        epochs=None,
        per_device_batch_size=None,
        learning_rate=None,
        lora_r=None,
        lora_alpha=None,
        load_in_4bit=None,
        config="configs/qlora/qlora_config_qwen_05b.yaml",
    )
    assert cfg.method == "qlora"
    assert cfg.qlora.load_in_4bit is True


def test_trainer_writes_state(tmp_path: Path) -> None:
    cfg = load_config("configs/qlora/qlora_config_qwen_05b.yaml")
    cfg.output_dir = str(tmp_path / "run")
    trainer = LoRATrainer(cfg)
    trainer.train()
    assert (tmp_path / "run" / "trainer_state.json").exists()
    assert (tmp_path / "run" / "checkpoint-0001" / "adapter_model.safetensors").exists()
    assert (tmp_path / "run" / "checkpoint-0001" / "trainer_state.json").exists()
    assert (tmp_path / "run" / "metrics" / "train_metrics.json").exists()
    assert (tmp_path / "run" / "run_manifest.json").exists()
    assert (tmp_path / "run" / "artifacts_manifest.json").exists()
    assert (tmp_path / "run" / "logs" / "events.jsonl").exists()
    assert (tmp_path / "run" / "data" / "dataset_summary.json").exists()
    assert (tmp_path / "run" / "data" / "dataset_registry_entry.json").exists()
    assert (tmp_path / "run" / "checkpoints" / "latest_checkpoint.json").exists()
    assert (tmp_path / "run" / "checkpoints" / "checkpoint_index.json").exists()
    assert (tmp_path / "run" / "checkpoints" / "checkpoint_index.md").exists()
    assert (tmp_path / "run_history.jsonl").exists()
    assert (tmp_path / "dataset_registry.jsonl").exists()
    dataset_summary = json.loads((tmp_path / "run" / "data" / "dataset_summary.json").read_text())
    dataset_path = Path(cfg.data.train_file)
    assert dataset_summary["records"] == 2
    assert dataset_summary["messages"] == 4
    assert dataset_summary["average_messages_per_record"] == 2.0
    assert dataset_summary["role_counts"] == {"assistant": 2, "user": 2}
    assert dataset_summary["records_with_system"] == 0
    assert dataset_summary["dataset_size_bytes"] == dataset_path.stat().st_size
    dataset_digest = sha256(dataset_path.read_bytes()).hexdigest()
    assert dataset_summary["dataset_sha256"] == dataset_digest
    assert dataset_summary["dataset_version"] == f"sha256:{dataset_digest[:12]}"
    assert dataset_summary["dataset_registry_entry"] == "dataset_registry_entry.json"
    dataset_registry_entry = json.loads((tmp_path / "run" / "data" / "dataset_registry_entry.json").read_text())
    assert dataset_registry_entry["dataset_id"] == f"train@{dataset_summary['dataset_version']}"
    assert dataset_registry_entry["dataset_sha256"] == dataset_summary["dataset_sha256"]
    assert dataset_registry_entry["registered_from"]["run_output_dir"] == str(tmp_path / "run")
    run_manifest = json.loads((tmp_path / "run" / "run_manifest.json").read_text())
    assert run_manifest["dataset"]["id"] == dataset_registry_entry["dataset_id"]
    assert run_manifest["dataset"]["version"] == dataset_summary["dataset_version"]
    assert run_manifest["dataset"]["role_counts"] == {"assistant": 2, "user": 2}
    assert run_manifest["artifacts"]["dataset_registry_entry"] == "data/dataset_registry_entry.json"
    trainer_state = json.loads((tmp_path / "run" / "trainer_state.json").read_text())
    assert trainer_state["dataset_id"] == dataset_registry_entry["dataset_id"]
    assert trainer_state["dataset_version"] == dataset_summary["dataset_version"]
    assert trainer_state["dataset_sha256"] == dataset_summary["dataset_sha256"]
    latest_checkpoint = json.loads((tmp_path / "run" / "checkpoints" / "latest_checkpoint.json").read_text())
    assert latest_checkpoint["checkpoint_index"] == "checkpoint_index.json"
    checkpoint_index = json.loads((tmp_path / "run" / "checkpoints" / "checkpoint_index.json").read_text())
    assert checkpoint_index["artifact_type"] == "finetune_checkpoint_index"
    assert checkpoint_index["latest_checkpoint"] == "checkpoint-0001"
    assert checkpoint_index["checkpoints"][0]["resumable"] is True
    assert checkpoint_index["checkpoints"][0]["adapter_model_sha256"]
    assert "Finetune Checkpoint Index" in (tmp_path / "run" / "checkpoints" / "checkpoint_index.md").read_text()
    artifacts_manifest = json.loads((tmp_path / "run" / "artifacts_manifest.json").read_text())
    adapter_entry = file_artifact_entry(tmp_path / "run", "checkpoint-0001/adapter_model.safetensors")
    assert adapter_entry in artifacts_manifest["file_artifacts"]
    registry_artifact_entry = file_artifact_entry(tmp_path / "run", "data/dataset_registry_entry.json")
    assert registry_artifact_entry in artifacts_manifest["file_artifacts"]
    checkpoint_index_entry = file_artifact_entry(tmp_path / "run", "checkpoints/checkpoint_index.json")
    assert checkpoint_index_entry in artifacts_manifest["file_artifacts"]
    registry_history = (tmp_path / "dataset_registry.jsonl").read_text()
    assert dataset_registry_entry["dataset_id"] in registry_history
    run_report = build_run_history_report(
        tmp_path / "run_history.jsonl",
        dataset_id=dataset_registry_entry["dataset_id"],
        model=cfg.model.name_or_path,
        method=cfg.method,
    )
    assert run_report["report_type"] == "finetune_run_index"
    assert run_report["total_run_count"] == 1
    assert run_report["run_count"] == 1
    assert run_report["dataset_count"] == 1
    assert run_report["model_count"] == 1
    assert run_report["method_counts"] == {cfg.method: 1}
    assert run_report["runs"][0]["run_manifest_file"] == str(tmp_path / "run" / "run_manifest.json")
    assert run_report["runs"][0]["checkpoint_index_file"] == str(
        tmp_path / "run" / "checkpoints" / "checkpoint_index.json"
    )
    assert run_report["model_summaries"][0]["latest_run_manifest_file"] == str(tmp_path / "run" / "run_manifest.json")
    assert run_report["model_summaries"][0]["latest_checkpoint_index_file"] == str(
        tmp_path / "run" / "checkpoints" / "checkpoint_index.json"
    )
    assert run_report["dataset_summaries"][0]["dataset_id"] == dataset_registry_entry["dataset_id"]
    run_markdown = render_run_history_markdown(run_report)
    assert "Finetune Run Index" in run_markdown
    assert "Run Manifest" in run_markdown
    assert "Checkpoint Index" in run_markdown
    run_json = save_run_history_report(run_report, tmp_path / "run_index.json")
    run_md = save_run_history_markdown(run_report, tmp_path / "run_index.md")
    assert run_json.exists()
    assert run_md.exists()
    registry_report = build_dataset_registry_report(tmp_path / "dataset_registry.jsonl")
    assert registry_report["report_type"] == "finetune_dataset_registry"
    assert registry_report["total_entry_count"] == 1
    assert registry_report["entry_count"] == 1
    assert registry_report["dataset_count"] == 1
    assert registry_report["datasets"][0]["dataset_id"] == dataset_registry_entry["dataset_id"]
    assert registry_report["datasets"][0]["registered_count"] == 1
    assert registry_report["datasets"][0]["models"] == [cfg.model.name_or_path]
    assert registry_report["duplicate_entry_count"] == 0
    markdown = render_dataset_registry_markdown(registry_report)
    assert "Finetune Dataset Registry" in markdown
    assert dataset_registry_entry["dataset_id"] in markdown
    assert "Duplicate registrations" in markdown
    json_report = save_dataset_registry_report(registry_report, tmp_path / "dataset_registry_report.json")
    markdown_report = save_dataset_registry_markdown(registry_report, tmp_path / "dataset_registry_report.md")
    assert json_report.exists()
    assert markdown_report.exists()
    append_dataset_registry(tmp_path / "dataset_registry.jsonl", dataset_registry_entry)
    duplicate_report = build_dataset_registry_report(
        tmp_path / "dataset_registry.jsonl",
        method=cfg.method,
        model=cfg.model.name_or_path,
    )
    assert duplicate_report["entry_count"] == 2
    assert duplicate_report["dataset_count"] == 1
    assert duplicate_report["duplicate_entry_count"] == 1
    assert duplicate_report["total_entry_count"] == 2
    assert duplicate_report["method_filter"] == cfg.method
    assert duplicate_report["model_filter"] == cfg.model.name_or_path
    empty_filter_report = build_dataset_registry_report(tmp_path / "dataset_registry.jsonl", method="lora")
    assert empty_filter_report["total_entry_count"] == 2
    assert empty_filter_report["entry_count"] == 0
    assert empty_filter_report["dataset_count"] == 0

    changed_entry = {
        **dataset_registry_entry,
        "dataset_id": "train@sha256:changed",
        "dataset_version": "sha256:changed",
        "dataset_sha256": "changed",
        "records": dataset_registry_entry["records"] + 1,
        "role_counts": {"assistant": 3, "user": 3},
    }
    append_dataset_registry(tmp_path / "dataset_registry.jsonl", changed_entry)
    diff_report = build_dataset_registry_diff(
        tmp_path / "dataset_registry.jsonl",
        left_dataset_id=dataset_registry_entry["dataset_id"],
        right_dataset_id=changed_entry["dataset_id"],
    )
    assert diff_report["report_type"] == "finetune_dataset_diff"
    assert diff_report["identical_dataset_sha256"] is False
    assert "dataset_sha256" in diff_report["changed_fields"]
    assert "records" in diff_report["changed_fields"]
    diff_markdown = render_dataset_registry_diff_markdown(diff_report)
    assert "Finetune Dataset Diff" in diff_markdown
    assert "dataset_sha256" in diff_markdown
    diff_json = save_dataset_registry_diff(diff_report, tmp_path / "dataset_registry_diff.json")
    diff_md = save_dataset_registry_diff_markdown(diff_report, tmp_path / "dataset_registry_diff.md")
    assert diff_json.exists()
    assert diff_md.exists()
    with pytest.raises(ValueError, match="Dataset not found"):
        build_dataset_registry_diff(
            tmp_path / "dataset_registry.jsonl",
            left_dataset_id="missing",
            right_dataset_id=changed_entry["dataset_id"],
        )


def test_trainer_rejects_missing_dataset(tmp_path: Path) -> None:
    cfg = load_config("configs/lora/lora_config_qwen_05b.yaml")
    cfg.data.train_file = str(tmp_path / "missing.jsonl")
    cfg.output_dir = str(tmp_path / "run")
    with pytest.raises(FileNotFoundError, match="Training dataset not found"):
        LoRATrainer(cfg)


def test_trainer_rejects_invalid_dataset_schema(tmp_path: Path) -> None:
    train_file = tmp_path / "bad.jsonl"
    train_file.write_text(json.dumps({"text": "missing chat messages"}) + "\n")
    cfg = load_config("configs/lora/lora_config_qwen_05b.yaml")
    cfg.data.train_file = str(train_file)
    cfg.output_dir = str(tmp_path / "run")

    trainer = LoRATrainer(cfg)
    with pytest.raises(ValueError, match="messages must be a non-empty list"):
        trainer.train()


def test_trainer_rejects_dataset_without_assistant_response(tmp_path: Path) -> None:
    train_file = tmp_path / "bad.jsonl"
    train_file.write_text(json.dumps({"messages": [{"role": "user", "content": "Hi"}]}) + "\n")
    cfg = load_config("configs/lora/lora_config_qwen_05b.yaml")
    cfg.data.train_file = str(train_file)
    cfg.output_dir = str(tmp_path / "run")

    trainer = LoRATrainer(cfg)
    with pytest.raises(ValueError, match="one user message and one assistant response"):
        trainer.train()


def test_export_adapter(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint"
    checkpoint.mkdir()
    (checkpoint / "trainer_state.json").write_text(
        json.dumps(
            {
                "method": "lora",
                "model": "Qwen/Qwen2.5-0.5B-Instruct",
                "train_file": "./data/train.jsonl",
                "dataset_id": "train@sha256:abc123",
                "dataset_version": "sha256:abc123",
                "dataset_sha256": "abc123",
                "epochs": 1,
            }
        )
    )
    (checkpoint / "adapter_config.json").write_text(
        json.dumps(
            {
                "format": "mock-peft-adapter",
                "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
            }
        )
    )
    (checkpoint / "adapter_model.safetensors").write_text("weights")
    output = export_adapter(checkpoint, tmp_path / "adapter")
    assert (output / "adapter_config.json").exists()
    assert (output / "adapter_model.safetensors").exists()
    assert (output / "export_manifest.json").exists()
    assert (tmp_path / "export_history.jsonl").exists()
    manifest = json.loads((output / "export_manifest.json").read_text())
    adapter_entry = file_artifact_entry(output, "adapter_model.safetensors")
    assert manifest["artifact_type"] == "finetune_adapter_export"
    assert manifest["status"] == "success"
    assert manifest["duration_seconds"] >= 0
    assert manifest["exported_file_count"] == 3
    assert manifest["base_model"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert manifest["adapter_format"] == "mock-peft-adapter"
    assert manifest["lineage"]["training_method"] == "lora"
    assert manifest["lineage"]["train_file"] == "./data/train.jsonl"
    assert manifest["lineage"]["dataset_id"] == "train@sha256:abc123"
    assert manifest["lineage"]["dataset_version"] == "sha256:abc123"
    assert adapter_entry in manifest["file_artifacts"]
    history = (tmp_path / "export_history.jsonl").read_text()
    assert '"dataset_id": "train@sha256:abc123"' in history
    assert '"dataset_version": "sha256:abc123"' in history
    assert '"adapter_model_sha256"' in history
    assert '"duration_seconds"' in history
    assert '"status": "success"' in history
    assert '"export_manifest_file"' in history
    export_report = build_export_history_report(
        tmp_path / "export_history.jsonl",
        dataset_id="train@sha256:abc123",
        model="Qwen/Qwen2.5-0.5B-Instruct",
    )
    assert export_report["report_type"] == "finetune_export_index"
    assert export_report["total_export_count"] == 1
    assert export_report["export_count"] == 1
    assert export_report["dataset_count"] == 1
    assert export_report["model_count"] == 1
    assert export_report["status_counts"] == {"success": 1}
    assert export_report["model_summaries"][0]["base_model"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert export_report["model_summaries"][0]["export_count"] == 1
    assert export_report["model_summaries"][0]["dataset_count"] == 1
    assert export_report["dataset_summaries"][0]["dataset_id"] == "train@sha256:abc123"
    assert export_report["dataset_summaries"][0]["export_count"] == 1
    assert export_report["dataset_summaries"][0]["model_count"] == 1
    assert export_report["total_duration_seconds"] >= 0
    assert export_report["average_duration_seconds"] is not None
    assert export_report["exports"][0]["output_dir"] == str(output)
    assert export_report["exports"][0]["export_manifest_file"] == str(output / "export_manifest.json")
    assert export_report["exports"][0]["status"] == "success"
    assert export_report["exports"][0]["duration_seconds"] >= 0
    assert export_report["model_summaries"][0]["latest_export_manifest_file"] == str(output / "export_manifest.json")
    assert export_report["dataset_summaries"][0]["latest_export_manifest_file"] == str(output / "export_manifest.json")
    export_markdown = render_export_history_markdown(export_report)
    assert "Finetune Export Index" in export_markdown
    assert "train@sha256:abc123" in export_markdown
    assert "Export Manifest" in export_markdown
    assert "Duration Seconds" in export_markdown
    assert "Model Summaries" in export_markdown
    assert "Dataset Summaries" in export_markdown
    export_json = save_export_history_report(export_report, tmp_path / "export_index.json")
    export_md = save_export_history_markdown(export_report, tmp_path / "export_index.md")
    assert export_json.exists()
    assert export_md.exists()


def test_cli_save_export(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint"
    checkpoint.mkdir()
    (checkpoint / "trainer_state.json").write_text("{}")
    (checkpoint / "adapter_config.json").write_text("{}")
    (checkpoint / "adapter_model.safetensors").write_text("weights")
    output = export_adapter(checkpoint, tmp_path / "saved")
    assert (output / "trainer_state.snapshot.json").exists()
    assert (output / "adapter_model.safetensors").exists()


def test_export_adapter_rejects_incomplete_checkpoint(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint"
    checkpoint.mkdir()
    with pytest.raises(FileNotFoundError, match="missing required adapter files"):
        export_adapter(checkpoint, tmp_path / "adapter")
