from src.repository.repository import (
    StudentRepositoryTextFile,
    StudentRepositoryBinary,
    StudentRepositoryInMemory,
)
from src.domain.domain import Student


class StudentService:
    def __init__(self, repository_type, filename=None):
        if repository_type == "memory":
            self.student_repository = StudentRepositoryInMemory()
        elif repository_type == "textfile":
            self.student_repository = StudentRepositoryTextFile(filename)
        elif repository_type == "binary":
            self.student_repository = StudentRepositoryBinary(filename)
        else:
            raise ValueError("Invalid repository type")
        self.undo_lists_for_filter = []

    def getStudents(self):
        return self.student_repository.getStudentsList()

    def addStudent(self, id: int, name: str, group: int):
        new_student = Student(id, name, group)
        student_list = self.student_repository.getStudentsList()
        for student in student_list:
            if student.getId() == new_student.getId():
                raise ValueError("Student id must be unique")
        self.student_repository.addStudent(new_student)

    def filterStudents(self, group):
        students_list = self.student_repository.getStudentsList()
        self.undo_lists_for_filter.append(students_list)
        self.student_repository.setStudentsList([student for student in students_list if student.getGroup() != group])

    def undoAddStudent(self):
        list_of_students = self.student_repository.getStudentsList()
        last_student = list_of_students[-1]
        self.student_repository.deleteStudent(last_student)

    def undoFilterStudents(self):
        list_before_filter = self.undo_lists_for_filter.pop()
        self.student_repository.setStudentsList(list_before_filter)

    def initializeStudentList(self):
        if hasattr(self.student_repository, "initializeStudentList"):
            self.student_repository.initializeStudentList()
