from functions import (add_number, insert_number, remove_number, remove_range, replace_number)


def test_add_number():
    numbers = []
    add_number(numbers, complex(3, 4))
    assert numbers == [3 + 4j], "Test failed: add_number should append the number to the list."

    add_number(numbers, complex(1, -2))
    assert numbers == [3 + 4j, 1 - 2j], "Test failed: add_number should append another number correctly."


def test_insert_number():
    numbers = [1 + 2j, 3 - 4j]
    insert_number(numbers, 0 + 1j, 1)
    assert numbers == [1 + 2j, 0 + 1j, 3 - 4j], "Test failed: insert_number should insert at the correct position."

    try:
        insert_number(numbers, 0 + 1j, 10)  # Invalid position
    except IndexError as e:
        assert str(e) == "Invalid position", f"Test failed: insert_number should raise 'Invalid position' error. Got {str(e)}"


def test_remove_number():
    numbers = [1 + 2j, 3 - 4j]
    remove_number(numbers, 1)
    assert numbers == [1 + 2j], "Test failed: remove_number should remove the correct number."

    try:
        remove_number(numbers, 10)  # Invalid position
    except IndexError as e:
        assert str(e) == "Invalid position", f"Test failed: remove_number should raise 'Invalid position' error. Got {str(e)}"


def test_remove_range():
    numbers = [1 + 2j, 3 - 4j, 5 + 6j]
    remove_range(numbers, 0, 1)
    assert numbers == [5 + 6j], "Test failed: remove_range should remove numbers from the correct range."

    try:
        remove_range(numbers, 1, 0)  # Invalid range (start > end)
    except IndexError as e:
        assert str(e) == "Invalid range", f"Test failed: remove_range should raise 'Invalid range' error. Got {str(e)}"

    # Test removing out-of-bounds
    try:
        remove_range(numbers, -1, 5)  # Invalid range
    except IndexError as e:
        assert str(e) == "Invalid range", f"Test failed: remove_range should raise 'Invalid range' error. Got {str(e)}"


def test_replace_number():
    numbers = [1 + 2j, 1 + 2j, 3 - 4j]
    replace_number(numbers, 1 + 2j, 0 + 0j)
    assert numbers == [0 + 0j, 0 + 0j, 3 - 4j], "Test failed"

    # Test replacing non-existing number (should do nothing)
    replace_number(numbers, 1 + 1j, 0 + 0j)  # 1+1j is not in the list
    assert numbers == [0 + 0j, 0 + 0j, 3 - 4j], "Test failed"


# Run all tests
test_add_number()
test_remove_number()
test_remove_range()
test_insert_number()
test_replace_number()

print("All tests passed")
