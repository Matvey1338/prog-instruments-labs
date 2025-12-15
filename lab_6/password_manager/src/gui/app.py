import tkinter as tk
from tkinter import messagebox, ttk
from src.logic.generator import generate_password
from src.logic.strength import check_strength
from src.logic.storage import PasswordStorage


class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 6: Password Manager")
        self.root.geometry("500x400")
        self.storage = PasswordStorage()

        # UI Elements
        tk.Label(root, text = "Service:").pack(pady = 5)
        self.entry_service = tk.Entry(root)
        self.entry_service.pack()

        tk.Label(root, text = "Username:").pack(pady = 5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        tk.Label(root, text = "Password:").pack(pady = 5)
        self.entry_password = tk.Entry(root)
        self.entry_password.pack()

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady = 10)

        tk.Button(btn_frame, text = "Generate Random", command = self.do_generate).pack(side = tk.LEFT, padx = 5)
        tk.Button(btn_frame, text = "Check Strength", command = self.do_check).pack(side = tk.LEFT, padx = 5)
        tk.Button(btn_frame, text = "Save", command = self.do_save).pack(side = tk.LEFT, padx = 5)

        self.lbl_info = tk.Label(root, text = "...", fg = "blue")
        self.lbl_info.pack(pady = 5)

        tk.Button(root, text = "Show All Passwords", command = self.show_window).pack(pady = 10)

    def do_generate(self):
        pwd = generate_password(length = 16)
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, pwd)
        self.do_check()

    def do_check(self):
        pwd = self.entry_password.get()
        strength = check_strength(pwd)
        self.lbl_info.config(text = f"Strength: {strength}")

    def do_save(self):
        srv = self.entry_service.get()
        usr = self.entry_username.get()
        pwd = self.entry_password.get()
        try:
            self.storage.save_entry(srv, usr, pwd)
            messagebox.showinfo("Success", "Saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_window(self):
        top = tk.Toplevel(self.root)
        top.title("Stored Passwords")
        text = tk.Text(top)
        text.pack()

        data = self.storage.get_all()
        for item in data:
            text.insert(tk.END, f"{item['service']} | {item['username']} | {item['password']}\n")