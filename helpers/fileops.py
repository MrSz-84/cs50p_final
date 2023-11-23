import tqdm

import csv
import datetime
import os
import sys
import typing

import dbops
import gridops
import validateops


def db_to_file(db_name: str) -> None:
    """
    Saves DB contents into a csv file

    :param db_name: Name of the db file for connection purposes
    """

    cursor, db_conn = dbops.conn_to_db(db_name)
    cursor.execute("SELECT * FROM statistics")
    db = cursor.fetchall()

    cursor.execute("SELECT * FROM statistics")
    names = list(map(lambda header: header[0], cursor.description))

    # Combines names and values into a list of dicts
    combined = [{key: val for key, val in zip(names, entry)} for entry in db]

    # Write to file
    f = open_file("../dbdump.csv", mode="w")
    with f:
        writer = csv.DictWriter(f, fieldnames=names)
        writer.writeheader()
        for row in tqdm.tqdm(combined, desc="Copying..."):
            writer.writerow(
                {
                    names[0]: row[names[0]],
                    names[1]: row[names[1]],
                    names[2]: row[names[2]],
                    names[3]: row[names[3]],
                    names[4]: row[names[4]],
                    names[5]: row[names[5]],
                    names[6]: row[names[6]],
                    names[7]: row[names[7]],
                    names[8]: row[names[8]],
                }
            )
    db_conn.close()


def write_to_file(
    sudoku_data: dict[str, str], grid: list, method_name, comparison=False
) -> None:
    """
    Writes a bunch of data to a file called "results.csv".
    Creates file if it doesn't exist, appends if it does.

    :param sudoku_data: A dict contain ing puzzle and/or solution provided for comparison
    :param grid: A list of list representing generated sudoku solution
    :param comparison: Result of comparison if generated solution is equivalent to provided one
    :param method_name: A string representing solve method name
    """

    puzzle = sudoku_data["puzzle"]
    solution_discovered = gridops.grid_to_str(grid)

    # Check for solutions presence
    if len(sudoku_data) == 2 and comparison:
        solution_provided = sudoku_data["solution"]
    else:
        solution_provided = "N/A"
    datetime_obj = datetime.datetime.now()
    date = datetime_obj.date()
    time = datetime_obj.time().strftime("%H:%M:%S")

    # Open file, create variables and write to file using DictWriter.
    f = open_file("../results.csv", mode="a")
    with f:
        fieldnames = [
            "date",
            "time",
            "method",
            "puzzle",
            "discoveredSolution",
            "identical",
            "providedSolution",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # If we are at the beginning of the file, also write headers.
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "date": date,
                "time": time,
                "method": method_name,
                "puzzle": puzzle,
                "discoveredSolution": solution_discovered,
                "identical": comparison,
                "providedSolution": solution_provided,
            }
        )


def read_file(file: str, solutions: bool) -> list[str]:
    """
    Returns list of dicts with sudoku puzzles
    or puzzles and solutions pairs provided by the user.
    Solutions are provided by the user.
    Output is going to be used to fed into the solver.

    :param file: A string containing filename with extension or path to the file
    :param solutions: A boolean value depending on flag given by the user
    :return: A list of dicts containing sudoku data. Puzzles and solutions or puzzles only
    :rtype: list
    """

    # Add rows (dicts) to puzzles list.
    puzzles = []
    f = open_file(file)
    with f:
        lines_read = 0
        lines_valid = 0
        bad = 0

        # How to act when solutions flag is True.
        if solutions:
            lines_loc = lines_positions(file)
            header = validateops.determine_headers(file, lines_loc)
            reader = csv.DictReader(f, fieldnames=header)
            for row in reader:
                lines_read += 1
                validation = validateops.validate_rows(row, header, solutions)
                if validation:
                    lines_valid += 1
                    puzzles.append(row)
                if not validation:
                    bad += 1
            if bad / lines_read > 0.96:
                sys.exit(
                    f"Your data is in mess...\n"
                    f"{bad/lines_read: .0%} of your data can't pass validation.\n"
                    f"Check it and try again."
                )

        # How to act when solutions flag is False
        else:
            reader = csv.DictReader(f)
            header = list(reader.fieldnames)
            for row in reader:
                lines_read += 1
                validation = validateops.validate_rows(row, header, solutions)
                if validation:
                    puzzles.append(row)
                    lines_valid += 1
                if not validation:
                    bad += 1
            if bad / lines_read > 0.96:
                sys.exit(
                    f"Your data is in mess...\n"
                    f"{bad/lines_read: .0%} of your data can't pass validation.\n"
                    f"Probably you have solutions in your file. \nUse '-s' flag."
                )

    return puzzles


def open_file(filename: str, mode="r") -> typing.IO:
    """
    Opens the file of given name or path.

    :param filename: filename or filepath
    :param mode: File open mode. Here read mode.
    :raise IOError: If something's wrong with the file
    :return: A IO object
    :rtype: file object
    """

    try:
        f = open(filename, mode, newline="", encoding="utf-8")
    except IOError as e:
        sys.exit(f"I/O error occurred: {os.strerror(e.errno)}")

    return f


def lines_positions(file: str) -> list[int]:
    """
    Returns a list with 200 new line locations from a file. Uses tell() function
    If file has less lines stops at file end.

    :param file: filename or filepath as a str
    :raise IOError: If something's wrong with the file
    :return: A list composed of new line starting locations as int
    :rtype: list
    """

    f = open_file(file)
    with f:
        lines_loc = []
        lines = 0
        while lines < 200:
            line = f.readline()
            if not line:
                break
            lines += 1
            pos = f.tell()
            lines_loc.append(pos)

    return lines_loc


def linesread(file: str, line_loc: int) -> str:
    """
    Returns line read from a file to help determine which column is the puzzle,
    and which is the solution.

    :param file: filename or filepath as a str
    :param line_loc: Integer number of byte position for a given line
    :raise IOError: If something's wrong with the file
    :return: A string containing puzzle and solution separated with comma
    :rtype: str
    """

    f = open_file(file)
    with f:
        f.seek(line_loc)
        line = f.readline().strip()

    return line
