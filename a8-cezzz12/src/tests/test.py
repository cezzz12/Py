import os
import unittest
from src.repository.repository import InMemoryRepository, BinaryFileRepository
from src.domain.domain import Student, Discipline


class TestRepositories(unittest.TestCase):
    def setUp(self):
        # Set up for tests
        self.student = Student(1, "John Doe")
        self.discipline = Discipline(1, "FP")
        self.binary_file_path = "test_students.bin"

    def tearDown(self):
        # Cleanup after tests
        if os.path.exists(self.binary_file_path):
            os.remove(self.binary_file_path)

    # Test 1: Test adding and retrieving a student in an in-memory repository
    def test_add_student_in_memory_repository(self):
        repo = InMemoryRepository()
        repo.add(self.student)
        retrieved = repo.find_by_id(1)

        self.assertIsNotNone(retrieved, "Student was not added to the repository.")
        self.assertEqual(retrieved.student_id, self.student.student_id)
        self.assertEqual(retrieved.name, self.student.name)

    # Test 2: Test adding, saving, and loading a student in a binary file repository
    def test_binary_file_repository(self):
        repo = BinaryFileRepository(self.binary_file_path)
        repo.add(self.student)

        # Ensure the student is saved in the repository
        self.assertEqual(len(repo.get_all()), 1, "Student was not saved to the binary file repository.")

        # Create a new instance of BinaryFileRepository and load data
        new_repo = BinaryFileRepository(self.binary_file_path)
        loaded_student = new_repo.find_by_id(1)

        # Assert that the loaded data matches the original student
        self.assertIsNotNone(loaded_student, "Student was not loaded from the binary file repository.")
        self.assertEqual(loaded_student.student_id, self.student.student_id)
        self.assertEqual(loaded_student.name, self.student.name)


if __name__ == "__main__":
    unittest.main()
