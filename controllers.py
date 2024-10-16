from views import ConsoleView
import chess

class ChessController:
    def __init__(self):
        self.board = chess.Board()
        self.view = ConsoleView()
        self.white_castling = 0
        self.black_castling = 0

    def display(self):
        self.view.display_board(self.board)

    def move(self, move):
        try:
            if self.white_castling == 0:
                if move.lower() in ["kg1"]:
                    if chess.Move.from_uci("e1g1") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e1g1"))
                        self.white_castling = 1
                        return 0
                    else:
                        print("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc1"]:
                    if chess.Move.from_uci("e1c1") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e1c1"))
                        self.white_castling = 1
                        return 0
                    else:
                        print("Hetmańska roszada nie jest legalna.")
                        return 1
            if self.black_castling == 0:
                if move.lower() in ["kg8"]:
                    if chess.Move.from_uci("e8g8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8g8"))
                        self.black_castling = 1
                        return 0
                    else:
                        print("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc8"]:
                    if chess.Move.from_uci("e8c8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8c8"))
                        self.black_castling = 1
                        return 0
                    else:
                        print("Roszada nie jest legalna.")
                        return 1

            chess_move = self.board.push_san(move)

            if chess_move in self.board.legal_moves:
                self.board.push(chess_move)

                if self.board.is_checkmate():
                    print("Mate")
                    return 1
                elif self.board.is_stalemate():
                    print("Stalemate")
                    return 1
                else:
                    return 0

        except ValueError:
            print("Nielegalny ruch")
            return 1




