from rich.console import Console
from rich.text import Text
from models import chrs, Color, Piece
import chess

class ConsoleView:
    def __init__(self):
        self.console = Console()

    def display_board(self, board):
        self.console.print("")

        for i in range(8):
            colored_row = Text()
            row_number = str(8 - i)
            colored_row.append(f"  {row_number}   ")

            for j in range(8):
                piece = board.piece_at(chess.square(j, 7 - i))
                if piece is None:
                    colored_row.append(chrs[(Color.WHITE, Piece.EMPTY)], style="dim")
                else:
                    color = Color.WHITE if piece.color == chess.WHITE else Color.BLACK
                    piece_type = {
                        chess.PAWN: Piece.PAWN,
                        chess.ROOK: Piece.ROOK,
                        chess.KNIGHT: Piece.KNIGHT,
                        chess.BISHOP: Piece.BISHOP,
                        chess.QUEEN: Piece.QUEEN,
                        chess.KING: Piece.KING,
                    }[piece.piece_type]

                    if color == Color.WHITE:
                        colored_row.append(chrs[(color, piece_type)], style="bright_white")
                    else:
                        colored_row.append(chrs[(color, piece_type)], style="red")

            self.console.print(colored_row)

        column_labels = "      a b c d e f g h"
        self.console.print("")
        self.console.print(column_labels)