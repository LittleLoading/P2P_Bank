from Core.Response import Response
from Commands import BankCode, AccountCreate, AccountDeposit, AccountWithdrawal, AccountBalance, AccountRemove, \
    BankAmount, BankClients, RobberyPlan


class BankController:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def process_command(self, raw_data):
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
            elif cmd_code == "RP":
                return RobberyPlan.execute(parts, self.config)
            elif cmd_code == "help" or "HELP":
                return ("Your Options: \n"
                        "BC  ->  bank code\n"
                        "AC  ->  creation of an account\n"
                        "AD  ->  deposit to the account (AD <account>/<ip> <value>)\n"
                        "AW  ->  withdrawal from the account (AW <account>/<ip> <value>)\n"
                        "AB  ->  balance of the account (AB <account>/<ip>)\n"
                        "AR  ->  delete the account (AR <account>/<ip>)\n"
                        "BA  ->  total balance of bank\n"
                        "BN  ->  number of clients of the bank\n"
                        )

            else:
                return Response.error(f"ER Command {cmd_code} not found.")
        except Exception as e:
            return Response.error(f"ERROR: {str(e)}")
