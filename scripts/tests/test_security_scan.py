from __future__ import annotations

from scripts.security_scan import ROOT, local_username, risky_filename_issue, scan_text_file


def test_security_scan_flags_high_confidence_secret_shapes() -> None:
    local_path = "/" + "Users" + "/example/project/.env"
    issues = scan_text_file(
        ROOT / "README.md",
        "\n".join(
            [
                "OPENAI_API_KEY=sk-" + "a" * 32,
                f"local_path={local_path}",
            ]
        ),
    )

    assert {issue.check for issue in issues} == {
        "OpenAI-style long key",
        "Local absolute path",
    }


def test_security_scan_flags_personal_markers_without_storing_examples() -> None:
    personal_email = "learner" + "@gmail.com"
    phone_number = "138" + "0013" + "8000"
    national_id = "110101" + "19900101" + "123X"

    issues = scan_text_file(
        ROOT / "README.md",
        "\n".join([personal_email, phone_number, national_id]),
    )

    assert {issue.check for issue in issues} == {
        "Personal email address",
        "Potential phone number",
        "Potential Chinese national ID",
    }


def test_security_scan_flags_local_username_when_available() -> None:
    username = local_username()
    if username is None:
        return

    issues = scan_text_file(ROOT / "README.md", f"owner={username}")

    assert any(issue.check == "Local username" for issue in issues)


def test_security_scan_flags_risky_public_file_types() -> None:
    assert risky_filename_issue(ROOT / ".env") is not None
    assert risky_filename_issue(ROOT / ".env.local") is not None
    assert risky_filename_issue(ROOT / "adapter_model.safetensors") is not None
    assert risky_filename_issue(ROOT / "train.log") is not None
    assert risky_filename_issue(ROOT / "secret.pem") is not None


def test_security_scan_allows_public_env_examples() -> None:
    assert risky_filename_issue(ROOT / ".env.example") is None
    assert risky_filename_issue(ROOT / "projects" / "ai-gateway" / ".env.example") is None
