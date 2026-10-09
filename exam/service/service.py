from domain.domain import Student


class StudentService:
    def __init__(self, repository):
        self.repository = repository

    def add_student(self, student_id, name, attendance, grade):
        """Validate and add a student."""
        if student_id <= 0 or any(student.id == student_id for student in self.repository.get_all()):
            raise ValueError("Invalid or duplicate student ID")
        if len(name.split()) < 2 or any(len(word) < 3 for word in name.split()):
            raise ValueError("Invalid name")
        if attendance <= 0:
            raise ValueError("Attendance must be positive")
        if not (0 <= grade <= 10):
            raise ValueError("Grade must be between 0 and 10")

        student = Student(student_id, name, attendance, grade)
        self.repository.add_student(student)

    def sort_students(self):
        """Sort students by grade (descending), then by name."""
        return sorted(self.repository.get_all(), key=lambda x: (-x.grade, x.name))

    def apply_bonus(self, p, b):
        """Apply bonus to students with at least p attendances."""
        for student in self.repository.get_all():
            if student.attendance >= p:
                student.apply_bonus(b)
        self.repository.update_file()

    def find_students_by_name_substring(self, substring):
        """Find students by substring and sort by name."""
        students = [student for student in self.repository.get_all() if substring.lower() in student.name.lower()]
        return sorted(students, key=lambda x: x.name)
