import mysql.connector
import json
import sys

try:
    from .db_init_script import INIT_SQL_COMMANDS
except ImportError:
    INIT_SQL_COMMANDS = ""


class Database:
    """
    Manages MySQL database connection and initialization
    """

    def __init__(self, config_file='dbconfig.json', auto_init=True):
        """

        :param config_file: path to the JSON CONFIGURATION file
        :param auto_init: If True, the class attempts to create the DB and tables if connection fails or to update them
        """
        self.config = self._load_config(config_file)
        self.connection = None
        self.cursor = None

        try:

            #self.engine = mysql.connector.connect()

            self.connect()

            if auto_init:
                self._execute_script(INIT_SQL_COMMANDS)


        except mysql.connector.Error as err:

            if err.errno == 1049 and auto_init:
                print("--> Database doesnt exist, making new one...")
                self._create_database_and_tables()
            else:
                print(f"CRITICAL DB ERROR: {err}")
                sys.exit(1)

    def _ensure_database_exists(self):
        """Connects to mysql server and creates db if doesnt exists"""
        try:
            tmp_conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            tmp_cursor = tmp_conn.cursor()
            tmp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            tmp_conn.commit()
            tmp_cursor.close()
            tmp_conn.close()
        except mysql.connector.Error as err:
            print(f"Failed to ensure DB exists: {err}")
            sys.exit(1)


    def _load_config(self, config_file):
        """
        Loads database credentials from a JSON file
        :param config_file: path to the JSON CONFIGURATION file
        :return: database connection credentials
        """
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Config Error: {e}")
            sys.exit(1)

    def connect(self):
        """
        Connects to the database, bruh like simple as that
        :return: nothing
        """
        self.connection = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def _create_database_and_tables(self):
        """
        create db schema
        connect to serrver, create database, reconect to db, run init sql script
        :return: nothing
        """
        try:
            conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            cursor = conn.cursor()
            db_name = self.config['database']
            print(f"--> Creating database '{db_name}'")
            cursor.execute(f"create database if not exists {db_name}")
            conn.commit()
            cursor.close()
            conn.close()

            self.connect()
            print("--> creating tables and saving data")
            self._execute_script(INIT_SQL_COMMANDS)
            print("--> making db done")

        except mysql.connector.Error as err:
            print(f"Failed to initialize database: {err}")
            sys.exit(1)

    def _execute_script(self, script):
        """
        executes a raw sql script with multiple commands, commands must be separated by ;
        :param script:db init script
        :return:
        """
        commands = script.split(';')
        for command in commands:
            if command.strip():
                try:
                    self.cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Warning during init: {err}")
        self.connection.commit()

    def commit(self):
        """
        Safe comimit that tests if connection is working, checks first if connection exists
        :return: nothng
        """
        if self.connection:
            try:
                self.connection.commit()
            except mysql.connector.Error as err:
                print(f"Commit error: {err}")

    def close(self):
        """
        closes the cursor and the db connection
        :return: nothing
        """
        try:
            if self.cursor: self.cursor.close()
            if self.connection: self.connection.close()
        except:
            pass

    def add_account(self, account_number):
        """
        Vloží náhodně vygenerované číslo účtu.
        id se vygeneruje automaticky díky AUTO_INCREMENT.
        """
        cursor = self.connection.cursor()
        try:
            # id vynecháváme, vloží se samo
            query = "INSERT INTO accounts (account_number, balance) VALUES (%s, %s)"
            cursor.execute(query, (account_number, 0))
            self.connection.commit()
            return True
        except mysql.connector.IntegrityError:
            # Nastane, pokud vygenerované account_number již v DB existuje (díky UNIQUE constraint)
            return False
        finally:
            cursor.close()

    def get_next_free_account_number(self):
        """
        ai gen
        :return:
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT t1.account_number + 1 AS gap
                FROM accounts t1
                WHERE NOT EXISTS (
                    SELECT * FROM accounts t2 
                    WHERE t2.account_number = t1.account_number + 1
                ) 
                AND t1.account_number >= %s 
                AND t1.account_number < %s
                ORDER BY t1.account_number ASC
                LIMIT 1
            """

            cursor.execute(query, (10000, 99999))
            result = cursor.fetchone()

            if result:
                return int(result[0])

            cursor.execute("SELECT COUNT(*) FROM accounts")
            if cursor.fetchone()[0] == 0:
                return 10000

            return None
        finally:
            cursor.close()