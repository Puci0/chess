import time
from views import ConsoleView
from .file_manager import FileManager
from models import CustomBoard, Player, MoveResult
from .command import CommandManager, MoveCommand


class BotGameController:
    def __init__(self, view: ConsoleView):
        self.view = view
        self.file_manager = FileManager()
        self.board = None
        self.current_player = None
        self.filename = None
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        self.filename = self.file_manager.get_new_filename('bot')
        self.board = CustomBoard()
        self.command_manager = CommandManager()
        self.current_player = Player.HUMAN

        while self.is_running:
            self.view.display_board(self.board)

            if self.current_player == Player.HUMAN:
                result = self.__handle_human_turn()
            else:
                result = self.__handle_bot_turn()

            if result == MoveResult.GAME_ENDED:
                self.view.end_game('Surrender!')
                break

            elif result == MoveResult.MATE:
                message = 'You win!' if self.current_player == Player.HUMAN else 'Bot wins!'
                message = 'Checkmate! ' + message
                self.view.end_game(message)
                break

            elif result == MoveResult.STALEMATE:
                self.view.end_game("Stalemate! It's a draw.")
                break

            self.current_player = Player.BOT if self.current_player == Player.HUMAN else Player.HUMAN

    def __handle_human_turn(self) -> MoveResult:
        while True:
            move = self.view.enter_move()

            move_command = MoveCommand(self.board, move)
            result = self.command_manager.execute_command(move_command)

            if result == MoveResult.INVALID_MOVE:
                self.view.display_board(self.board)
                self.view.display_message('Illegal move, try again.\n')
                continue

            break

        play_sound = False

        if result != MoveResult.GAME_ENDED:
            self.file_manager.save_move(self.filename, move)
            play_sound = True

        self.view.display_board(self.board, play_sound=play_sound)

        return result

    def __handle_bot_turn(self) -> MoveResult:
        self.view.display_message('Bot is thinking...')
        move = self.board.get_bot_move()
        time.sleep(1.5)

        move_command = MoveCommand(self.board, move)
        result = self.command_manager.execute_command(move_command)

        self.view.display_board(self.board, play_sound=True)
        self.file_manager.save_move(self.filename, move)

        return result
