import mysql.connector
import json
import sys

INIT_SQL_COMMANDS = """
    create table if not exists accounts(
    id int primary key auto_increment,
    account_number varchar(50) unique,
    balance bigint default 0,
    created_at timestamp default current_timestamp
);
"""


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
            # self.engine = mysql.connector.connect()
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
        executes a raw sql script with multiple Commands, Commands must be separated by ;
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
        Safe commit that tests if connection is working, checks first if connection exists
        :return: nothing
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

    def deposit_money(self, account_number, amount):
        """
        deposits money into account_number
        returns true if success, returns false if account doesnt exits
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id from accounts where account_number = %s", (account_number,))
            if not cursor.fetchone():
                return False

            query = "update accounts set balance = balance + %s where account_number = %s"
            cursor.execute(query, (amount, account_number))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[DB ERR] Error while depositing: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def withdraw_money(self, account_number, amount):
        """
        Tries to withdraw money from account_number
        :param self:
        :param account_number: users account number
        :param amount: amout to withdraw from account_number
        :return: true if success, returns false if account doesnt exits or error durring process
        """
        cursor = self.connection.cursor()
        try:
            query_check = "select balance from accounts where account_number = %s"
            cursor.execute(query_check, (account_number,))
            result = cursor.fetchone()

            if not result:
                return False, "ER Account does not exists in our bank."

            current_balance = result[0]

            if current_balance < amount:
                return False, "ER Not enough money in the account"

            if amount <= 0:
                return False, "ER Not enough money in the account"

            query_update = "update accounts set balance = balance - %s where account_number = %s"
            cursor.execute(query_update, (amount, account_number))
            self.connection.commit()
            return True, None

        except Exception as e:
            self.connection.rollback()
            return False, f"ER Error in db: {str(e)}"
        finally:
            cursor.close()

    def get_balance(self, account_number):
        """
        Fetches the current balance of a specific account
        Returns the balance (int) if successful, or None if the account does not exist
        """
        cursor = self.connection.cursor()
        try:
            query = "select balance from accounts where account_number = %s"
            cursor.execute(query, (account_number,))
            result = cursor.fetchone()

            if result:
                return int(result[0])
            return None
        except Exception as e:
            print(f"[DB ERR] Balance fetch error: {e}")
            return None
        finally:
            cursor.close()


    def delete_account(self, account_number):
        """
        Deletes an account from the database
        :param account_number: account number we want to delete
        :return: true if success, false if not
        """
        cursor = self.connection.cursor()
        try:
            query_check = "select balance from accounts where account_number = %s"
            cursor.execute(query_check, (account_number,))
            result = cursor.fetchone()

            if not result:
                return False, "ER Account in our bank doesnt exist"

            current_balance = int(result[0])

            if current_balance != 0:
                return False, "ER Cant delete bank account that has money on it"

            query_delete = "delete from accounts where account_number = %s"
            cursor.execute(query_delete, (account_number,))
            self.connection.commit()
            return True, None

        except Exception as e:
            self.connection.rollback()
            return False, f"ER Database error: {str(e)}"
        finally:
            cursor.close()

    # Database/Database.py

    def get_total_bank_amount(self):
        """
        Calculates the sum of all balances across all accounts
        :return:  the total amount (int)
        """
        cursor = self.connection.cursor()
        try:
            query = "SELECT COALESCE(SUM(balance), 0) FROM accounts" #coalesce bcs sum can return null and we need 0
            cursor.execute(query)
            result = cursor.fetchone()
            return int(result[0]) if result else 0
        except Exception as e:
            print(f"[DB ERR] Total amount calculation error: {e}")
            return 0
        finally:
            cursor.close()

    def get_total_clients_count(self):
        """
        Counts the total number of accounts (clients) in the bank
        :return: the count (int)
        """
        cursor = self.connection.cursor()
        try:
            query = "SELECT COUNT(*) FROM accounts"
            cursor.execute(query)
            result = cursor.fetchone()
            return int(result[0]) if result else 0
        except Exception as e:
            print(f"[DB ERR] Client count error: {e}")
            return 0
        finally:
            cursor.close()