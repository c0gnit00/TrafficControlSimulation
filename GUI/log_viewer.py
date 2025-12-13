import os
import tkinter as tk
from tkinter import scrolledtext


class LogViewer(tk.Toplevel):
    def __init__(self, master, log_path: str):
        super().__init__(master)
        self.title("Traffic Logs")
        self.geometry("600x400")
        self.text = scrolledtext.ScrolledText(self, bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb")
        self.text.pack(fill="both", expand=True)
        self._load(log_path)

    def _load(self, path: str):
        if not os.path.exists(path):
            self.text.insert("1.0", "No log file found.")
            return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            self.text.insert("1.0", f.read())
        self.text.configure(state="disabled")

