import chess
import enum
import requests


class Player(enum.Enum):
    HUMAN = 0
    BOT = 1

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

chrs = {
    (Color.WHITE, Piece.EMPTY): "\u00B7 ",
    (Color.WHITE, Piece.PAWN): "P ",
    (Color.WHITE, Piece.ROOK): "R ",
    (Color.WHITE, Piece.KNIGHT): "N ",
    (Color.WHITE, Piece.BISHOP): "B ",
    (Color.WHITE, Piece.KING): "K ",
    (Color.WHITE, Piece.QUEEN): "Q ",
    (Color.BLACK, Piece.EMPTY): "\u00B7 ",
    (Color.BLACK, Piece.PAWN): "P ",
    (Color.BLACK, Piece.ROOK): "R ",
    (Color.BLACK, Piece.KNIGHT): "N ",
    (Color.BLACK, Piece.BISHOP): "B ",
    (Color.BLACK, Piece.KING): "K ",
    (Color.BLACK, Piece.QUEEN): "Q ",
}

class CustomBoard(chess.Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.API_URL = 'https://chess-api.com/v1'

    def get_eval(self):
        params = {
            'fen': self.fen(),
            'depth': 1,
            'maxThinkingTime': 1
        }
        # dodac obsluge bledow
        response = requests.post(self.API_URL, json=params)

        data = response.json()
        eval = data['eval']

        return eval

    def get_bot_move(self, depth=4, maxThinkingTime=50):
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