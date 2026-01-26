import tkinter
from tkinter import scrolledtext


class BankWatcher:
    def __init__(self, root, shutdown):
        self.root = root
        self.root.title("P2P Bank")

        self.log = scrolledtext.ScrolledText(root, width=60, height=20)
        self.log.pack(padx=10, pady=10)
        self.shutdown_button = tkinter.Button(root, text="Turn off", command=shutdown, bg="red", fg="white")
        self.shutdown_button.pack(pady=5)

    def add_log(self, message):
        """
        Message window about server status.
        :param message: string
        :return: message on screen
        """
        self.log.insert(tkinter.END, f"{message}\n")
        self.log.see(tkinter.END)
