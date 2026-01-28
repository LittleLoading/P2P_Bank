import tkinter as tk
from tkinter import ttk, scrolledtext, END
import sv_ttk
import pywinstyles
import sys


class BankWatcher:
    def __init__(self, root, shutdown):
        self.root = root
        self.root.title("P2P Bank")
        sv_ttk.set_theme("dark")
        self.apply_theme_to_titlebar(self.root)

        style = ttk.Style()
        style.configure("TFrame", bg="#000000")
        style.configure("TLabel", bg="#000000", fg="#fafafa")

        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        ttk.Label(self.main_frame, text="Communication Log", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        ttk.Label(self.main_frame, text="Active Nodes", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w", padx=(15, 0), pady=(0, 5))

        self.log_container = ttk.Frame(self.main_frame)
        self.log_container.grid(row=1, column=0, sticky="nsew")
        self.log = tk.Text(
            self.log_container,
            width=60,
            height=20,
            font=("Consolas", 10),
            bg="#1c1c1c",
            fg="#fafafa",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.log_container, orient=tk.VERTICAL, command=self.log.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.log.tag_config("ERROR", foreground="#ff6b6b")
        self.log.tag_config("SUCCESS", foreground="#69db7c")
        self.log.tag_config("INFO", foreground="#4dadf7")

        self.user_list = tk.Listbox(
            self.main_frame, width=25, height=20, font=("Segoe UI", 10),
            bg="#1c1c1c", fg="#fafafa", selectbackground="#0078d4",
            borderwidth=0, highlightthickness=1, highlightbackground="#333333"
        )
        self.user_list.grid(row=1, column=1, padx=(15, 0), sticky="nsew")

        self.shutdown_button = ttk.Button(root, text="Turn off Server", command=shutdown, style="Accent.TButton")
        self.shutdown_button.pack(pady=(0, 20))

    def add_log(self, message):
        """
        Message window about server status.
        :param message: string
        :return: message on screen
        """
        self.log.config(state=tk.NORMAL)
        tag = "INFO"
        if "ERROR" in message.upper() or "EXCEPTION" in message.upper() or "ER" in message.upper():
            tag = "ERROR"
        elif "SUCCESS" in message.upper() or "OK" in message.upper():
            tag = "SUCCESS"

        self.log.insert(tk.END, f"{message}\n", tag)
        self.log.config(state=tk.DISABLED)
        self.log.see(tk.END)

    def update_user_list(self, users):
        """
        Updates list of users, so that when new user connects the list updates.
        :param users: string list
        """
        self.user_list.delete(0, END)
        for user in users:
            self.user_list.insert(END, user)

    def apply_theme_to_titlebar(self, root):
        """
        Changes windows title bar to dark mode - from library.
        :param root:
        :return:
        """
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

