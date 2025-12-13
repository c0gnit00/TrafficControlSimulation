import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime

from backend_client import BackendClient
from map_view import MapView
from control_panel import ControlPanel
from analytics_panel import AnalyticsPanel
from log_viewer import LogViewer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart City Traffic Control System")
        self.geometry("1400x850")
        self.configure(bg="#0b1220")

        self.backend = BackendClient()
        try:
            self.backend.start()
        except Exception as exc:
            messagebox.showerror("Backend Error", 
                f"Failed to start C++ backend:\n{exc}\n\n"
                "Ensure CPPBackend.exe is built (Release x64).")
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
        right.rowconfigure(0, weight=0)
        right.rowconfigure(1, weight=0)
        right.rowconfigure(2, weight=1)
        right.rowconfigure(3, weight=0)

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

        # Bottom buttons
        style = ttk.Style()
        style.configure("Action.TButton", 
            padding=12, 
            font=("Segoe UI", 11, "bold"), 
            background="#334155", 
            foreground="#f8fafc", 
            relief="flat", 
            borderwidth=0
        )
        style.map("Action.TButton", 
            background=[("active", "#1f2937")], 
            relief=[("pressed", "flat")]
        )

        bottom_frame = tk.Frame(right, bg="#0b1220")
        bottom_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=(10, 10))
        bottom_frame.columnconfigure(0, weight=1)

        ttk.Button(
            bottom_frame, 
            text="Open Logs", 
            style="Action.TButton", 
            command=self._open_logs
        ).grid(row=0, column=0, sticky="ew", pady=2)

        ttk.Button(
            bottom_frame, 
            text="Export Logs", 
            style="Action.TButton", 
            command=self._export_logs
        ).grid(row=1, column=0, sticky="ew", pady=2)

        self.after(200, self._tick)

    def _add_vehicle(self, start, end, vtype):
        if start == end:
            messagebox.showwarning("Invalid Route", "Start and end must be different!")
            return False
        resp = self.backend.send(f"ROUTE {start} {end} 0")
        if resp == "OK":
            messagebox.showinfo("Success", f"Normal vehicle added: {start} → {end}")
            return True
        else:
            messagebox.showerror("Error", "Could not add vehicle. No valid route.")
            return False

    def _add_emergency(self, start, end, vtype):
        if start == end:
            messagebox.showwarning("Invalid Route", "Start and end must be different!")
            return False
        resp = self.backend.send(f"ROUTE {start} {end} 1")
        if resp == "OK":
            messagebox.showinfo("Success", f"Emergency vehicle added: {start} → {end}")
            return True
        else:
            messagebox.showerror("Error", "Could not add emergency vehicle.")
            return False

    def _incident(self):
        resp = self.backend.send("INCIDENT")
        if resp == "OK":
            messagebox.showinfo("Incident Reported", 
                "⚠️ Traffic incident created!\n\n"
                "A random road has been blocked.\n"
                "Active vehicles will reroute automatically.")
        else:
            messagebox.showerror("Error", "Could not create incident.")

    def _clear_incidents(self):
        resp = self.backend.send("CLEAR")
        if resp == "OK":
            messagebox.showinfo("Incidents Cleared", 
                "All incidents cleared!\n\n"
                "All roads are now accessible.\n"
                "Vehicles will recalculate optimal routes.")
        else:
            messagebox.showerror("Error", "Could not clear incidents.")

    def _reset(self):
        result = messagebox.askyesno("Reset Simulation", 
            "Are you sure you want to reset?\n\n"
            "This will:\n"
            "• Remove all vehicles\n"
            "• Clear all incidents\n"
            "• Reset signal timings\n"
            "• Clear maintenance flags")
        
        if result:
            resp = self.backend.send("RESET")
            if resp == "OK":
                messagebox.showinfo("Reset Complete", "Simulation reset to initial state.")

    def _set_signal(self, node, green):
        resp = self.backend.send(f"SET_SIGNAL {node} {1 if green else 0}")
        return resp == "OK"

    def _block(self, a, b, on):
        cmd = "BLOCK" if on else "UNBLOCK"
        resp = self.backend.send(f"{cmd} {a} {b}")
        if resp == "OK":
            action = "blocked" if on else "unblocked"
            messagebox.showinfo("Road Control", f"Road {a} ↔ {b} {action}.")
            return True
        return False

    def _maintenance(self, a, b, on):
        cmd = "MAINT" if on else "UNMAINT"
        resp = self.backend.send(f"{cmd} {a} {b}")
        if resp == "OK":
            action = "enabled" if on else "disabled"
            messagebox.showinfo("Maintenance", f"Maintenance {action}: {a} ↔ {b}")
            return True
        return False

    def _save_snapshot(self, path):
        ok = self.backend.save_snapshot_file(path)
        if ok:
            messagebox.showinfo("Snapshot Saved", 
                f"Saved to: {path}\n\n"
                "Includes: vehicles, roads, incidents, signals")
        else:
            messagebox.showerror("Save Failed", "Could not save snapshot.")
        return ok

    def _load_snapshot(self, path):
        result = messagebox.askyesno("Load Snapshot",
            "Loading will reset current simulation.\n\nContinue?")
        
        if not result:
            return False
        
        ok = self.backend.load_snapshot_file(path)
        if ok:
            messagebox.showinfo("Snapshot Loaded",
                f"Loaded from: {path}\n\n"
                "Restored: vehicles, incidents, signals")
        else:
            messagebox.showerror("Load Failed", "Invalid snapshot file.")
        return ok

    def _open_logs(self):
        log_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "traffic_log_cpp.txt"
        ))
        if not os.path.exists(log_path):
            messagebox.showinfo("No Logs", 
                "No log file found yet.\n\n"
                "Logs are created automatically as you use the system.")
            return
        LogViewer(self, log_path)

    def _export_logs(self):
        dest = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export Logs",
            initialfile=f"traffic_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not dest:
            return
        
        ok = self.backend.export_logs(dest)
        if ok:
            messagebox.showinfo("Logs Exported", f"Exported to: {dest}")
        else:
            messagebox.showerror("Export Failed", "Could not export logs.")

    def _tick(self):
        try:
            self.backend.send("STEP")
            self.snapshot = self.backend.snapshot()
            self.canvas.render(self.snapshot)
            self.analytics.update_stats(self.snapshot)
        except Exception as exc:
            messagebox.showerror("Backend Crashed", f"Backend stopped:\n{exc}")
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
