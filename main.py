import threading
from Network.Server import Server
from JsonParser import JsonParser
from UI.BankWatcher import BankWatcher
import tkinter as tk


def main():
    config = JsonParser.get_config("IPconfig.json")
    if not config:
        return

    root = tk.Tk()

    def shutdown_callback():
        print("Turning off")
        root.quit()
        root.destroy()

    monitor = BankWatcher(root, shutdown_callback)

    def process_command(command):
        return f"{command} OK\n"

    in_com = "BA"

    server = Server(config["host"], config["port"], config["timeout"], process_command(in_com), monitor)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
