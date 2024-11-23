from .file_manager import FileManager
from .server_client import ServerClient
from models import CustomBoard, MoveResult, Player
from views import ConsoleView


class MultiplayerGameController:
    def __init__(self, view: ConsoleView) -> None:
        self.view = view
        self.file_manager = FileManager()
        self.client = ServerClient(self.view)
        self.board = None
        self.current_player = None
        self.filename = None
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        self.filename = self.file_manager.get_new_filename('multiplayer')
        self.board = CustomBoard()

        self.view.display_board(self.board)

        if not self.initialize_connection():
            return

        flip_board = self.initialize_game()

        while self.is_running:
            self.view.display_board(self.board, flip=flip_board)

            if self.is_player_turn():
                result = self.handle_player_turn(flip_board)
            else:
                result = self.handle_opponent_turn(flip_board)

            if result == MoveResult.GAME_ENDED:
                message = 'Surrender!' if self.current_player == Player.PLAYER_1 else 'Opponent surrendered!'
                self.view.end_game(message)
                break

            elif result == MoveResult.MATE:
                message = 'You win!' if self.current_player == Player.PLAYER_1 else 'You lost!'
                message = 'Checkmate! ' + message
                self.view.end_game(message)
                break

            elif result == MoveResult.STALEMATE:
                self.view.end_game("Stalemate! It's a draw.")
                break

        self.client.close()

    def is_player_turn(self) -> bool:
        data = self.client.receive_message()

        if data == 'Wprowadz swoj ruch: ':
            self.current_player = Player.PLAYER_1
            return True
        else:
            self.current_player = Player.PLAYER_2
            return False

    def handle_player_turn(self, flip_board: bool) -> MoveResult:
        while True:
            move = self.view.enter_move()
            result = self.board.move(move)

            if result == MoveResult.INVALID_MOVE:
                self.view.display_board(self.board, flip=flip_board)
                self.view.display_message('Illegal move, try again.\n')
                continue

            break

        self.view.display_board(self.board, flip=flip_board)
        self.client.send_message(move)

        if result != MoveResult.GAME_ENDED:
            self.file_manager.save_move(self.filename, move)

        return result

    def handle_opponent_turn(self, flip_board: bool) -> MoveResult:
        self.view.display_message("Waiting for opponent's move...")

        move = self.client.receive_message()

        # if move is None:
        #     return MoveResult.GAME_ENDED

        result = self.board.move(move)
        self.view.display_board(self.board, flip=flip_board)

        if result != MoveResult.GAME_ENDED:
            self.file_manager.save_move(self.filename, move)

        return result

    def initialize_connection(self) -> bool:
        if not self.client.connect():
            self.view.display_message("Unable to connect to the server. Make sure the server is running.")
            return False

        data = self.client.receive_message()
        if data == 'Oczekiwanie na przeciwnika.':
            self.view.display_message('Waiting for the opponent.')

        return True

    def initialize_game(self) -> bool:
        data = self.client.receive_message()
        flip_board = bool(int(data))

        data = self.client.receive_message()
        self.view.display_board(self.board)
        if data == 'Rozpoczynanie partii.':
            self.view.display_message('Rozpoczynanie partii.')

        return flip_board