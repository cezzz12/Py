import os
import pickle
from src.domain.domain import Student, Discipline, Grade, ValidationException, NotFoundException


class BaseRepository:
    def __init__(self):
        self._entities = {}

    def add(self, entity):
        if self._get_id(entity) in self._entities:
            raise ValidationException("Entity already exists.")
        self._entities[self._get_id(entity)] = entity

    def remove(self, entity_id):
        if entity_id not in self._entities:
            raise NotFoundException("Entity not found.")
        del self._entities[entity_id]

    def get_all(self) -> list:
        return list(self._entities.values())

    def find_by_id(self, entity_id):
        return self._entities.get(entity_id)

    def find_by_name(self, partial_name: str):
        return [entity for entity in self._entities.values() if partial_name.lower() in entity.name.lower()]

    def _get_id(self, entity):
        raise NotImplementedError


class InMemoryRepository(BaseRepository):
    def _get_id(self, entity):
        if isinstance(entity, Student):
            return entity.student_id
        elif isinstance(entity, Discipline):
            return entity.discipline_id
        elif isinstance(entity, Grade):
            return f"{entity.discipline_id}-{entity.student_id}"


class TextFileRepository(BaseRepository):
    def __init__(self, file_path, entity_type):
        super().__init__()
        self._file_path = file_path
        self._entity_type = entity_type
        self._load()

    def add(self, entity):
        super().add(entity)
        self._save()

    def remove(self, entity_id):
        super().remove(entity_id)
        self._save()

    def _save(self):
        with open(self._file_path, "w") as file:
            for entity in self._entities.values():
                file.write(self._entity_to_text(entity) + "\n")

    def _load(self):
        if not os.path.exists(self._file_path):
            return
        with open(self._file_path, "r") as file:
            for line in file:
                entity = self._text_to_entity(line.strip())
                self._entities[self._get_id(entity)] = entity

    def _entity_to_text(self, entity):
        if isinstance(entity, Student):
            return f"{entity.student_id},{entity.name}"
        elif isinstance(entity, Discipline):
            return f"{entity.discipline_id},{entity.name}"
        elif isinstance(entity, Grade):
            return f"{entity.discipline_id},{entity.student_id},{entity.grade_value}"

    def _text_to_entity(self, text):
        parts = text.split(",")
        if self._entity_type == Student:
            return Student(int(parts[0]), parts[1])
        elif self._entity_type == Discipline:
            return Discipline(int(parts[0]), parts[1])
        elif self._entity_type == Grade:
            return Grade(int(parts[0]), int(parts[1]), float(parts[2]))

    def _get_id(self, entity):
        if isinstance(entity, Student):
            return entity.student_id
        elif isinstance(entity, Discipline):
            return entity.discipline_id
        elif isinstance(entity, Grade):
            return f"{entity.discipline_id}-{entity.student_id}"


class BinaryFileRepository(BaseRepository):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        self._load()

    def add(self, entity):
        super().add(entity)
        self._save()

    def remove(self, entity_id):
        super().remove(entity_id)
        self._save()

    def _save(self):
        with open(self._file_path, "wb") as file:
            pickle.dump(self._entities, file)

    def _load(self):
        if not os.path.exists(self._file_path):
            return
        with open(self._file_path, "rb") as file:
            try:
                self._entities = pickle.load(file)
            except EOFError:
                self._entities = {}

    def _get_id(self, entity):
        if isinstance(entity, Student):
            return entity.student_id
        elif isinstance(entity, Discipline):
            return entity.discipline_id
        elif isinstance(entity, Grade):
            return f"{entity.discipline_id}-{entity.student_id}"
