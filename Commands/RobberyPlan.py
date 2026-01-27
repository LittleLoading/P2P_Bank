from Core.Response import Response
from Network.Scanner import NetworkScanner


def execute(parts, config):
    """
    method to filter the bank with the certain amount of money to rob with the lest amount of clients that it will efect
    :param parts: rp <amount>
    :param config: {'host': '127.0.0.1', 'port': 65525, 'timeout': 20}
    :return: response success or error
    """
    try:
        target_amount = int(parts[1])
        my_ip = config.get("host")

        if not target_amount > 0:
            return Response.error("ER target amount must be greater than 0")

        banks = NetworkScanner.scan_network(my_ip)
        if not banks:
            return Response.error("ER No targets found in network.")

        banks.sort(key=lambda b: b['money'] / b['clients'] if b['clients'] > 0 else b['money'], reverse=True)

        selected_ips = []
        total_loot = 0
        total_victims = 0

        for b in banks:
            if total_loot < target_amount:
                selected_ips.append(f"{b['ip']}:{b['port']}")
                total_loot += b['money']
                total_victims += b['clients']
            else:
                break

        target_list = ", ".join(selected_ips)
        message = f"To achieve {target_amount} is needed to rob: {target_list} " \
                  f"Gain {total_loot} having: {total_victims} clients"

        return Response.success("RP", message)

    except (IndexError, ValueError):
        return Response.error("ER Usage: RP <amount>")
    except Exception as e:
        return Response.error(f"ER Planning failed: {str(e)}")