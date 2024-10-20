from controllers import ChessController, ChessClient, ChessSerwer
import threading
import time

def start_server():
    global controller
    server = ChessSerwer()
    controller = server.controller

def start_client(server_ip='18.199.224.209', server_port=12345):
    client = ChessClient(server_ip, server_port)
    if not client.is_server_alive():
        print("Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony.")
        return
    controller.set_client(client)
    threading.Thread(target=client.receive_moves, daemon=True).start()
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
            mode = input("Do you want to start a server or join as a client? (server/client): ").strip().lower()

            if mode == "server":
                server_started_event = threading.Event()
                server_thread = threading.Thread(target=start_server, daemon=True)
                server_thread.start()
                print("Uruchamianie serwera...")

                server_started_event.wait()

            elif mode == "client":
                start_client()

        elif choose == "q":
            break