import time
from datetime import datetime
from views import ConsoleView, TerminalView
from models import Player, CustomBoard
import pathlib
import socket


class ChessClient:
    def __init__(self, server_ip='3.75.88.7', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.server_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            return True
        except (socket.error, ConnectionRefusedError):
            self.connected = False
            return False

    def close(self):
        if self.connected:
            self.server_socket.close()
            self.connected = False

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
        self.view = ConsoleView()
        self.terminal_view = TerminalView()
        self.client = ChessClient()
        self.board = None

        self.current_player = None

        self.history_games_path = (pathlib.Path(__file__).parent / 'history').resolve()
        self.history_games_path.mkdir(exist_ok=True)

        self.bot_games_path = self.bot_games_path = self.history_games_path / 'bot_games'
        self.bot_games_path.mkdir(exist_ok=True)

        self.multi_games_path = self.history_games_path / 'multiplayer_games'
        self.multi_games_path.mkdir(exist_ok=True)

        self.filename = None

    def init_menu(self):
        while True:
            choice = self.view.get_menu_choice()

            if choice == "play with bot":
                self.play_with_bot()

            elif choice == "display history":
                self.display_history()

            elif choice == "play with another player":
                self.play_multiplayer()

            elif choice == "q":
                break


    def play_with_bot(self):
        self.board = CustomBoard()
        self.current_player = Player.HUMAN
        self.filename = self.bot_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

        while True:
            self.terminal_view.clear_terminal()
            self.view.display_board(self.board, flip=False)

            if self.current_player == Player.HUMAN:
                # human playing
                move = self.view.enter_move()
                if self.board.is_move_valid(move):
                    self.board.move(move)
                    self.save_move(move)
                    self.current_player = Player.BOT
                else:
                    time.sleep(1)
                    continue

            else:
                # bot playing
                print('Bot is thinking...')
                move = self.board.get_bot_move(depth=4, maxThinkingTime=50)
                self.board.move(move)
                self.save_move(move)
                self.current_player = Player.HUMAN

    def play_multiplayer(self):
        self.board = CustomBoard()
        self.filename = self.multi_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

        if not self.client.connect():
            self.view.display_message("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
            return

        self.terminal_view.clear_terminal()

        data = self.client.receive_message()
        if data == 'Oczekiwanie na przeciwnika.':
            self.view.display_message('Oczekiwanie na przeciwnika.')

        data = self.client.receive_message()
        FLIP_BOARD = bool(int(data))

        data = self.client.receive_message()
        if data == 'Rozpoczynanie partii.':
            self.view.display_message('Rozpoczynanie partii.')

        while True:
            data = self.client.receive_message()

            self.terminal_view.clear_terminal()
            self.view.display_board(self.board, FLIP_BOARD)

            if data == 'Wprowadz swoj ruch: ':
                move = self.view.enter_move()

                if self.board.is_move_valid(move):
                    self.board.move(move)
                    self.save_move(move)
                else:
                    time.sleep(1)
                    continue

                self.client.send_message(move)

            elif data == 'Oczekiwanie':
                self.view.display_message('Oczekiwanie na ruch przeciwnika...')

                move = self.client.receive_message()

                if move is None:
                    self.view.display_message("Gra została zakończona.")
                    break

                self.board.move(move)
                self.save_move(move)


    def save_move(self, move):
        with open(self.filename, 'a') as f:
            f.write(f"{move}\n")


    def display_history(self):
        self.terminal_view.clear_terminal()
        self.terminal_view.navigate_files(self.bot_games_path, self.multi_games_path, self)

    def analise_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]

        current_index = -1
        self.terminal_view.clear_terminal()
        self.board = CustomBoard()
        self.view.display_board(self.board)

        while True:
            key = self.terminal_view.get_user_input("Use 'd' to move forward, 'a' to move back, other key to quit: ")
            if key == 'd':
                self.terminal_view.clear_terminal()
                if current_index + 1 < len(self.moves):
                    current_index += 1
                    self.board.push_san(self.moves[current_index])
                    self.view.display_board(self.board)
                else:
                    self.view.display_board(self.board)
                    self.view.display_message("!!! That was last move. !!!\n")
            elif key == 'a':
                self.terminal_view.clear_terminal()
                if current_index - 1 >= 0:
                    current_index -= 1
                    self.board.pop()
                    self.view.display_board(self.board)
                else:
                    self.view.display_board(self.board)
                    self.view.display_message("!!! That was first move !!!\n")
            else:
                self.terminal_view.clear_terminal()
                break

    def automatic_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]
        self.board = CustomBoard()
        self.view.display_board(self.board)
        for move in self.moves:
            self.board.push_san(move)
            self.terminal_view.clear_terminal()
            self.view.display_board(self.board)
            time.sleep(1)

        self.terminal_view.get_user_input("Press any key to quit...")