from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import box
from models import Color, Piece, MenuOption, HistoryOption, CustomBoard
from typing import Tuple, List, Union
import sounddevice as sd
import soundfile as sf
import chess
import os
import msvcrt
import shutil
import time
import curses
import numpy as np
import sys


class ConsoleView:
    def __init__(self) -> None:
        self.screen = None
        self.console = Console()

        os.system("color 8F")
        os.system('mode con: cols=166 lines=48')
        os.system('cls' if os.name == 'nt' else 'clear')

        curses.wrapper(self.__initialize_screen)

        color_1 = (144, 140, 140)
        color_2 = (112, 108, 100)
        background_color = (61, 61, 59)

        curses.init_color(10, round(color_1[0] * 3.92), round(color_1[1] * 3.92), round(color_1[2] * 3.92))
        curses.init_color(11, round(color_2[0] * 3.92), round(color_2[1] * 3.92), round(color_2[2] * 3.92))
        curses.init_color(12, round(background_color[0] * 3.92), round(background_color[1] * 3.92), round(background_color[2] * 3.92))

        curses.init_pair(17, curses.COLOR_WHITE, 12)
        curses.init_pair(18, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(19, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(20, curses.COLOR_BLACK, 10)
        curses.init_pair(21, curses.COLOR_BLACK, 11)
        curses.init_pair(22, curses.COLOR_WHITE, 10)
        curses.init_pair(23, curses.COLOR_WHITE, 11)
        curses.init_pair(24, 12, 12)
        curses.init_pair(25, 10, 11)
        curses.init_pair(26, 11, 10)

        self.WHITE_ON_GRAY = curses.color_pair(17)
        self.WHITE_ON_WHITE = curses.color_pair(18)
        self.BLACK_ON_BLACK = curses.color_pair(19)
        self.BLACK_ON_GREEN = curses.color_pair(20)
        self.BLACK_ON_YELLOW = curses.color_pair(21)
        self.WHITE_ON_GREEN = curses.color_pair(22)
        self.WHITE_ON_YELLOW = curses.color_pair(23)
        self.GREEN_ON_YELLOW = curses.color_pair(25)
        self.YELLOW_ON_GREEN = curses.color_pair(26)

        self.chrs = {
            Piece.EMPTY: np.array(list((
                "           "
                "           "
                "           "
                "           "
                "           "
            ))).reshape((5, 11)),
            Piece.PAWN: np.array(list((
                "           "
                "    (#)    "
                "    )#(    "
                "   (###)   "
                "  [#####]  "
            ))).reshape((5, 11)),
            Piece.ROOK: np.array(list((
                "   [`'`]   "
                "    |:|    "
                "    |:|    "
                "    |:|    "
                "   [___]   "
            ))).reshape((5, 11)),
            Piece.KNIGHT: np.array(list((
                "   _/|     "
                "   // o\\   "
                "   || ._)  "
                "   //__\\   "
                "   )___(   "
            ))).reshape((5, 11)),
            Piece.BISHOP: np.array(list((
                "     o     "
                "    (^)    "
                "   -=H=-   "
                "    ] [    "
                "   /___\   "
            ))).reshape((5, 11)),
            Piece.KING: np.array(list((
                "    +++    "
                "    / \\    "
                "    | |    "
                "    [ ]    "
                "   [___]   "
            ))).reshape((5, 11)),
            Piece.QUEEN: np.array(list((
                "    ***    "
                "    / \\    "
                "    | |    "
                "    [ ]    " 
                "   [___]   "
            ))).reshape((5, 11)),
        }

        self.chess_text = [
            " ██████╗██╗  ██╗███████╗███████╗███████╗",
            "██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝",
            "██║     ███████║█████╗  ███████╗███████╗",
            "██║     ██╔══██║██╔══╝  ╚════██║╚════██║",
            "╚██████╗██║  ██║███████╗███████║███████║",
            " ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝",
            "                                        ",
            "                                        "
        ]

        self.game_history_text = [
            " ██████╗  █████╗ ███╗   ███╗███████╗     ██╗  ██╗██╗███████╗████████╗ ██████╗ ██████╗ ██╗   ██╗",
            "██╔════╝ ██╔══██╗████╗ ████║██╔════╝     ██║  ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝",
            "██║  ███╗███████║██╔████╔██║█████╗       ███████║██║███████╗   ██║   ██║   ██║██████╔╝ ╚████╔╝ ",
            "██║   ██║██╔══██║██║╚██╔╝██║██╔══╝       ██╔══██║██║╚════██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝  ",
            "╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗     ██║  ██║██║███████║   ██║   ╚██████╔╝██║  ██║   ██║   ",
            "╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝      ╚═╝  ╚═╝╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ",
        ]

        self.pieces = [
            "   .::.                                                                                                     .::.    ",
            "   _::_                                                                                                     _::_    ",
            " _/____\_                                                        ()                                       _/____\_  ",
            " \      /                                                      <~~~~>                                     \      /  ",
            "  \____/                                                        \__/                                       \____/   ",
            "  (____)            __/'''\               ______               (____)                                      (____)   ",
            "   |  |            ]___ o  }             (______)               |  |                                        |  |    ",
            "   |__|                /   }              \ __ /                |  |                    __                  |__|    ",
            "  /    \             /~    }               |  |                 |__|                   (  )                /    \\  ",
            " (______)            \____/                |__|                /____\                   ||                (______)  ",
            "(________)           /____\               /____\              (______)                 /__\              (________) ",
            "/________\          (______)             (______)            (________)               (____)             /________\\",
        ]

        self.options = [
            "Play with bot",
            "Play multiplayer",
            "Display history",
            "Leave the game"
        ]

        self.animated_text_displayed_menu = False
        self.animated_text_displayed_history = False
        self.move_sound = self.resource_path("./models/move_sound.mp3")
        self.data, self.fs = sf.read(self.move_sound, dtype='float32')

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def __play_move_sound(self):
        sd.play(self.data, self.fs)

    def __initialize_screen(self, screen) -> None:
        self.screen = screen
        rows, cols = self.screen.getmaxyx()
        board_width = 8 * 11
        x_offset = max(0, (cols - board_width) // 2)
        self.offset = x_offset

    def display_menu(self) -> MenuOption:
        self.__clear_terminal()
        selected_index = 0

        if not self.animated_text_displayed_menu:
            self.__display_text(4, self.chess_text, animated=True, delay=0.02)
            self.__draw_table(selected_index)
            self.__display_text(22, self.pieces, animated=True, delay=0)
            self.animated_text_displayed_menu = True

        while True:
            self.__display_text(4, self.chess_text)
            self.__draw_table(selected_index)
            self.__display_text(22, self.pieces)

            key = msvcrt.getch()
            if key == b'w' and selected_index > 0:
                selected_index -= 1
                self.console.clear()
                for _ in self.chess_text:
                    self.console.print(Text(" ", style="on gray25"))
                self.__draw_table(selected_index, True)
            elif key == b's' and selected_index < len(self.options) - 1:
                selected_index += 1
                self.console.clear()
                for _ in self.chess_text:
                    self.console.print(Text(" ", style="on gray25"))
                self.__draw_table(selected_index, True)
            elif key == b'\r':
                if selected_index == 0:
                    return MenuOption.PLAY_WITH_BOT
                elif selected_index == 1:
                    return MenuOption.PLAY_MULTIPLAYER
                elif selected_index == 2:
                    return MenuOption.DISPLAY_HISTORY
                elif selected_index == 3:
                    os.system("color 0F")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return MenuOption.LEAVE_THE_GAME

    def __display_text(self, n: int, text_lines: list, animated: bool = False, delay: float = 0.02) -> None:
        terminal_width = shutil.get_terminal_size().columns
        displayed_text = []

        if animated:
            max_length = max(len(line) for line in text_lines)
            displayed_text = [""] * len(text_lines)

            for char_index in range(max_length + 1):
                for line_index, line in enumerate(text_lines):
                    centered_line = line[:char_index].center(terminal_width)
                    displayed_text[line_index] = centered_line
                styled_text = Text("\n" * n + "\n".join(displayed_text), style="on gray25")
                self.console.clear()
                self.console.print(styled_text)
                time.sleep(delay)

        else:
            for line in text_lines:
                centered_line = line.center(terminal_width)
                displayed_text.append(centered_line)

            styled_text = Text("\n" * n + "\n".join(displayed_text), style="on gray25")
            self.console.clear()
            self.console.print(styled_text)

    def __draw_table(self, selected_index: int, margin: bool = False) -> None:
        highlight_style = "rgb(123,129,129) on gray100"

        table = Table(show_header=False, box=box.ROUNDED, show_lines=True)
        table.add_column(justify="center")

        for index, option in enumerate(self.options):
            if index == selected_index:
                table.add_row(Text(option, style=highlight_style))
            else:
                table.add_row(Text(option))
        if not margin:
            self.console.print(table, justify="center", overflow="crop")
        else:
            self.console.print("\n")
            self.console.print(table, justify="center", overflow="crop")

    def enter_move(self) -> str:
        self.display_message("Enter a move: ")
        return self.screen.getstr().decode()

    def display_message(self, message: str) -> None:
        self.screen.addstr(" " * self.offset)
        self.screen.addstr(message)
        self.screen.refresh()

    def end_game(self, message: str = None) -> None:
        if message:
            self.display_message(message)
            msvcrt.getch()

        curses.endwin()

    def get_user_input_for_analysis(self) -> str:
        self.display_message("Use 'd' to move forward, 'a' to move back, any other key to quit: ")
        key = msvcrt.getch()
        if key == b'd':
            return 'forward'
        elif key == b'a':
            return 'backward'
        else:
            return 'quit'

    def display_board(self, board: CustomBoard, flip: bool=False, play_sound: bool = False) -> None:
        self.screen.clear()
        self.screen.bkgd(curses.color_pair(24))

        self.screen.attron(self.WHITE_ON_GRAY)
        self.screen.addstr("\n")

        eval = board.get_eval()
        self.__display_eval(eval)

        column_labels = "abcdefgh"

        if flip:
            board = board.transform(chess.flip_horizontal).transform(chess.flip_vertical)
            column_labels = column_labels[::-1]


        for row_index in range(8):
            if flip:
                row_number = str(row_index + 1)
            else:
                row_number = str(8 - row_index)

            for i in range(5):
                self.screen.addstr(" " * self.offset)
                for column_index in range(8):

                    for j in range(11):
                        is_white_square = (row_index + column_index) % 2 == 0

                        if column_index==0 and i==0 and j==0:
                            color_pair = self.YELLOW_ON_GREEN if is_white_square else self.GREEN_ON_YELLOW
                            self.screen.addstr(str(row_number), color_pair | curses.A_BOLD)
                            continue

                        if row_index==7 and i==4 and j==10:
                            color_pair = self.YELLOW_ON_GREEN if is_white_square else self.GREEN_ON_YELLOW
                            self.screen.addstr(column_labels[column_index], color_pair | curses.A_BOLD)
                            continue

                        piece = board.piece_at(chess.square(column_index, 7 - row_index))

                        is_white_square = (row_index + column_index) % 2 == 0

                        if is_white_square:
                            color_pair = self.BLACK_ON_GREEN if piece and piece.color == chess.BLACK else self.WHITE_ON_GREEN
                        else:
                            color_pair = self.BLACK_ON_YELLOW if piece and piece.color == chess.BLACK else self.WHITE_ON_YELLOW


                        if piece is None:
                            self.screen.addstr(self.chrs[Piece.EMPTY][i, j], color_pair)
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
                                self.screen.addstr(self.chrs[piece_type][i, j], color_pair | curses.A_BOLD)
                            else:
                                self.screen.addstr(self.chrs[piece_type][i, j], color_pair)

                self.screen.addstr('\n')

        self.screen.refresh()

        if play_sound:
            self.__play_move_sound()

    def __display_eval(self, eval_score) -> None:
        bar_length = 11 * 8
        max_eval = 25

        eval = max(-max_eval, min(max_eval, eval_score))

        normalized_eval = eval / max_eval
        black_count = int((1 - normalized_eval) / 2 * bar_length)

        white_count = bar_length - black_count

        for _ in range(2):
            self.screen.addstr(" " * self.offset)
            for _ in range(white_count):
                self.screen.addstr(" ", self.WHITE_ON_WHITE)
            for _ in range(black_count):
                self.screen.addstr(" ", self.BLACK_ON_BLACK)
            self.screen.addstr('\n')
        self.screen.addstr('\n')

    def __clear_terminal(self) -> None:
        os.system('cls')

    def __display_files(self, files1: List, files2: List, selected_index: List[int]) -> None:
        # terminal_width = shutil.get_terminal_size().columns
        highlight_style = "rgb(123,129,129) on gray100"

        table = Table(show_header=True)
        table.add_column("BOT GAMES", width=42, header_style="bold white on #767676", justify="center")
        table.add_column("MULTIPLAYER GAMES", width=42, header_style="bold white on #767676", justify="center")

        max_files = max(len(files1), len(files2))
        for i in range(max_files):
            folder1_display = (f">[{highlight_style}]{files1[i]}[/]"
                               if selected_index[0] == 1 and i == selected_index[1]
                               else f" {files1[i]}") if i < len(files1) else ""

            folder2_display = (f"> [{highlight_style}]{files2[i]}[/]"
                               if selected_index[0] == 2 and i == selected_index[1]
                               else f"  {files2[i]}") if i < len(files2) else ""

            table.add_row(folder1_display, folder2_display)

        self.console.print("\n" * 10)
        self.console.print(table, justify="center")
        self.console.print("\n[bold white on #767676] Press W to go up, S to go down, Tab to switch column, Enter to open in analysis mode, R to run game with 1sec delay, Q to quit[/]", justify="center")

    def __extract_date_from_filename(self, filename: str) -> datetime:
        splits = filename.split('_')[1:]
        date_str = splits[0] + "-" + splits[1]
        date_str = date_str.replace('-', ' ')[:-4]
        return datetime.strptime(date_str, "%d %m %Y %H %M %S")

    def display_history(self, bot_files: List[str], multiplayer_files: List[str]) -> Tuple[HistoryOption, Union[str, None], int]:
        self.__clear_terminal()

        bot_files = sorted(bot_files, key=self.__extract_date_from_filename)[-25:]
        multiplayer_files = sorted(multiplayer_files, key=self.__extract_date_from_filename)[-25:]

        if not self.animated_text_displayed_history:
            self.__display_text(4, self.game_history_text, animated=True, delay=0.001)
            self.animated_text_displayed_history = True
        else:
            self.__display_text(4, self.game_history_text)

        selected_index = [1, 0]

        while True:
            self.console.clear()
            self.__display_files(bot_files, multiplayer_files, selected_index)

            choice = msvcrt.getch()

            if choice == b'q':
                return HistoryOption.QUIT, None, -1

            if choice == b'a':
                selected_index[0] = 1
                selected_index[1] = 0

            elif choice == b'd':
                selected_index[0] = 2
                selected_index[1] = 0

            if choice in [b'w', b's']:
                if selected_index[0] == 1:
                    if choice == b'w' and selected_index[1] > 0:
                        selected_index[1] -= 1
                    elif choice == b's' and selected_index[1] < len(bot_files) - 1:
                        selected_index[1] += 1
                else:
                    if choice == b'w' and selected_index[1] > 0:
                        selected_index[1] -= 1
                    elif choice == b's' and selected_index[1] < len(multiplayer_files) - 1:
                        selected_index[1] += 1

            elif choice == b'\r':
                if selected_index[0] == 1:
                    return HistoryOption.ANALISE_GAME, bot_files[selected_index[1]], 1
                else:
                    return HistoryOption.ANALISE_GAME, multiplayer_files[selected_index[1]], 2

            elif choice == b'r':
                if selected_index[0] == 1:
                    return HistoryOption.AUTOMATIC_GAME, bot_files[selected_index[1]], 1
                else:
                    return HistoryOption.AUTOMATIC_GAME, multiplayer_files[selected_index[1]], 2
