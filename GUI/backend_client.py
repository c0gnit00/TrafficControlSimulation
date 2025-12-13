import json
import os
import subprocess
import threading
from datetime import datetime

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(CURR_DIR, ".."))
BINARY_CANDIDATES = [
    os.path.join(CURR_DIR, "CPPBackend.exe"),
    os.path.join(ROOT, "CPPBackend", "x64", "Release", "CPPBackend.exe"),
]


class BackendClient:
    """Enhanced wrapper around the C++ backend process."""

    def __init__(self):
        self.proc = None
        self.lock = threading.Lock()

    def start(self):
        exe = next((p for p in BINARY_CANDIDATES if os.path.exists(p)), None)
        if not exe:
            raise FileNotFoundError("CPPBackend.exe not found. Build it first (Release x64).")
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
                raise RuntimeError("Backend not running")
            self.proc.stdin.write(line + "\n")
            self.proc.stdin.flush()
            return self.proc.stdout.readline().strip()

    def snapshot(self) -> dict:
        raw = self.send("SNAPSHOT")
        return json.loads(raw)

    def save_snapshot_file(self, path: str) -> bool:
        """Save current state to JSON file using C++ backend"""
        try:
            resp = self.send(f"SAVE {path}")
            return resp == "OK"
        except Exception as e:
            print(f"Save snapshot error: {e}")
            return False

    def load_snapshot_file(self, path: str) -> bool:
        """Load state from JSON file and reconstruct simulation"""
        try:
            with open(path, 'r') as f:
                snapshot = json.load(f)
            
            # Reset simulation first
            self.send("RESET")
            
            # Restore vehicles
            for vehicle in snapshot.get("vehicles", []):
                if vehicle.get("done") or vehicle.get("completed"):
                    continue
                
                path_nodes = vehicle.get("path", [])
                if len(path_nodes) < 2:
                    continue
                
                nodes_dict = {n["id"]: n for n in snapshot.get("nodes", [])}
                from_node = nodes_dict[vehicle["from"]]["name"]
                to_node = nodes_dict[vehicle["to"]]["name"]
                is_emergency = 1 if vehicle.get("emergency") else 0
                
                self.send(f"ROUTE {from_node} {to_node} {is_emergency}")
            
            # Restore incidents (blocked roads)
            for road in snapshot.get("roads", []):
                if road.get("incident"):
                    nodes_dict = {n["id"]: n for n in snapshot.get("nodes", [])}
                    from_name = nodes_dict[road["from"]]["name"]
                    to_name = nodes_dict[road["to"]]["name"]
                    self.send(f"BLOCK {from_name} {to_name}")
            
            # Restore maintenance
            for road in snapshot.get("roads", []):
                if road.get("maintenance"):
                    nodes_dict = {n["id"]: n for n in snapshot.get("nodes", [])}
                    from_name = nodes_dict[road["from"]]["name"]
                    to_name = nodes_dict[road["to"]]["name"]
                    self.send(f"MAINT {from_name} {to_name}")
            
            # Restore signal states
            for node in snapshot.get("nodes", []):
                green_state = 1 if node.get("green") else 0
                self.send(f"SET_SIGNAL {node['name']} {green_state}")
            
            return True
        except Exception as e:
            print(f"Load snapshot error: {e}")
            return False

    def export_logs(self, dest_path: str) -> bool:
        """Export current log file to specified location"""
        try:
            import shutil
            log_path = os.path.join(ROOT, "traffic_log_cpp.txt")
            if not os.path.exists(log_path):
                return False
            shutil.copy(log_path, dest_path)
            return True
        except Exception as e:
            print(f"Export logs error: {e}")
            return False

    def close(self):
        if self.proc and self.proc.poll() is None:
            try:
                self.send("QUIT")
            except Exception:
                pass
            self.proc.terminate()
