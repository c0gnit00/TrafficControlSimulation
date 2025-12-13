import tkinter as tk


class MapView(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#0b1220", highlightthickness=0, **kwargs)

    def render(self, snapshot: dict):
        self.delete("all")
        nodes = {n["id"]: n for n in snapshot.get("nodes", [])}
        if not nodes:
            return
        # Compute bounding box to center network
        xs = [n["x"] for n in nodes.values()]
        ys = [n["y"] for n in nodes.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = self.winfo_width() or 1200
        height = self.winfo_height() or 800
        margin = 60
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)
        offset_x = (width - span_x) / 2 - min_x
        offset_y = (height - span_y) / 2 - min_y

        def tx(x):
            return x + offset_x

        def ty(y):
            return y + offset_y

        # Roads
        for road in snapshot.get("roads", []):
            u = nodes.get(road["from"])
            v = nodes.get(road["to"])
            if not u or not v:
                continue
            congestion = road.get("c", 0.0)
            if road.get("incident"):
                color = "#ef4444"
            elif road.get("maintenance"):
                color = "#f59e0b"
            else:
                if congestion > 0.66:
                    color = "#dc2626"
                elif congestion > 0.33:
                    color = "#f59e0b"
                else:
                    color = "#10b981"
            self.create_line(tx(u["x"]), ty(u["y"]), tx(v["x"]), ty(v["y"]), fill=color, width=6, capstyle="round")
            cx = (tx(u["x"]) + tx(v["x"])) / 2
            cy = (ty(u["y"]) + ty(v["y"])) / 2
            self.create_text(cx, cy, text=f"{int(congestion*100)}%", fill="#d1d5db", font=("Segoe UI", 9))

        # Vehicles
        for vehicle in snapshot.get("vehicles", []):
            path = vehicle.get("path", [])
            if len(path) < 2 or vehicle.get("done"):
                continue
            p = vehicle.get("progress", 0.0)
            idx = int(vehicle.get("pathIndex", 0))
            from_id = path[min(idx, len(path) - 2)]
            to_id = path[min(idx + 1, len(path) - 1)]
            u = nodes.get(from_id)
            v = nodes.get(to_id)
            if not u or not v:
                continue
            x = tx(u["x"] + (v["x"] - u["x"]) * p)
            y = ty(u["y"] + (v["y"] - u["y"]) * p)
            color = "#ef4444" if vehicle.get("emergency") else "#3b82f6"
            self.create_oval(x - 8, y - 8, x + 8, y + 8, fill=color, outline="#ffffff", width=2)

        # Intersections (larger circles with node names inside)
        for node in nodes.values():
            fill = "#22c55e" if node.get("green") else "#ef4444"
            x = tx(node["x"])
            y = ty(node["y"])
            # Increased circle size from 18 to 24
            self.create_oval(x - 24, y - 24, x + 24, y + 24, fill=fill, outline="#0b1220", width=3)
            # Draw node name inside the circle
            self.create_text(x, y, text=node["name"], fill="#ffffff", font=("Segoe UI", 14, "bold"))