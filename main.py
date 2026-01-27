import threading

from Core.BankController import BankController
from Database.Database import Database
from Network.Server import Server
from Core.JsonParser import JsonParser
from UI.BankWatcher import BankWatcher
import tkinter as tk


def main():
    config = JsonParser.get_config("IPconfig.json")
    if not config:
        return

    db = Database()

    root = tk.Tk()

    def shutdown_callback():
        print("Turning off")
        root.quit()
        root.destroy()

    monitor = BankWatcher(root, shutdown_callback)

    controller = BankController(config, db)

    server = Server(config["host"], config["port"], controller)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    print(f"[*] Bank Running {config['host']}:{config['port']}")
    root.mainloop()


if __name__ == "__main__":
    main()
