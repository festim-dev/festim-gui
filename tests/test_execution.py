import time
import zipfile
from pathlib import Path

from festim_gui import execution
from festim_gui.execution import (
    ScriptExecutionManager,
    read_latest_run_record,
    resolve_run_root,
)


def test_resolve_run_root_uses_system_tempdir(monkeypatch, tmp_path):
    monkeypatch.setattr(execution.tempfile, "gettempdir", lambda: str(tmp_path))

    resolved = resolve_run_root()

    assert resolved == tmp_path


def test_script_execution_manager_runs_script(monkeypatch, tmp_path):
    monkeypatch.setattr(execution.tempfile, "gettempdir", lambda: str(tmp_path))

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


def test_script_execution_manager_records_latest_vtx_output(monkeypatch, tmp_path):
    monkeypatch.setattr(execution.tempfile, "gettempdir", lambda: str(tmp_path))

    manager = ScriptExecutionManager()
    manager.start(
        "\n".join(
            [
                "from pathlib import Path",
                'output_dir = Path("out") / "field_export.bp"',
                "output_dir.mkdir(parents=True, exist_ok=True)",
                '(output_dir / "data.0").write_text("bp data\\n", encoding="utf-8")',
                'print("created vtx output")',
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

    finished = next(event for event in events if event.kind == "finished")
    latest_run = read_latest_run_record()

    assert finished.return_code == 0
    assert any(Path(p).match("out/field_export.bp") for p in finished.vtx_paths)
    assert Path(finished.results_archive_path).is_file()
    with zipfile.ZipFile(finished.results_archive_path) as archive:
        assert archive.namelist() == ["field_export.bp/data.0"]
    assert latest_run is not None
    assert latest_run["vtx_paths"] == finished.vtx_paths
    assert latest_run["results_archive_path"] == finished.results_archive_path
