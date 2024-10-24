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

    def get_menu_choice(self):
        choice = input("\nChoose what you want:\n 'play with bot','play with another player', 'display history', 'q': ")
        return choice

    def enter_move(self):
        move = input("Enter a move: ")
        return move

    def display_board(self, board, flip: bool=False):
        self.clear_terminal()
        self.console.print("")

        eval = board.get_eval()
        self.display_eval(eval)

        if flip:
            board = board.transform(chess.flip_horizontal).transform(chess.flip_vertical)

        for i in range(8):
            colored_row = Text()
            if flip:
                row_number = str(i + 1)
            else:
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

        column_labels = "a b c d e f g h"
        if flip:
            column_labels = column_labels[::-1]
        column_labels = "      " + column_labels
        self.console.print("")
        self.console.print(column_labels)
        self.console.print("")

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

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')


class TerminalView:
    def __init__(self):
        self.term = Terminal()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_files(self, files1, files2, selected_index):
        self.clear_terminal()

        print(self.term.bold("Game History Manager"))
        print(f"\n{' ' * 2}{self.term.bold('Bot Games'):<45}{self.term.bold('Multiplayer Games')}")

        max_files = max(len(files1), len(files2))

        for i in range(max_files):
            # Dla pierwszej kolumny
            if i < len(files1):
                if selected_index[0] == 1 and i == selected_index[1]:
                    folder1_display = self.term.bold(self.term.white(f"> {files1[i]}     "))
                else:
                    folder1_display = self.term.blue(f"  {files1[i]}     ")
            else:
                folder1_display = " " * 35

            # Dla drugiej kolumny
            if i < len(files2):
                if selected_index[0] == 2 and i == selected_index[1]:
                    folder2_display = self.term.bold(self.term.white(f"> {files2[i]}"))
                else:
                    folder2_display = self.term.blue(f"  {files2[i]}")
            else:
                folder2_display = ""

            print(folder1_display + folder2_display)

        print(
            "\nPress W to go up, S to go down, Tab to switch column, Enter to open in analysis mode, R to run game with 1sec delay, Q to quit:")

    def navigate_files(self, folder1_path, folder2_path, controller):
        current_directory1 = folder1_path
        current_directory2 = folder2_path

        selected_index = [1, 0]  # [kolumna, indeks pliku]

        while True:
            files1 = os.listdir(current_directory1)
            files2 = os.listdir(current_directory2)

            num_files1 = len(files1)
            num_files2 = len(files2)

            self.display_files(files1, files2, selected_index)

            choice = msvcrt.getch()

            if choice == b'q':
                break

            if choice == b'\t':
                # Zmiana kolumny
                selected_index[0] = 2 if selected_index[0] == 1 else 1
                selected_index[1] = 0

            if choice == b'w':
                # Ruch w górę
                if selected_index[0] == 1:
                    selected_index[1] = (selected_index[1] - 1) % num_files1
                else:
                    selected_index[1] = (selected_index[1] - 1) % num_files2

            elif choice == b's':
                # Ruch w dół
                if selected_index[0] == 1:
                    selected_index[1] = (selected_index[1] + 1) % num_files1
                else:
                    selected_index[1] = (selected_index[1] + 1) % num_files2

            elif choice == b'\r':
                # Wybór pliku
                if selected_index[0] == 1:
                    selected = files1[selected_index[1]]
                    new_path = os.path.join(current_directory1, selected)
                    if os.path.isdir(new_path):
                        current_directory1 = new_path
                        selected_index[1] = 0
                    elif os.path.isfile(new_path):
                        controller.analise_game(new_path)
                        break
                else:
                    selected = files2[selected_index[1]]
                    new_path = os.path.join(current_directory2, selected)
                    if os.path.isdir(new_path):
                        current_directory2 = new_path
                        selected_index[1] = 0
                    elif os.path.isfile(new_path):
                        controller.analise_game(new_path)
                        break

            elif choice == b'r':
                # Automatyczne uruchomienie gry
                if selected_index[0] == 1:
                    selected = files1[selected_index[1]]
                    new_path = os.path.join(current_directory1, selected)
                    controller.automatic_game(new_path)
                else:
                    selected = files2[selected_index[1]]
                    new_path = os.path.join(current_directory2, selected)
                    controller.automatic_game(new_path)

    def get_user_input(self, message):
        print(message)
        return msvcrt.getch().decode("utf-8")