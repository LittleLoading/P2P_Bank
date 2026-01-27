import tkinter
from tkinter import scrolledtext, Frame, Listbox, END


class BankWatcher:
    def __init__(self, root, shutdown):
        self.root = root
        self.root.title("P2P Bank")

        self.main_frame = Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.log = scrolledtext.ScrolledText(self.main_frame, width=50, height=20)
        self.log.grid(row=0, column=0)
        self.user_list = Listbox(self.main_frame, width=20, height=20)
        self.user_list.grid(row=0, column=1, padx=(10, 0))
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

    def update_user_list(self, users):
        """
        Updates list of users, so that when new user connects the list updates.
        :param users: string list
        """
        self.user_list.delete(0, END)
        for user in users:
            self.user_list.insert(END, user)

