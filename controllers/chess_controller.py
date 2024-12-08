from .history_controller import HistoryController
from .bot_game_controller import BotGameController
from .multiplayer_game_controller import MultiplayerGameController
from config import Config
from views import ConsoleView, GuiView
from models import MenuOption

class ChessController:
    def __init__(self) -> None:
        self.config = Config()

        if self.config.get('view_type') == 'console':
            self.view = ConsoleView()
        elif self.config.get('view_type') == 'gui':
            self.view = GuiView()

        self.bot_game_controller = BotGameController(self.view)
        self.multiplayer_game_controller = None
        self.history_controller = HistoryController(self.view)
        self.is_running = False

    def run(self) -> None:
        self.is_running = True

        while self.is_running:
            selected_option = self.view.display_menu()

            if selected_option == MenuOption.PLAY_WITH_BOT:
                self.bot_game_controller.run()

            elif selected_option == MenuOption.PLAY_MULTIPLAYER:
                self.multiplayer_game_controller = MultiplayerGameController(self.view)
                self.multiplayer_game_controller.run()

            elif selected_option == MenuOption.DISPLAY_HISTORY:
                self.history_controller.run()

            elif selected_option == MenuOption.LEAVE_THE_GAME:
                self.is_running = False