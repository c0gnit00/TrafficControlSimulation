import tkinter as tk


class AnalyticsPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f172a")
        self.stats_var = tk.StringVar(value="")
        self.time_var = tk.StringVar(value="")
        self.columnconfigure(0, weight=1)
        tk.Label(self, text="Analytics", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", pady=(15, 0), padx=(20, 20))
        tk.Label(self, textvariable=self.time_var, fg="#9ca3af", bg="#0f172a", font=("Consolas", 11)).grid(row=1, column=0, sticky="w", pady=2, padx=(20, 20))
        tk.Label(self, textvariable=self.stats_var, fg="#10b981", bg="#0f172a", font=("Consolas", 11), justify="left").grid(row=2, column=0, sticky="w", pady=6, padx=(20, 20))

    def update_stats(self, snapshot: dict):
        stats = snapshot.get("stats", {})
        time_val = snapshot.get("time", 0.0)
        self.time_var.set(f"Sim Time: {time_val:.1f}h")
        self.stats_var.set(
            f"Vehicles: {stats.get('totalVehicles',0)}  Emerg: {stats.get('emergencyVehicles',0)}\n"
            f"Routes: {stats.get('routesCalculated',0)}  Incidents: {stats.get('incidentsReported',0)}\n"
            f"Distance: {stats.get('totalDistance',0):.1f}"
        )

