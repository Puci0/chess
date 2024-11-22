import enum


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