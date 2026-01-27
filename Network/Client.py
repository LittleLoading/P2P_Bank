import socket


class ProxyClient:
    """
    Handles outgoing connections to other bank nodes
    """
    @staticmethod
    def forward_command(target_ip, port, command_string, timeout=5):
        """
        Connects to another node, sends the command, and returns the response.
        :param target_ip: ip address of the target node
        :param port: port of the target node
        :param command_string: command that we want to send
        :param timeout: number of seconds to wait for a response
        :return: response from the target node
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)

                s.connect((target_ip, port))

                s.sendall(f"{command_string}\n".encode('utf-8'))

                response = s.recv(1024).decode('utf-8').strip()
                return response if response else "ER Peer disconnected without response."

        except socket.timeout:
            return "ER Connection timed out after 5 seconds."
        except Exception as e:
            return f"ER Could not connect to bank {target_ip}: {str(e)}"