# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog


# class ControlPanel(tk.Frame):
#     def __init__(self, master, names, on_add, on_emergency, on_incident, on_clear, on_reset, on_signal, on_block, on_maint, on_save, on_load):
#         super().__init__(master, bg="#0f172a")
#         self.names = names
#         self.on_add = on_add
#         self.on_emergency = on_emergency
#         self.on_incident = on_incident
#         self.on_clear = on_clear
#         self.on_reset = on_reset
#         self.on_signal = on_signal
#         self.on_block = on_block
#         self.on_maint = on_maint
#         self.on_save = on_save
#         self.on_load = on_load

#         style = ttk.Style()
#         style.theme_use("clam")
#         btn_bg = "#2563eb"
#         btn_fg = "#f8fafc"
#         style.configure("Primary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background=btn_bg, foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Primary.TButton", background=[("active", "#1d4ed8")], relief=[("pressed", "flat")])
#         style.configure("Emergency.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Emergency.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
#         style.configure("Secondary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#334155", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Secondary.TButton", background=[("active", "#1f2937")], relief=[("pressed", "flat")])
#         style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 10))
#         # Enhanced beautiful comboboxes with better styling
#         style.configure("TCombobox", padding=12, font=("Segoe UI", 11, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
#         style.configure("Small.TCombobox", padding=10, font=("Segoe UI", 10, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("Small.TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
#         # Note: Using tk.Checkbutton instead of ttk for better control over checkmark appearance
#         self.columnconfigure(0, weight=1)

#         tk.Label(self, text="Routes", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=(20, 20))

#         self.start_var = tk.StringVar(value=names[0])
#         self.end_var = tk.StringVar(value=names[-1])
#         self.type_var = tk.StringVar(value="auto")

#         form = tk.Frame(self, bg="#0f172a")
#         form.grid(row=1, column=0, sticky="ew", pady=(6, 6), padx=(20, 20))
#         form.columnconfigure(1, weight=1)
#         tk.Label(form, text="Start", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.start_var, values=names, width=18, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="End", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.end_var, values=names, width=18, style="TCombobox").grid(row=1, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="Vehicle", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.type_var, values=["auto", "car", "bus", "bike", "truck"], width=18, style="TCombobox").grid(row=2, column=1, sticky="ew", padx=5, pady=4)

#         # Routes buttons in 2-column layout with equal widths
#         routes_btn_frame = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame.grid(row=2, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame, text="Add Normal Route", style="Primary.TButton", command=self._add).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame, text="Add Emergency Route", style="Emergency.TButton", command=self._add_emergency).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         routes_btn_frame2 = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame2.grid(row=3, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame2.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame2.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame2, text="Report Incident", style="Secondary.TButton", command=self.on_incident).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame2, text="Clear Incidents", style="Secondary.TButton", command=self.on_clear).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         ttk.Button(self, text="Reset Simulation", style="Secondary.TButton", command=self.on_reset).grid(row=4, column=0, sticky="ew", pady=2, padx=(20, 20))

#         # Manual overrides - clean and compact layout
#         tk.Label(self, text="Manual Override", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=5, column=0, sticky="w", pady=(12, 4), padx=(20, 20))
#         self.signal_node = tk.StringVar(value=names[0])
#         self.signal_state = tk.BooleanVar(value=True)
#         row = tk.Frame(self, bg="#0f172a")
#         row.grid(row=6, column=0, sticky="ew", pady=2, padx=(20, 20))
#         row.columnconfigure(0, weight=1)
#         row.columnconfigure(1, weight=0)
#         row.columnconfigure(2, weight=1)
#         # Increased dropdown size, larger checkbox, Apply button same width as Unblock
#         ttk.Combobox(row, textvariable=self.signal_node, values=names, width=18, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
#         # Use tk.Checkbutton for better control - shows checkmark instead of X
#         tk.Checkbutton(row, text="Green", variable=self.signal_state, bg="#0f172a", fg="#e5e7eb", 
#                       font=("Segoe UI", 12, "bold"), selectcolor="#ffffff", 
#                       activebackground="#0f172a", activeforeground="#e5e7eb",
#                       indicatoron=True).grid(row=0, column=1, padx=4, pady=2, sticky="w")
#         ttk.Button(row, text="Apply", style="Secondary.TButton", command=self._apply_signal).grid(row=0, column=2, padx=(4, 0), sticky="ew", pady=2)

