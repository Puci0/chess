import socket
import time


class ChessServer:
    def __init__(self, host='0.0.0.0', port=12345, verbose=True):
        self.verbose = verbose
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        if self.verbose:
            print(f"Serwer szachowy uruchomiony na {host}:{port}")

        self.clients = []
        self.players = {}
        self.run()

    def run(self):
        if self.verbose:
            print("Oczekiwanie na graczy ...")

        while len(self.clients) < 2:
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
            if len(self.clients) == 2:
                print("Obaj gracze są połączeni, gra może się rozpocząć.")
                time.sleep(1)
                self.players['PLAYER_1'].sendall('Rozpoczynanie partii.'.encode())
                self.players['PLAYER_2'].sendall('Rozpoczynanie partii.'.encode())
                self.start_game()

    def start_game(self):
        time.sleep(1)
        current_player = 'PLAYER_1'

        while True:
            try:
                # Przełącz na drugiego gracza i wyślij mu ruch
                next_player = 'PLAYER_2' if current_player == 'PLAYER_1' else 'PLAYER_1'

                self.players[current_player].sendall('Wprowadz swoj ruch: '.encode())
                time.sleep(1)
                self.players[next_player].sendall('Oczekiwanie'.encode())

                # Odbierz ruch od gracza, który jest aktualnie na ruchu
                move = self.players[current_player].recv(1024).decode()
                if not move:
                    print(f"{current_player} zakończył połączenie.")
                    break
                print(f"Otrzymano ruch od {current_player}: {move}")


                # Wyślij ruch do drugiego gracza
                self.players[next_player].sendall(move.encode())
                # Powiadom obecnego gracza, że ruch został przekazany

                # Zmiana tury
                current_player = next_player
                time.sleep(1)

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