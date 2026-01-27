from Response import Response
from commands import BankCode, AccountCreate, AccountDeposit, AccountWithdrawal, AccountBalance, AccountRemove, \
    BankAmount, BankClients


class BankController:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def proccess_command(self, raw_data):
        if not raw_data:
            return ""

        full_raw_command = raw_data.strip()

        parts = raw_data.strip().split()
        if not parts:
            return Response.error("ER Unknown command")

        cmd_code = parts[0].upper()

        try:
            if cmd_code == "BC":
                return BankCode.execute(self.config)

            elif cmd_code == "AC":
                return AccountCreate.execute(self.config, self.db)
            elif cmd_code == "AD":
                return AccountDeposit.execute(parts, self.config, self.db, full_raw_command)
            elif cmd_code == "AW":
                return AccountWithdrawal.execute(parts, self.config, self.db, full_raw_command)
            elif cmd_code == "AB":
                return AccountBalance.execute(parts, self.config, self.db, full_raw_command)
            elif cmd_code == "AR":
                return AccountRemove.execute(parts, self.config, self.db)
            elif cmd_code == "BA":
                return BankAmount.execute(self.db)
            elif cmd_code == "BN":
                return BankClients.execute(self.db)

            else:
                return Response.error(f"ER Command {cmd_code} not found.")

        except Exception as e:
            return Response.error(f"ERROR: {str(e)}")