#         # Block/maintenance
#         tk.Label(self, text="Road Control", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=7, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         self.block_from = tk.StringVar(value=names[0])
#         self.block_to = tk.StringVar(value=names[1])
#         road_row = tk.Frame(self, bg="#0f172a")
#         road_row.grid(row=8, column=0, sticky="ew", pady=2, padx=(20, 20))
#         road_row.columnconfigure(0, weight=1)
#         road_row.columnconfigure(1, weight=1)
#         ttk.Combobox(road_row, textvariable=self.block_from, values=names, width=15, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=2, pady=4)
#         ttk.Combobox(road_row, textvariable=self.block_to, values=names, width=15, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=2, pady=4)
#         ttk.Button(road_row, text="Block", style="Secondary.TButton", command=lambda: self._block(True)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Unblock", style="Secondary.TButton", command=lambda: self._block(False)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint On", style="Secondary.TButton", command=lambda: self._maint(True)).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint Off", style="Secondary.TButton", command=lambda: self._maint(False)).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

#         # Save/load
#         tk.Label(self, text="State", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=9, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         ttk.Button(self, text="Save Snapshot", style="Secondary.TButton", command=self._save).grid(row=10, column=0, sticky="ew", pady=2, padx=(20, 20))
#         ttk.Button(self, text="Load Snapshot", style="Secondary.TButton", command=self._load).grid(row=11, column=0, sticky="ew", pady=(2, 20), padx=(20, 20))

#     def _add(self):
#         resp = self.on_add(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add vehicle.")

#     def _add_emergency(self):
#         resp = self.on_emergency(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add emergency vehicle.")

#     def _apply_signal(self):
#         ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
#         if not ok:
#             messagebox.showwarning("Signals", "Could not update signal.")

#     def _block(self, on):
#         ok = self.on_block(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change road block.")

#     def _maint(self, on):
#         ok = self.on_maint(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change maintenance.")

#     def _save(self):
#         path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_save(path)
#         if not ok:
#             messagebox.showwarning("Save", "Could not save snapshot.")

#     def _load(self):
#         path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_load(path)
#         if not ok:
#             messagebox.showwarning("Load", "Could not load snapshot.")

# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog


# class ControlPanel(tk.Frame):
#     def __init__(self, master, names, on_add, on_emergency, on_incident, on_clear, on_reset, on_signal, on_block, on_maint, on_save, on_load):
#         super().__init__(master, bg="#0f172a")
#         self.names = names
#         self.on_add = on_add
#         self.on_emergency = on_emergency
#         self.on_incident = on_incident
#         self.on_clear = on_clear
#         self.on_reset = on_reset
#         self.on_signal = on_signal
#         self.on_block = on_block
#         self.on_maint = on_maint
#         self.on_save = on_save
#         self.on_load = on_load

#         style = ttk.Style()
#         style.theme_use("clam")
#         btn_bg = "#2563eb"
#         btn_fg = "#f8fafc"
#         style.configure("Primary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background=btn_bg, foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Primary.TButton", background=[("active", "#1d4ed8")], relief=[("pressed", "flat")])
#         style.configure("Emergency.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Emergency.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
#         style.configure("Secondary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#334155", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Secondary.TButton", background=[("active", "#1f2937")], relief=[("pressed", "flat")])
        
