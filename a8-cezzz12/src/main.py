import os
from src.repository.repository import InMemoryRepository, TextFileRepository, BinaryFileRepository
from src.domain.domain import Student, Discipline, Grade
from src.services.services import StudentService, DisciplineService, GradeService
from src.ui.ui import ConsoleUI
from faker import Faker


def generate_data(student_service, discipline_service):
    fake = Faker()
    predefined_disciplines = ["FP", "ASC", "Analysis", "Algebra", "Logic"]
    for i in range(1, 21):
        if not student_service._student_repo.find_by_id(i):
            student_service.add_student(i, fake.name())
    for i, discipline_name in enumerate(predefined_disciplines, start=1):
        if not discipline_service._discipline_repo.find_by_id(i):
            discipline_service.add_discipline(i, discipline_name)


def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        if file_path.endswith(".txt"):
            open(file_path, "w").close()
        elif file_path.endswith(".bin"):
            open(file_path, "wb").close()

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
        print("Selected: In-Memory Repository")
    elif choice == "2":
        ensure_file_exists("students.txt")
        ensure_file_exists("disciplines.txt")
        ensure_file_exists("grades.txt")
        student_repo = TextFileRepository("students.txt", Student)
        discipline_repo = TextFileRepository("disciplines.txt", Discipline)
        grade_repo = TextFileRepository("grades.txt", Grade)
        print("Selected: Text-File Repository")
    elif choice == "3":
        ensure_file_exists("students.bin")
        ensure_file_exists("disciplines.bin")
        ensure_file_exists("grades.bin")
        student_repo = BinaryFileRepository("students.bin")
        discipline_repo = BinaryFileRepository("disciplines.bin")
        grade_repo = BinaryFileRepository("grades.bin")
        print("Selected: Binary-File Repository (Pickle)")
    else:
        print("Invalid choice. Exiting.")
        return

    student_service = StudentService(student_repo, grade_repo)
    discipline_service = DisciplineService(discipline_repo, grade_repo)
    grade_service = GradeService(grade_repo, student_repo, discipline_repo)

    generate_data(student_service, discipline_service)

    ui = ConsoleUI(student_service, discipline_service, grade_service)
    ui.run()


if __name__ == "__main__":
    main()
