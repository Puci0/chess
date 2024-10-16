import controllers
import chess
from controllers import ChessController
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

controller = ChessController()
while(True):
    controller.display()
    move = input("enter a move: ")
    if controller.move(move) == 1:
        break
    clear_terminal()