#         # Toggle button styles for Green/Red states
#         style.configure("Green.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#16a34a", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Green.TButton", background=[("active", "#15803d")], relief=[("pressed", "flat")])
#         style.configure("Red.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Red.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
        
#         style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 10))
#         # Enhanced beautiful comboboxes with better styling
#         style.configure("TCombobox", padding=12, font=("Segoe UI", 11, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
#         style.configure("Small.TCombobox", padding=10, font=("Segoe UI", 10, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("Small.TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
        
#         self.columnconfigure(0, weight=1)

#         tk.Label(self, text="Routes", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=(20, 20))

#         self.start_var = tk.StringVar(value=names[0])
#         self.end_var = tk.StringVar(value=names[-1])
#         self.type_var = tk.StringVar(value="auto")

#         form = tk.Frame(self, bg="#0f172a")
#         form.grid(row=1, column=0, sticky="ew", pady=(6, 6), padx=(20, 20))
#         form.columnconfigure(1, weight=1)
#         tk.Label(form, text="Start", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.start_var, values=names, width=18, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="End", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.end_var, values=names, width=18, style="TCombobox").grid(row=1, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="Vehicle", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.type_var, values=["auto", "car", "bus", "bike", "truck"], width=18, style="TCombobox").grid(row=2, column=1, sticky="ew", padx=5, pady=4)

#         # Routes buttons in 2-column layout with equal widths
#         routes_btn_frame = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame.grid(row=2, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame, text="Add Normal Route", style="Primary.TButton", command=self._add).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame, text="Add Emergency Route", style="Emergency.TButton", command=self._add_emergency).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         routes_btn_frame2 = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame2.grid(row=3, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame2.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame2.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame2, text="Report Incident", style="Secondary.TButton", command=self.on_incident).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame2, text="Clear Incidents", style="Secondary.TButton", command=self.on_clear).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         ttk.Button(self, text="Reset Simulation", style="Secondary.TButton", command=self.on_reset).grid(row=4, column=0, sticky="ew", pady=2, padx=(20, 20))

#         # Manual overrides - clean and compact layout
#         tk.Label(self, text="Manual Override", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=5, column=0, sticky="w", pady=(12, 4), padx=(20, 20))
#         self.signal_node = tk.StringVar(value=names[0])
#         self.signal_state = tk.BooleanVar(value=True)
#         row = tk.Frame(self, bg="#0f172a")
#         row.grid(row=6, column=0, sticky="ew", pady=2, padx=(20, 20))
#         row.columnconfigure(0, weight=1)
#         row.columnconfigure(1, weight=0)
#         row.columnconfigure(2, weight=1)
        
#         # Dropdown for node selection
#         ttk.Combobox(row, textvariable=self.signal_node, values=names, width=18, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
        
#         # Replace the checkbox with a toggle button
#         self.signal_btn = ttk.Button(row, text="🟢 Green", style="Green.TButton", command=self._toggle_signal)
#         self.signal_btn.grid(row=0, column=1, padx=4, pady=2, sticky="ew")
        
#         # Apply button
#         ttk.Button(row, text="Apply", style="Secondary.TButton", command=self._apply_signal).grid(row=0, column=2, padx=(4, 0), sticky="ew", pady=2)

#         # Block/maintenance
#         tk.Label(self, text="Road Control", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=7, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         self.block_from = tk.StringVar(value=names[0])
#         self.block_to = tk.StringVar(value=names[1])
#         road_row = tk.Frame(self, bg="#0f172a")
#         road_row.grid(row=8, column=0, sticky="ew", pady=2, padx=(20, 20))
#         road_row.columnconfigure(0, weight=1)
#         road_row.columnconfigure(1, weight=1)
#         ttk.Combobox(road_row, textvariable=self.block_from, values=names, width=15, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=2, pady=4)
#         ttk.Combobox(road_row, textvariable=self.block_to, values=names, width=15, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=2, pady=4)
#         ttk.Button(road_row, text="Block", style="Secondary.TButton", command=lambda: self._block(True)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Unblock", style="Secondary.TButton", command=lambda: self._block(False)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint On", style="Secondary.TButton", command=lambda: self._maint(True)).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint Off", style="Secondary.TButton", command=lambda: self._maint(False)).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

