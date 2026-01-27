from Network.Client import ProxyClient
from Core.Response import Response


def execute(raw_parts, config, db, full_raw_command):
    """
    Command: AW <account>/<ip> <amount>
    """
    try:
        if len(raw_parts) < 3:
            return Response.error("ER account number and amount is not in correct format")

        target_part = raw_parts[1]
        amount_str = raw_parts[2]

        if "/" not in target_part:
            return Response.error("ER account number and amount is not in correct format")

        acc_num_str, bank_ip = target_part.split("/")


        if not acc_num_str.isdigit() or not amount_str.isdigit():
            return Response.error("ER account number and amount is not in correct format")

        acc_num = int(acc_num_str)
        amount = int(amount_str)
        my_ip = config.get("host")


        if bank_ip == my_ip:
            success, error_msg = db.withdraw_money(acc_num, amount)
            if success:
                return Response.success("AW")
            else:
                return Response.error(error_msg)
        if bank_ip != my_ip:
            print(f"[PROXY] Forwarding command to {bank_ip}...")
            return ProxyClient.forward_command(bank_ip, config['port'], full_raw_command)
    except Exception as e:
        return Response.error(f"ER error while withdrawing {str(e)}")