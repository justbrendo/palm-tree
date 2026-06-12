import json
import subprocess

import typer
from typer.testing import CliRunner

from palm_tree.cli import app


runner = CliRunner()


def invoke_help(command):
    return runner.invoke(
        app,
        [command, "--help"],
        env={"COLUMNS": "120", "NO_COLOR": "1", "TERM": "dumb"},
    )


def test_cli_app_is_typer_app():
    assert isinstance(app, typer.Typer)


def test_cli_app_can_show_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Mine repositories for maintenance and evolution signals." in result.output


def test_info_command_exists():
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0


def test_version_command_exists():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0


def test_version_command_prints_package_version(monkeypatch):
    monkeypatch.setattr("palm_tree.cli.package_version", lambda name: "1.2.3")

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "palm-tree 1.2.3" in result.output


def test_info_command_has_repo_option():
    result = invoke_help("info")

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_info_command_accepts_repo_option(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)

    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_info_command_reports_git_repository(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)

    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "Git repository: yes" in result.output


def test_info_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_summary_command_exists():
    result = runner.invoke(app, ["summary"])

    assert result.exit_code == 0


def test_summary_command_has_repo_option():
    result = invoke_help("summary")

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_summary_command_has_json_option():
    result = invoke_help("summary")

    assert result.exit_code == 0
    assert "--json" in result.output


def test_summary_command_prints_repository_summary(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_repository_summary",
        lambda repo: {
            "changed_files": 2,
            "cochange_pairs": 1,
            "commits": 3,
            "total_added": 13,
            "total_churn": 20,
            "total_deleted": 7,
        },
    )

    result = runner.invoke(app, ["summary", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "metric\tvalue" in result.output
    assert "commits\t3" in result.output
    assert "changed_files\t2" in result.output
    assert "cochange_pairs\t1" in result.output
    assert "total_churn\t20" in result.output


def test_summary_command_prints_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_repository_summary",
        lambda repo: {
            "changed_files": 2,
            "cochange_pairs": 1,
            "commits": 3,
            "total_added": 13,
            "total_churn": 20,
            "total_deleted": 7,
        },
    )

    result = runner.invoke(app, ["summary", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "changed_files": 2,
        "cochange_pairs": 1,
        "commits": 3,
        "total_added": 13,
        "total_churn": 20,
        "total_deleted": 7,
    }


def test_summary_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["summary", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_hotspots_command_exists():
    result = runner.invoke(app, ["hotspots"])

    assert result.exit_code == 0


def test_cochanges_command_exists():
    result = runner.invoke(app, ["cochanges"])

    assert result.exit_code == 0


def test_cochanges_command_has_repo_option():
    result = invoke_help("cochanges")

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_cochanges_command_has_limit_option():
    result = invoke_help("cochanges")

    assert result.exit_code == 0
    assert "--limit" in result.output


def test_cochanges_command_has_min_count_option():
    result = invoke_help("cochanges")

    assert result.exit_code == 0
    assert "--min-count" in result.output


def test_cochanges_command_has_json_option():
    result = invoke_help("cochanges")

    assert result.exit_code == 0
    assert "--json" in result.output


def test_cochanges_command_accepts_repo_option(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_cochanges_command_reports_no_cochanges(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_cochanges", lambda repo: [])

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "No cochanges found." in result.output


def test_cochanges_command_reads_cochanges(monkeypatch, tmp_path):
    calls = []

    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_cochanges",
        lambda repo: calls.append(repo) or [],
    )

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert calls == [tmp_path]


def test_cochanges_command_prints_ranked_pairs(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_cochanges",
        lambda repo: [
            {"left": "README.md", "right": "tests/test_cli.py", "count": 2},
            {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 1},
        ],
    )

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "count\tleft\tright" in result.output
    assert "2\tREADME.md\ttests/test_cli.py" in result.output
    assert "1\tREADME.md\tsrc/palm_tree/cli.py" in result.output


def test_cochanges_command_limits_output(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_cochanges",
        lambda repo: [
            {"left": "README.md", "right": "tests/test_cli.py", "count": 3},
            {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 2},
            {"left": "src/palm_tree/cli.py", "right": "tests/test_cli.py", "count": 1},
        ],
    )

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path), "--limit", "2"])

    assert result.exit_code == 0
    assert "3\tREADME.md\ttests/test_cli.py" in result.output
    assert "2\tREADME.md\tsrc/palm_tree/cli.py" in result.output
    assert "1\tsrc/palm_tree/cli.py\ttests/test_cli.py" not in result.output


def test_cochanges_command_filters_by_min_count(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_cochanges",
        lambda repo: [
            {"left": "README.md", "right": "tests/test_cli.py", "count": 3},
            {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 2},
            {"left": "src/palm_tree/cli.py", "right": "tests/test_cli.py", "count": 1},
        ],
    )

    result = runner.invoke(
        app, ["cochanges", "--repo", str(tmp_path), "--min-count", "2"]
    )

    assert result.exit_code == 0
    assert "3\tREADME.md\ttests/test_cli.py" in result.output
    assert "2\tREADME.md\tsrc/palm_tree/cli.py" in result.output
    assert "1\tsrc/palm_tree/cli.py\ttests/test_cli.py" not in result.output


def test_cochanges_command_prints_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_cochanges",
        lambda repo: [
            {"left": "README.md", "right": "tests/test_cli.py", "count": 2},
            {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 1},
        ],
    )

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == [
        {"left": "README.md", "right": "tests/test_cli.py", "count": 2},
        {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 1},
    ]