#         # Save/load
#         tk.Label(self, text="State", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=9, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         ttk.Button(self, text="Save Snapshot", style="Secondary.TButton", command=self._save).grid(row=10, column=0, sticky="ew", pady=2, padx=(20, 20))
#         ttk.Button(self, text="Load Snapshot", style="Secondary.TButton", command=self._load).grid(row=11, column=0, sticky="ew", pady=(2, 20), padx=(20, 20))

#     def _toggle_signal(self):
#         """Toggle between Green and Red signal states"""
#         self.signal_state.set(not self.signal_state.get())
#         if self.signal_state.get():
#             self.signal_btn.config(text="🟢 Green", style="Green.TButton")
#         else:
#             self.signal_btn.config(text="🔴 Red", style="Red.TButton")

#     def _add(self):
#         resp = self.on_add(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add vehicle.")

#     def _add_emergency(self):
#         resp = self.on_emergency(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add emergency vehicle.")

#     def _apply_signal(self):
#         ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
#         if not ok:
#             messagebox.showwarning("Signals", "Could not update signal.")

#     def _block(self, on):
#         ok = self.on_block(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change road block.")

#     def _maint(self, on):
#         ok = self.on_maint(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change maintenance.")

#     def _save(self):
#         path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_save(path)
#         if not ok:
#             messagebox.showwarning("Save", "Could not save snapshot.")

#     def _load(self):
#         path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_load(path)
#         if not ok:
#             messagebox.showwarning("Load", "Could not load snapshot.")

# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog


# class ControlPanel(tk.Frame):
#     def __init__(self, master, names, on_add, on_emergency, on_incident, on_clear, on_reset, on_signal, on_block, on_maint, on_save, on_load):
#         super().__init__(master, bg="#0f172a")
#         self.names = names
#         self.on_add = on_add
#         self.on_emergency = on_emergency
#         self.on_incident = on_incident
#         self.on_clear = on_clear
#         self.on_reset = on_reset
#         self.on_signal = on_signal
#         self.on_block = on_block
#         self.on_maint = on_maint
#         self.on_save = on_save
#         self.on_load = on_load

#         style = ttk.Style()
#         style.theme_use("clam")
#         btn_bg = "#2563eb"
#         btn_fg = "#f8fafc"
#         style.configure("Primary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background=btn_bg, foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Primary.TButton", background=[("active", "#1d4ed8")], relief=[("pressed", "flat")])
#         style.configure("Emergency.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Emergency.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
#         style.configure("Secondary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#334155", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Secondary.TButton", background=[("active", "#1f2937")], relief=[("pressed", "flat")])
        
#         # Toggle button styles for Green/Red states
#         style.configure("Green.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#16a34a", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Green.TButton", background=[("active", "#15803d")], relief=[("pressed", "flat")])
#         style.configure("Red.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
#         style.map("Red.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
        
#         style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 10))
#         # Enhanced beautiful comboboxes with better styling
#         style.configure("TCombobox", padding=12, font=("Segoe UI", 11, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
#         style.configure("Small.TCombobox", padding=10, font=("Segoe UI", 10, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
#         style.map("Small.TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
        
#         self.columnconfigure(0, weight=1)

#         tk.Label(self, text="Routes", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=(20, 20))

#         self.start_var = tk.StringVar(value=names[0])
#         self.end_var = tk.StringVar(value=names[-1])
#         self.type_var = tk.StringVar(value="auto")

