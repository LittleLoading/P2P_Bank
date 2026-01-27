import socket
import threading
from Core.Response import Response


class Server:
    def __init__(self, host, port, timeout, controller, ui):
        self.srv_socket = None
        self.host = host
        self.port = port
        self.timeout = timeout
        self.ui = ui
        self.controller = controller
        self.running = True
        self.active_users = []

    def start(self):
        """
        Starts a server and handles all clients parallely.
        """
        self.srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv_socket.bind((self.host, self.port))
        self.srv_socket.listen(5)
        self.ui.add_log(f"Server is running on {self.host}:{self.port}")
        while self.running:
            try:
                client_socket, address = self.srv_socket.accept()
                self.active_users.append(address)
                self.ui.update_user_list([f"{a[0]}:{a[1]}" for a in self.active_users])
                self.ui.add_log(f"User Connected: {address}")
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()
            except Exception as e:
                Response.error(f"EXCEPTION: {e}")

    def handle_client(self, client_socket, address):
        """
        Listens on server port and awaits clients. Works for one client.
        :param client_socket:
        :param address: client address
        """
        self.ui.add_log(f"Handling client: {address}")
        client_socket.settimeout(self.timeout)
        try:
            with client_socket:
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        message = data.decode('utf-8').strip()
                        self.ui.add_log(f"Message from {address}: {message}")
                        response = self.controller.process_command(message)
                        client_socket.sendall(response.encode('utf-8'))
                    except socket.timeout:
                        self.ui.add_log(f"TIMEOUT {address}")
                        break
        except Exception as e:
            self.ui.add_log(f"THREAD ERROR: {e}")

        if address in self.active_users:
            self.active_users.remove(address)
        formatted_users = [f"{a[0]}:{a[1]}" for a in self.active_users]
        self.ui.update_user_list(formatted_users)
        self.ui.add_log(f"Client {address} disconnected.")




