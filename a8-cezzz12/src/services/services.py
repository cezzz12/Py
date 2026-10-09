from src.domain.domain import Student, Discipline, Grade, NotFoundException


class StudentService:
    def __init__(self, student_repo, grade_repo):
        self._student_repo = student_repo
        self._grade_repo = grade_repo

    def add_student(self, student_id: int, name: str):
        self._student_repo.add(Student(student_id, name))

    def remove_student(self, student_id: int):
        self._student_repo.remove(student_id)
        self._grade_repo._entities = {key: val for key, val in self._grade_repo._entities.items() if val.student_id != student_id}

    def get_all_students(self) -> list:
        return self._student_repo.get_all()

    def search_students(self, query: str):
        return self._student_repo.find_by_name(query)


class DisciplineService:
    def __init__(self, discipline_repo, grade_repo):
        self._discipline_repo = discipline_repo
        self._grade_repo = grade_repo

    def add_discipline(self, discipline_id: int, name: str):
        self._discipline_repo.add(Discipline(discipline_id, name))

    def remove_discipline(self, discipline_id: int):
        self._discipline_repo.remove(discipline_id)
        self._grade_repo._entities = {key: val for key, val in self._grade_repo._entities.items() if val.discipline_id != discipline_id}

    def get_all_disciplines(self) -> list:
        return self._discipline_repo.get_all()

    def search_disciplines(self, query: str):
        return self._discipline_repo.find_by_name(query)


class GradeService:
    def __init__(self, grade_repo, student_repo, discipline_repo):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._discipline_repo = discipline_repo

    def add_grade(self, discipline_id: int, student_id: int, grade_value: float):
        if not self._student_repo.find_by_id(student_id):
            raise NotFoundException("Student not found.")
        if not self._discipline_repo.find_by_id(discipline_id):
            raise NotFoundException("Discipline not found.")
        self._grade_repo.add(Grade(discipline_id, student_id, grade_value))

    def get_all_grades(self) -> list:
        return self._grade_repo.get_all()
