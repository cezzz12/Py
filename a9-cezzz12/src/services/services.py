from src.domain.domain import Student, Discipline, Grade, ValidationException
from src.command import AddEntityCommand, RemoveEntityCommand


class StudentService:
    def __init__(self, student_repo, grade_repo, command_manager):
        self._student_repo = student_repo
        self._grade_repo = grade_repo
        self._command_manager = command_manager

    def add_student(self, student_id, name):
        student = Student(student_id, name)
        command = AddEntityCommand(self._student_repo, student)
        self._command_manager.execute(command)

    def remove_student(self, student_id):
        command = RemoveEntityCommand(self._student_repo, student_id)
        self._command_manager.execute(command)

    def get_all_students(self):
        return self._student_repo.get_all()

    def search_students_by_name(self, name):
        return self._student_repo.find_by_name(name)


class DisciplineService:
    def __init__(self, discipline_repo, grade_repo, command_manager):
        self._discipline_repo = discipline_repo
        self._grade_repo = grade_repo
        self._command_manager = command_manager

    def add_discipline(self, discipline_id, name):
        discipline = Discipline(discipline_id, name)
        command = AddEntityCommand(self._discipline_repo, discipline)
        self._command_manager.execute(command)

    def remove_discipline(self, discipline_id):
        command = RemoveEntityCommand(self._discipline_repo, discipline_id)
        self._command_manager.execute(command)

    def get_all_disciplines(self):
        return self._discipline_repo.get_all()

    def search_disciplines_by_name(self, name):
        return self._discipline_repo.find_by_name(name)


class GradeService:
    def __init__(self, grade_repo, student_repo, discipline_repo, command_manager):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._discipline_repo = discipline_repo
        self._command_manager = command_manager

    def add_grade(self, student_id, discipline_id, grade_value):
        if not self._student_repo.find_by_id(student_id) or not self._discipline_repo.find_by_id(discipline_id):
            raise ValidationException("Student and discipline must exist")
        if not 1 <= grade_value <= 10:
            raise ValidationException("Grade must be between 1 and 10")
        grade = Grade(discipline_id, student_id, grade_value)
        command = AddEntityCommand(self._grade_repo, grade)
        self._command_manager.execute(command)

    def get_all_grades(self):
        return self._grade_repo.get_all()


class StatisticsService:
    def __init__(self, grade_repo, student_repo, discipline_repo):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._discipline_repo = discipline_repo

    def failing_students(self):
        """
        Returns a list of students who are failing at one or more disciplines
        (average grade < 5 in any discipline).
        """
        failing_students = []
        all_grades = self._grade_repo.get_all()

        for student in self._student_repo.get_all():
            student_failing = False
            for discipline in self._discipline_repo.get_all():
                # Get grades for this student in a specific discipline
                grades = [
                    grade.grade_value for grade in all_grades
                    if grade.student_id == student.student_id and grade.discipline_id == discipline.discipline_id
                ]
                if grades and sum(grades) / len(grades) < 5:
                    student_failing = True
                    break
            if student_failing:
                failing_students.append(student)

        return failing_students

    def best_students(self):
        """
        Returns the students sorted in descending order by their aggregated average
        (average of their average grades across disciplines).
        """
        students_with_avg = []
        all_grades = self._grade_repo.get_all()

        for student in self._student_repo.get_all():
            discipline_averages = []
            for discipline in self._discipline_repo.get_all():
                # Get grades for this student in a specific discipline
                grades = [
                    grade.grade_value for grade in all_grades
                    if grade.student_id == student.student_id and grade.discipline_id == discipline.discipline_id
                ]
                if grades:
                    discipline_averages.append(sum(grades) / len(grades))

            if discipline_averages:
                # Calculate aggregated average
                aggregated_avg = sum(discipline_averages) / len(discipline_averages)
                students_with_avg.append((student, aggregated_avg))

        # Sort by aggregated average, in descending order
        return sorted(students_with_avg, key=lambda x: x[1], reverse=True)

    def best_disciplines(self):
        """
        Returns the disciplines sorted in descending order by the average of all
        grades received by students in the discipline.
        """
        disciplines_with_avg = []
        all_grades = self._grade_repo.get_all()

        for discipline in self._discipline_repo.get_all():
            # Get all grades for this discipline
            grades = [
                grade.grade_value for grade in all_grades
                if grade.discipline_id == discipline.discipline_id
            ]
            if grades:
                discipline_average = sum(grades) / len(grades)
                disciplines_with_avg.append((discipline, discipline_average))

        # Sort by average grade, in descending order
        return sorted(disciplines_with_avg, key=lambda x: x[1], reverse=True)
