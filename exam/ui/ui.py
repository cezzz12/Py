import os
from service.service import StudentService


class StudentUI:
    def __init__(self, service):
        self.service = service
        self.output_file = "results.txt"
        self._ensure_file_exists()
        self._initialize_students()

    def _ensure_file_exists(self):
        """Ensure the results file exists."""
        if not os.path.exists(self.output_file):
            with open(self.output_file, "w") as f:
                pass  # Create an empty file

    def _initialize_students(self):
        """Initialize results file with 10 predefined students."""
        initial_students = [
            "101, Badescu Mihai, 13, 9",
            "102, Avram Ionut, 13, 9",
            "103, Vaxim Raluca, 12, 8",
            "104, Popescu Roxana, 10, 10",
            "105, Popescu Andrei, 9, 10",
            "186, Popescu Marius, 8, 10",
            "107, Micu Matei, 14, 5",
            "108, Micu Alexia, 11, 8",
            "109, Micu Maria, 5, 8",
            "110, Marius Ioan, 12, 5",
        ]

        if os.stat(self.output_file).st_size == 0:
            for student in initial_students:
                id, name, attendance, grade = student.split(", ")
                self.service.add_student(int(id), name, int(attendance), int(grade))

    def write_to_file(self, content):
        """Write content to the results file."""
        with open(self.output_file, "a") as f:
            f.write(content + "\n")

    def display_menu(self):
        print("Student Management System")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Apply Bonus")
        print("4. Find Students By Name Substring")
        print("0. Exit")

    def handle_add_student(self):
        try:
            student_id = int(input("Enter Student ID: "))
            name = input("Enter Name (first and last name): ")
            attendance = int(input("Enter Attendance Count: "))
            grade = int(input("Enter Grade (0-10): "))
            self.service.add_student(student_id, name, attendance, grade)
            self.write_to_file(f"Student added successfully: {student_id}, {name}, {attendance}, {grade}")
            print("Student added successfully!")
        except ValueError as e:
            self.write_to_file(f"Error: {e}")
            print(f"Error: {e}")

    def handle_display_students(self):
        students = self.service.sort_students()
        if students:
            for student in students:
                self.write_to_file(str(student))
            print("Students saved to results.txt")
        else:
            self.write_to_file("No students available.")
            print("No students available.")

    def handle_apply_bonus(self):
        try:
            p = int(input("Enter minimum attendance: "))
            b = int(input("Enter bonus grade: "))
            self.service.apply_bonus(p, b)
            self.write_to_file(f"Bonus of {b} applied to students with at least {p} attendance.")
            print(f"Bonus of {b} applied to students with at least {p} attendance.")
        except ValueError as e:
            self.write_to_file(f"Error: {e}")
            print(f"Error: {e}")

    def handle_find_students_by_name_substring(self):
        substring = input("Enter name substring: ")
        students = self.service.find_students_by_name_substring(substring)
        if students:
            for student in students:
                self.write_to_file(str(student))
            print(f"Students matching '{substring}' saved to results.txt")
        else:
            self.write_to_file(f"No students found with name containing '{substring}'.")
            print(f"No students found with name containing '{substring}'.")

    def run(self):
        while True:
            self.display_menu()
            option = input("Choose an option: ")
            if option == "1":
                self.handle_add_student()
            elif option == "2":
                self.handle_display_students()
            elif option == "3":
                self.handle_apply_bonus()
            elif option == "4":
                self.handle_find_students_by_name_substring()
            elif option == "0":
                if os.path.getsize(self.output_file) == 0:
                    print("Warning: No data written to results.txt!")
                self.write_to_file("Exiting program.")
                print("Exiting program.")
                break
            else:
                self.write_to_file("Invalid option. Please try again.")
                print("Invalid option. Please try again.")
