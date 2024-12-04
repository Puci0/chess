import os
import pathlib
import time
from typing import List
from views import ConsoleView
from models import CustomBoard, HistoryOption
from .command import CommandManager, MoveCommand


class HistoryController:
    def __init__(self, view: ConsoleView) -> None:
        self.view = view

        self.history_games_path = pathlib.Path.home() / "Documents" / "ChessHistory"
        self.history_games_path.mkdir(exist_ok=True)

        self.bot_games_path = self.history_games_path / 'bot_games'
        self.bot_games_path.mkdir(exist_ok=True)

        self.multi_games_path = self.history_games_path / 'multiplayer_games'
        self.multi_games_path.mkdir(exist_ok=True)

        self.is_running = False

    def run(self) -> None:
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
        board = CustomBoard()
        self.view.display_board(board)

        command_manager = CommandManager()

        current_index = -1

        while True:
            action = self.view.get_user_input_for_analysis()

            if action == 'forward':
                if current_index + 1 < len(moves):
                    current_index += 1

                    move = MoveCommand(board, moves[current_index])
                    command_manager.execute_command(move)

                    self.view.display_board(board)
                else:
                    self.view.display_board(board)
                    self.view.display_message("That was last move!\n")
            elif action == 'backward':
                if current_index >= 0:
                    current_index -= 1

                    command_manager.undo()

                    self.view.display_board(board)
                else:
                    self.view.display_board(board)
            else:
                self.view.end_game()
                break

    def automatic_game(self, moves: List[str]) -> None:
        command_manager = CommandManager()

        board = CustomBoard()
        self.view.display_board(board)
        for move in moves:
            time.sleep(1)

            move = MoveCommand(board, move)
            command_manager.execute_command(move)

            self.view.display_board(board)

        self.view.end_game("Press any key to continue...")