import pygame
from models import CustomBoard, MenuOption, HistoryOption
from typing import List, Union, Tuple
import sounddevice as sd
import soundfile as sf
import pathlib
import chess
import os
import sys

class GuiView:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.running = True
        self.square_size = 750 // 8

        self.button_text_color = (0,0,0)
        self.button_font = pygame.font.Font(None, 36)
        self.text_list = ["Play with bot", "Play multiplayer", "Display history", "Leave game"]

        self.button_bot = pygame.Rect((self.SCREEN_WIDTH-250)/2,270,250,50) # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_multiplayer = pygame.Rect((self.SCREEN_WIDTH-250)/2, 340, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_history = pygame.Rect((self.SCREEN_WIDTH-250)/2, 410, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_leave_game = pygame.Rect((self.SCREEN_WIDTH-250)/2, 480, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_list = [self.button_bot, self.button_multiplayer, self.button_history, self.button_leave_game]

        self.button_color = (255,255,255)
        self.board_colors = {
            # "white": (240, 217, 181),
            # "black": (181, 136, 99),
            "white": (157, 156, 154),
            "black": (126, 125, 123),
        }
        self.board_x_offset = (self.SCREEN_WIDTH - (self.square_size * 8)) // 2
        self.board_y_offset = 100

        self.font = pygame.font.SysFont('Arial', 18)
        self.text_color = (0, 0, 0)

        self.piece_images = self.load_piece_images()

        self.pieces_menu_path = pathlib.Path() / "images" / "menu_pieces.png"
        self.chess_string_menu_path = pathlib.Path() / "images" / "chess_string_menu.png"

        self.move_sound = self.__resource_path("./models/move_sound.mp3")
        self.data, self.fs = sf.read(self.move_sound, dtype='float32')

    def load_piece_images(self):
        pieces_path = pathlib.Path() / "images" / "pieces"

        pieces = {}
        piece_types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["white", "black"]
        for color in colors:
            for piece in piece_types:
                filename = pieces_path / f"{color}-{piece}.png"
                image = pygame.image.load(filename)
                image = pygame.transform.scale(image, (self.square_size, self.square_size))
                pieces[f"{color}_{piece}"] = image
        return pieces

    def __resource_path(self, relative_path: str) -> os.path:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def display_menu(self):
        current_cursor = pygame.SYSTEM_CURSOR_ARROW

        while self.running:
            self.screen.fill((61, 61, 59))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button_history.collidepoint(mouse_pos):
                            return MenuOption.DISPLAY_HISTORY
                        elif self.button_leave_game.collidepoint(mouse_pos):
                            pygame.quit()
                            #return MenuOption.LEAVE_THE_GAME
                        elif self.button_bot.collidepoint(mouse_pos):
                            return MenuOption.PLAY_WITH_BOT
                        elif self.button_multiplayer.collidepoint(mouse_pos):
                            return MenuOption.PLAY_MULTIPLAYER

            # render buttons and texts on
            for button,text in zip(self.button_list,self.text_list):
                pygame.draw.rect(self.screen, self.button_color, button, border_radius=20)
                self.render_button_text(button, text)

            # mouse change on buttons
            mouse_pos = pygame.mouse.get_pos()
            for button in self.button_list:
                if button.collidepoint(mouse_pos):
                    self.render_border_image(button)
                    if current_cursor != pygame.SYSTEM_CURSOR_HAND:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        current_cursor = pygame.SYSTEM_CURSOR_HAND
                    break
            else:
                if current_cursor != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    current_cursor = pygame.SYSTEM_CURSOR_ARROW

            # render images
            self.render_image(self.pieces_menu_path,55,600)
            self.render_image(self.chess_string_menu_path, 280,20)

            pygame.display.update()
        pygame.quit()

    def render_button_text(self, button_rect, text):
        text_surface = self.button_font.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface,text_rect)

    def render_border_image(self, button_rect):
        transparent_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        self.screen.blit(transparent_surface, button_rect.topleft)
        pygame.draw.rect(self.screen, (0,0,0), button_rect, 4, border_radius=20)

    def render_image(self, image_path, x, y):
        image = pygame.image.load(image_path)
        self.screen.blit(image, (x,y))

    def __play_move_sound(self) -> None:
        sd.play(self.data, self.fs)

    def enter_move(self) -> str:
        pass

    def display_board(self, board: CustomBoard, flip: bool=False, play_sound: bool = False) -> None:
        eval = board.get_eval()
        self.__display_eval(eval)

        column_labels = "abcdefgh"
        if flip:
            board = board.transform(chess.flip_horizontal).transform(chess.flip_vertical)
            column_labels = column_labels[::-1]


        for row in range(8):
            if flip:
                row_number = str(row + 1)
            else:
                row_number = str(8 - row)

            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size

                is_white_square = (row + col) % 2 == 0
                color = self.board_colors["white"] if is_white_square else self.board_colors["black"]

                pygame.draw.rect(self.screen, color, (x + self.board_x_offset, y + self.board_y_offset, self.square_size, self.square_size))

                if col == 0:
                    text_surface = self.font.render(row_number, True, self.text_color)
                    self.screen.blit(text_surface, (self.board_x_offset + self.square_size * 0.03, row * self.square_size + self.square_size * 0.03 + self.board_y_offset))

                if row == 7:
                    text_surface = self.font.render(column_labels[col], True, self.text_color)
                    self.screen.blit(text_surface, (self.board_x_offset + + self.square_size * 0.89 + col * self.square_size, row * self.square_size + self.square_size * 0.8 + self.board_y_offset))

                piece = board.piece_at(chess.square(col, 7 - row))

                if piece:
                    color_name = "white" if piece.color == chess.WHITE else "black"
                    piece_name = {
                        chess.PAWN: "pawn",
                        chess.ROOK: "rook",
                        chess.KNIGHT: "knight",
                        chess.BISHOP: "bishop",
                        chess.QUEEN: "queen",
                        chess.KING: "king",
                    }[piece.piece_type]
                    image_key = f"{color_name}_{piece_name}"

                    self.screen.blit(self.piece_images[image_key], (x + self.board_x_offset, y + + self.board_y_offset))


        pygame.display.flip()

        if play_sound:
            self.__play_move_sound()

    def __display_eval(self, eval_score) -> None:
        bar_length = self.square_size * 8
        bar_height = 40
        max_eval = 25

        eval = max(-max_eval, min(max_eval, eval_score))

        normalized_eval = eval / max_eval

        black_width = int((1 - normalized_eval) / 2 * bar_length)
        white_width = bar_length - black_width


        white_color = (240, 240, 240)
        black_color = (10, 10, 10)

        bar_x = 0
        bar_y = 30
        pygame.draw.rect(self.screen, white_color, (bar_x + self.board_x_offset, bar_y, white_width, bar_height))
        pygame.draw.rect(self.screen, black_color, (bar_x + white_width + self.board_x_offset, bar_y, black_width, bar_height))

    def display_history(self, bot_files: List[str], multiplayer_files: List[str]) -> Tuple[HistoryOption, Union[str, None], int]:
        pass