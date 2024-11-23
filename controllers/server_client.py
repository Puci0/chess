import socket
from typing import Union
from views import ConsoleView


class ServerClient:
    def __init__(self, view: ConsoleView, server_ip: str = '18.194.209.148', server_port: int = 12345) -> None:
        self.view = view
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self) -> bool:
        # try:
        # with open('test.txt', 'a') as f:
        #     f.write(str(type(self.server_socket)))
        self.server_socket.connect((self.server_ip, self.server_port))
        self.connected = True
        return True
        # except (socket.error, ConnectionRefusedError):

        self.connected = False
        return False

    def close(self) -> None:
        if self.connected:
            self.server_socket.close()
            self.connected = False

    def receive_message(self) -> Union[str, None]:
        if not self.connected:
            self.view.display_message("No connection to the server.")
            return None

        try:
            message = self.server_socket.recv(1024).decode()
            if message:
                return message
        except OSError as e:
            self.view.display_message(f"Error while receiving message: {e}")

    def send_message(self, message: str) -> None:
        if not self.connected:
            self.view.display_message("No connection to the server.")
            return
        try:
            self.server_socket.sendall(message.encode())
        except OSError as e:
            self.view.display_message(f"Error while sending messages: {e}")
