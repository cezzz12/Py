from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class CommandManager:
    """Handles execution, undo, and redo operations."""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command: Command):
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            raise Exception("Nothing to undo.")
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        if not self._redo_stack:
            raise Exception("Nothing to redo.")
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)


class AddEntityCommand(Command):
    def __init__(self, repository, entity):
        self._repository = repository
        self._entity = entity

    def execute(self):
        self._repository.add(self._entity)

    def undo(self):
        entity_id = self._repository._get_id(self._entity)
        self._repository.remove(entity_id)


class RemoveEntityCommand(Command):
    def __init__(self, repository, entity_id):
        self._repository = repository
        self._entity_id = entity_id
        self._backup = None

    def execute(self):
        self._backup = self._repository.find_by_id(self._entity_id)
        self._repository.remove(self._entity_id)

    def undo(self):
        self._repository.add(self._backup)
