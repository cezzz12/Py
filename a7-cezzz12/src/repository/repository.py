import pickle
import os
from src.domain.domain import Student

class StudentRepositoryInMemory:
    def __init__(self):
        self.list_of_students = [
            Student(100, "Luca", 917),
            Student(102, "Cristian", 912),
            Student(104, "John", 913),
            Student(105, "Mihai", 915),
            Student(106, "Matei", 917),
            Student(107, "Alexandru", 917),
            Student(112, "Mihnea", 911),
            Student(205, "Marius", 910),
            Student(230, "Cezar", 917),
            Student(135, "Andrei", 911)
        ]

    def addStudent(self, student):
        self.list_of_students.append(student)

    def getStudentsList(self):
        return self.list_of_students.copy()

    def setStudentsList(self, list_of_students):
        self.list_of_students = list_of_students

    def deleteStudent(self, student):
        self.list_of_students.remove(student)


class StudentRepositoryTextFile:
    def __init__(self, filename):
        self.filename = filename
        self.ensure_file_exists()
        self.initializeStudentList()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w'):
                pass

    def initializeStudentList(self):
        current_students = self.getStudentsList()
        if not current_students:  # Ensure at least 10 students in the file
            initial_students = [
                Student(100, "Luca", 917),
                Student(102, "Cristian", 912),
                Student(104, "John", 913),
                Student(105, "Mihai", 915),
                Student(106, "Matei", 917),
                Student(107, "Alexandru", 917),
                Student(112, "Mihnea", 911),
                Student(205, "Marius", 910),
                Student(230, "Cezar", 917),
                Student(135, "Andrei", 911)
            ]
            self.setStudentsList(initial_students)

    def addStudent(self, student):
        with open(self.filename, 'a') as file:
            file.write(f"{student.id},{student.name},{student.group}\n")

    def getStudentsList(self):
        students = []
        with open(self.filename, 'r') as file:
            for line in file:
                id, name, group = line.strip().split(',')
                students.append(Student(int(id), name, int(group)))
        return students

    def setStudentsList(self, list_of_students):
        with open(self.filename, 'w') as file:
            for student in list_of_students:
                file.write(f"{student.id},{student.name},{student.group}\n")

    def deleteStudent(self, student_to_delete):
        students = self.getStudentsList()
        students = [student for student in students if student.id != student_to_delete.id]
        self.setStudentsList(students)

class StudentRepositoryBinary:
    def __init__(self, filename):
        self.filename = filename
        self.ensure_file_exists()
        self.initializeStudentList()

    def ensure_file_exists(self):
        """Ensure the binary file exists and is initialized."""
        if not os.path.exists(self.filename):
            # If the file doesn't exist, create it with an empty list
            with open(self.filename, 'wb') as file:
                pickle.dump([], file)

    def initializeStudentList(self):
        """Initialize the file with 10 students if it's empty."""
        students = self.getStudentsList()
        if not students:  # Ensure at least 10 students in the file
            initial_students = [
                Student(100, "Luca", 917),
                Student(102, "Cristian", 912),
                Student(104, "John", 913),
                Student(105, "Mihai", 915),
                Student(106, "Matei", 917),
                Student(107, "Alexandru", 917),
                Student(112, "Mihnea", 911),
                Student(205, "Marius", 910),
                Student(230, "Cezar", 917),
                Student(135, "Andrei", 911),
            ]
            self.setStudentsList(initial_students)

    def addStudent(self, student):
        """Add a student to the binary file."""
        students = self.getStudentsList()
        students.append(student)
        self.setStudentsList(students)

    def getStudentsList(self):
        """Retrieve all students from the binary file."""
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError) as e:
            # If there's an error loading the file, return an empty list and initialize
            print(f"Error loading student list: {e}. Reinitializing file...")
            self.ensure_file_exists()  # Reinitialize the file if there's an issue
            return []

    def setStudentsList(self, list_of_students):
        """Save a list of students to the binary file."""
        with open(self.filename, 'wb') as file:
            pickle.dump(list_of_students, file)

    def deleteStudent(self, student_to_delete):
        """Delete a student from the binary file."""
        students = self.getStudentsList()
        students = [student for student in students if student.id != student_to_delete.id]
        self.setStudentsList(students)
