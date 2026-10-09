#
# The program's functions are implemented here. There is no user interaction in this file, therefore no input/print statements. Functions here
# communicate via function parameters, the return statement and raising of exceptions. 
#
import cmath
from typing import List, Tuple
from texttable import Texttable

def add_number(numbers: List[complex], number: complex) -> None:
    """
    Adds a complex number to the list.

    :param numbers: List of complex numbers.
    :param number: The complex number to add.
    """
    numbers.append(number)


def insert_number(numbers: List[complex], number: complex, position: int) -> None:
    """
    Inserts a complex number at the specified position in the list.

    :param numbers: List of complex numbers.
    :param number: The complex number to insert.
    :param position: Position to insert the number.
    :raises IndexError: If the position is invalid.
    """
    if position < 0 or position > len(numbers):
        raise IndexError("Invalid position")
    numbers.insert(position, number)


def remove_number(numbers: List[complex], position: int) -> None:
    """
    Removes a number at a specific position.

    :param numbers: List of complex numbers.
    :param position: Position of the number to remove.
    :raises IndexError: If the position is invalid.
    """
    if position < 0 or position >= len(numbers):
        raise IndexError("Invalid position")
    numbers.pop(position)


def remove_range(numbers: List[complex], start: int, end: int) -> None:
    """
    Removes numbers in a specified range.

    :param numbers: List of complex numbers.
    :param start: Start position.
    :param end: End position.
    :raises IndexError: If the range is invalid.
    """
    if start < 0 or end >= len(numbers) or start > end:
        raise IndexError("Invalid range")
    del numbers[start:end + 1]


def replace_number(numbers: List[complex], old: complex, new: complex) -> None:
    """
    Replaces all occurrences of a number with a new number.

    :param numbers: List of complex numbers.
    :param old: Number to replace.
    :param new: Number to replace with.
    """
    for i in range(len(numbers)):
        if numbers[i] == old:
            numbers[i] = new


def filter_real(numbers: List[complex]) -> None:
    """
    Filters the list, keeping only real numbers.

    :param numbers: List of complex numbers.
    """
    numbers[:] = [num for num in numbers if num.imag == 0]


def filter_modulo(numbers: List[complex], operator: str, value: float) -> None:
    """
    Filters the list based on the modulus of the numbers.

    :param numbers: List of complex numbers.
    :param operator: Operator for comparison ('<', '=', '>').
    :param value: Value to compare against.
    :raises ValueError: If the operator is invalid.
    """
    if operator not in {'<', '=', '>'}:
        raise ValueError("Invalid operator")
    if operator == '<':
        numbers[:] = [num for num in numbers if abs(num) < value]
    elif operator == '=':
        numbers[:] = [num for num in numbers if abs(num) == value]
    elif operator == '>':
        numbers[:] = [num for num in numbers if abs(num) > value]


def list_numbers(numbers: List[complex]) -> str:
    """
    Returns a table of all numbers.

    :param numbers: List of complex numbers.
    :return: Formatted table as a string.
    """
    table = Texttable()
    table.header(["Index", "Real Part", "Imaginary Part", "Modulus"])
    for idx, num in enumerate(numbers):
        table.add_row([idx, num.real, num.imag, abs(num)])
    return table.draw()


def undo_last_state(commands: List[List[complex]]) -> List[complex]:
    """
    Undoes the last state.

    :param commands: List of saved commands.
    :return: The most recent previous command.
    :raises IndexError: If no undo is available.
    """
    if len(commands) < 2:
        raise IndexError("No undo available")
    commands.pop()
    return commands[-1].copy()

