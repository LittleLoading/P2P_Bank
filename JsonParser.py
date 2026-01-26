import json
import os
from tkinter import messagebox


class JsonParser:
    @staticmethod
    def source_path(relative_path):
        """
        Finds path to configuration file.
        :param relative_path: file name
        :return: path to file
        """
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

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

