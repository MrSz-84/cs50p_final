import os

import gridops


def clear_screen():
    """
    Clears terminal window.
    """

    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def compare(grid: list[list[str]], sol_str: dict[str]) -> bool:
    """
    Compares generated solution to the solution provided via file by the user

    :param grid: A list of list representing generated sudoku solution
    :param sol_str: A string with provided solution to given puzzle for comparison
    :return: True or false
    :rtype: bool
    """

    return gridops.grid_to_str(grid) == sol_str["solution"]


def cwd_main_dir():
    """
    Sets new cwd.
    """
    main_dir = os.path.split(os.path.abspath(__file__))[0].rstrip('/helpers')
    os.chdir(main_dir)
    print(os.getcwd)
