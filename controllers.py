import time
import chess
from datetime import datetime
from views import ConsoleView, TerminalView
from models import Player, CustomBoard
import pathlib
import socket


class ChessClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def is_server_alive(self):
        try:
            self.server_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            return True
        except (socket.error, ConnectionRefusedError):
            self.connected = False
            return False

    def receive_message(self):
        if not self.connected:
            print("Brak połączenia z serwerem.")
            return None

        try:
            message = self.server_socket.recv(1024).decode()
            if message:
                return message
        except OSError as e:
            print(f"Blad podczas odbierania wiadomosci: {e}")

    def send_message(self, message):
        if not self.connected:
            print("Brak połączenia z serwerem.")
            return
        try:
            self.server_socket.sendall(message.encode())
        except OSError as e:
            print(f"Blad podczas wysylania wiadomosci: {e}")

class ChessController:
    def __init__(self):
        self.board = CustomBoard()
        self.view = ConsoleView()
        self.terminal_view = TerminalView()
        self.white_castling = 0
        self.black_castling = 0
        self.folder_path = (pathlib.Path(__file__).parent / 'chess_history').resolve()
        self.folder_path.mkdir(exist_ok=True)
        self.current_player = Player.HUMAN
        self.client = None

    def set_client(self, client):
        self.client = client

    def display(self):
        self.view.display_board(self.board)

    def move(self, move):
        try:
            if self.white_castling == 0:
                if move.lower() in ["kg1"]:
                    if chess.Move.from_uci("e1g1") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e1g1"))
                        self.white_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc1"]:
                    if chess.Move.from_uci("e1c1") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e1c1"))
                        self.white_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

            if self.black_castling == 0:
                if move.lower() in ["kg8"]:
                    if chess.Move.from_uci("e8g8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8g8"))
                        self.black_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc8"]:
                    if chess.Move.from_uci("e8c8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8c8"))
                        self.black_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

            chess_move = self.board.push_san(move)

            if chess_move in self.board.legal_moves:
                self.board.push(chess_move)

                if self.board.is_checkmate():
                    self.view.display_message("Mate")
                    return 1
                elif self.board.is_stalemate():
                    self.view.display_message("Stalemate")
                    return 1
                else:
                    return 0

        except ValueError:
            self.view.display_message("Illegal move. Game finished. \n")
            return 1

    def play_with_bot(self):
        self.filename = self.folder_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

        while True:
            self.terminal_view.clear_terminal()
            self.display()
            if self.current_player == Player.HUMAN:
                # human playing
                move = input("Enter a move: ")
                if self.move(move) == 1:
                    break
                self.save_move(move)

                self.current_player = Player.BOT
            else:
                # bot playing
                print('Bot is thinking...')
                move = self.board.get_bot_move(depth=4, maxThinkingTime=50)

                if self.move(move) == 1:
                    break
                self.save_move(move)

                self.current_player = Player.HUMAN

    def play_multiplayer(self):
        data = self.client.receive_message()
        if data == 'Oczekiwanie na przeciwnika.':
            self.view.display_message('Oczekiwanie na przeciwnika.')

        data = self.client.receive_message()
        if data == 'Rozpoczynanie partii.':
            self.view.display_message('Rozpoczynanie partii.')

        while True:
            self.terminal_view.clear_terminal()
            self.display()

            data = self.client.receive_message()
            if data == 'Wprowadz swoj ruch: ':
                move = input("Wprowadź swój ruch: ")

                if self.move(move) == 1:
                    break

                self.client.send_message(move)

            elif data.decode() == 'Oczekiwanie':
                self.view.display_message('Oczekiwanie na ruch przeciwnika...')

                move = self.client.receive_message()

                if move is None:
                    self.view.display_message("Gra została zakończona.")
                    break
                if self.move(move) == 1:
                    break


    def save_move(self, move):
        with open(self.filename, 'a') as f:
            f.write(f"{move}\n")

    def display_history(self):
        self.terminal_view.clear_terminal()
        self.terminal_view.navigate_files(self.folder_path, self)

    def analise_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]

        current_index = -1
        self.terminal_view.clear_terminal()
        self.board = chess.Board()
        self.display()

        while True:
            key = self.terminal_view.get_user_input("Use 'd' to move forward, 'a' to move back, other key to quit: ")
            if key == 'd':
                self.terminal_view.clear_terminal()
                if current_index + 1 < len(self.moves):
                    current_index += 1
                    self.board.push_san(self.moves[current_index])
                    self.display()
                else:
                    self.display()
                    self.view.display_message("!!! That was last move. !!!\n")
            elif key == 'a':
                self.terminal_view.clear_terminal()
                if current_index - 1 >= 0:
                    current_index -= 1
                    self.board.pop()
                    self.display()
                else:
                    self.display()
                    self.view.display_message("!!! That was first move !!!\n")
            else:
                self.terminal_view.clear_terminal()
                break

    def automatic_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]
        self.board = chess.Board()
        self.display()
        for move in self.moves:
            self.board.push_san(move)
            self.terminal_view.clear_terminal()
            self.display()
            time.sleep(1)