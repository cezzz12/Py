from repository.repository import StudentRepository
from service.service import StudentService
from ui.ui import StudentUI


def main():
    filename = "students.txt"
    repository = StudentRepository(filename)
    service = StudentService(repository)
    ui = StudentUI(service)
    ui.run()


if __name__ == "__main__":
    main()
