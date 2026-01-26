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

    watcher = BankWatcher(root, shutdown_callback)

    class DummyController:
        def proccess_command(self, cmd):
            return f"{cmd} OK\n"

    server = Server(config["host"], config["port"], DummyController())
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
