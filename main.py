from controllers import ChessController

while(True):
    controller = ChessController()
    choose = input("\nchoose what you want: 'play', 'display history', 'q': ")

    if choose == "play":
        controller.play_game()

    elif choose == "display history":
        controller.terminal_view.clear_terminal()
        controller.display_history()

    elif choose == "q":
        break