#         form = tk.Frame(self, bg="#0f172a")
#         form.grid(row=1, column=0, sticky="ew", pady=(6, 6), padx=(20, 20))
#         form.columnconfigure(1, weight=1)
#         tk.Label(form, text="Start", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.start_var, values=names, width=18, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="End", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.end_var, values=names, width=18, style="TCombobox").grid(row=1, column=1, sticky="ew", padx=5, pady=4)
#         tk.Label(form, text="Vehicle", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8))
#         ttk.Combobox(form, textvariable=self.type_var, values=["auto", "car", "bus", "bike", "truck"], width=18, style="TCombobox").grid(row=2, column=1, sticky="ew", padx=5, pady=4)

#         # Routes buttons in 2-column layout with equal widths
#         routes_btn_frame = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame.grid(row=2, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame, text="Add Normal Route", style="Primary.TButton", command=self._add).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame, text="Add Emergency Route", style="Emergency.TButton", command=self._add_emergency).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         routes_btn_frame2 = tk.Frame(self, bg="#0f172a")
#         routes_btn_frame2.grid(row=3, column=0, sticky="ew", pady=2, padx=(20, 20))
#         routes_btn_frame2.columnconfigure(0, weight=1, uniform="btn")
#         routes_btn_frame2.columnconfigure(1, weight=1, uniform="btn")
#         ttk.Button(routes_btn_frame2, text="Report Incident", style="Secondary.TButton", command=self.on_incident).grid(row=0, column=0, sticky="ew", padx=(0, 2))
#         ttk.Button(routes_btn_frame2, text="Clear Incidents", style="Secondary.TButton", command=self.on_clear).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
#         ttk.Button(self, text="Reset Simulation", style="Secondary.TButton", command=self.on_reset).grid(row=4, column=0, sticky="ew", pady=2, padx=(20, 20))

#         # Manual overrides - clean and compact layout
#         tk.Label(self, text="Manual Override", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=5, column=0, sticky="w", pady=(12, 4), padx=(20, 20))
#         self.signal_node = tk.StringVar(value=names[0])
#         self.signal_state = tk.BooleanVar(value=True)
#         row = tk.Frame(self, bg="#0f172a")
#         row.grid(row=6, column=0, sticky="ew", pady=2, padx=(20, 20))
#         row.columnconfigure(0, weight=1)
#         row.columnconfigure(1, weight=1)
        
#         # Dropdown for node selection
#         ttk.Combobox(row, textvariable=self.signal_node, values=names, width=18, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
        
#         # Toggle button that applies signal immediately
#         self.signal_btn = ttk.Button(row, text="Green", style="Green.TButton", command=self._toggle_signal)
#         self.signal_btn.grid(row=0, column=1, padx=(4, 0), pady=2, sticky="ew")

#         # Block/maintenance
#         tk.Label(self, text="Road Control", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=7, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         self.block_from = tk.StringVar(value=names[0])
#         self.block_to = tk.StringVar(value=names[1])
#         road_row = tk.Frame(self, bg="#0f172a")
#         road_row.grid(row=8, column=0, sticky="ew", pady=2, padx=(20, 20))
#         road_row.columnconfigure(0, weight=1)
#         road_row.columnconfigure(1, weight=1)
#         ttk.Combobox(road_row, textvariable=self.block_from, values=names, width=15, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=2, pady=4)
#         ttk.Combobox(road_row, textvariable=self.block_to, values=names, width=15, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=2, pady=4)
#         ttk.Button(road_row, text="Block", style="Secondary.TButton", command=lambda: self._block(True)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Unblock", style="Secondary.TButton", command=lambda: self._block(False)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint On", style="Secondary.TButton", command=lambda: self._maint(True)).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
#         ttk.Button(road_row, text="Maint Off", style="Secondary.TButton", command=lambda: self._maint(False)).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

