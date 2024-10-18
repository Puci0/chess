from controllers import ChessController
from datetime import datetime

while(True):
    controller = ChessController()
    choose = input("\nchoose what you want: 'play', 'display history', 'q': ")

    if choose == "play":
        folder_path = "C:\\Users\\user\\Desktop\\chess_history\\"
        date_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        while(True):
            controller.terminal_view.clear_terminal()
            controller.display()
            move = input("enter a move: ")
            if controller.move(move) == 1:
                break
            controller.save_move(move, folder_path, date_time)

    elif choose == "display history":
        controller.terminal_view.clear_terminal()
        controller.display_history()

    elif choose == "q":
        break