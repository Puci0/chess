import pygame
from models import CustomBoard, MenuOption, HistoryOption
from typing import List, Union, Tuple
from datetime import datetime

class GuiView:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.running = True

        self.button_text_color = (0,0,0)
        self.button_font = pygame.font.Font(None, 36)
        self.text_list = ["Play with bot", "Play multiplayer", "Display history", "Leave game"]

        self.button_bot = pygame.Rect((self.SCREEN_WIDTH-250)/2,270,250,50) # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_multiplayer = pygame.Rect((self.SCREEN_WIDTH-250)/2, 340, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_history = pygame.Rect((self.SCREEN_WIDTH-250)/2, 410, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_leave_game = pygame.Rect((self.SCREEN_WIDTH-250)/2, 480, 250, 50)  # (x_start_od_lewej,y_start_od_gory,szerokosc,wysokosc)
        self.button_list = [self.button_bot, self.button_multiplayer, self.button_history, self.button_leave_game]

        self.button_color = (255,255,255)

        self.pieces_menu_path = "C:\\Users\\user\\Desktop\\chess\\images\\menu_pieces.png"
        self.chess_string_menu_path = "C:\\Users\\user\\Desktop\\chess\\images\\chess_string_menu.png"
        self.history_path = "C:\\Users\\user\\Desktop\\chess\\images\\history.png"

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

    def __extract_date_from_filename(self, filename: str) -> datetime:
        splits = filename.split('_')[1:]
        date_str = splits[0] + "-" + splits[1]
        date_str = date_str.replace('-', ' ')[:-4]
        return datetime.strptime(date_str, "%d %m %Y %H %M %S")

    def display_history(self, bot_files: List[str], multiplayer_files: List[str]) -> Tuple[HistoryOption, Union[str, None], int]:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        bot_files = sorted(bot_files, key=self.__extract_date_from_filename)[-25:]
        multiplayer_files = sorted(multiplayer_files, key=self.__extract_date_from_filename)[-25:]

        font = pygame.font.Font(None, 30)

        while True:
            self.screen.fill((61, 61, 59))
            mouse_pos = pygame.mouse.get_pos()

            self.render_image(self.history_path, 240, 30)
            legend_surface = font.render(f"Type{' ' * 15}Winner {' '*20} Action {' '*18} Moves {' '*32} Datetime", True, (255, 255, 255))
            rect_x = 150
            rect_y = 200
            rect_width = 900
            rect_height = 45
            pygame.draw.rect(self.screen, (46, 45, 43), (rect_x, rect_y, rect_width, rect_height))
            title_rect = legend_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
            self.screen.blit(legend_surface, title_rect)

            y_offset = 250
            bot_file_rects = []
            analize_bot_rects = []
            auto_bot_rects = []
            for file in bot_files:
                text_surface = font.render(f"Bot {' ' * 15} Skibibot {' ' * 53} 40 {' ' * 20 + str(self.__extract_date_from_filename(file))}", True, (0, 0, 0))
                text_height = text_surface.get_height()
                rect = pygame.Rect(150, y_offset, 900, text_height + 10)
                bot_file_rects.append((rect, file))
                pygame.draw.rect(self.screen, (255,255,255), rect)
                self.screen.blit(text_surface, (rect.x + 5, rect.y + 5))
                button_width = 50
                button_height = 20
                button_gap = 10
                button_x_start = rect.x + 15 + font.size("Bot")[0] + font.size("Skibibot")[0] + 15

                button_rect1 = pygame.Rect(button_x_start + 180, rect.y + 5, button_width, button_height)
                analize_bot_rects.append((button_rect1,file))
                pygame.draw.rect(self.screen, (85, 175, 218), button_rect1)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect1, 2)

                button_rect2 = pygame.Rect(button_x_start + button_width + button_gap + 180, rect.y + 5, button_width,button_height)
                auto_bot_rects.append((button_rect2,file))
                pygame.draw.rect(self.screen, (85, 175, 218), button_rect2)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect2, 2)

                if button_rect1.collidepoint(mouse_pos):
                    self.render_border_image(button_rect1,0,3)
                if button_rect2.collidepoint(mouse_pos):
                    self.render_border_image(button_rect2,0,3)

                font_small = pygame.font.Font(None, 16)

                text1 = font_small.render("Analiza", True, (255, 255, 255))
                text1_width = text1.get_width()
                text1_height = text1.get_height()
                text1_x = button_rect1.x + (button_width - text1_width) // 2
                text1_y = button_rect1.y + (button_height - text1_height) // 2
                self.screen.blit(text1, (text1_x, text1_y))

                text2 = font_small.render("Auto", True, (255, 255, 255))
                text2_width = text2.get_width()
                text2_height = text2.get_height()
                text2_x = button_rect2.x + (button_width - text2_width) // 2
                text2_y = button_rect2.y + (button_height - text2_height) // 2
                self.screen.blit(text2, (text2_x, text2_y))

                y_offset += 35

            multiplayer_file_rects = []
            analize_multiplayer_rects = []
            auto_multiplayers_rects = []
            for file in multiplayer_files:
                text_surface = font.render(f"Online {' ' * 10} Pucio {' ' * 57} 35 {' ' * 20 + str(self.__extract_date_from_filename(file))}", True, (0, 0, 0))
                text_height = text_surface.get_height()
                rect = pygame.Rect(150, y_offset, 900, text_height + 10)
                multiplayer_file_rects.append((rect, file))
                pygame.draw.rect(self.screen, (255,255,255), rect)
                self.screen.blit(text_surface, (rect.x + 5, rect.y + 5))
                button_width = 50
                button_height = 20
                button_gap = 10
                button_x_start = rect.x + 15 + font.size("Bot")[0] + font.size("Skibibot")[0] + 15

                button_rect1 = pygame.Rect(button_x_start + 180, rect.y + 5, button_width, button_height)
                analize_multiplayer_rects.append((button_rect1,file))
                pygame.draw.rect(self.screen, (85, 175, 218), button_rect1)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect1, 2)

                button_rect2 = pygame.Rect(button_x_start + button_width + button_gap + 180, rect.y + 5, button_width,button_height)
                auto_multiplayers_rects.append((button_rect2,file))
                pygame.draw.rect(self.screen, (85, 175, 218), button_rect2)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect2, 2)

                if button_rect1.collidepoint(mouse_pos):
                    self.render_border_image(button_rect1,0,3)
                if button_rect2.collidepoint(mouse_pos):
                    self.render_border_image(button_rect2,0,3)

                font_small = pygame.font.Font(None, 16)

                text1 = font_small.render("Analiza", True, (255, 255, 255))
                text1_width = text1.get_width()
                text1_height = text1.get_height()
                text1_x = button_rect1.x + (button_width - text1_width) // 2
                text1_y = button_rect1.y + (button_height - text1_height) // 2
                self.screen.blit(text1, (text1_x, text1_y))

                text2 = font_small.render("Auto", True, (255, 255, 255))
                text2_width = text2.get_width()
                text2_height = text2.get_height()
                text2_x = button_rect2.x + (button_width - text2_width) // 2
                text2_y = button_rect2.y + (button_height - text2_height) // 2
                self.screen.blit(text2, (text2_x, text2_y))
                y_offset += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, file in analize_bot_rects:
                            if rect.collidepoint(mouse_pos):
                                #print("bot_analize", rect)
                                return HistoryOption.ANALISE_GAME, file, 1

                        for rect, file in auto_bot_rects:
                             if rect.collidepoint(mouse_pos):
                                 #print("bot_auto", rect, file)
                                 return HistoryOption.AUTOMATIC_GAME, file, 1

                        for rect, file in analize_multiplayer_rects:
                            if rect.collidepoint(mouse_pos):
                                #print("mp_analize",rect)
                                return HistoryOption.ANALISE_GAME, file, 2

                        for rect, file in auto_multiplayers_rects:
                            if rect.collidepoint(mouse_pos):
                                #print("mp_auto",rect)
                                return HistoryOption.AUTOMATIC_GAME, file, 2