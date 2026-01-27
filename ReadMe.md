# P2P Bank
This project simulates banking processes and works with TCP connection as peer to peer. It uses database for saving 
loggs and configuration files for connection.

## Used Libraries
* mysql
    ```python
    
  ```


## Database Setup
1. Open MySQL Workbench and create database 'bank'.
2. Create a new usage with all privileges to this database.
3. Fill in the dbconfig.json right connection info.
4. All done, now the project.

## Project Setup
1. Open project file.
2. Download all needed libraries (more in [Used Libraries](#Used-Libraries)).
3. Run main and app should pop up.
4. Continue in putty as a client and watch application window as admin.
    

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

### AI chats
* About logs - [chat](https://gemini.google.com/app/c79f906a86f557c3?hl=cs)
* Upgraded method for searching json files - [chat](https://gemini.google.com/app/b5fe04a1df9a980e)

## Authors
* [David Houra](https://github.com/LittleLoading)
* [Nikola Poláchová](https://github.com/Niko2357)