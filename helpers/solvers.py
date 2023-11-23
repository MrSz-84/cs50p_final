from dlxsudoku import Sudoku

import random

import gridops


def cake_algo(grid: list[list[str]]) -> str:
    """
    If you do this test calculation, You get a CAKE!

    :param grid: A list of list representing sudoku puzzle
    :return: A string containing life thoughts.
    :rtype: str
    """

    # Cake is cake :)
    strings = ["THERE", "IS", "NO", "CAKE‼"]
    for row in range(9):
        for col in range(9):
            grid[row][col] = " "
    col = 1
    row = 1
    for string in strings:
        for char in string:
            grid[row][col] = char
            col += 1
        row += 1
        if row == 2:
            row += 1
        if row == 4:
            col += 1
        if row == 5:
            row += 1
            col -= len(string) + 2
        else:
            col -= len(string) - 1
    return "The cake is a LIE‼"


def random_walk(grid: list[list[str]]) -> bool:
    """
    Made in association with CS50 Duck debugger. It solves, but its random...
    Sometimes it gets stuck, sometimes it takes some time to solve,
    and sometimes its solves the problem quite fast (rarely)...

    :param grid: A list of list representing sudoku puzzle
    :return: A boolean value for indication if there is a solution or not
    :rtype: bool
    """

    # It's too random...
    to_check = find_empty(grid)
    if not to_check:
        return True
    row, col = to_check
    tried_vals = set()
    possible = True
    while possible:
        num = random.randint(1, 9)
        tried_vals.add(num)
        if len(tried_vals) >= 9:
            possible = False
        if validator(grid, str(num), to_check):
            grid[row][col] = str(num)
            if random_walk(grid):
                return True
            grid[row][col] = "0"

    return False


def dlxsudoku_module(data: dict[str]) -> list[list[str]]:
    """
    Sudoku solver found on PyPl using induction, Dancing Links and brute force.
    https://pypi.org/project/dlxsudoku/

    :param data: Raw sudoku data containing puzzle and/or solution
    :return: Grid containing solution to given sudoku puzzle
    :rtype: list
    """

    # Create an object and call methods
    puzzle = data["puzzle"]
    s1 = Sudoku(puzzle)
    s1.solve()
    solution = {"puzzle": s1.to_oneliner()}
    solution = gridops.make_grid(solution)

    return solution


def boost_bact_r_solve(grid: list[list[str]], valid_vals: dict[tuple]) -> bool:
    """
    A backtracking recursive algorithm for solving sudoku puzzle.
    Takes additional argument being a dict of possible values for given board field.
    Algorithm writes values to the list which was the argument in function call.

    :param grid: A list of list representing sudoku puzzle
    :param valid_vals: A dict containing possible values for each free board field
    :return: Boolean value indicating if solution was found or not
    :rtype: bool
    """

    # Test showed that leaving finding empty cell to external function,
    # result in shorter process duration in comparison to passing the whole free cells list,
    # as in the bact_r_solve algorithm.
    to_check = find_empty(grid)
    if not to_check:
        return True
    row, col = to_check
    for num in valid_vals[(row, col)]:
        if validator(grid, str(num), to_check):
            grid[row][col] = str(num)
            if boost_bact_r_solve(grid, valid_vals):
                return True
            grid[row][col] = str(0)

    return False


def ordered_valid_vals(valid_vals: dict[tuple, list[str]]) -> dict[tuple, list[str]]:
    """
    Checks the frequency od found valid values for given grid field,
    and orders them by ascending order

    :param valid_vals: A dict of strings containing available values for given fields
    :return: A dict of strings containing available values for given fields in ascending order
    :rtype: dict of strings
    """

    # Check whether cell coordinates are in in valid vals.
    prioritized_valid_vals = {}
    for row in range(9):
        for col in range(9):
            if (row, col) not in valid_vals:
                continue

            # Count the number of digit appearances in valid values.
            num_of_appearances = {}
            for digit in valid_vals[(row, col)]:
                if digit not in num_of_appearances:
                    num_of_appearances[digit] = 0
                num_of_appearances[digit] += 1

            # Sort valid values by frequency
            sorted_valid_vals = []
            for digit in num_of_appearances:
                sorted_valid_vals.append((num_of_appearances[digit], digit))
            sorted_valid_vals.sort()

            # Update prioritized valid values dict.
            prioritized_valid_vals[(row, col)] = [
                digit for (_, digit) in sorted_valid_vals
            ]

    # Update valid vals dicty with sorted valid values.
    for (row, col), sorted_valid_vals in prioritized_valid_vals.items():
        valid_vals[(row, col)] = sorted_valid_vals

    return valid_vals


