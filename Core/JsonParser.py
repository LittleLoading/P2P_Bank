import json
from tkinter import messagebox
from pathlib import Path


class JsonParser:
    @staticmethod
    def source_path(relative_path):
        """
        Finds path to configuration file.
        :param relative_path: file name
        :return: path to file
        """
        cur_dir = Path(__file__).parent.resolve()
        for directory in [cur_dir] + list(cur_dir.parents):
            full_path = directory / relative_path
            if full_path.exists():
                return str(full_path)

    @staticmethod
    def get_config(filename):
        """
        Reads the configuration file.
        :param filename: file name
        :return: information from the file
        """
        try:
            file = JsonParser.source_path(filename)
            with open(file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {filename} couldn't be found.")
            return None
        except Exception as e:
            messagebox.showerror("Reading Error", f"\n{str(e)}")
            return None

