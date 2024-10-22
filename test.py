import chess

def is_not_legal(self,move):
    if move not in self.board.legal_moves:
        return 0

def move(self, move):
    if self.white_castling == 0:
        if move.lower() in ["kg1"]:
            if chess.Move.from_uci("e1g1") in self.board.legal_moves:
                 self.board.push(chess.Move.from_uci("e1g1"))
                self.white_castling = 1
            else:
                self.view.display_message("Roszada nie jest legalna. Wprowadz ruch ponownie")

        if move.lower() in ["kc1"]:
            if chess.Move.from_uci("e1c1") in self.board.legal_moves:
                self.board.push(chess.Move.from_uci("e1c1"))
                self.white_castling = 1
            else:
                self.view.display_message("Roszada nie jest legalna.")

    if self.black_castling == 0:
        if move.lower() in ["kg8"]:
            if chess.Move.from_uci("e8g8") in self.board.legal_moves:
                self.board.push(chess.Move.from_uci("e8g8"))
                self.black_castling = 1
            else:
                self.view.display_message("Roszada nie jest legalna.")

        if move.lower() in ["kc8"]:
            if chess.Move.from_uci("e8c8") in self.board.legal_moves:
                self.board.push(chess.Move.from_uci("e8c8"))
                self.black_castling = 1
            else:
                self.view.display_message("Roszada nie jest legalna.")

    chess_move = self.board.push_san(move)

    if chess_move in self.board.legal_moves:
        self.board.push(chess_move)

        if self.board.is_checkmate():
            self.view.display_message("Mate")
            return 1
        elif self.board.is_stalemate():
            self.view.display_message("Stalemate")
            return 1
    else:
        print("Nielegalny ruch. Wykonaj ruch ponownie.")


# def move(self, move):
#     try:
#         if self.white_castling == 0:
#             if move.lower() in ["kg1"]:
#                 if chess.Move.from_uci("e1g1") in self.board.legal_moves:
#                     self.board.push(chess.Move.from_uci("e1g1"))
#                     self.white_castling = 1
#                     return 0
#                 else:
#                     self.view.display_message("Roszada nie jest legalna.")
#                     return 1
#
#             if move.lower() in ["kc1"]:
#                 if chess.Move.from_uci("e1c1") in self.board.legal_moves:
#                     self.board.push(chess.Move.from_uci("e1c1"))
#                     self.white_castling = 1
#                     return 0
#                 else:
#                     self.view.display_message("Roszada nie jest legalna.")
#                     return 1
#
#         if self.black_castling == 0:
#             if move.lower() in ["kg8"]:
#                 if chess.Move.from_uci("e8g8") in self.board.legal_moves:
#                     self.board.push(chess.Move.from_uci("e8g8"))
#                     self.black_castling = 1
#                     return 0
#                 else:
#                     self.view.display_message("Roszada nie jest legalna.")
#                     return 1
#
#             if move.lower() in ["kc8"]:
#                 if chess.Move.from_uci("e8c8") in self.board.legal_moves:
#                     self.board.push(chess.Move.from_uci("e8c8"))
#                     self.black_castling = 1
#                     return 0
#                 else:
#                     self.view.display_message("Roszada nie jest legalna.")
#                     return 1
#
#         chess_move = self.board.push_san(move)
#
#         if chess_move in self.board.legal_moves:
#             self.board.push(chess_move)
#
#             if self.board.is_checkmate():
#                 self.view.display_message("Mate")
#                 return 1
#             elif self.board.is_stalemate():
#                 self.view.display_message("Stalemate")
#                 return 1
#             else:
#                 return 0
#
#     except ValueError:
#         self.view.display_message("Illegal move. Game finished. \n")
#         return 1
