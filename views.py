from rich.console import Console
from rich.text import Text
from models import chrs, Color, Piece
import chess
from blessed import Terminal
import os
import msvcrt


class ConsoleView:
    def __init__(self):
        self.console = Console()

    def display_board(self, board):
        self.console.print("")

        eval = board.get_eval()
        self.display_eval(eval)

        for i in range(8):
            colored_row = Text()
            row_number = str(8 - i)
            colored_row.append(f"  {row_number}   ")

            for j in range(8):
                piece = board.piece_at(chess.square(j, 7 - i))
                if piece is None:
                    colored_row.append(chrs[(Color.WHITE, Piece.EMPTY)], style="dim")
                else:
                    color = Color.WHITE if piece.color == chess.WHITE else Color.BLACK
                    piece_type = {
                        chess.PAWN: Piece.PAWN,
                        chess.ROOK: Piece.ROOK,
                        chess.KNIGHT: Piece.KNIGHT,
                        chess.BISHOP: Piece.BISHOP,
                        chess.QUEEN: Piece.QUEEN,
                        chess.KING: Piece.KING,
                    }[piece.piece_type]

                    if color == Color.WHITE:
                        colored_row.append(chrs[(color, piece_type)], style="bright_white")
                    else:
                        colored_row.append(chrs[(color, piece_type)], style="red")

            self.console.print(colored_row)

        column_labels = "      a b c d e f g h"
        self.console.print("")
        self.console.print(column_labels)

    def display_eval(self, eval_score):
        bar_length = 15
        max_eval = 10

        eval = max(-max_eval, min(max_eval, eval_score))

        # black_count = round((1 - ((eval + max_eval)) / (2 * max_eval)) * bar_length)

        normalized_eval = eval / max_eval
        black_count = int((1 - normalized_eval) / 2 * bar_length)

        white_count = bar_length - black_count

        bar = '■' * white_count + '□' * black_count

        print(f"     |{bar}|")

    def display_message(self, message):
        self.console.print(message)

class TerminalView:
    def __init__(self):
        self.term = Terminal()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_files(self, files, selected_index):
        self.clear_terminal()
        print(self.term.bold("Game History Manager"))
        print("Files: ")

        for i, file in enumerate(files):
            if i == selected_index:
                print(self.term.bold(self.term.white(f"> {file}")))
            else:
                print(self.term.blue(f"  {file}"))

        print("\nPress W to go up, S to go down, Enter to open in analysis mode, R to run game with 1sec delay, Q to quit:")

    def navigate_files(self, folder_path, controller):
        current_directory = folder_path
        selected_index = 0

        while True:
            files = os.listdir(current_directory)
            num_files = len(files)

            self.display_files(files, selected_index)

            choice = msvcrt.getch()
            if choice == b'q':
                break
            elif choice == b'w':
                selected_index = (selected_index - 1) % num_files
            elif choice == b's':
                selected_index = (selected_index + 1) % num_files
            elif choice == b'\r':
                selected = files[selected_index]
                new_path = os.path.join(current_directory, selected)
                if os.path.isdir(new_path):
                    current_directory = new_path
                    selected_index = 0
                elif os.path.isfile(new_path):
                    controller.analise_game(new_path)
                    break
            elif choice == b'r':
                selected = files[selected_index]
                new_path = os.path.join(current_directory, selected)
                controller.automatic_game(new_path)

    def get_user_input(self, message):
        print(message)
        return msvcrt.getch().decode("utf-8")