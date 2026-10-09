import os
from domain.domain import Student


class StudentRepository:
    def __init__(self, filename):
        self.filename = filename
        self.students = self.read_from_file()

    def read_from_file(self):
        students = []
        if not os.path.exists(self.filename):
            # If file doesn't exist, create it and return an empty list.
            with open(self.filename, 'w'): pass
            return students

        with open(self.filename, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    # Parse and validate the student data.
                    student_data = line.strip().split(", ")
                    if len(student_data) != 4:
                        raise ValueError(f"Line {line_number} is malformed: {line.strip()}")

                    student_id = int(student_data[0])
                    name = student_data[1]
                    attendance = int(student_data[2])
                    grade = int(student_data[3])

                    students.append(Student(student_id, name, attendance, grade))
                except (ValueError, IndexError) as e:
                    print(f"Error processing line {line_number}: {e}. Skipping line.")
        return students

    def write_to_file(self, student):
        with open(self.filename, 'a') as f:
            f.write(f"{student}\n")

    def update_file(self):
        with open(self.filename, "w") as f:
            for student in self.students:
                f.write(f"{student}\n")

    def get_all(self):
        return self.students

    def add_student(self, student):
        self.students.append(student)
        self.update_file()