def test_cochanges_command_prints_empty_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_cochanges", lambda repo: [])

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == []


def test_cochanges_command_rejects_non_positive_limit(tmp_path):
    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path), "--limit", "0"])

    assert result.exit_code != 0
    assert "Invalid value" in result.output


def test_cochanges_command_rejects_non_positive_min_count(tmp_path):
    result = runner.invoke(
        app, ["cochanges", "--repo", str(tmp_path), "--min-count", "0"]
    )

    assert result.exit_code != 0
    assert "Invalid value" in result.output


def test_cochanges_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_hotspots_command_has_repo_option():
    result = invoke_help("hotspots")

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_hotspots_command_has_limit_option():
    result = invoke_help("hotspots")

    assert result.exit_code == 0
    assert "--limit" in result.output


def test_hotspots_command_has_min_churn_option():
    result = invoke_help("hotspots")

    assert result.exit_code == 0
    assert "--min-churn" in result.output


def test_hotspots_command_has_json_option():
    result = invoke_help("hotspots")

    assert result.exit_code == 0
    assert "--json" in result.output


def test_hotspots_command_accepts_repo_option(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_hotspots_command_reports_no_hotspots(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "No hotspots found." in result.output


def test_hotspots_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_hotspots_command_prints_ranked_files(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "churn\tadded\tdeleted\tpath" in result.output
    assert "12\t10\t2\tREADME.md" in result.output
    assert "4\t0\t4\tsrc/palm_tree/cli.py" in result.output


def test_hotspots_command_limits_output(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "tests/test_cli.py", "added": 4, "deleted": 2, "churn": 6},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--limit", "2"])

    assert result.exit_code == 0
    assert "12\t10\t2\tREADME.md" in result.output
    assert "6\t4\t2\ttests/test_cli.py" in result.output
    assert "4\t0\t4\tsrc/palm_tree/cli.py" not in result.output


def test_hotspots_command_filters_by_min_churn(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "tests/test_cli.py", "added": 4, "deleted": 2, "churn": 6},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(
        app, ["hotspots", "--repo", str(tmp_path), "--min-churn", "6"]
    )

    assert result.exit_code == 0
    assert "12\t10\t2\tREADME.md" in result.output
    assert "6\t4\t2\ttests/test_cli.py" in result.output
    assert "4\t0\t4\tsrc/palm_tree/cli.py" not in result.output


def test_hotspots_command_rejects_non_positive_limit(tmp_path):
    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--limit", "0"])

    assert result.exit_code != 0
    assert "Invalid value" in result.output


def test_hotspots_command_rejects_negative_min_churn(tmp_path):
    result = runner.invoke(
        app, ["hotspots", "--repo", str(tmp_path), "--min-churn", "-1"]
    )

    assert result.exit_code != 0
    assert "Invalid value" in result.output


def test_hotspots_command_prints_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == [
        {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
    ]


def test_hotspots_command_limits_json_output(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "tests/test_cli.py", "added": 4, "deleted": 2, "churn": 6},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(
        app, ["hotspots", "--repo", str(tmp_path), "--limit", "2", "--json"]
    )

    assert result.exit_code == 0
    assert json.loads(result.output) == [
        {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
        {"path": "tests/test_cli.py", "added": 4, "deleted": 2, "churn": 6},
    ]


def test_hotspots_command_prints_empty_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == []


def test_hotspots_command_handles_real_empty_git_history(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "No hotspots found." in result.output


def test_hotspots_command_reads_real_git_history(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Add readme"], cwd=tmp_path, check=True)

    readme.write_text("hello\nworld\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update readme"], cwd=tmp_path, check=True)

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "churn\tadded\tdeleted\tpath" in result.output
    assert "2\t2\t0\tREADME.md" in result.output


def test_cochanges_command_reads_real_git_history(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    cli = tmp_path / "cli.py"
    readme.write_text("hello\n")
    cli.write_text("print('hello')\n")
    subprocess.run(["git", "add", "README.md", "cli.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Add readme and cli"], cwd=tmp_path, check=True)

    readme.write_text("hello\nworld\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update readme"], cwd=tmp_path, check=True)

    result = runner.invoke(app, ["cochanges", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "count\tleft\tright" in result.output
    assert "1\tREADME.md\tcli.py" in result.output


def test_summary_command_reads_real_git_history(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    cli = tmp_path / "cli.py"
    readme.write_text("hello\n")
    cli.write_text("print('hello')\n")
    subprocess.run(["git", "add", "README.md", "cli.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Add readme and cli"], cwd=tmp_path, check=True)

    readme.write_text("hello\nworld\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update readme"], cwd=tmp_path, check=True)

    result = runner.invoke(app, ["summary", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "metric\tvalue" in result.output
    assert "commits\t2" in result.output
    assert "changed_files\t2" in result.output
    assert "cochange_pairs\t1" in result.output
    assert "total_churn\t3" in result.output
