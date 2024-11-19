from models import Player, CustomBoard, MoveResult, MenuOption, HistoryOption
from views import ConsoleView
from datetime import datetime
import pathlib
import socket
import time
import msvcrt
from typing import List
import os


class ChessClient:
    def __init__(self, view: ConsoleView, server_ip='18.194.209.148', server_port=12345):
        self.view = view
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
            self.view.display_message("Brak połączenia z serwerem.")
            return None

        try:
            message = self.server_socket.recv(1024).decode()
            if message:
                return message
        except OSError as e:
            self.view.display_message(f"Blad podczas odbierania wiadomosci: {e}")

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
        self.client = ChessClient(self.view)
        self.history_controller = HistoryController(self.view)
        self.board = None
        self.current_player = None

    def run(self) -> None:
        self.is_running = True

        while self.is_running:
            selected_option = self.view.display_menu()

            if selected_option == MenuOption.PLAY_WITH_BOT:
                self.play_with_bot()
            elif selected_option == MenuOption.PLAY_MULTIPLAYER:
                self.play_multiplayer()
            elif selected_option == MenuOption.DISPLAY_HISTORY:
                self.history_controller.manage_game_history()
            elif selected_option == MenuOption.LEAVE_THE_GAME:
                self.is_running = False


    def play_with_bot(self) -> None:
        filename = self.history_controller.get_new_filename('bot')
        self.board = CustomBoard()
        self.current_player = Player.HUMAN

        self.view.display_board(self.board)
        while True:
            if self.current_player == Player.HUMAN:
                # Human playing
                move = self.view.enter_move()

                result = self.board.move(move)

                if result == MoveResult.GAME_ENDED:
                    self.view.display_board(self.board)
                    self.view.display_message('Surrender!\nPress any key to continue...')
                    msvcrt.getch()
                    self.view.endwin()
                    break

                if result == MoveResult.INVALID_MOVE:
                    self.view.display_board(self.board)
                    self.view.display_message('Illegal move, try again.\n')
                    continue

            else:
                # Bot playing
                self.view.display_message('Bot is thinking...')
                move = self.board.get_bot_move(depth=4, maxThinkingTime=50)
                time.sleep(1.5)
                result = self.board.move(move)

            self.view.display_board(self.board, flip=False)
            self.history_controller.save_move(filename, move)

            if result == MoveResult.MATE:
                self.view.display_board(self.board)
                message = 'You win!' if self.current_player == Player.HUMAN else 'Bot wins!'
                message = 'Checkmate! ' + message
                self.view.display_message(message)
                msvcrt.getch()
                self.view.endwin()
                break
            elif result == MoveResult.STALEMATE:
                self.view.display_board(self.board)
                self.view.display_message("Stalemate! It's a draw.")
                msvcrt.getch()
                self.view.endwin()
                break

            self.current_player = Player.BOT if self.current_player == Player.HUMAN else Player.HUMAN

    def play_multiplayer(self):
        filename = self.history_controller.get_new_filename('multiplayer')
        self.board = CustomBoard()

        self.view.display_board(self.board)

        if not self.client.connect():
            self.view.display_message("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
            return

        data = self.client.receive_message()
        if data == 'Oczekiwanie na przeciwnika.':
            self.view.display_message('Oczekiwanie na przeciwnika.')

        data = self.client.receive_message()
        FLIP_BOARD = bool(int(data))


        data = self.client.receive_message()
        self.view.display_board(self.board)
        if data == 'Rozpoczynanie partii.':
            self.view.display_message('Rozpoczynanie partii.')

        while True:
            data = self.client.receive_message()

            self.view.display_board(self.board, FLIP_BOARD)

            if data == 'Wprowadz swoj ruch: ':
                self.current_player = Player.PLAYER_1

                while True:

                    move = self.view.enter_move()

                    if move.strip().lower() == 'ff':
                        self.view.display_board(self.board, FLIP_BOARD)
                        self.view.display_message('Surrender! Press any key to continue...')
                        msvcrt.getch()
                        self.view.endwin()
                        return

                    if self.board.is_move_valid(move):
                        break
                    else:
                        self.view.display_board(self.board, FLIP_BOARD)
                        self.view.display_message('Illegal move, try again.\n')

                self.client.send_message(move)

            elif data == 'Oczekiwanie':
                self.current_player = Player.PLAYER_2
                self.view.display_message('Oczekiwanie na ruch przeciwnika...')

                move = self.client.receive_message()

                if move is None:
                    self.view.display_message("Gra została zakończona.")
                    break

            result = self.board.move(move)
            self.history_controller.save_move(filename, move)
            if result == "Mate":
                message = 'You win!' if self.current_player == Player.PLAYER_1 else 'You lost!'
                message = 'Checkmate! ' + message
                self.view.display_message(message)
                time.sleep(2)
                break
            elif result == "Stalemate":
                self.view.display_message("Stalemate! It's a draw.")
                time.sleep(2)
                break


class HistoryController:
    def __init__(self, view: ConsoleView):
        self.view = view

        self.history_games_path = (pathlib.Path(__file__).parent / 'history').resolve()
        self.history_games_path.mkdir(exist_ok=True)

        self.bot_games_path = self.history_games_path / 'bot_games'
        self.bot_games_path.mkdir(exist_ok=True)

        self.multi_games_path = self.history_games_path / 'multiplayer_games'
        self.multi_games_path.mkdir(exist_ok=True)

    def manage_game_history(self) -> None:
        self.is_running = True

        while self.is_running:
            bot_files = os.listdir(self.bot_games_path)
            multiplayer_files = os.listdir(self.multi_games_path)

            selected_option, file_name, folder_type = self.view.display_history(bot_files, multiplayer_files)

            if selected_option == HistoryOption.QUIT:
                break

            if folder_type == 1:
                path = self.bot_games_path / file_name
            else:
                path = self.multi_games_path / file_name

            moves = self.read_moves(path)

            if selected_option == HistoryOption.ANALISE_GAME:
                self.analise_game(moves)
            elif selected_option == HistoryOption.AUTOMATIC_GAME:
                self.automatic_game(moves)


    def read_moves(self, file_path: pathlib.Path) -> List[str]:
        with open(file_path, 'r') as f:
            moves = [move.strip() for move in f.readlines()]

        return moves

    def analise_game(self, moves: List[str]) -> None:
        current_index = -1
        board = CustomBoard()
        self.view.display_board(board)

        while True:
            action = self.view.get_user_input_for_analysis()

            if action == 'forward':
                if current_index + 1 < len(moves):
                    current_index += 1
                    board.push_san(moves[current_index])
                    self.view.display_board(board)
                else:
                    self.view.display_board(board)
                    self.view.display_message("That was last move!\n")
            elif action == 'backward':
                if current_index - 1 >= 0:
                    current_index -= 1
                    board.pop()
                    self.view.display_board(board)
                else:
                    self.view.display_board(board)
                    self.view.display_message("That was first move!\n")
            else:
                self.view.endwin()
                break

    def automatic_game(self, moves: List[str]) -> None:
        self.board = CustomBoard()
        self.view.display_board(self.board)
        for move in moves:
            time.sleep(1)
            self.board.push_san(move)
            self.view.display_board(self.board)


        self.view.display_message("Press any key to continue...")
        msvcrt.getch()
        self.view.endwin()

    def get_new_filename(self, game_type: str) -> pathlib.Path:
        if game_type == 'bot':
            return self.bot_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"
        elif game_type == 'multiplayer':
            return self.multi_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

    def save_move(self, filename: pathlib.Path, move: str) -> None:
        with open(filename, 'a') as f:
            f.write(f"{move}\n")
