# P2P Bank
This project simulates banking processes and works with TCP connection as peer to peer. It uses database for saving 
loggs and configuration files for connection.

### Used from previous projects
* Reading from configuration json file:
 ```python
  def get_connection():
    """
    Connects to database.
    :return: connection or None
    """
    try:
        base_path = resource_path()
        file_path = os.path.join(base_path, "config.json")
        with open(file_path, "r") as file:
            db_config = json.load(file)
            return oracledb.connect(user=db_config["user"], password=db_config["password"], dsn=db_config["dsn"])
    except FileNotFoundError:
        messagebox.showerror("Error", f"File config.json not found!")
        return None
    except Exception as e:
        messagebox.showerror("Connection Error", f"Detail:\n{str(e)}")
        return None
 ```

### AI chats
* About logs - [chat](https://gemini.google.com/app/c79f906a86f557c3?hl=cs)
  