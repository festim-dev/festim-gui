import os
import queue
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path

FESTIM_GUI_TMP_ENV_VAR = "FESTIM_GUI_TMP"


@dataclass(slots=True)
class ExecutionEvent:
    kind: str
    text: str = ""
    output_dir: str = ""
    log_path: str = ""
    return_code: int | None = None


@dataclass(slots=True)
class ActiveRun:
    output_dir: Path
    log_path: Path
    process: subprocess.Popen


def resolve_run_root() -> Path:
    configured_root = os.environ.get(FESTIM_GUI_TMP_ENV_VAR)
    run_root = (
        Path(configured_root).expanduser()
        if configured_root
        else Path(tempfile.gettempdir())
    )
    run_root.mkdir(parents=True, exist_ok=True)

    if not os.access(run_root, os.W_OK | os.X_OK):
        msg = f"Run root is not writable: {run_root}"
        raise RuntimeError(msg)

    return run_root


class ScriptExecutionManager:
    def __init__(self):
        self._event_queue = queue.SimpleQueue()
        self._lock = threading.Lock()
        self._active_run = None

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self._active_run is not None

    def drain_events(self) -> list[ExecutionEvent]:
        events = []
        while True:
            try:
                events.append(self._event_queue.get_nowait())
            except queue.Empty:
                return events

    def start(self, script_text: str) -> ActiveRun:
        with self._lock:
            if self._active_run is not None:
                msg = "A simulation is already running."
                raise RuntimeError(msg)

            run_root = resolve_run_root()
            run_dir = Path(tempfile.mkdtemp(prefix="festim-gui-", dir=run_root))
            script_path = run_dir / "generated.py"
            log_path = run_dir / "run.log"
            script_path.write_text(script_text, encoding="utf-8")

            process = subprocess.Popen(
                [sys.executable, "-u", script_path.name],
                cwd=run_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            run = ActiveRun(
                output_dir=run_dir,
                log_path=log_path,
                process=process,
            )
            self._active_run = run

        self._event_queue.put(
            ExecutionEvent(
                kind="started",
                output_dir=str(run.output_dir),
                log_path=str(run.log_path),
            )
        )

        threading.Thread(target=self._stream_run, args=(run,), daemon=True).start()
        return run

    # TODO: support stop/cancel for the active process from the Run page.
    def _stream_run(self, run: ActiveRun) -> None:
        return_code = None

        try:
            with run.log_path.open("w", encoding="utf-8") as log_file:
                stdout = run.process.stdout
                if stdout is None:
                    msg = "Simulation process did not expose a stdout stream."
                    raise RuntimeError(msg)

                for line in stdout:
                    log_file.write(line)
                    log_file.flush()
                    self._event_queue.put(
                        ExecutionEvent(
                            kind="log",
                            text=line,
                        )
                    )

                return_code = run.process.wait()
        except Exception as exc:
            self._event_queue.put(
                ExecutionEvent(
                    kind="error",
                    text=f"[festim-gui] {exc}\n",
                )
            )
            return_code = run.process.wait()
        finally:
            if run.process.stdout is not None:
                run.process.stdout.close()

            self._event_queue.put(
                ExecutionEvent(
                    kind="finished",
                    output_dir=str(run.output_dir),
                    log_path=str(run.log_path),
                    return_code=return_code,
                )
            )

            with self._lock:
                if self._active_run is run:
                    self._active_run = None
