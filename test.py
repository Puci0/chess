# from rich.console import Console
# from rich.text import Text
# from rich.table import Table
# from rich import box
# import time
# import os
# import shutil
# import msvcrt
#
# console = Console()
#
# chess_text = [
#     " ██████╗██╗  ██╗███████╗███████╗███████╗",
#     "██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝",
#     "██║     ███████║█████╗  ███████╗███████╗",
#     "██║     ██╔══██║██╔══╝  ╚════██║╚════██║",
#     "╚██████╗██║  ██║███████╗███████║███████║",
#     " ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝"
# ]
#
#
# king = [
#     "   .::.                                                                                                     .::.    ",
#     "   _::_                                                                                                     _::_    ",
#     " _/____\_                                                        ()                                       _/____\_  ",
#     " \      /                                                      <~~~~>                                     \      /  ",
#     "  \____/                                                        \__/                                       \____/   ",
#     "  (____)            __/'''\               ______               (____)                                      (____)   ",
#     "   |  |            ]___ o  }             (______)               |  |                                        |  |    ",
#     "   |__|                /   }              \ __ /                |  |                    __                  |__|    ",
#     "  /    \             /~    }               |  |                 |__|                   (  )                /    \\  ",
#     " (______)            \____/                |__|                /____\                   ||                (______)  ",
#     "(________)           /____\               /____\              (______)                 /__\              (________) ",
#     "/________\          (______)             (______)            (________)               (____)             /________\\"
# ]
#
#
# def display_text_animated(n,console, text_lines, delay=0.05):
#     terminal_width = shutil.get_terminal_size().columns
#     max_length = max(len(line) for line in text_lines)
#     displayed_text = [""] * len(text_lines)
#
#     for char_index in range(max_length + 1):
#         for line_index, line in enumerate(text_lines):
#             centered_line = line[:char_index].center(terminal_width)
#             displayed_text[line_index] = centered_line
#         styled_text = Text("\n" * n + "\n".join(displayed_text), style="on gray25")
#         console.clear()
#         console.print(styled_text)
#         time.sleep(delay)
#
# options = [
#     "play with bot",
#     "play multiplayer",
#     "display history",
#     "leave the game"
# ]
# selected_index = 0
# highlight_style = "rgb(123,129,129) on gray100"
#
# def draw_table(console, selected_index, margin=False):
#     table = Table(show_header=False, box=box.ROUNDED, show_lines=True)
#     table.add_column(justify="center")
#
#     for index, option in enumerate(options):
#         if index == selected_index:
#             table.add_row(Text(option, style=highlight_style))
#         else:
#             table.add_row(Text(option))
#
#     if margin == False:
#         console.print(table, justify="center", overflow="crop")
#     else:
#         console.print("\n" * 2)
#         console.print(table, justify="center", overflow="crop")
#
#
#
# os.system("color 8F")
# os.system('cls' if os.name == 'nt' else 'clear')
# display_text_animated(3,console, chess_text, delay=0.02)
# draw_table(console, selected_index)
# display_text_animated(18,console, king, delay=0)
#
# while True:
#     key = msvcrt.getch()
#     if key == b'w' and selected_index > 0:
#         selected_index -= 1
#         console.clear()
#         for line in chess_text:
#             console.print(Text(" ", style="on gray25"))
#         draw_table(console, selected_index, True)
#     elif key == b's' and selected_index < len(options) - 1:
#         selected_index += 1
#         console.clear()
#         for line in chess_text:
#             console.print(Text(" ", style="on gray25"))
#         draw_table(console, selected_index, True)
#     elif key == b'q':
#         break


# from rich.console import Console
# from rich.table import Table
#
# # Tworzymy nową tabelę szachownicy
# table = Table(show_header=False)
#
#
# for _ in range(8):
#     table.add_column()
#
# for _ in range(8):
#     table.add_row('P', 'p', ' ', ' ', ' ', ' ', ' ', ' ')
import pathlib
from datetime import datetime

history_games_path = (pathlib.Path(__file__).parent / 'history').resolve()
history_games_path.mkdir(exist_ok=True)

bot_games_path = history_games_path / 'bot_games'
bot_games_path.mkdir(exist_ok=True)

multi_games_path = history_games_path / 'multiplayer_games'
multi_games_path.mkdir(exist_ok=True)


print(type(bot_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"))