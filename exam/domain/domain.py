class Student:
    def __init__(self, id, name, attendance, grade):
        self.id = id
        self.name = name
        self.attendance = attendance
        self.grade = grade

    def __str__(self):
        return f"{self.id} {self.name} {self.attendance} {self.grade}"

    def apply_bonus(self, bonus):
        """Apply bonus to the grade."""
        self.grade = min(self.grade + bonus, 10)
