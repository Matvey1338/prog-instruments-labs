import tkinter as tk
from src.gui.app import PasswordApp

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()