#         # Save/load
#         tk.Label(self, text="State", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=9, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
#         ttk.Button(self, text="Save Snapshot", style="Secondary.TButton", command=self._save).grid(row=10, column=0, sticky="ew", pady=2, padx=(20, 20))
#         ttk.Button(self, text="Load Snapshot", style="Secondary.TButton", command=self._load).grid(row=11, column=0, sticky="ew", pady=(2, 20), padx=(20, 20))

#     def _toggle_signal(self):
#         """Toggle between Green and Red signal states and apply immediately"""
#         self.signal_state.set(not self.signal_state.get())
#         if self.signal_state.get():
#             self.signal_btn.config(text="Green", style="Green.TButton")
#         else:
#             self.signal_btn.config(text="Red", style="Red.TButton")
        
#         # Apply the signal change immediately
#         ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
#         if not ok:
#             messagebox.showwarning("Signals", "Could not update signal.")
#             # Revert the button state if operation failed
#             self.signal_state.set(not self.signal_state.get())
#             if self.signal_state.get():
#                 self.signal_btn.config(text="Green", style="Green.TButton")
#             else:
#                 self.signal_btn.config(text="Red", style="Red.TButton")

#     def _add(self):
#         resp = self.on_add(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add vehicle.")

#     def _add_emergency(self):
#         resp = self.on_emergency(self.start_var.get(), self.end_var.get(), self.type_var.get())
#         if not resp:
#             messagebox.showwarning("Route", "Could not add emergency vehicle.")

#     def _apply_signal(self):
#         ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
#         if not ok:
#             messagebox.showwarning("Signals", "Could not update signal.")

#     def _block(self, on):
#         ok = self.on_block(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change road block.")

#     def _maint(self, on):
#         ok = self.on_maint(self.block_from.get(), self.block_to.get(), on)
#         if not ok:
#             messagebox.showwarning("Road", "Could not change maintenance.")

#     def _save(self):
#         path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_save(path)
#         if not ok:
#             messagebox.showwarning("Save", "Could not save snapshot.")

