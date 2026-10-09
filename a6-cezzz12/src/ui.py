import re
import random
'''
we use the re module to parse our complex numbers and to validate input formats
'''
from typing import List
from functions import (add_number, insert_number, remove_number, remove_range,
                              replace_number, filter_real, filter_modulo, list_numbers, undo_last_state)


def parse_complex_number(input_str: str) -> complex:
    """
    Parses a complex number from a string.

    :param input_str: String representing a complex number (e.g., "4+3i").
    :return: A complex number.
    :raises ValueError: If the input is not a valid complex number.
    """
    match = re.match(r"^(-?\d+)\+(-?\d+)i$", input_str)
    if not match:
        raise ValueError("Invalid complex number format")
    real, imag = map(int, match.groups())
    return complex(real, imag)


def run_ui():
    numbers = [complex(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(10)]
    undo_stack = [numbers.copy()]  # Keeps track of states for undo

    while True:
        print("EXIT:exits the program")
        print("ADD: add X to the list")
        print("INSERT: inserts X at position Y")
        print("REMOVE:removes the number at position X or remove 1 to 3 – removes the numbers at positions 1,2, and 3")
        print("REPLACE:replaces X with Y")
        print("LIST:displays the list of numbers")
        print("list real <start position> to <end position>")
        print("list modulo [ < | = | > ] <number>prints list with conditions")
        print("FILTER the list:filter real or filter modulo [ < | = | > ] <number>")
        print("UNDO:undo the last command")
        command = input("Enter command: ").strip()
        if command == "exit":
            print("Exiting program.")
            break

        try:
            if command.startswith("add "):
                number = parse_complex_number(command[4:])
                add_number(numbers, number)

            elif command.startswith("insert "):
                match = re.match(r"insert (.+) at (\d+)", command)
                if not match:
                    raise ValueError("Invalid command format")
                number = parse_complex_number(match.group(1))
                position = int(match.group(2))
                insert_number(numbers, number, position)

            elif command.startswith("remove "):
                if " to " in command:
                    start, end = map(int, command[7:].split(" to "))
                    remove_range(numbers, start, end)
                else:
                    position = int(command[7:])
                    remove_number(numbers, position)

            elif command.startswith("replace "):
                match = re.match(r"replace (.+) with (.+)", command)
                if not match:
                    raise ValueError("Invalid command format")
                old = parse_complex_number(match.group(1))
                new = parse_complex_number(match.group(2))
                replace_number(numbers, old, new)

            elif command.startswith("filter "):
                if command == "filter real":
                    filter_real(numbers)
                else:
                    match = re.match(r"filter modulo ([<=>]) (\d+)", command)
                    if not match:
                        raise ValueError("Invalid command format")
                    operator = match.group(1)
                    value = float(match.group(2))
                    filter_modulo(numbers, operator, value)

            elif command.startswith("list"):
                if command == "list":
                    print(list_numbers(numbers))
                elif command.startswith("list real"):
                    start, end = map(int, re.findall(r"(\d+)", command))
                    print(
                        list_numbers(
                            [num for idx, num in enumerate(numbers) if start <= idx <= end and num.imag == 0]
                        )
                    )
                elif "modulo" in command:
                    match = re.match(r"list modulo ([<=>]) (\d+)", command)
                    if not match:
                        raise ValueError("Invalid command format")
                    operator = match.group(1)
                    value = float(match.group(2))
                    filtered = []
                    if operator == "<":
                        filtered = [num for num in numbers if abs(num) < value]
                    elif operator == "=":
                        filtered = [num for num in numbers if abs(num) == value]
                    elif operator == ">":
                        filtered = [num for num in numbers if abs(num) > value]
                    print(list_numbers(filtered))
                else:
                    raise ValueError("Invalid list command")

            elif command == "undo":
                numbers = undo_last_state(undo_stack)

            else:
                raise ValueError("Unknown command")

            # Save state for undo after every change
            undo_stack.append(numbers.copy())

        except Exception as e:
            print(f"Error: {e}")
