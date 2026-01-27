from Core.Response import Response
from Commands import BankCode, AccountCreate


class BankController:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def proccess_command(self, raw_data):
        if not raw_data:
            return ""

        parts = raw_data.strip().split()
        if not parts:
            return Response.error("ER Unknown command")

        cmd_code = parts[0].upper()

        try:
            if cmd_code == "BC":
                return BankCode.execute(self.config)

            elif cmd_code == "AC":
                return AccountCreate.execute(self.config, self.db)


            else:
                return Response.error(f"ER Command {cmd_code} not found.")

        except Exception as e:
            return Response.error(f"ERROR: {str(e)}")
