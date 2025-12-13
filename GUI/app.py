import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from backend_client import BackendClient
from map_view import MapView
from control_panel import ControlPanel
from analytics_panel import AnalyticsPanel
from log_viewer import LogViewer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart City Traffic Control")
        self.geometry("1400x850")
        self.configure(bg="#0b1220")

        self.backend = BackendClient()
        try:
            self.backend.start()
        except Exception as exc:
            messagebox.showerror("Backend error", str(exc))
            sys.exit(1)

        self.snapshot = self.backend.snapshot()
        names = [n["name"] for n in self.snapshot.get("nodes", [])]

        # Layout
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = MapView(self)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        right = tk.Frame(self, bg="#0b1220")
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right.columnconfigure(0, weight=1)

        self.controls = ControlPanel(
            right,
            names,
            on_add=self._add_vehicle,
            on_emergency=self._add_emergency,
            on_incident=self._incident,
            on_clear=self._clear_incidents,
            on_reset=self._reset,
            on_signal=self._set_signal,
            on_block=self._block,
            on_maint=self._maintenance,
            on_save=self._save_snapshot,
            on_load=self._load_snapshot,
        )
        self.controls.grid(row=0, column=0, sticky="ew", pady=(15, 5), padx=(10, 10))

        self.analytics = AnalyticsPanel(right)
        self.analytics.grid(row=1, column=0, sticky="ew", pady=(5, 10), padx=(10, 10))

        # Style the Open Logs button to match other buttons
        style = ttk.Style()
        style.configure("Secondary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#334155", foreground="#f8fafc", relief="flat", borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#1f2937")], relief=[("pressed", "flat")])
        open_logs_frame = tk.Frame(right, bg="#0b1220")
        open_logs_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15), padx=(10, 10))
        open_logs_frame.columnconfigure(0, weight=1)
        ttk.Button(open_logs_frame, text="Open Logs", style="Secondary.TButton", command=self._open_logs).grid(row=0, column=0, sticky="ew")

        self.after(200, self._tick)

    def _add_vehicle(self, start, end, vtype):
        resp = self.backend.send(f"ROUTE {start} {end} 0")
        return resp == "OK"

    def _add_emergency(self, start, end, vtype):
        resp = self.backend.send(f"ROUTE {start} {end} 1")
        return resp == "OK"

    def _incident(self):
        self.backend.send("INCIDENT")

    def _clear_incidents(self):
        self.backend.send("CLEAR")

    def _reset(self):
        self.backend.send("RESET")

    def _set_signal(self, node, green):
        resp = self.backend.send(f"SET_SIGNAL {node} {1 if green else 0}")
        return resp == "OK"

    def _block(self, a, b, on):
        cmd = "BLOCK" if on else "UNBLOCK"
        resp = self.backend.send(f"{cmd} {a} {b}")
        return resp == "OK"

    def _maintenance(self, a, b, on):
        cmd = "MAINT" if on else "UNMAINT"
        resp = self.backend.send(f"{cmd} {a} {b}")
        return resp == "OK"

    def _save_snapshot(self, path):
        resp = self.backend.send(f"SAVE {path}")
        return resp == "OK"

    def _load_snapshot(self, path):
        messagebox.showinfo("Load Snapshot", "Load is not yet implemented in the backend.")
        return False

    def _open_logs(self):
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "traffic_log_cpp.txt"))
        LogViewer(self, log_path)

    def _tick(self):
        try:
            self.backend.send("STEP")
            self.snapshot = self.backend.snapshot()
            self.canvas.render(self.snapshot)
            self.analytics.update_stats(self.snapshot)
        except Exception as exc:
            messagebox.showerror("Backend crashed", str(exc))
            self.backend.close()
            return
        self.after(200, self._tick)

    def on_close(self):
        self.backend.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

