from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import box
import time
import os
import shutil
import msvcrt

console = Console()

chess_text = [
    " ██████╗██╗  ██╗███████╗███████╗███████╗",
    "██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝",
    "██║     ███████║█████╗  ███████╗███████╗",
    "██║     ██╔══██║██╔══╝  ╚════██║╚════██║",
    "╚██████╗██║  ██║███████╗███████║███████║",
    " ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝"
]

# chess_text = [
#     "                                            .::.",
#     "                                            _::_",
#     "                                            _/____\_",
#     "                                            \      /"
#     "                                           \____/"
#     "                                           (____)"
#     " ██████╗██╗  ██╗███████╗███████╗███████╗    |  |",
#     "██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝    |__|",
#     "██║     ███████║█████╗  ███████╗███████╗   /    \\",
#     "██║     ██╔══██║██╔══╝  ╚════██║╚════██║   (______)",
#     "╚██████╗██║  ██║███████╗███████║███████║   (________)",
#     " ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   /________\\"
# ]

king = [
    "   .::.",
    "   _::_",
    "   _/____\_",
    "   \      /",
    "  \____/",
    "  (____)",
    "   |  |",
    "   |__|",
    "  /    \\",
    "  (______)",
    "  (________)",
    "  /________\\"
]

def display_text_animated(console, text_lines, delay=0.05):
    terminal_width = shutil.get_terminal_size().columns
    max_length = max(len(line) for line in text_lines)
    displayed_text = [""] * len(text_lines)

    for char_index in range(max_length + 1):
        for line_index, line in enumerate(text_lines):
            centered_line = line[:char_index].center(terminal_width)
            displayed_text[line_index] = centered_line
        styled_text = Text("\n" * 3 + "\n".join(displayed_text), style="on gray25")
        console.clear()
        console.print(styled_text)
        time.sleep(delay)

os.system("color 8F")
os.system('cls' if os.name == 'nt' else 'clear')


display_text_animated(console, chess_text, delay=0.02)
#display_text_animated(console, king, delay=0.02)

options = [
    "play with bot",
    "play multiplayer",
    "display history",
    "leave the game"
]

selected_index = 0
highlight_style = "rgb(123,129,129) on gray100"

def draw_table(console, selected_index, margin=False):
    table = Table(show_header=False, box=box.ROUNDED, show_lines=True)
    table.add_column(justify="center")

    for index, option in enumerate(options):
        if index == selected_index:
            table.add_row(Text(option, style=highlight_style))
        else:
            table.add_row(Text(option))

    if margin == False:
        console.print(table, justify="center", overflow="crop")
    else:
        console.print("\n" * 2)
        console.print(table, justify="center", overflow="crop")

draw_table(console, selected_index)

while True:
    key = msvcrt.getch()
    if key == b'w' and selected_index > 0:
        selected_index -= 1
        console.clear()
        for line in chess_text:
            console.print(Text(" ", style="on gray25"))
        draw_table(console, selected_index, True)
    elif key == b's' and selected_index < len(options) - 1:
        selected_index += 1
        console.clear()
        for line in chess_text:
            console.print(Text(" ", style="on gray25"))
        draw_table(console, selected_index, True)
    elif key == b'q':
        break


