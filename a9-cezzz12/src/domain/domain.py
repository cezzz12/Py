class Student:
    def __init__(self, student_id: int, name: str):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"Student [ID: {self.student_id}, Name: {self.name}]"


class Discipline:
    def __init__(self, discipline_id: int, name: str):
        self.discipline_id = discipline_id
        self.name = name

    def __str__(self):
        return f"Discipline [ID: {self.discipline_id}, Name: {self.name}]"


class Grade:
    def __init__(self, discipline_id: int, student_id: int, grade_value: float):
        self.discipline_id = discipline_id
        self.student_id = student_id
        self.grade_value = grade_value

    def __str__(self):
        return f"Grade [Discipline ID: {self.discipline_id}, Student ID: {self.student_id}, Grade: {self.grade_value}]"


class ValidationException(Exception):
    pass


class NotFoundException(Exception):
    pass
