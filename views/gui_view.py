import pygame
from models import CustomBoard, MenuOption, HistoryOption
from typing import List, Union, Tuple, Dict
import sounddevice as sd
import soundfile as sf
import pathlib
import chess
import os
import sys
from datetime import datetime


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
            'highlight': (185, 202, 67),
        }
        self.board_x_offset = (self.SCREEN_WIDTH - (self.square_size * 8)) // 2
        self.board_y_offset = 100

        self.font = pygame.font.SysFont('Arial', 16)
        self.text_color = (0, 0, 0)

        self.piece_images = self.load_piece_images()

        self.pieces_menu_path = pathlib.Path() / "images" / "menu_pieces.png"
        self.chess_string_menu_path = pathlib.Path() / "images" / "chess_string_menu.png"
        self.history_path = pathlib.Path() / "images" / "history.png"

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
                    self.render_border_image(button,20)
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

    def render_border_image(self, button_rect, radius, border_thickness=4):
        transparent_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        self.screen.blit(transparent_surface, button_rect.topleft)
        pygame.draw.rect(self.screen, (0,0,0), button_rect, border_thickness, radius)

    def render_image(self, image_path, x, y):
        image = pygame.image.load(image_path)
        self.screen.blit(image, (x,y))

    def __play_move_sound(self) -> None:
        sd.play(self.data, self.fs)

    def display_message(self, message: str) -> None:
        pass

    def end_game(self, message: str) -> None:
        dialog_width = 270
        dialog_height = 130

        # Kolory i styl
        dialog_color = (50, 50, 50)
        text_color = (255, 255, 255)
        button_color = (200, 200, 200)
        button_hover_color = (180, 180, 180)

        # Utwórz fonty
        font = pygame.font.SysFont(None, 30)
        button_font = pygame.font.SysFont(None, 25)

        # Pozycjonowanie okienka dialogowego na środku ekranu
        dialog_x = (self.screen.get_width() - dialog_width) // 2
        dialog_y = (self.screen.get_height() - dialog_height) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

        # Przyciski
        button_width = 150
        button_height = 50
        button_x = dialog_x + (dialog_width - button_width) // 2
        button_y = dialog_y + dialog_height - button_height - 20
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        running = False

            # Rysowanie tła okienka dialogowego
            pygame.draw.rect(self.screen, dialog_color, dialog_rect, border_radius=10)

            # Rysowanie wiadomości
            message_surface = font.render(message, True, text_color)
            message_rect = message_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + dialog_height // 3 - 10))
            self.screen.blit(message_surface, message_rect)

            # Sprawdź, czy mysz jest nad przyciskiem
            mouse_over_button = button_rect.collidepoint(pygame.mouse.get_pos())
            current_button_color = button_hover_color if mouse_over_button else button_color

            # Rysowanie przycisku
            pygame.draw.rect(self.screen, current_button_color, button_rect, border_radius=5)

            # Rysowanie tekstu na przycisku
            button_text_surface = button_font.render("Wróć do menu", True, text_color)
            button_text_rect = button_text_surface.get_rect(center=button_rect.center)
            self.screen.blit(button_text_surface, button_text_rect)

            # Odśwież tylko dialog i przycisk
            pygame.display.update([dialog_rect, button_rect])

    def draw_surrender_button(self, rect, mouse_pos):
        rect_color = (80, 80, 80) if rect.collidepoint(mouse_pos) else (67, 67, 67)
        font_color = (250, 250, 250) if rect.collidepoint(mouse_pos) else (100, 100, 100)

        pygame.draw.rect(self.screen, rect_color, rect, border_radius=10)

        text_surface = pygame.font.Font(None, 36).render("Surrender", True, font_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def enter_move(self) -> str:
        selected_square = None
        button_rect = pygame.Rect(12, 785, 200, 60)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(mouse_pos):
                        return 'ff'

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = mouse_pos

                    col = (x - self.board_x_offset) // self.square_size
                    row = (y - self.board_y_offset) // self.square_size

                    if 0 <= col < 8 and 0 <= row < 8:
                        clicked_square = (row, col)

                        if selected_square is None:
                            selected_square = clicked_square
                            self.__highlight_square(selected_square)
                        elif selected_square == clicked_square:
                            self.__unhighlight_square(selected_square)
                            selected_square = None
                        else:
                            start_pos = self.__square_to_notation(selected_square)
                            end_pos = self.__square_to_notation(clicked_square)
                            move = f"{start_pos}{end_pos}"

                            return move

            self.draw_surrender_button(button_rect, mouse_pos)
            pygame.display.flip()

    def __square_to_notation(self, square: Tuple) -> str:
        row, col = square

        column_label = chr(ord('a') + col)
        row_label = str(8 - row)

        return f"{column_label}{row_label}"

    def __highlight_square(self, selected_square: Tuple) -> None:
        row, col = selected_square
        x = col * self.square_size + self.board_x_offset
        y = row * self.square_size + self.board_y_offset

        pygame.draw.rect(self.screen, self.board_colors['highlight'], (x, y, self.square_size, self.square_size), 3)
        # pygame.display.flip()

    def __unhighlight_square(self, selected_square: Tuple) -> None:
        row, col = selected_square
        x = col * self.square_size + self.board_x_offset
        y = row * self.square_size + self.board_y_offset

        is_white_square = (row + col) % 2 == 0
        color = self.board_colors["white"] if is_white_square else self.board_colors["black"]

        pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size), 3)
        # pygame.display.flip()

    def display_board(self, board: CustomBoard, flip: bool=False, play_sound: bool = False) -> None:
        self.screen.fill((61, 61, 59))

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
                    self.screen.blit(text_surface, (self.board_x_offset + self.square_size * 0.04, row * self.square_size + self.square_size * 0.03 + self.board_y_offset))

                if row == 7:
                    text_surface = self.font.render(column_labels[col], True, self.text_color)
                    self.screen.blit(text_surface, (self.board_x_offset + self.square_size * 0.88 + col * self.square_size, row * self.square_size + self.square_size * 0.78 + self.board_y_offset))

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

    def __extract_date_from_filename(self, filename: str) -> datetime:
        splits = filename.split('_')[1:]
        date_str = splits[0] + "-" + splits[1]
        date_str = date_str.replace('-', ' ')[:-4]
        return datetime.strptime(date_str, "%d %m %Y %H %M %S")

    def display_header(self,font):
        legend_surface = font.render(f"Type{' ' * 15}Winner {' ' * 20} Action {' ' * 18} Moves {' ' * 32} Datetime",True, (255, 255, 255))
        rect_x = 150
        rect_y = 200
        rect_width = 900
        rect_height = 45
        pygame.draw.rect(self.screen, (46, 45, 43), (rect_x, rect_y, rect_width, rect_height))
        title_rect = legend_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        self.screen.blit(legend_surface, title_rect)

    def draw_history_section(self, files: Dict[str, int], y_offset: int, type, mouse_pos: Tuple[int, int], font) -> Tuple[
        int, List[Tuple[pygame.Rect, str]], List[Tuple[pygame.Rect, str]], List[Tuple[pygame.Rect, str]]]:
        file_rects = []
        analyze_rects = []
        auto_rects = []

        for file, count in files.items():
            if count < 10:
                if type == "Online":
                    text_surface = font.render(
                        f"{type} {' ' * 12} Player {' ' * 55} {count} {' ' * 22 + str(self.__extract_date_from_filename(file))}",
                        True, (0, 0, 0))
                else:
                    text_surface = font.render(
                        f"{type} {' ' * 17} Player {' ' * 55} {count} {' ' * 22 + str(self.__extract_date_from_filename(file))}",
                        True, (0, 0, 0))
            else:
                if type == "Online":
                    text_surface = font.render(
                        f"{type} {' ' * 12} Player {' ' * 55} {count} {' ' * 20 + str(self.__extract_date_from_filename(file))}",
                        True, (0, 0, 0))
                else:
                    text_surface = font.render(
                        f"{type} {' ' * 17} Player {' ' * 55} {count} {' ' * 20 + str(self.__extract_date_from_filename(file))}",
                        True, (0, 0, 0))
            text_height = text_surface.get_height()
            rect = pygame.Rect(150, y_offset, 900, text_height + 10)
            file_rects.append((rect, file))
            pygame.draw.rect(self.screen, (255, 255, 255), rect)
            self.screen.blit(text_surface, (rect.x + 5, rect.y + 5))

            button_width = 50
            button_height = 20
            button_gap = 10
            button_x_start = rect.x + 330

            # Analyze button
            button_rect1 = pygame.Rect(button_x_start, rect.y + 5, button_width, button_height)
            analyze_rects.append((button_rect1, file))
            pygame.draw.rect(self.screen, (85, 175, 218), button_rect1)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect1, 2)

            # Auto button
            button_rect2 = pygame.Rect(button_x_start + button_width + button_gap, rect.y + 5, button_width,
                                       button_height)
            auto_rects.append((button_rect2, file))
            pygame.draw.rect(self.screen, (78, 133, 222), button_rect2)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect2, 2)

            # Highlight buttons on hover
            if button_rect1.collidepoint(mouse_pos):
                self.render_border_image(button_rect1, 0, 3)
            if button_rect2.collidepoint(mouse_pos):
                self.render_border_image(button_rect2, 0, 3)

            # Add button labels
            font_small = pygame.font.Font(None, 16)
            text1 = font_small.render("Analiza", True, (255, 255, 255))
            text2 = font_small.render("Auto", True, (255, 255, 255))
            self.screen.blit(text1, (button_rect1.x + (button_width - text1.get_width()) // 2,
                                     button_rect1.y + (button_height - text1.get_height()) // 2))
            self.screen.blit(text2, (button_rect2.x + (button_width - text2.get_width()) // 2,
                                     button_rect2.y + (button_height - text2.get_height()) // 2))

            y_offset += 35

        return y_offset, file_rects, analyze_rects, auto_rects

    def display_history(self, bot_files: Dict[str, int], multiplayer_files: Dict[str, int]) -> Tuple[
        HistoryOption, Union[str, None], int]:

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        bot_files_list = sorted(bot_files.keys(), key=self.__extract_date_from_filename)[-8:]
        multiplayer_files_list = sorted(multiplayer_files.keys(), key=self.__extract_date_from_filename)[-8:]
        bot_files = {file: bot_files[file] for file in bot_files_list}
        multiplayer_files = {file: multiplayer_files[file] for file in multiplayer_files_list}
        font = pygame.font.Font(None, 30)

        while True:
            self.screen.fill((61, 61, 59))
            mouse_pos = pygame.mouse.get_pos()

            self.render_image(self.history_path, 240, 30)

            self.display_header(font)

            y_offset = 250

            y_offset, bot_file_rects, analize_bot_rects, auto_bot_rects = self.draw_history_section(bot_files, y_offset, "Bot",
                                                                                                    mouse_pos, font)

            y_offset, multiplayer_file_rects, analize_multiplayer_rects, auto_multiplayers_rects = self.draw_history_section(
                multiplayer_files, y_offset, "Online", mouse_pos, font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, file in analize_bot_rects:
                            if rect.collidepoint(mouse_pos):
                                return HistoryOption.ANALISE_GAME, file, 1

                        for rect, file in auto_bot_rects:
                            if rect.collidepoint(mouse_pos):
                                return HistoryOption.AUTOMATIC_GAME, file, 1

                        for rect, file in analize_multiplayer_rects:
                            if rect.collidepoint(mouse_pos):
                                return HistoryOption.ANALISE_GAME, file, 2

                        for rect, file in auto_multiplayers_rects:
                            if rect.collidepoint(mouse_pos):
                                return HistoryOption.AUTOMATIC_GAME, file, 2