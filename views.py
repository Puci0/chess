from rich.console import Console
from rich.text import Text
from models import chrs, Color, Piece
import chess
from blessed import Terminal
import os
class ConsoleView:
    def __init__(self):
        self.console = Console()

    def display_board(self, board):
        self.console.print("")

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


class TerminalView:
    def __init__(self):
        self.term = Terminal()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def list_files(self, directory):
        current_directory = directory
        selected_index = 0

        while True:
            files = os.listdir(current_directory)
            num_files = len(files)

            self.clear_terminal()
            print(self.term.bold("Game History Manager"))
            print("Files: ")

            for idx, file in enumerate(files):
                if idx == selected_index:
                    print(self.term.bold(self.term.white(f"> {file}")))
                else:
                    print(self.term.blue(f"  {file}"))

            print("\nPress W to go up, S to go down, Enter to open, Q to quit:")

            with self.term.cbreak():
                choice = self.term.inkey()
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'w':
                    selected_index = (selected_index - 1) % num_files
                elif choice.lower() == 's':
                    selected_index = (selected_index + 1) % num_files
                elif choice == "\r":
                    selected = files[selected_index]
                    new_path = os.path.join(current_directory, selected)

                    if os.path.isdir(new_path):
                        current_directory = new_path
                        selected_index = 0
                    elif os.path.isfile(new_path):
                        self.open_file(new_path)

    def open_file(self, file_path):
        self.clear_terminal()
        with open(file_path, 'r') as f:
            print(f.read())
        input(self.term.bold("Press Enter to return..."))

