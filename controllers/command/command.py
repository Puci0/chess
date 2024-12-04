from abc import ABC, abstractmethod
from models import CustomBoard


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class MoveCommand(Command):
    def __init__(self, board: CustomBoard, move: str):
        self.board = board
        self.move = move

    def execute(self):
        self.board.push_san(self.move)

    def undo(self):
        self.board.pop()


class CommandManager:
    def __init__(self):
        self.executed_commands = []
        self.undone_commands = []

    def execute_command(self, command: Command):
        command.execute()
        self.executed_commands.append(command)
        self.undone_commands.clear()

    def undo(self):
        if len(self.executed_commands) > 0:
            command = self.executed_commands.pop()
            command.undo()
            self.undone_commands.append(command)

    # def redo(self):
    #     if len(self.undone_commands) > 0:
    #         command = self.undone_commands.pop()
    #         command.execute()
    #         self.executed_commands.append(command)

    # def replay(self):
    #     pass