def scan_for_valid_vals(grid: list[list[str]]) -> dict[tuple, list[str]]:
    """
    Function scanning given sudoku grid, and filling a dictionary with tuple (row, col) as keys,
    and a list of possible values for given free field of sudoku grid.
    List is provided by "find_valid_vals" function.

    :param grid: A list of list representing sudoku puzzle
    :return: A dict with key[(row, col) tuple]: [list of possible values]
    :rtype: dict of strings
    """

    valid_vals = {
        (row, col): find_valid_vals(grid, (row, col))
        for row in range(9)
        for col in range(9)
        if grid[row][col] == "0"
    }
    valid_vals = ordered_valid_vals(valid_vals)

    return valid_vals


def find_valid_vals(grid: list[list[str]], position: tuple[int, int]) -> set:
    """
    Finds possible values for given sudoku field (row col) tuple.
    Adds them to the set, and returns it

    :param grid: A list of list representing sudoku puzzle
    :param position: A tuple with row and column indices of a grid
    :return: A set of possible values for given grid's field
    :rtype: set
    """

    y_axis, x_axis = position
    valid_numbers = set()

    for digit in range(1, 10):
        # Continue if digit is in the set
        if grid[y_axis][x_axis] == str(digit):
            continue

        # Check row, column, and square for possible cell digits.
        for row in range(9):
            if grid[y_axis][row] == str(digit) or grid[row][x_axis] == str(digit):
                break
        else:
            # Else clause for loops is executed once,
            # after loop reaches its final iteration.
            # Thank you, Cisco Networking Academy :)
            square_y = y_axis // 3
            square_x = x_axis // 3
            for row in range(square_y * 3, square_y * 3 + 3):
                for col in range(square_x * 3, square_x * 3 + 3):
                    if grid[row][col] == str(digit):
                        break
            else:
                valid_numbers.add(str(digit))

    return valid_numbers


def bact_r_solve(grid: list[list[str]], free_fields: list[tuple], depth=0) -> bool:
    """
    A backtracking recursive algorithm for solving sudoku puzzle.
    Algorithm writes values to the list which was the argument in function call.

    :param grid: A list of list representing sudoku puzzle
    :param free_fields: A list of tuples representing free cells of sudoku grid
    :param depth: A value indicating where for loop should start iteration over free cells
    :return: Boolean value indicating if solution was found or not
    :rtype: bool
    """

    # Choose next free field. Start at depth argument.
    # Return True if reached end of the list.
    if depth == len(free_fields):
        return True
    for item in range(depth, len(free_fields)):
        to_check = free_fields[item]
        break
    row, col = to_check

    # Check every possible combination.
    # Return True if everything was solved.
    for num in range(1, 10):
        if validator(grid, str(num), to_check):
            grid[row][col] = str(num)
            depth += 1
            if bact_r_solve(grid, free_fields, depth):
                return True
            grid[row][col] = "0"
            depth -= 1

    return False


def validator(grid: list, digit: str, position: tuple) -> bool:
    """
    Algorithm for validating if given value at given grid's position can be put in it,
    based of games rules, row, column and 3x3 square can't contain duplicates of any 1-9 value.

    :param grid: A list of list representing sudoku puzzle
    :param digit: A value to put into given grid's field
    :param position: A tuple with row and column indices
    :return: True or False for given value
    :rtype: bool
    """

    y_axis, x_axis = position

    # Check row for duplicates
    for row in range(9):
        if grid[y_axis][row] == digit and x_axis != row:
            return False

    # Check col for duplicates
    for col in range(9):
        if grid[col][x_axis] == digit and y_axis != col:
            return False

    # Check 3x3 square for duplicates
    square_x = x_axis // 3
    square_y = y_axis // 3
    for row in range(square_y * 3, square_y * 3 + 3):
        for col in range(square_x * 3, square_x * 3 + 3):
            if grid[row][col] == digit and (row, col) != position:
                return False

    return True


def find_empty(grid: list[list[str]]) -> tuple:
    """
    Checks if given board field is empty or not returning row, col tuple.
    Returns None otherwise.

    :param grid: A list of list representing sudoku puzzle
    :return: A tuple containing row and colum indices or None value
    :rtype: tuple or None value
    """

    for row in range(9):
        for col in range(9):
            if grid[row][col] == "0":
                return row, col


def list_of_free_fields(grid: list[list[str]]) -> list[tuple[int, int]]:
    """
    Make list of free fields to speed up recursion & backtrack algorithm.

    :param grid: A list of list representing sudoku puzzle
    :return: A list of tuples containing free cells addresses
    :rtype: list of tuples of integers
    """

    free_fields = []
    for row in range(9):
        for col in range(9):
            if grid[row][col] == "0":
                free_fields.append((row, col))
    return free_fields
