from datetime import datetime
import pathlib


class FileManager:
    def __init__(self):
        # self.history_games_path = (pathlib.Path(__file__).parent.parent / 'history').resolve()
        self.history_games_path = pathlib.Path.home() / "Documents" / "ChessHistory"
        self.history_games_path.mkdir(exist_ok=True)

        self.bot_games_path = self.history_games_path / 'bot_games'
        self.bot_games_path.mkdir(exist_ok=True)

        self.multi_games_path = self.history_games_path / 'multiplayer_games'
        self.multi_games_path.mkdir(exist_ok=True)

    def get_new_filename(self, game_type: str) -> pathlib.Path:
        if game_type == 'bot':
            return self.bot_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"
        elif game_type == 'multiplayer':
            return self.multi_games_path / f"game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

    def save_move(self, filename: pathlib.Path, move: str) -> None:
        with open(filename, 'a') as f:
            f.write(f"{move}\n")
