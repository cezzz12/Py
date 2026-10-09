import os
from src.repository.repository import InMemoryRepository, TextFileRepository, BinaryFileRepository
from src.domain.domain import Student, Discipline, Grade
from src.services.services import StudentService, DisciplineService, GradeService
from src.ui.ui import ConsoleUI
from src.command import CommandManager
from faker import Faker


def generate_data(student_service, discipline_service):
    fake = Faker()
    predefined_disciplines = ["FP", "ASC", "Analysis", "Algebra", "Logic"]
    for i in range(1, 21):
        if not student_service._student_repo.find_by_id(i):
            student_service.add_student(i, fake.name())  # Generate a student with ID and a fake name
    for i, discipline_name in enumerate(predefined_disciplines, start=1):
        if not discipline_service._discipline_repo.find_by_id(i):
            discipline_service.add_discipline(i, discipline_name)  # Add predefined disciplines


def main():
    print("Choose repository type:")
    print("1. In-Memory Repository")
    print("2. Text-File Repository")
    print("3. Binary-File Repository")
    choice = input("Enter choice: ")

    if choice == "1":
        student_repo = InMemoryRepository()
        discipline_repo = InMemoryRepository()
        grade_repo = InMemoryRepository()
    elif choice == "2":
        student_repo = TextFileRepository("students.txt", Student)
        discipline_repo = TextFileRepository("disciplines.txt", Discipline)
        grade_repo = TextFileRepository("grades.txt", Grade)
    elif choice == "3":
        student_repo = BinaryFileRepository("students.bin")
        discipline_repo = BinaryFileRepository("disciplines.bin")
        grade_repo = BinaryFileRepository("grades.bin")
    else:
        print("Invalid choice. Exiting.")
        return

    # Initialize command manager and services
    command_manager = CommandManager()
    student_service = StudentService(student_repo, grade_repo, command_manager)
    discipline_service = DisciplineService(discipline_repo, grade_repo, command_manager)
    grade_service = GradeService(grade_repo, student_repo, discipline_repo, command_manager)

    # Generate sample data
    generate_data(student_service, discipline_service)

    # Run console user interface
    ui = ConsoleUI(student_service, discipline_service, grade_service, command_manager)
    ui.run()


if __name__ == "__main__":
    main()
