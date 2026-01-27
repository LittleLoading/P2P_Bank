# commands/AccountBalance.py
from Network.Client import ProxyClient
from Response import Response


def execute(raw_parts, config, db,full_raw_command ):
    """
    Command: AB <account>/<ip>
    Success Response: AB <number>
    Error Response: ER format account number is not correct (or other error)
    """
    try:
        if len(raw_parts) < 2:
            return Response.error("ER format account number is not correct")

        target_part = raw_parts[1]  # Expected: "10001/10.1.2.3"

        if "/" not in target_part:
            return Response.error("ER format account number is not correct")

        acc_num_str, bank_ip = target_part.split("/")

        if not acc_num_str.isdigit() or not (10000 <= int(acc_num_str) <= 99999):
            return Response.error("ER format account number is not correct")

        acc_num = int(acc_num_str)
        my_ip = config.get("host")


        if bank_ip == my_ip:
            balance = db.get_balance(acc_num)
            if balance is not None:
                return Response.success("AB", str(balance))
            else:
                return Response.error("ER account in our bank doesnt exist")
        if bank_ip != my_ip:
            print(f"[PROXY] Forwarding command to {bank_ip}...")
            return ProxyClient.forward_command(bank_ip, config['port'], full_raw_command)

    except Exception as e:
        return Response.error(f"ER Chyba při zjišťování zůstatku: {str(e)}")