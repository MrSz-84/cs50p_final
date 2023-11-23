import numpy as np


def print_grid(grid: list[list[str]]) -> object:
    """
    returns grid using NumPy matrix method

    :param grid: List of list representing sudoku puzzle
    :return: A grid being a NumPy object
    :rtype: numpy matrix object
    """

    return np.matrix(grid)


def make_grid(entry: dict[str, str]) -> list[list[str]]:
    """
    Takes a dict as an input.
    Manipulates a string and creates a 9x9 grid out of it.
    The grid is a list of list made of 9 rows with 9 separated string chars inside.


    :param entry: A string containing sudoku puzzle to solve
    :return: A list of lists (2d grid) with strings inside
    :rtype: list
    """

    line = entry.get("puzzle")
    return [[char for char in line[i * 9: (i + 1) * 9]] for i in range(9)]


def grid_to_str(grid: list[list[str]]) -> str:
    """
    Creates string form of a grid ready for writing to a file,
    or comparison with provided dataset.

    :param grid: A list of list representing sudoku puzzle
    :return: A string concatenated from the grid
    :rtype: str
    """

    return "".join([val for row in grid for val in row])
