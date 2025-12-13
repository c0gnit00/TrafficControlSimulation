import os
import tkinter as tk
from tkinter import scrolledtext, ttk


class LogViewer(tk.Toplevel):
    """Enhanced log viewer with refresh and search"""
    
    def __init__(self, master, log_path: str):
        super().__init__(master)
        self.log_path = log_path
        self.title("Traffic System Logs")
        self.geometry("800x600")
        self.configure(bg="#0b1220")
        
        # Toolbar
        toolbar = tk.Frame(self, bg="#1e293b", height=50)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        style = ttk.Style()
        style.configure("Tool.TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background="#334155",
            foreground="#f8fafc"
        )
        
        ttk.Button(toolbar, text="Refresh", style="Tool.TButton",
                  command=self._reload).pack(side="left", padx=5)
        
        ttk.Button(toolbar, text="Clear Display", style="Tool.TButton",
                  command=self._clear).pack(side="left", padx=5)
        
        tk.Label(toolbar, text="Search:", bg="#1e293b", fg="#e5e7eb",
                font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._highlight_search)
        search_entry = tk.Entry(toolbar, textvariable=self.search_var,
                               bg="#0f172a", fg="#e5e7eb", insertbackground="#e5e7eb",
                               font=("Segoe UI", 10), width=30)
        search_entry.pack(side="left", padx=5)
        
        # Log text area
        self.text = scrolledtext.ScrolledText(
            self,
            bg="#0b1220",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            font=("Consolas", 10),
            wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tags for highlighting
        self.text.tag_configure("highlight", background="#fbbf24", foreground="#000000")
        self.text.tag_configure("error", foreground="#ef4444")
        self.text.tag_configure("success", foreground="#10b981")
        self.text.tag_configure("warning", foreground="#f59e0b")
        
        self._load()
    
    def _load(self):
        self.text.delete("1.0", "end")
        
        if not os.path.exists(self.log_path):
            self.text.insert("1.0", 
                "No log file found.\n\n"
                "Logs are automatically created as you:\n"
                "Add vehicles\n"
                "Report incidents\n"
                "Change signals\n"
                "Block roads\n\n"
                "Start using the system to generate logs!")
            self.text.configure(state="disabled")
            return
        
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if not content.strip():
                self.text.insert("1.0", "Log file is empty.")
            else:
                self.text.insert("1.0", content)
                self._apply_highlighting()
            
            self.text.configure(state="disabled")
            self.text.see("end")
        except Exception as e:
            self.text.insert("1.0", f"Error reading logs:\n{e}")
            self.text.configure(state="disabled")
    
    def _apply_highlighting(self):
        content = self.text.get("1.0", "end")
        
        for i, line in enumerate(content.split('\n'), 1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"
            
            if "incident" in line.lower() or "blocked" in line.lower():
                self.text.tag_add("error", line_start, line_end)
            elif "added" in line.lower() or "success" in line.lower():
                self.text.tag_add("success", line_start, line_end)
            elif "cleared" in line.lower() or "reset" in line.lower():
                self.text.tag_add("warning", line_start, line_end)
    
    def _reload(self):
        self.text.configure(state="normal")
        self._load()
    
    def _clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "Display cleared. Click Refresh to reload.")
        self.text.configure(state="disabled")
    
    def _highlight_search(self, *args):
        self.text.tag_remove("highlight", "1.0", "end")
        
        search_term = self.search_var.get()
        if not search_term:
            return
        
        start_pos = "1.0"
        while True:
            start_pos = self.text.search(search_term, start_pos, 
                                        stopindex="end", nocase=True)
            if not start_pos:
                break
            
            end_pos = f"{start_pos}+{len(search_term)}c"
            self.text.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
