class ConsoleUI:
    ADD_COMMAND = "add"
    REMOVE_COMMAND = "remove"
    LIST_COMMAND = "list"
    SEARCH_COMMAND = "search"
    EXIT_COMMAND = "exit"

    def __init__(self, student_service, discipline_service, grade_service):
        self.student_service = student_service
        self.discipline_service = discipline_service
        self.grade_service = grade_service

    def display_menu(self):
        print("\nWhat would you like to do?")
        print(f"Type '{self.ADD_COMMAND}' to add")
        print(f"Type '{self.REMOVE_COMMAND}' to remove")
        print(f"Type '{self.LIST_COMMAND}' to list")
        print(f"Type '{self.SEARCH_COMMAND}' to search")
        print(f"Type '{self.EXIT_COMMAND}' to exit")

    def handle_add(self):
        print("\nAdd Menu:")
        print("student or discipline")
        choice = input("What would you like to add? ").strip().lower()
        if choice == "student":
            student_id = input("Enter the student ID: ")
            student_name = input("Enter the student name: ")
            self.student_service.add_student(int(student_id), student_name)
            print(f"Student '{student_name}' added successfully!")
        elif choice == "discipline":
            discipline_id = input("Enter the discipline ID: ")
            discipline_name = input("Enter the discipline name: ")
            self.discipline_service.add_discipline(int(discipline_id), discipline_name)
            print(f"Discipline '{discipline_name}' added successfully!")
        else:
            print("Invalid choice. Returning to main menu.")

    def handle_remove(self):
        print("\nRemove Menu:")
        print("student or discipline")
        choice = input("What would you like to remove? ").strip().lower()
        if choice == "student":
            student_id = input("Enter the student ID to remove: ")
            self.student_service.remove_student(int(student_id))
            print(f"Student with ID {student_id} removed successfully!")
        elif choice == "discipline":
            discipline_id = input("Enter the discipline ID to remove: ")
            self.discipline_service.remove_discipline(int(discipline_id))
            print(f"Discipline with ID {discipline_id} removed successfully!")
        else:
            print("Invalid choice. Returning to main menu.")

    def handle_list(self):
        print("\nList Menu:")
        print("students or disciplines")
        choice = input("What would you like to list? ").strip().lower()
        if choice == "students":
            students = self.student_service.list_students()
            print("\nStudents:")
            for student in students:
                print(f"ID: {student.student_id}, Name: {student.name}")
        elif choice == "disciplines":
            disciplines = self.discipline_service.list_disciplines()
            print("\nDisciplines:")
            for discipline in disciplines:
                print(f"ID: {discipline.discipline_id}, Name: {discipline.name}")
        else:
            print("Invalid choice. Returning to main menu.")

    def handle_search(self):
        print("\nSearch Menu:")
        print("students or disciplines")
        choice = input("What would you like to search? ").strip().lower()
        if choice == "student":
            student_id = input("Enter the student ID to search: ")
            student = self.student_service.search_student(int(student_id))
            if student:
                print(f"Student found: ID: {student.student_id}, Name: {student.name}")
            else:
                print("Student not found.")
        elif choice == "discipline":
            discipline_id = input("Enter the discipline ID to search: ")
            discipline = self.discipline_service.search_discipline(int(discipline_id))
            if discipline:
                print(f"Discipline found: ID: {discipline.discipline_id}, Name: {discipline.name}")
            else:
                print("Discipline not found.")
        else:
            print("Invalid choice. Returning to main menu.")

    def run(self):
        while True:
            self.display_menu()
            user_choice = input("Enter your choice: ").strip().lower()
            if user_choice == self.ADD_COMMAND:
                self.handle_add()
            elif user_choice == self.REMOVE_COMMAND:
                self.handle_remove()
            elif user_choice == self.LIST_COMMAND:
                self.handle_list()
            elif user_choice == self.SEARCH_COMMAND:
                self.handle_search()
            elif user_choice == self.EXIT_COMMAND:
                print("Goodbye!")
                break
            else:
                print("Invalid command. Please try again.")
