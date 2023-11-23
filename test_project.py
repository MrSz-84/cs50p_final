import contextlib
import io

import pytest
import sys

import project
from helpers import fileops
from helpers import gridops
from helpers import printops
from helpers import solvers
from helpers import validateops


def test_confirmation_positive():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If function's output isn't exact match.
    """

    func1 = "ARE YOU SURE TOU WANT TO DROP TABLE STATISTICS???\nTHIS IS IRREVERSIBLE PROCESS. ALL DATA WILL BE LOST!!:\n    Y. Drop the table\n    N. Dont drop the table.\n\n    0. Exit program"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.confirmation()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func1


def test_confirmation_negative():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If test ends with a success
    """

    func2 = "Some fancy text"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.confirmation()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func2


def test_print_other_actions_pos():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If function's output isn't exact match.
    """

    func3 = "Choose what you want to do:\n    1. Drop a record.\n    2. Drop the table.\n    3. Save DB to file.\n\n    0. Exit program\n    B. Get back to previous menu"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.print_other_actions()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func3


def test_print_other_actions_neg():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If test ends with a success
    """

    func4 = "Some fancy text...4"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.print_other_actions()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func4


def test_print_main_menu_pos():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If function's output isn't exact match.
    """

    func5 = "Choose what you want to do:\n    1. Show all stats.\n    2. Show stats for given presentation method only.\n    3. Show stats for given solve method only.\n    4. Show stats for given date.\n    5. Other actions.\n\n    0. Exit program."

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.print_main_menu()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func5


def test_print_main_menu_neg():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If test ends with a success
    """

    func6 = "Some fancy text...6"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.print_main_menu()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func6


def test_print_presentation_method_menu_pos():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If function's output isn't exact match.
    """

    func7 = "Choose presentation method to display stats for:\n    1. Test pipeline.\n    2. To file.\n    3. To screen.\n\n    0. Exit program\n    B. Get back to previous menu"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.print_presentation_method_menu()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func7


def test_print_presentation_method_menu_neg():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If test ends with a success
    """

    func8 = "Some fancy text...8"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.print_presentation_method_menu()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func8


