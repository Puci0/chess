from controllers import ChessController, ChessClient


def start_client(server_ip='18.159.103.78', server_port=12345):
    client = ChessClient(server_ip, server_port)
    if not client.is_server_alive():
        print("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
        return

    controller = ChessController()
    controller.set_client(client)
    controller.play_multiplayer()


if __name__ == "__main__":
    controller = ChessController()

    while True:
        choose = input("\nChoose what you want:\n 'play with bot','play with another player', 'display history', 'q': ")

        if choose == "play with bot":
            controller.play_with_bot()

        elif choose == "display history":
            controller.terminal_view.clear_terminal()
            controller.display_history()

        elif choose == "play with another player":
            controller.terminal_view.clear_terminal()
            start_client()

        elif choose == "q":
            break
