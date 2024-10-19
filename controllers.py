import time
import chess
from datetime import datetime
from views import ConsoleView, TerminalView

class ChessController:
    def __init__(self):
        self.board = chess.Board()
        self.view = ConsoleView()
        self.terminal_view = TerminalView()
        self.white_castling = 0
        self.black_castling = 0
        self.folder_path = "C:\\Users\\user\\Desktop\\chess_history\\"
        self.filename = f"{self.folder_path}game_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"

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
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc1"]:
                    if chess.Move.from_uci("e1c1") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e1c1"))
                        self.white_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

            if self.black_castling == 0:
                if move.lower() in ["kg8"]:
                    if chess.Move.from_uci("e8g8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8g8"))
                        self.black_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

                if move.lower() in ["kc8"]:
                    if chess.Move.from_uci("e8c8") in self.board.legal_moves:
                        self.board.push(chess.Move.from_uci("e8c8"))
                        self.black_castling = 1
                        return 0
                    else:
                        self.view.display_message("Roszada nie jest legalna.")
                        return 1

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
                    return 0

        except ValueError:
            self.view.display_message("Illegal move. Game finished. \n")
            return 1

    def play_game(self):
        date_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        while True:
            self.terminal_view.clear_terminal()
            self.display()
            move = input("Enter a move: ")
            if self.move(move) == 1:
                break
            self.save_move(move, self.folder_path, date_time)

    def open_file(self, filename):
        return open(filename, "a")

    def save_move(self, move, folder_path, date_time):
        with self.open_file(f"{folder_path}game_{date_time}.txt") as f:
            f.write(f"{move}\n")

    def display_history(self):
        self.terminal_view.clear_terminal()
        self.terminal_view.navigate_files(self.folder_path, self)

    def analise_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]

        current_index = -1
        self.terminal_view.clear_terminal()
        self.board = chess.Board()
        self.display()

        while True:
            key = self.terminal_view.get_user_input("Use 'd' to move forward, 'a' to move back, other key to quit: ")
            if key == 'd':
                self.terminal_view.clear_terminal()
                if current_index + 1 < len(self.moves):
                    current_index += 1
                    self.board.push_san(self.moves[current_index])
                    self.display()
                else:
                    self.display()
                    self.view.display_message("!!! That was last move. !!!\n")
            elif key == 'a':
                self.terminal_view.clear_terminal()
                if current_index - 1 >= 0:
                    current_index -= 1
                    self.board.pop()
                    self.display()
                else:
                    self.display()
                    self.view.display_message("!!! That was first move !!!\n")
            else:
                self.terminal_view.clear_terminal()
                break

    def automatic_game(self, file_path):
        with open(file_path, 'r') as f:
            self.moves = [move.strip() for move in f.readlines()]
        self.board = chess.Board()
        self.display()
        for move in self.moves:
            self.board.push_san(move)
            self.terminal_view.clear_terminal()
            self.display()
            time.sleep(1)