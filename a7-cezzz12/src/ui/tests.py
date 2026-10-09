import unittest
import tempfile
from pathlib import Path
from src.services.services import StudentService

class TestStudentService(unittest.TestCase):
    def test_add_and_duplicate(self):
        service = StudentService("memory")
        before = len(service.getStudents())
        service.addStudent(999, "Test Student", 100)
        self.assertEqual(len(service.getStudents()), before + 1)
        with self.assertRaises(ValueError):
            service.addStudent(999, "Duplicate", 200)

    def test_filter_and_undo(self):
        service = StudentService("memory")
        before = service.getStudents()
        service.filterStudents(917)
        self.assertTrue(all(s.group != 917 for s in service.getStudents()))
        service.undoFilterStudents()
        self.assertEqual(service.getStudents(), before)

    def test_persistence_preserves_small_lists(self):
        with tempfile.TemporaryDirectory() as directory:
            for kind in ("textfile", "binary"):
                filename = str(Path(directory) / kind)
                service = StudentService(kind, filename)
                service.filterStudents(917)
                expected = [(s.id, s.name, s.group) for s in service.getStudents()]
                restarted = StudentService(kind, filename)
                self.assertEqual([(s.id, s.name, s.group) for s in restarted.getStudents()], expected)

if __name__ == "__main__":
    unittest.main()
