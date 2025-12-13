import json
import os
import subprocess
import threading

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(CURR_DIR, ".."))
BINARY_CANDIDATES = [
    os.path.join(CURR_DIR, "CPPBackend.exe"),
    os.path.join(ROOT, "CPPBackend", "x64", "Release", "CPPBackend.exe"),
]


class BackendClient:
    """Thin wrapper around the C++ backend process."""

    def __init__(self):
        self.proc = None
        self.lock = threading.Lock()

    def start(self):
        exe = next((p for p in BINARY_CANDIDATES if os.path.exists(p)), None)
        if not exe:
            raise FileNotFoundError("traffic_core binary not found. Build it with CMake/VS first.")
        self.proc = subprocess.Popen(
            [exe, "--serve"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def send(self, line: str) -> str:
        with self.lock:
            if not self.proc or self.proc.poll() is not None:
                raise RuntimeError("backend not running")
            self.proc.stdin.write(line + "\n")
            self.proc.stdin.flush()
            return self.proc.stdout.readline().strip()

    def snapshot(self) -> dict:
        raw = self.send("SNAPSHOT")
        return json.loads(raw)

    def close(self):
        if self.proc and self.proc.poll() is None:
            try:
                self.send("QUIT")
            except Exception:
                pass
            self.proc.terminate()

