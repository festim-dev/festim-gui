import time
from pathlib import Path

from festim_gui.execution import (
    FESTIM_GUI_TMP_ENV_VAR,
    ScriptExecutionManager,
    resolve_run_root,
)


def test_resolve_run_root_uses_env_var(monkeypatch, tmp_path):
    run_root = tmp_path / "festim-runs"
    monkeypatch.setenv(FESTIM_GUI_TMP_ENV_VAR, str(run_root))

    resolved = resolve_run_root()

    assert resolved == run_root
    assert resolved.is_dir()


def test_script_execution_manager_runs_script(monkeypatch, tmp_path):
    run_root = tmp_path / "festim-runs"
    monkeypatch.setenv(FESTIM_GUI_TMP_ENV_VAR, str(run_root))

    manager = ScriptExecutionManager()
    manager.start(
        "\n".join(
            [
                "from pathlib import Path",
                'print("hello from test")',
                'output_dir = Path("out")',
                "output_dir.mkdir(exist_ok=True)",
                '(output_dir / "result.txt").write_text("done\\n", encoding="utf-8")',
                "",
            ]
        )
    )

    events = []
    deadline = time.time() + 5
    while time.time() < deadline:
        events.extend(manager.drain_events())
        if any(event.kind == "finished" for event in events):
            break
        time.sleep(0.05)

    started = next(event for event in events if event.kind == "started")
    finished = next(event for event in events if event.kind == "finished")
    output_dir = Path(started.output_dir)

    assert any(
        event.kind == "log" and "hello from test" in event.text for event in events
    )
    assert output_dir.is_dir()
    assert (output_dir / "script.py").is_file()
    assert (output_dir / "run.log").is_file()
    assert (output_dir / "out" / "result.txt").read_text(encoding="utf-8") == "done\n"
    assert finished.return_code == 0
    assert not manager.is_running