#     def _load(self):
#         path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
#         if not path:
#             return
#         ok = self.on_load(path)
#         if not ok:
#             messagebox.showwarning("Load", "Could not load snapshot.")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ControlPanel(tk.Frame):
    def __init__(self, master, names, on_add, on_emergency, on_incident, on_clear, on_reset, on_signal, on_block, on_maint, on_save, on_load):
        super().__init__(master, bg="#0f172a")
        self.names = names
        self.on_add = on_add
        self.on_emergency = on_emergency
        self.on_incident = on_incident
        self.on_clear = on_clear
        self.on_reset = on_reset
        self.on_signal = on_signal
        self.on_block = on_block
        self.on_maint = on_maint
        self.on_save = on_save
        self.on_load = on_load

        style = ttk.Style()
        style.theme_use("clam")
        btn_bg = "#2563eb"
        btn_fg = "#f8fafc"
        style.configure("Primary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background=btn_bg, foreground=btn_fg, relief="flat", borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#1d4ed8")], relief=[("pressed", "flat")])
        style.configure("Emergency.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
        style.map("Emergency.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
        style.configure("Secondary.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#334155", foreground=btn_fg, relief="flat", borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#1f2937")], relief=[("pressed", "flat")])
        
        # Toggle button styles for Green/Red states
        style.configure("Green.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#16a34a", foreground=btn_fg, relief="flat", borderwidth=0)
        style.map("Green.TButton", background=[("active", "#15803d")], relief=[("pressed", "flat")])
        style.configure("Red.TButton", padding=12, font=("Segoe UI", 11, "bold"), background="#dc2626", foreground=btn_fg, relief="flat", borderwidth=0)
        style.map("Red.TButton", background=[("active", "#b91c1c")], relief=[("pressed", "flat")])
        
        style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 10))
        # Enhanced beautiful comboboxes with better styling
        style.configure("TCombobox", padding=12, font=("Segoe UI", 11, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
        style.map("TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
        style.configure("Small.TCombobox", padding=10, font=("Segoe UI", 10, "bold"), fieldbackground="#0f172a", background="#3b82f6", foreground=btn_fg, borderwidth=2, relief="flat", arrowcolor="#fbbf24", bordercolor="#60a5fa")
        style.map("Small.TCombobox", fieldbackground=[("readonly", "#0f172a"), ("focus", "#1e293b")], background=[("readonly", "#3b82f6"), ("focus", "#2563eb")], arrowcolor=[("readonly", "#fbbf24"), ("focus", "#fcd34d")], bordercolor=[("focus", "#fbbf24"), ("!focus", "#60a5fa")])
        
        self.columnconfigure(0, weight=1)

        tk.Label(self, text="Routes", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=(20, 20))

        self.start_var = tk.StringVar(value=names[0])
        self.end_var = tk.StringVar(value=names[-1])
        self.type_var = tk.StringVar(value="auto")

        form = tk.Frame(self, bg="#0f172a")
        form.grid(row=1, column=0, sticky="ew", pady=(6, 6), padx=(20, 20))
        form.columnconfigure(1, weight=1)
        tk.Label(form, text="Start", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(form, textvariable=self.start_var, values=names, width=18, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=5, pady=4)
        tk.Label(form, text="End", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(form, textvariable=self.end_var, values=names, width=18, style="TCombobox").grid(row=1, column=1, sticky="ew", padx=5, pady=4)
        tk.Label(form, text="Vehicle", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(form, textvariable=self.type_var, values=["auto", "car", "bus", "bike", "truck"], width=18, style="TCombobox").grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        # Routes buttons in 2-column layout with equal widths
        routes_btn_frame = tk.Frame(self, bg="#0f172a")
        routes_btn_frame.grid(row=2, column=0, sticky="ew", pady=2, padx=(20, 20))
        routes_btn_frame.columnconfigure(0, weight=1, uniform="btn")
        routes_btn_frame.columnconfigure(1, weight=1, uniform="btn")
        ttk.Button(routes_btn_frame, text="Add Normal Route", style="Primary.TButton", command=self._add).grid(row=0, column=0, sticky="ew", padx=(0, 2))
        ttk.Button(routes_btn_frame, text="Add Emergency Route", style="Emergency.TButton", command=self._add_emergency).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
        routes_btn_frame2 = tk.Frame(self, bg="#0f172a")
        routes_btn_frame2.grid(row=3, column=0, sticky="ew", pady=2, padx=(20, 20))
        routes_btn_frame2.columnconfigure(0, weight=1, uniform="btn")
        routes_btn_frame2.columnconfigure(1, weight=1, uniform="btn")
        ttk.Button(routes_btn_frame2, text="Report Incident", style="Secondary.TButton", command=self.on_incident).grid(row=0, column=0, sticky="ew", padx=(0, 2))
        ttk.Button(routes_btn_frame2, text="Clear Incidents", style="Secondary.TButton", command=self.on_clear).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
        ttk.Button(self, text="Reset Simulation", style="Secondary.TButton", command=self.on_reset).grid(row=4, column=0, sticky="ew", pady=2, padx=(20, 20))

        # Manual overrides - clean and compact layout
        tk.Label(self, text="Manual Override", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=5, column=0, sticky="w", pady=(12, 4), padx=(20, 20))
        self.signal_node = tk.StringVar(value=names[0])
        self.signal_state = tk.BooleanVar(value=True)
        row = tk.Frame(self, bg="#0f172a")
        row.grid(row=6, column=0, sticky="ew", pady=2, padx=(20, 20))
        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)
        
        # Dropdown for node selection (reduced width to match Road Control layout)
        ttk.Combobox(row, textvariable=self.signal_node, values=names, width=15, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=(0, 2), pady=2)
        
        # Toggle button that applies signal immediately
        self.signal_btn = ttk.Button(row, text="Green", style="Green.TButton", command=self._toggle_signal)
        self.signal_btn.grid(row=0, column=1, padx=(2, 0), pady=2, sticky="ew")

        # Block/maintenance
        tk.Label(self, text="Road Control", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=7, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
        self.block_from = tk.StringVar(value=names[0])
        self.block_to = tk.StringVar(value=names[1])
        road_row = tk.Frame(self, bg="#0f172a")
        road_row.grid(row=8, column=0, sticky="ew", pady=2, padx=(20, 20))
        road_row.columnconfigure(0, weight=1)
        road_row.columnconfigure(1, weight=1)
        ttk.Combobox(road_row, textvariable=self.block_from, values=names, width=15, style="TCombobox").grid(row=0, column=0, sticky="ew", padx=2, pady=4)
        ttk.Combobox(road_row, textvariable=self.block_to, values=names, width=15, style="TCombobox").grid(row=0, column=1, sticky="ew", padx=2, pady=4)
        ttk.Button(road_row, text="Block", style="Secondary.TButton", command=lambda: self._block(True)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(road_row, text="Unblock", style="Secondary.TButton", command=lambda: self._block(False)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(road_row, text="Maint On", style="Secondary.TButton", command=lambda: self._maint(True)).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(road_row, text="Maint Off", style="Secondary.TButton", command=lambda: self._maint(False)).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        # Save/load
        tk.Label(self, text="State", fg="#e5e7eb", bg="#0f172a", font=("Segoe UI", 13, "bold")).grid(row=9, column=0, sticky="w", pady=(10, 4), padx=(20, 20))
        ttk.Button(self, text="Save Snapshot", style="Secondary.TButton", command=self._save).grid(row=10, column=0, sticky="ew", pady=2, padx=(20, 20))
        ttk.Button(self, text="Load Snapshot", style="Secondary.TButton", command=self._load).grid(row=11, column=0, sticky="ew", pady=(2, 20), padx=(20, 20))

    def _toggle_signal(self):
        """Toggle between Green and Red signal states and apply immediately"""
        self.signal_state.set(not self.signal_state.get())
        if self.signal_state.get():
            self.signal_btn.config(text="Green", style="Green.TButton")
        else:
            self.signal_btn.config(text="Red", style="Red.TButton")
        
        # Apply the signal change immediately
        ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
        if not ok:
            messagebox.showwarning("Signals", "Could not update signal.")
            # Revert the button state if operation failed
            self.signal_state.set(not self.signal_state.get())
            if self.signal_state.get():
                self.signal_btn.config(text="Green", style="Green.TButton")
            else:
                self.signal_btn.config(text="Red", style="Red.TButton")

    def _add(self):
        resp = self.on_add(self.start_var.get(), self.end_var.get(), self.type_var.get())
        if not resp:
            messagebox.showwarning("Route", "Could not add vehicle.")

    def _add_emergency(self):
        resp = self.on_emergency(self.start_var.get(), self.end_var.get(), self.type_var.get())
        if not resp:
            messagebox.showwarning("Route", "Could not add emergency vehicle.")

    def _apply_signal(self):
        ok = self.on_signal(self.signal_node.get(), self.signal_state.get())
        if not ok:
            messagebox.showwarning("Signals", "Could not update signal.")

    def _block(self, on):
        ok = self.on_block(self.block_from.get(), self.block_to.get(), on)
        if not ok:
            messagebox.showwarning("Road", "Could not change road block.")

    def _maint(self, on):
        ok = self.on_maint(self.block_from.get(), self.block_to.get(), on)
        if not ok:
            messagebox.showwarning("Road", "Could not change maintenance.")

    def _save(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if not path:
            return
        ok = self.on_save(path)
        if not ok:
            messagebox.showwarning("Save", "Could not save snapshot.")

    def _load(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if not path:
            return
        ok = self.on_load(path)
        if not ok:
            messagebox.showwarning("Load", "Could not load snapshot.")