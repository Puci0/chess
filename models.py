import chess
import enum
import requests
import numpy as np


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

chrs = {
    (Color.WHITE, Piece.EMPTY): np.array(list((
    "           "
    "           "
    "           "
    "           "
    "           "
))).reshape((5, 11)),
    (Color.WHITE, Piece.PAWN): np.array(list((
    "           "
    "     ()    "
    "     )(    "
    "    (  )   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.WHITE, Piece.ROOK): np.array(list((
    "   [`'`']  "
    "    |::|   "
    "    |::|   "
    "    |::|   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.WHITE, Piece.KNIGHT): np.array(list((
    "   _/|     "
    "   // o\\   "
    "   || ._)  "
    "   //__\\   "
    "   )___(   "
))).reshape((5, 11)),
    (Color.WHITE, Piece.BISHOP): np.array(list((
    "      o    "
    "     (^)   "
    "    -=H=-  "
    "     ] [   "
    "    /___\  "
))).reshape((5, 11)),
    (Color.WHITE, Piece.KING): np.array(list((
    "    ++++   "
    "    /  \\   "
    "    |  |   "
    "    [  ]   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.WHITE, Piece.QUEEN): np.array(list((
    "    ****   "
    "    /  \\   "
    "    |  |   "
    "    [  ]   " 
    "   [____]  "
))).reshape((5, 11)),
    (Color.BLACK, Piece.EMPTY): np.array(list((
    "           "
    "           "
    "           "
    "           "
    "           "
))).reshape((5, 11)),
    (Color.BLACK, Piece.PAWN): np.array(list((
    "           "
    "     ()    "
    "     )(    "
    "    (  )   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.BLACK, Piece.ROOK): np.array(list((
    # "            "
    "   [`'`']  "
    "    |::|   "
    "    |::|   "
    "    |::|   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.BLACK, Piece.KNIGHT): np.array(list((
    "   _/|     "
    "   // o\\   "
    "   || ._)  "
    "   //__\\   "
    "   )___(   "
))).reshape((5, 11)),
    (Color.BLACK, Piece.BISHOP): np.array(list((
    "      o    "
    "     (^)   "
    "    -=H=-  "
    "     ] [   "
    "    /___\\  "
))).reshape((5, 11)),
    (Color.BLACK, Piece.KING): np.array(list((
    "    ++++   "
    "    /  \\   "
    "    |  |   "
    "    [  ]   "
    "   [____]  "
))).reshape((5, 11)),
    (Color.BLACK, Piece.QUEEN): np.array(list((
    "    ****   "
    "    /  \\   "
    "    |  |   "
    "    [  ]   " 
    "   [____]  "
))).reshape((5, 11)),
}

# chrs = {
#     (Color.WHITE, Piece.EMPTY): "\u00B7 ",
#     (Color.WHITE, Piece.PAWN): "\u2659 ",
#     (Color.WHITE, Piece.ROOK): "\u2656 ",
#     (Color.WHITE, Piece.KNIGHT): "\u2658 ",
#     (Color.WHITE, Piece.BISHOP): "\u2657 ",
#     (Color.WHITE, Piece.KING): "\u2654 ",
#     (Color.WHITE, Piece.QUEEN): "\u2655 ",
#     (Color.BLACK, Piece.EMPTY): "\u00B7 ",
#     (Color.BLACK, Piece.PAWN): "\u265F ",
#     (Color.BLACK, Piece.ROOK): "\u265C ",
#     (Color.BLACK, Piece.KNIGHT): "\u265E ",
#     (Color.BLACK, Piece.BISHOP): "\u265D ",
#     (Color.BLACK, Piece.KING): "\u265A ",
#     (Color.BLACK, Piece.QUEEN): "\u265B ",
# }

class CustomBoard(chess.Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.API_URL = 'https://chess-api.com/v1'
        self.__eval = 0

    def get_eval(self):
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

    def move(self, move):
        chess_move = self.parse_san(move)
        self.push(chess_move)
        if self.is_checkmate():
            return "Mate"
        elif self.is_stalemate():
            return "Stalemate"
        else:
            return True

    def is_move_valid(self, move):
        try:
            chess_move = self.parse_san(move)
            if chess_move in self.legal_moves:
                return True
        except ValueError:
            pass
        return False

