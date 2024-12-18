import requests
import chess
from config import Config
from .game_enums import MoveResult


def validate_decorator(func):
    def wrapper(self, move: str):
        if move.strip().lower() == 'ff':
            return MoveResult.GAME_ENDED

        try:
            chess_move = self.parse_san(move)
            if chess_move in self.legal_moves:
                return func(self,chess_move)
        except ValueError:
            return MoveResult.INVALID_MOVE

    return wrapper

class CustomBoard(chess.Board):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Config()
        self.API_URL = 'https://chess-api.com/v1'
        self.__eval = 0

    def get_eval(self) -> float:
        params = {
            'fen': self.fen(),
            'depth': 1,
            'maxThinkingTime': 1
        }

        response = requests.post(self.API_URL, json=params)

        data = response.json()

        try:
            eval = data['eval']
            self.__eval = eval
        except KeyError:
            eval = self.__eval

        return eval

    def get_bot_move(self) -> str:
        params = {
            'fen': self.fen(),
            'depth': self.config.get('depth'),
            'maxThinkingTime': self.config.get('max_thinking_time'),
        }

        response = requests.post(self.API_URL, json=params)

        data = response.json()
        move = data['move']

        return move

    @validate_decorator
    def move(self, move: chess.Move) -> MoveResult:
        self.push(move)

        if self.is_checkmate():
            return MoveResult.MATE
        elif self.is_stalemate():
            return MoveResult.STALEMATE
        else:
            return MoveResult.SUCCESS

    # def is_move_valid(self, move: str) -> bool:
    #     try:
    #         chess_move = self.parse_san(move)
    #         if chess_move in self.legal_moves:
    #             return True
    #     except ValueError:
    #         return False