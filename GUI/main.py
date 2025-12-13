"""Entry point kept for compatibility; delegates to the modular GUI."""
from app import App


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

