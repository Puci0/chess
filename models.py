import chess
import enum
import requests


class Player(enum.Enum):
    HUMAN = 0
    BOT = 1
    PLAYER_1 = 2
    PLAYER_2 = 3

class Color(enum.Enum):
    WHITE = 0
    BLACK = 1

class Piece(enum.Enum):
    EMPTY = enum.auto()
    PAWN = enum.auto()
    ROOK = enum.auto()
    KNIGHT = enum.auto()
    BISHOP = enum.auto()
    KING = enum.auto()
    QUEEN = enum.auto()

class MoveResult(enum.Enum):
    SUCCESS = "Success"
    MATE = "Mate"
    STALEMATE = "Stalemate"
    INVALID_MOVE = "Invalid Move"
    GAME_ENDED = "Game Ended"

class MenuOption(enum.Enum):
    PLAY_WITH_BOT = 1
    PLAY_MULTIPLAYER = 2
    DISPLAY_HISTORY = 3
    LEAVE_THE_GAME = 4

class HistoryOption(enum.Enum):
    ANALISE_GAME = 1
    AUTOMATIC_GAME = 2
    QUIT = 3

class CustomBoard(chess.Board):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.API_URL = 'https://chess-api.com/v1'
        self.__eval = 0

    def get_eval(self) -> float:
        params = {
            'fen': self.fen(),
            'depth': 1,
            'maxThinkingTime': 1
        }
        # dodac obsluge bledow
        response = requests.post(self.API_URL, json=params)

        data = response.json()

        try:
            eval = data['eval']
            self.__eval = eval
        except KeyError:
            eval = self.__eval

        return eval

    def get_bot_move(self, depth: int = 4, maxThinkingTime: int = 50) -> str:
        params = {
            'fen': self.fen(),
            'depth': depth,
            'maxThinkingTime': maxThinkingTime
        }
        # dodac obsluge bledow
        response = requests.post(self.API_URL, json=params)

        data = response.json()
        move = data['move']

        return move

    def move(self, move: str) -> MoveResult:
        if move.strip().lower() == 'ff':
            return MoveResult.GAME_ENDED

        if not self.is_move_valid(move):
            return MoveResult.INVALID_MOVE

        chess_move = self.parse_san(move)
        self.push(chess_move)

        if self.is_checkmate():
            return MoveResult.MATE
        elif self.is_stalemate():
            return MoveResult.STALEMATE
        else:
            return MoveResult.SUCCESS

    def is_move_valid(self, move: str) -> bool:
        try:
            chess_move = self.parse_san(move)
            if chess_move in self.legal_moves:
                return True
        except ValueError:
            return False
