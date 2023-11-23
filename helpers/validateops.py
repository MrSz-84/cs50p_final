import os
import re
import sys
import datetime

import fileops


def validate_file(filename: str) -> bool:
    """
    Validates if file of given filename/filepath exists and returns T or F.

    :param filename: Filename or path and file for validation
    :type filename: str
    :return: True or False
    :rtype: bool
    """

    return os.path.isfile(f"{filename}")


def determine_headers(file: str, lines_loc: list[int]) -> list[str]:
    """
    Returns header list for csv.DictReader() based on the sample of data read from a file.

    :param file: filename or filepath as a str
    :param lines_loc: List of integer number of byte position for a given line
    :raise IOError: If something's wrong with the file
    :return: A list of headers for csv.DictReader() determining where are the puzzles,
    and where are the solutions
    :rtype: list

    """

    STEP = 3
    stats_dict = {"puzzle_l": [], "solution_l": []}
    pattern_p = re.compile(r"(\d{81})")
    pattern_s = re.compile(r"([1-9]{81})")
    counter = 0

    # Check the file's rows to check where are puzzles and solutions.
    for i in range(0, len(lines_loc), STEP):
        counter += 1
        line = re.split(r"(?<=\d),(?=\d)", fileops.linesread(file, lines_loc[i]))
        if len(line) != 2:
            continue
        if bool(pattern_p.match(line[0])) and bool(pattern_s.match(line[1])):
            stats_dict["puzzle_l"].append(1)
        if bool(pattern_s.match(line[0])) and bool(pattern_p.match(line[1])):
            stats_dict["solution_l"].append(1)
    puzzle_l = len(stats_dict["puzzle_l"]) / counter
    solution_l = len(stats_dict["solution_l"]) / counter
    if (
        len(stats_dict["puzzle_l"]) / counter >= 0.67
        and len(stats_dict["solution_l"]) / counter <= 0.33
    ):
        return ["puzzle", "solution"]
    elif (
        len(stats_dict["solution_l"]) / counter >= 0.67
        and len(stats_dict["puzzle_l"]) / counter < 0.33
    ):
        return ["solution", "puzzle"]
    else:
        print(
            f"Your data is in mess. \n",
            f"Puzzles in the first col constitute a share of {puzzle_l: .0%} in {counter} lines. \n",
            f"Solutions in the first col constitute a share of {solution_l: .0%} in {counter} lines.",
        )
        sys.exit()


def validate_rows(row: dict[str, str], header: list[str], solutions: bool) -> bool:
    """
    Returns True if row is valid or False if not.

    :param row: A dict containing line read from a file
    :param header: A list containing fieldnames for validation
    :param solutions: A boolean value depending on flag given by the user
    :return: True if validation is positive, False if it's negative
    :rtype: bool
    """

    # Set patterns
    pattern_p = re.compile(r"(^\d{81}$)")
    pattern_s = re.compile(r"(^[1-9]{81}$)")
    if header[0] == "puzzle":
        left_col = "puzzle"
    elif header[0] == "solution":
        left_col = "solution"

    # validation if solutions flag is True.
    if solutions:
        line = [v for v in row.values()]
        if len(line) != 2:
            return False
        if not line[0].isdigit() or not line[1].isdigit():
            return False
        if left_col == "puzzle":
            if (
                not bool(pattern_p.match(line[0]))
                or not bool(pattern_s.match(line[1]))
                or "0" not in line[0]
                or "0" in line[1]
            ):
                return False
        if left_col == "solution":
            if (
                not bool(pattern_s.match(line[0]))
                or not bool(pattern_p.match(line[1]))
                or "0" in line[0]
                or "0" not in line[1]
            ):
                return False

    # Validation if solutions flag is False
    else:
        if left_col != "puzzle":
            return False
        if len(row) != 1:
            return False
        if not row[left_col].isdigit():
            return False
        if (
            not bool(pattern_p.match(row[left_col]))
            or bool(pattern_s.match(row[left_col]))
            or "0" not in row[left_col]
        ):
            return False

    return True


def validate_date(chosen_date: str) -> bool:
    """
    Validates if a string is in valid date format, and a valid date.

    :param chosen_date: A string containing date for validation
    :return: Output either false or true
    :rtype: bool
    """

    # Validate if date was entered if so, validate accordingly
    if not chosen_date:
        return False
    pattern = re.compile(
        r"""^((?:20[0-3][0-9])|(?:1\d\d\d))
            -((?:0\d)|(?:1[0-2]))
            -((?:[0-2]\d)|(?:3[0-1]))$""",
        re.X,
    )
    if not bool(pattern.match(chosen_date)):
        return False
    m = re.search(pattern, chosen_date)
    try:
        datetime.date(int(m[1]), int(m[2]), int(m[3]))
    except ValueError:
        return False
    return True
