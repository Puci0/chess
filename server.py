import socket
import time


class ChessServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print(f"Serwer szachowy uruchomiony na {host}:{port}")

        self.clients = []
        self.players = {}
        self.run()

    def run(self):
        # while len(self.clients) < 2:
        while True:
            self.wait_for_players()
            self.start_game()
            # print("Oczekiwanie na graczy...")
            #
            # client_socket, addr = self.server_socket.accept()
            # if len(self.clients) == 0:
            #     self.players['PLAYER_1'] = client_socket
            #     print(f"Gracz 1 połączony: {addr}")
            #     self.players['PLAYER_1'].sendall('Oczekiwanie na przeciwnika.'.encode())
            # else:
            #     self.players['PLAYER_2'] = client_socket
            #     print(f"Gracz 2 połączony: {addr}")
            #     self.players['PLAYER_2'].sendall('Oczekiwanie na przeciwnika.'.encode())
            #
            # self.clients.append(client_socket)
            #
            # if len(self.clients) == 2:
            #     print("Obaj gracze są połączeni, gra może się rozpocząć.")
            #
            #     # wysylanie wiadomosci o flipowaniu planszy
            #     self.players['PLAYER_1'].sendall(str(int(False)).encode())
            #     self.players['PLAYER_2'].sendall(str(int(True)).encode())
            #
            #     time.sleep(1)
            #
            #     self.players['PLAYER_1'].sendall('Rozpoczynanie partii.'.encode())
            #     self.players['PLAYER_2'].sendall('Rozpoczynanie partii.'.encode())
            #     self.start_game()

    def wait_for_players(self):
        self.clients = []
        self.players = {}

        while len(self.clients) < 2:
            print("Oczekiwanie na graczy...")
            client_socket, addr = self.server_socket.accept()

            if len(self.clients) == 0:
                self.players['PLAYER_1'] = client_socket
                print(f"Gracz 1 połączony: {addr}")
                self.players['PLAYER_1'].sendall('Oczekiwanie na przeciwnika.'.encode())
            else:
                self.players['PLAYER_2'] = client_socket
                print(f"Gracz 2 połączony: {addr}")
                self.players['PLAYER_2'].sendall('Oczekiwanie na przeciwnika.'.encode())

            self.clients.append(client_socket)

        print("Obaj gracze są połączeni, gra może się rozpocząć.")
        self.players['PLAYER_1'].sendall(str(int(False)).encode())
        self.players['PLAYER_2'].sendall(str(int(True)).encode())

        time.sleep(1)

        self.players['PLAYER_1'].sendall('Rozpoczynanie partii.'.encode())
        self.players['PLAYER_2'].sendall('Rozpoczynanie partii.'.encode())

    def start_game(self):
        time.sleep(2)
        current_player = 'PLAYER_1'

        while True:
            try:
                next_player = 'PLAYER_2' if current_player == 'PLAYER_1' else 'PLAYER_1'

                self.players[current_player].sendall('Wprowadz swoj ruch: '.encode())
                self.players[next_player].sendall('Oczekiwanie'.encode())

                move = self.players[current_player].recv(1024).decode()
                if not move:
                    print(f"{current_player} zakończył połączenie.")
                    break
                print(f"Otrzymano ruch od {current_player}: {move}")

                self.players[next_player].sendall(move.encode())

                current_player = next_player

            except (ConnectionResetError, BrokenPipeError):
                print(f"Połączenie z {current_player} zostało przerwane.")
                break

        self.close_connections()

    def close_connections(self):
        for client in self.clients:
            client.close()

        self.clients = []
        self.players = {'PLAYER_1': None, 'PLAYER_2': None}
        print("Gra zakończona, połączenia zamknięte.")


if __name__ == "__main__":
    ChessServer()