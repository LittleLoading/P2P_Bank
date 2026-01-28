import socket
import concurrent.futures
from Network.Client import ProxyClient


class NetworkScanner:
    @staticmethod
    def check_target(ip, port, my_ip):
        """Checks one IP/port and returns its BA and BN data."""
        if ip == my_ip: return None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    money_resp = ProxyClient.forward_command(ip, port, "BA")
                    clients_resp = ProxyClient.forward_command(ip, port, "BN")

                    money = int(money_resp.split()[1])
                    clients = int(clients_resp.split()[1])
                    return {'ip': ip, 'port': port, 'money': money, 'clients': clients}
        except:
            return None

    @staticmethod
    def scan_network(my_ip):
        """Scans subnet and ports 65525-65535 in parallel."""
        subnet_prefix = ".".join(my_ip.split(".")[:-1])
        ports = range(65525, 65536)
        found_banks = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(NetworkScanner.check_target, f"{subnet_prefix}.{i}", p, my_ip)
                       for i in range(1, 255) for p in ports]

            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    found_banks.append(res)
        return found_banks
