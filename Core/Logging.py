import json
import os
import threading
from datetime import datetime


class Logging:
    lock = threading.Lock()
    log_file = "log_file.json"

    @staticmethod
    def log(user, command, status, message):
        """
        Method that stores loggings in json file.
        :param user: ip address
        :param command: proceeding command
        :param status: status
        :param message: ending message
        """
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": str(user),
            "command": command,
            "status": status,
            "message": message
        }
        with Logging.lock:
            logs = []
            if os.path.exists(Logging.log_file):
                try:
                    with open(Logging.log_file, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    logs = []
            logs.append(log_entry)
            with open(Logging.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)

