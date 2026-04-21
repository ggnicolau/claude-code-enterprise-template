from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "new_repo.py"
SPEC = importlib.util.spec_from_file_location("new_repo", MODULE_PATH)
assert SPEC and SPEC.loader
new_repo = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = new_repo
SPEC.loader.exec_module(new_repo)


def test_should_confirm_creation_skips_prompt_with_yes_flag() -> None:
    args = argparse.Namespace(yes=True)

    assert new_repo.should_confirm_creation(args, interactive=True) is False


def test_should_prompt_skips_all_questions_with_yes_flag() -> None:
    args = argparse.Namespace(yes=True)

    assert new_repo.should_prompt(args, interactive=True) is False


def test_should_confirm_creation_skips_prompt_when_non_interactive() -> None:
    args = argparse.Namespace(yes=False)

    assert new_repo.should_confirm_creation(args, interactive=False) is False


def test_resolve_workflow_identifier_accepts_matching_name(
    monkeypatch,
) -> None:
    def fake_list_workflows(
        env: dict[str, str],
        full_name: str,
    ) -> list[dict[str, object]]:
        assert env == {"GH_TOKEN": "token"}
        assert full_name == "owner/repo"
        return [
            {
                "id": 42,
                "name": "Setup Kanban",
                "path": ".github/workflows/setup-kanban.yml",
            }
        ]

    monkeypatch.setattr(new_repo, "list_workflows", fake_list_workflows)

    workflow_id = new_repo.resolve_workflow_identifier(
        env={"GH_TOKEN": "token"},
        full_name="owner/repo",
        workflow_name="Setup Kanban",
        workflow_file="setup-kanban.yml",
        retries=1,
        delay_seconds=0,
    )

    assert workflow_id == "42"


def test_resolve_workflow_identifier_accepts_matching_path_suffix(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        new_repo,
        "list_workflows",
        lambda env, full_name: [
            {
                "id": 99,
                "name": "Bootstrap",
                "path": ".github/workflows/setup-kanban.yml",
            }
        ],
    )

    workflow_id = new_repo.resolve_workflow_identifier(
        env={},
        full_name="owner/repo",
        workflow_name="Setup Kanban",
        workflow_file="setup-kanban.yml",
        retries=1,
        delay_seconds=0,
    )

    assert workflow_id == "99"


def test_parse_args_supports_skip_clone_flag() -> None:
    args = new_repo.parse_args(["--name", "demo", "--skip-clone"])

    assert args.name == "demo"
    assert args.skip_clone is True


def test_build_local_clone_path_uses_parent_of_template_root(tmp_path: Path) -> None:
    clone_path = new_repo.build_local_clone_path("demo", base_dir=tmp_path)

    assert clone_path == tmp_path / "demo"


def test_ensure_local_clone_absent_raises_when_destination_exists(tmp_path: Path) -> None:
    destination = tmp_path / "demo"
    destination.mkdir()

    try:
        new_repo.ensure_local_clone_absent(destination)
    except RuntimeError as exc:
        assert str(destination) in str(exc)
    else:
        raise AssertionError("Era esperado erro quando a pasta local ja existe.")
