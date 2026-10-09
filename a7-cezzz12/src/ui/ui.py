from src.services.services import StudentService


def printDisplayMenu():
    print("0. Exit")
    print("1. Add a student")
    print("2. Display the list of students")
    print("3. Filter the list of students by group")
    print("4. Undo the last operation")


class UserInterface:
    ADD_OPTION = 1
    DISPLAY_OPTION = 2
    FILTER_OPTION = 3
    UNDO_OPTION = 4
    last_performed_operation = None

    def __init__(self, repository_type, filename=None):
        self.service = StudentService(repository_type, filename)

    def initializeStudentList(self):
        self.service.initializeStudentList()

    def run(self):
        self.initializeStudentList()
        while True:
            printDisplayMenu()
            option = self.__get_valid_input("Enter your choice: ", int)
            if option == 0:
                break
            if option == self.ADD_OPTION:
                self.__addStudent()
            elif option == self.DISPLAY_OPTION:
                self.__displayStudents()
            elif option == self.FILTER_OPTION:
                self.__filterStudents()
            elif option == self.UNDO_OPTION:
                self.__undoLastOperation()

    def __get_valid_input(self, prompt, input_type):
        while True:
            try:
                user_input = input(prompt)
                if user_input == '':
                    raise ValueError("Input cannot be empty!")
                return input_type(user_input)
            except ValueError as e:
                print(f"Invalid input. Please enter a valid {input_type.__name__}: {e}")

    def __addStudent(self):
        id = self.__get_valid_input("Enter student id: ", int)
        name = input("Enter student name: ")
        if not name:  # Ensure name is not empty
            print("Name cannot be empty!")
            return
        group = self.__get_valid_input("Enter student group: ", int)
        try:
            self.service.addStudent(id, name, group)
            self.last_performed_operation = "add"
        except ValueError as error:
            print(error)

    def __displayStudents(self):
        students = self.service.getStudents()
        if not students:
            print("No students to display.")
        else:
            for student in students:
                print(student)

    def __filterStudents(self):
        self.last_performed_operation = "filter"
        group = self.__get_valid_input("Enter student group: ", int)
        self.service.filterStudents(group)

    def __undoLastOperation(self):
        if self.last_performed_operation is None:
            print("You already have the initial list")
        elif self.last_performed_operation == "add":
            self.service.undoAddStudent()
        elif self.last_performed_operation == "filter":
            self.service.undoFilterStudents()
        self.last_performed_operation = None


def main():
    repository_type = input("Choose repository type (memory, textfile, binary): ").lower()
    while repository_type not in ["memory", "textfile", "binary"]:
        print("Invalid choice. Please choose either 'memory', 'textfile', or 'binary'.")
        repository_type = input("Choose repository type (memory, textfile, binary): ").lower()

    filename = None
    if repository_type in ["textfile", "binary"]:
        filename = input("Enter file path: ").strip()
        while not filename:
            print("File path cannot be empty!")
            filename = input("Enter file path: ").strip()

    ui = UserInterface(repository_type, filename)
    ui.run()


if __name__ == "__main__":
    main()
