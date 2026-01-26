import socket
import threading
from Response import Response


class Server:
    def __init__(self, host, port, controller):
        self.srv_socket = None
        self.host = host
        self.port = port
        self.controller = controller
        self.running = True

    def start(self):
        """
        Starts a server.
        :return:
        """
        self.srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv_socket.bind((self.host, self.port))
        self.srv_socket.listen(5)
        Response.success("listening", f"{self.host} : {self.port}")
        while self.running:
            try:
                client_socket, address = self.srv_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()
            except Exception as e:
                Response.error(f"EXCEPTION: {e}")

    def handle_client(self, client_socket, address):
        """
        Listens on server port and awaits clients.
        :param client_socket:
        :param address: client address
        :return:
        """
        client_socket.settimeout(5)
        Response.success(f"new connection from:", f"{address}")
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8').strip()
                    response = self.controller.proccess_command(message)
                    client_socket.sendall(response.encode('utf-8'))
                except socket.timeout:
                    Response.error(f"timeout")
                    client_socket.sendall("TIMEOUT\n".encode('utf-8'))
                    break
                except Exception as e:
                    Response.error(f"Thread Error: {e}")
                    break


