# commands/AccountDeposit.py
from Network.Client import ProxyClient
from Core.Response import Response


def execute(raw_parts, config, db, full_raw_command):
    """
    Command AD:  AD <account>/<ip> <amount>
    row_parts list commands example ['AD', '10001/127.0.0.1', '3000']
    """
    try:

        if len(raw_parts) < 3:
            return Response.error("ER number bank account and amount is not in correct format")

        target_part = raw_parts[1]  # "10001/127.0.0.1"
        amount_str = raw_parts[2]  # "3000"

        if "/" not in target_part:
            return Response.error("ER account number and amount is not in correct format")

        acc_num_str, bank_ip = target_part.split("/")

        if not acc_num_str.isdigit() or not amount_str.isdigit():
            return Response.error("ER account number and amount is not in correct format")

        acc_num = int(acc_num_str)
        amount = int(amount_str)
        my_ip = config.get("host")

        if amount < 0:
            return Response.error("ER amount cant be negative")


        if bank_ip == my_ip:
            if db.deposit_money(acc_num, amount):
                return Response.success("AD")
            else:
                return Response.error("ER Account in our bank doesnt exists")

        if bank_ip != my_ip:
            print(f"[PROXY] Forwarding command to {bank_ip}...")
            return ProxyClient.forward_command(bank_ip, config['port'], full_raw_command)

    except Exception as e:
        return Response.error(f"ER Error while handeling deposit: {str(e)}")