def test_print_solve_menu_pos():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If function's output isn't exact match.
    """

    func9 = "Choose solve method to display stats for:\n    1. R&B.\n    2. Boosted R&B.\n    3. DLXSudoku.\n    4. Random walk.\n    5. Cake Algorithm.\n\n    0. Exit program\n    B. Get back to previous menu"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.print_solve_menu()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func9


def test_print_solve_menu_neg():
    """
    Test written for checking if print output of a function is valid or not.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :raise AssertionError: If test ends with a success
    """

    func10 = "Some fancy text...10"

    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.print_solve_menu()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func10


def test_print_date_pos(monkeypatch):
    """
    Test written for checking if print output of a function is valid or not.

    First step is overriding users input, which is required by tested function.
    Without it program waits infinitely. This is Achieved by using builtin pytest's fixture
    monkeypatch. It uses setattr pointing to readline for data input.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :param monkeypatch: Builtin Pytest functionality
    :raise AssertionError: If function's output isn't exact match.
    """

    func11 = "Enter date in format YYYY-MM-DD\n\n>>>"
    monkeypatch.setattr(sys.stdin, "readline", lambda: "2023-11-19")
    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        printops.print_date()
    buffer_val = buffer.getvalue().strip()
    assert buffer_val == func11


def test_print_date_neg(monkeypatch):
    """
    Test written for checking if print output of a function is valid or not.

    First step is overriding users input, which is required by tested function.
    Without it program waits infinitely. This is Achieved by using builtin pytest's fixture
    monkeypatch. It uses setattr pointing to readline for data input.

    Test is executed by the usage of contextlib and io modules.
    Contextlib uses redirect_stdout for print output than with help of StringIO
    an object is created, and the data extraction processed by getvalue().

    :param monkeypatch: Builtin Pytest functionality
    :raise AssertionError: If function's output isn't an exception.
    """


    func12 = "Some fancy text...12"
    monkeypatch.setattr(sys.stdin, "readline", lambda: "2023-11-19")
    with contextlib.redirect_stdout(io.StringIO()) as buffer:
        with pytest.raises(AssertionError):
            printops.print_date()
            buffer_val = buffer.getvalue().strip()
            assert buffer_val == func12


def test_argparse_logic(monkeypatch):
    """
    Tests if argparse_logic function is doing what is should.
    Uses monkeypatch fixture to provide sys.argv arguments

    :param monkeypatch: Pytest builtin fixture
    :raises AssertionError: If positive test isn't valid
    :raises AttributeError: If no errors are raised where they should be.
    """

    monkeypatch.setattr(
        "sys.argv", ["project.py", "-m", "2", "-f", "sudoku.csv", "-s", "-tf"]
    )
    args, parser = project.argparse_logic()
    assert args.method == 2
    assert args.filename == "sudoku.csv"
    assert args.solutions == True
    assert args.statistics == False
    assert args.print == False
    with pytest.raises(AttributeError):
        args.file == "sudoku"
        args.method == 4
        args.statistics == False
        args.solutions == True
        args.group.print == True
    monkeypatch.setattr("sys.argv", ["project.py", "-f", "sudoku.txt"])
    args, parser = project.argparse_logic()
    assert args.method == 1
    assert args.filename == "sudoku.txt"
    assert args.solutions == False
    assert args.statistics == False
    assert args.print == True
    with pytest.raises(AttributeError):
        args.file == "sudoku"
        args.method == 4
        args.statistics == False
        args.solutions == True
        args.group.tofile == False


def test_validate_file():
    """
    Validates whether a file exists and if it is a file indeed.
    Tested function uses os.path.isfile() for the validation.

    :raises AssertionError: If test isn't valid
    """

    assert validateops.validate_file("sudoku.csv") == True
    assert validateops.validate_file("sudoku.txt") == True
    assert validateops.validate_file("project.py") == True
    assert validateops.validate_file("solutions.txt") == False
    assert validateops.validate_file("test_project.py") == True
    assert validateops.validate_file("shirtificate.png") == False


def test_linesread():
    """
    Checks if string returned is of 163 chars length and presence of 0

    The length is fixed for every line, because of the tested file's construction.
    Every line is built of sudoku puzzle and solution separated by comma.
    If all elements are present it means that tested function returned proper line for further
    processing.
    Every line should be of 163 chars long, contain 0 only in the left part.

    :raises AssertionError: If test isn't valid
    """

    assert len(fileops.linesread("sudoku.csv", 16)) == 163
    assert len(fileops.linesread("sudoku.csv", 180)) == 163
    assert len(fileops.linesread("sudoku.csv", 344).split(",")) == 2
    assert "0" in fileops.linesread("sudoku.csv", 836).split(",")[0]
    assert "0" not in fileops.linesread("sudoku.csv", 836).split(",")[1]


def test_open_file():
    """
    Checks if returned object is a file
    Tested function opens a file using built in method.

    :raises AssertionError: If test isn't valid
    """

    file = fileops.open_file("sudoku.csv")
    assert isinstance(file, open("sudoku.csv", "r").__class__)


def test_read_file():
    """
    Checks if returned object is of list type.

    Tested function should read through the file and return a list containing every valid line,
    of read file. So if we have a list object, we should be ready to proceed.

    :raises AssertionError: If test isn't valid
    """

    sudoku = fileops.read_file("sudoku.txt", False)
    assert isinstance(sudoku, fileops.read_file("sudoku.txt", False).__class__)
    sudoku = fileops.read_file("sudoku.csv", True)
    assert isinstance(sudoku, fileops.read_file("sudoku.txt", False).__class__)


def test_grid_to_str():
    """
    Test if joining grit to string gives the same result.

    This is needed for further test, comparison and programs functionality.

    :raises AssertionError: If test isn't valid
    """

    grid = [
        ["0", "7", "0", "0", "0", "0", "0", "4", "3"],
        ["0", "4", "0", "0", "0", "9", "6", "1", "0"],
        ["8", "0", "0", "6", "3", "4", "9", "0", "0"],
        ["0", "9", "4", "0", "5", "2", "0", "0", "0"],
        ["3", "5", "8", "4", "6", "0", "0", "2", "0"],
        ["0", "0", "0", "8", "0", "0", "5", "3", "0"],
        ["0", "8", "0", "0", "7", "0", "0", "9", "1"],
        ["9", "0", "2", "1", "0", "0", "0", "0", "5"],
        ["0", "0", "7", "0", "4", "0", "8", "0", "2"],
    ]

    assert (
        gridops.grid_to_str(grid)
        == "070000043040009610800634900094052000358460020000800530080070091902100005007040802"
    )
    assert (
        gridops.grid_to_str(grid)
        != "679518243543729618821634957794352186358461729216897534485276391962183475137945862"
    )


def test_find_empty():
    """
    Test if output is a tuple with row and col of the first free field.

    Crucial functionality for sudoku validator.

    :raises AssertionError: If test isn't valid
    """

    grid = [["0" for _ in range(9)] for _ in range(9)]
    assert solvers.find_empty(grid) == (0, 0)


def test_find_full():
    """
    Test if output is a tuple with row and col of the first occupied field.

    Crucial functionality for sudoku validator.

    :raises AssertionError: If test isn't valid
    """

    grid = [["1" for _ in range(9)] for _ in range(9)]
    assert solvers.find_empty(grid) == None


def test_validator():
    """
    Tests if validator is returning right boolean output

    No solution if it is against the rules. So validator should assert if given digit,
    can fit into checked cell.

    :raises AssertionError: If test isn't valid
    """

    grid = [
        ["0", "7", "0", "0", "0", "0", "0", "4", "3"],
        ["0", "4", "0", "0", "0", "9", "6", "1", "0"],
        ["8", "0", "0", "6", "3", "4", "9", "0", "0"],
        ["0", "9", "4", "0", "5", "2", "0", "0", "0"],
        ["3", "5", "8", "4", "6", "0", "0", "2", "0"],
        ["0", "0", "0", "8", "0", "0", "5", "3", "0"],
        ["0", "8", "0", "0", "7", "0", "0", "9", "1"],
        ["9", "0", "2", "1", "0", "0", "0", "0", "5"],
        ["0", "0", "7", "0", "4", "0", "8", "0", "2"],
    ]

    assert solvers.validator(grid, "1", (0, 0)) == True
    assert solvers.validator(grid, "3", (0, 0)) == False


def test_bact_r_solve():
    """
    Checks if tested function properly utilizes list_of_free_fields().

    Function should return a list containing tuples with address cells of "0" in the grid.
    If the function was implemented correctly solver algorithm will find a solution to given grid.

    :raises AssertionError: If test isn't valid
    """

    grid = [
        ["0", "7", "0", "0", "0", "0", "0", "4", "3"],
        ["0", "4", "0", "0", "0", "9", "6", "1", "0"],
        ["8", "0", "0", "6", "3", "4", "9", "0", "0"],
        ["0", "9", "4", "0", "5", "2", "0", "0", "0"],
        ["3", "5", "8", "4", "6", "0", "0", "2", "0"],
        ["0", "0", "0", "8", "0", "0", "5", "3", "0"],
        ["0", "8", "0", "0", "7", "0", "0", "9", "1"],
        ["9", "0", "2", "1", "0", "0", "0", "0", "5"],
        ["0", "0", "7", "0", "4", "0", "8", "0", "2"],
    ]
    free_fields = solvers.list_of_free_fields(grid)
    assert solvers.bact_r_solve(grid, free_fields) == True


def test_make_grid():
    """
    Checks if string conversion to a grid is valid

    Grid is necessary for most of solving algorithms. So conversion in both ways is crucial.

    :raises AssertionError: If test isn't valid
    """

    grid = [
        ["0", "7", "0", "0", "0", "0", "0", "4", "3"],
        ["0", "4", "0", "0", "0", "9", "6", "1", "0"],
        ["8", "0", "0", "6", "3", "4", "9", "0", "0"],
        ["0", "9", "4", "0", "5", "2", "0", "0", "0"],
        ["3", "5", "8", "4", "6", "0", "0", "2", "0"],
        ["0", "0", "0", "8", "0", "0", "5", "3", "0"],
        ["0", "8", "0", "0", "7", "0", "0", "9", "1"],
        ["9", "0", "2", "1", "0", "0", "0", "0", "5"],
        ["0", "0", "7", "0", "4", "0", "8", "0", "2"],
    ]

    string = {
        "puzzle": "070000043040009610800634900094052000358460020000800530080070091902100005007040802"
    }
    solution = {
        "puzzle": "679518243543729618821634957794352186358461729216897534485276391962183475137945862"
    }
    assert gridops.make_grid(string) == grid
    assert gridops.make_grid(solution) != grid


def test_validate_rows_puzzle():
    """
    Test puzzle data validation.

    Tested function should check if a read row is valid for further manipulation,
    and solving processes. It is done by checking if provided header of csv file is same as file
    contents. If i.g. puzzle, solution header is provided, "0" values should be only on the left
    part of each line.

    :raises AssertionError: If test isn't valid
    """

    puz_header = ["puzzle", "solution"]
    proper_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }
    wrong_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
    }
    proper_sol = {
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
    }
    wrong_sol = {
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
        "puzzle": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }

    solutions = True
    assert validateops.validate_rows(proper_puz, puz_header, solutions) == True
    assert validateops.validate_rows(wrong_puz, puz_header, solutions) == False
    assert validateops.validate_rows(proper_sol, puz_header, solutions) == False
    assert validateops.validate_rows(wrong_sol, puz_header, solutions) == False


def test_validate_rows_solution():
    """
    Tests solutions data validation.

    Tested function should check if a read row is valid for further manipulation,
    and solving processes. It is done by checking if provided header of csv file is same as file
    contents. If i.g. puzzle, solution header is provided, there should be no "0" values in the
    solution part of the line.
    part of each line.

    :raises AssertionError: If test isn't valid
    """

    sol_header = ["solution", "puzzle"]
    proper_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }
    wrong_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
    }
    proper_sol = {
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
    }
    wrong_sol = {
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
        "puzzle": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }

    solutions = True
    assert validateops.validate_rows(proper_puz, sol_header, solutions) == False
    assert validateops.validate_rows(wrong_puz, sol_header, solutions) == False
    assert validateops.validate_rows(proper_sol, sol_header, solutions) == True
    assert validateops.validate_rows(wrong_sol, sol_header, solutions) == False


def test_validate_rows_noflag():
    """
    Tests puzzle for data validation. Noflag for solutions.

    Tested function should check if a read row is valid for further manipulation,
    and solving processes. It is done by checking if provided header of csv file is same as file
    contents. If i.g. there should be no comma in any line, and it should contain "0" values.

    :raises AssertionError: If test isn't valid
    """

    puz_header = ["puzzle"]
    proper_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }
    only_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003"
    }
    solutions = False
    assert validateops.validate_rows(proper_puz, puz_header, solutions) == False
    assert validateops.validate_rows(only_puz, puz_header, solutions) == True


def test_write_to_file():
    """
    Test write to file functionality.

    When users desires to write sudoku puzzle solutions into the file, tested function should
    fulfill that desire. Test is simple, after using this function 'results.csv'
    file should be created. If so, when opened it should be an instance of parent class.

    :raises AssertionError: If test isn't valid
    """

    proper_sol = [
        ["2", "9", "5", "7", "4", "3", "8", "6", "1"],
        ["4", "3", "1", "8", "6", "5", "9", "2", "7"],
        ["8", "7", "6", "1", "9", "2", "5", "4", "3"],
        ["3", "8", "7", "4", "5", "9", "2", "1", "6"],
        ["6", "1", "2", "3", "8", "7", "4", "9", "5"],
        ["5", "4", "9", "2", "1", "6", "7", "3", "8"],
        ["7", "6", "3", "5", "2", "4", "1", "8", "9"],
        ["9", "2", "8", "6", "7", "1", "3", "5", "4"],
        ["1", "5", "4", "9", "3", "8", "6", "7", "2"],
    ]

    proper_puz = {
        "puzzle": "007300054245080900003040070070960000000020760000801002008294016609108020000007003",
        "solution": "867319254245786931913542678472963185381425769596871342738294516659138427124657893",
    }
    name = "Cake algorithm"
    fileops.write_to_file(proper_puz, proper_sol, name)
    assert validateops.validate_file("results.csv")
    file = fileops.open_file("results.csv")
    assert isinstance(file, open("results.csv", "r").__class__)


def test_cake_algo():
    """
    Tests if the output of Cake algorithm is as it should be.

    :raises AssertionError: If test isn't valid
    """

    proper_sol = [
        ["2", "9", "5", "7", "4", "3", "8", "6", "1"],
        ["4", "3", "1", "8", "6", "5", "9", "2", "7"],
        ["8", "7", "6", "1", "9", "2", "5", "4", "3"],
        ["3", "8", "7", "4", "5", "9", "2", "1", "6"],
        ["6", "1", "2", "3", "8", "7", "4", "9", "5"],
        ["5", "4", "9", "2", "1", "6", "7", "3", "8"],
        ["7", "6", "3", "5", "2", "4", "1", "8", "9"],
        ["9", "2", "8", "6", "7", "1", "3", "5", "4"],
        ["1", "5", "4", "9", "3", "8", "6", "7", "2"],
    ]
    assert solvers.cake_algo(proper_sol) == "The cake is a LIE‼"
    assert solvers.cake_algo(proper_sol) != "There is no cake‼"


def test_determine_headers():
    """
    Checks what is the output for give data set. This is another step of the data
    provided in the input file.

    :raises AssertionError: If test isn't valid
    """

    file = "sudoku.csv"
    lines_loc = [
        16,
        180,
        344,
        508,
        672,
        836,
        1000,
        1164,
        1328,
        1492,
        1656,
        1820,
        1984,
        2148,
        2312,
        2476,
        2640,
        2804,
        2968,
        3132,
        3296,
        3460,
        3624,
        3788,
        3952,
        4116,
        4280,
        4444,
        4608,
        4772,
        4936,
        5100,
        5264,
        5428,
        5592,
        5756,
        5920,
        6084,
        6248,
        6412,
        6576,
        6740,
        6904,
        7068,
        7232,
        7396,
        7560,
        7724,
        7888,
        8052,
        8216,
        8380,
        8544,
        8708,
        8872,
        9036,
        9200,
        9364,
        9528,
        9692,
        9856,
        10020,
        10184,
        10348,
        10512,
        10676,
        10840,
        11004,
        11168,
        11332,
        11496,
        11660,
        11824,
        11988,
        12152,
        12316,
        12480,
        12644,
        12808,
        12972,
        13136,
        13300,
        13464,
        13628,
        13792,
        13956,
        14120,
        14284,
        14448,
        14612,
        14776,
        14940,
        15104,
        15268,
        15432,
        15596,
        15760,
        15924,
        16088,
        16252,
        16416,
        16580,
        16744,
        16908,
        17072,
        17236,
        17400,
        17564,
        17728,
        17892,
        18056,
        18220,
        18384,
        18548,
        18712,
        18876,
        19040,
        19204,
        19368,
        19532,
        19696,
        19860,
        20024,
        20188,
        20352,
        20516,
        20680,
        20844,
        21008,
        21172,
        21336,
        21500,
        21664,
        21828,
        21992,
        22156,
        22320,
        22484,
        22648,
        22812,
        22976,
        23140,
        23304,
        23468,
        23632,
        23796,
        23960,
        24124,
        24288,
        24452,
        24616,
        24780,
        24944,
        25108,
        25272,
        25436,
        25600,
        25764,
        25928,
        26092,
        26256,
        26420,
        26584,
        26748,
        26912,
        27076,
        27240,
        27404,
        27568,
        27732,
        27896,
        28060,
        28224,
        28388,
        28552,
        28716,
        28880,
        29044,
        29208,
        29372,
        29536,
        29700,
        29864,
        30028,
        30192,
        30356,
        30520,
        30684,
        30848,
        31012,
        31176,
        31340,
        31504,
        31668,
        31832,
        31996,
        32160,
        32324,
        32488,
        32652,
    ]
    assert validateops.determine_headers(file, lines_loc) == ["puzzle", "solution"]
    assert validateops.determine_headers(file, lines_loc) != ["solution", "puzzle"]
