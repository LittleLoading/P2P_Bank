# P2P Bank
This project simulates banking processes and works with TCP connection as peer to peer. It uses database for saving 
loggs and configuration files for connection.

## Used Libraries
* mysql
    ```python
    pip install mysql-connector-python
  ```

## Database Setup
1. **Connect:** Open MySQL Workbench and connect to the **root** connection.
2. **Database**Open MySQL Workbench and create database called 'bank'
3. **Navigate:** Go to **Administration** (left sidebar) -> **Users and Privileges**.
4. **Add Account:** Click **Add Account** (bottom left).
5. **Login Details:**
   * **Login Name:** `bankuser`
   * **Authentication Type:** Standard (Default)
   * **Limit to Host Matching:** `%` (Default)
   * **Password:** `bankUserPassword`
6. **Schema Privileges:** * Go to the **Schema Privileges** tab for that user.
   * Click **Add Entry**, select **Selected Schema**, and choose `bank`.
7. **Permissions:** Select **"Select ALL"** (bottom right) to grant all permissions.
8. **Finish:** Click **Apply**.

inside the project than find dbconfig.json and fill it with the database connection credentials
```json
{
  "host": "127.0.0.1",
  "user": "<bankuser>",
  "password": "<bankUserPassword>",
  "database": "bank"
}
```

## Project Setup
1. Open project file.
2. Download all needed libraries (more in [Used Libraries](#Used-Libraries)).
3. Fill in the IPconfig.json file with your IP address and wanted port from given interval. 
```json
  {
  "host": "127.0.0.1", // <- Your ip address
  "port": 65525, // <- port 65525-65535
  "timeout": 20
  }
```
4. Run main and app should pop up.
5. Continue in Putty as a client and watch application window as admin. Connection type is RAW.
    

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
        file_path = os.path.join(base_path, "dbconfig.json")
        with open(file_path, "r") as file:
            db_config = json.load(file)
            return oracledb.connect(user=db_config["user"], password=db_config["password"], dsn=db_config["dsn"])
    except FileNotFoundError:
        messagebox.showerror("Error", f"File dbconfig.json not found!")
        return None
    except Exception as e:
        messagebox.showerror("Connection Error", f"Detail:\n{str(e)}")
        return None
 ```

 * Database class (most of the methods)
 ```python
        def __init__(self, config_file='dbconfig.json', auto_init=True):
        ....
        def _ensure_database_exists(self):
        ....
        def _load_config(self, config_file):
        ....
        def connect(self):
        ....
        def _create_database_and_tables(self):
        ....
        def _execute_script(self, script):
        ....
        def commit(self):
        ....
        def close(self):
        ....
 ```

### AI chats
In this project AI was used to make class diagrams and to help us fine-tune it, fix unknown errors or find better solutions.
* About logs - [chat](https://gemini.google.com/app/c79f906a86f557c3?hl=cs)
* About Proxy and hacker mode [chat](https://gemini.google.com/share/9a91692a0b61)
* Upgraded method for searching json files - [chat](https://gemini.google.com/app/b5fe04a1df9a980e)

## Authors
* [David Houra](https://github.com/LittleLoading) -  Database, Controller, Commands
* [Nikola Poláchová](https://github.com/Niko2357) - Network, Logging, UI, Testing
