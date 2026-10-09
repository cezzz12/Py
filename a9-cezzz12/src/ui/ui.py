from src.services.services import StatisticsService
class ConsoleUI:
    def __init__(self, student_service, discipline_service, grade_service, command_manager):
        self._student_service = student_service
        self._discipline_service = discipline_service
        self._grade_service = grade_service
        self._command_manager = command_manager
        self._statistics_service = StatisticsService(grade_service._grade_repo, student_service._student_repo, discipline_service._discipline_repo)

    def display_menu(self):
        print("\nMain Menu:")
        print("1. Add a record (student/discipline/grade)")
        print("2. Remove a record (student/discipline)")
        print("3. List all records (students, disciplines, grades)")
        print("4. Search for students or disciplines")
        print("5. Statistics (best students, failing students, best disciplines)")
        print("6. Undo last operation")
        print("7. Redo last operation")
        print("8. Exit")

    def add_student(self):
        try:
            student_id = int(input("Student ID: "))
            name = input("Student Name: ")
            self._student_service.add_student(student_id, name)
            print("Student added successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def add_discipline(self):
        try:
            discipline_id = int(input("Discipline ID: "))
            name = input("Discipline Name: ")
            self._discipline_service.add_discipline(discipline_id, name)
            print("Discipline added successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def add_grade(self):
        try:
            student_id = int(input("Student ID: "))
            discipline_id = int(input("Discipline ID: "))
            grade_value = float(input("Grade: "))
            self._grade_service.add_grade(student_id, discipline_id, grade_value)
            print("Grade added successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def remove_student(self):
        try:
            student_id = int(input("Student ID to remove: "))
            self._student_service.remove_student(student_id)
            print("Student removed successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def remove_discipline(self):
        try:
            discipline_id = int(input("Discipline ID to remove: "))
            self._discipline_service.remove_discipline(discipline_id)
            print("Discipline removed successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def list_students(self):
        students = self._student_service.get_all_students()
        if not students:
            print("No students found.")
        for student in students:
            print(student)

    def list_disciplines(self):
        disciplines = self._discipline_service.get_all_disciplines()
        if not disciplines:
            print("No disciplines found.")
        for discipline in disciplines:
            print(discipline)

    def list_grades(self):
        grades = self._grade_service.get_all_grades()
        if not grades:
            print("No grades found.")
        for grade in grades:
            print(grade)

    def search_students(self):
        name = input("Enter student name to search for: ")
        results = self._student_service.search_students_by_name(name)
        if not results:
            print("No matching students found.")
        for student in results:
            print(student)

    def search_disciplines(self):
        name = input("Enter discipline name to search for: ")
        results = self._discipline_service.search_disciplines_by_name(name)
        if not results:
            print("No matching disciplines found.")
        for discipline in results:
            print(discipline)

    def handle_statistics(self):
        print("\nStatistics Menu:")
        print("1. Failing students")
        print("2. Best students")
        print("3. Best disciplines")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            failing_students = self._statistics_service.failing_students()
            if not failing_students:
                print("No failing students.")
            for student in failing_students:
                print(student)
        elif choice == "2":
            best_students = self._statistics_service.best_students()
            if not best_students:
                print("No best students.")
            for student, average in best_students:
                print(f"{student} - Average: {average:.2f}")
        elif choice == "3":
            best_disciplines = self._statistics_service.best_disciplines()
            if not best_disciplines:
                print("No best disciplines.")
            for discipline, average in best_disciplines:
                print(f"{discipline} - Average Grade: {average:.2f}")
        else:
            print("Invalid choice. Returning to main menu.")

    def handle_undo(self):
        try:
            self._command_manager.undo()
            print("Undo performed successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def handle_redo(self):
        try:
            self._command_manager.redo()
            print("Redo performed successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                print("\n1. Add Student")
                print("2. Add Discipline")
                print("3. Add Grade")
                sub_choice = input("What would you like to add? ")
                if sub_choice == "1":
                    self.add_student()
                elif sub_choice == "2":
                    self.add_discipline()
                elif sub_choice == "3":
                    self.add_grade()
                else:
                    print("Invalid option.")
            elif choice == "2":
                print("\n1. Remove Student")
                print("2. Remove Discipline")
                sub_choice = input("What would you like to remove? ")
                if sub_choice == "1":
                    self.remove_student()
                elif sub_choice == "2":
                    self.remove_discipline()
                else:
                    print("Invalid option.")
            elif choice == "3":
                print("\nListing:")
                print("1. Students")
                print("2. Disciplines")
                print("3. Grades")
                sub_choice = input("What would you like to list? ")
                if sub_choice == "1":
                    self.list_students()
                elif sub_choice == "2":
                    self.list_disciplines()
                elif sub_choice == "3":
                    self.list_grades()
                else:
                    print("Invalid option.")
            elif choice == "4":
                print("\nSearching:")
                print("1. Search Students")
                print("2. Search Disciplines")
                sub_choice = input("What would you like to search? ")
                if sub_choice == "1":
                    self.search_students()
                elif sub_choice == "2":
                    self.search_disciplines()
                else:
                    print("Invalid option.")
            elif choice == "5":
                self.handle_statistics()
            elif choice == "6":
                self.handle_undo()
            elif choice == "7":
                self.handle_redo()
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid option.")
