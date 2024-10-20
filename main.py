from controllers import ChessController, ChessClient
import threading
import chess

# def start_client(server_ip='18.192.51.104', server_port=12345):
#     client = ChessClient(server_ip, server_port)
#     if not client.is_server_alive():
#         print("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
#         return
#     controller.set_client(client)
#     threading.Thread(target=client.receive_moves, daemon=True).start()
#     controller.play_multiplayer()

def start_client(server_ip='35.159.41.166', server_port=12345):
    client = ChessClient(server_ip, server_port)
    if not client.is_server_alive():
        print("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
        return

    # Inicjalizacja kontrolera i uruchomienie gry multiplayer
    controller = ChessController()
    controller.set_client(client)
    # threading.Thread(target=client.receive_moves, daemon=True).start()  # Odbieranie ruchów w tle
    controller.play_multiplayer()


if __name__ == "__main__":
    controller = ChessController()

    while True:
        choose = input("\nChoose what you want:\n 'play with bot','play with another player', 'display history', 'q': ")

        if choose == "play with bot":
            controller.play_game()

        elif choose == "display history":
            controller.terminal_view.clear_terminal()
            controller.display_history()

        elif choose == "play with another player":
            controller.terminal_view.clear_terminal()
            start_client()

        elif choose == "q":
            break