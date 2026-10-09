from src.services.services import StudentService

def test_add_student_memory():
    print("Test add for in-memory repository")
    try:
        service = StudentService("memory")
        service.initializeStudentList()
        initial_count = len(service.getStudents())

        service.addStudent(999, "Test Student", 999)
        assert len(service.getStudents()) == initial_count + 1, "Student not added in memory"

        print("In-memory test passed!")
    except Exception as e:
        print(f"In-memory test failed: {e}")

def test_add_student_textfile():
    print("Test add for text file repository")
    try:
        filename = "test_students.txt"
        service = StudentService("textfile", filename)
        service.initializeStudentList()
        initial_count = len(service.getStudents())

        service.addStudent(999, "Test Student", 999)
        assert len(service.getStudents()) == initial_count + 1, "Student not added to text file"

        print("Text file test passed!")
    except Exception as e:
        print(f"Text file test failed: {e}")
    finally:
        # Clean up the test file
        import os
        if os.path.exists(filename):
            os.remove(filename)

def test_add_student_binary():
    print("Test add for binary file repository")
    try:
        filename = "test_students.pkl"
        service = StudentService("binary", filename)
        service.initializeStudentList()
        initial_count = len(service.getStudents())

        service.addStudent(999, "Test Student", 999)
        assert len(service.getStudents()) == initial_count + 1, "Student not added to binary file"

        print("Binary file test passed!")
    except Exception as e:
        print(f"Binary file test failed: {e}")
    finally:
        # Clean up the test file
        import os
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_add_student_memory()
    test_add_student_textfile()
    test_add_student_binary()
