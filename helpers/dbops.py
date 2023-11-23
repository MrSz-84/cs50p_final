import tabulate

import os
import sqlite3
import sys

# code necessary for proper cross imports
main_dir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(main_dir)

import miscellaneous
import validateops


def get_data(db_name: str, db_content: str, target="") -> None:
    """
    Connects to DB and reads the data to be fetched from DB table.
    Then prints them to the screen.

    :param db_name: Name of database file
    :param db_content: What is to be read from the db
    :param target: A str describing what should be modified when dropping entry or table
    """

    cursor, db_conn = conn_to_db(db_name)

    # Create table headers
    cursor.execute("SELECT rowid, * FROM statistics")
    names = list(map(lambda header: header[0], cursor.description))

    # Get the data
    match db_content:
        case "all":
            cursor.execute(
                "SELECT rowid, * FROM statistics ORDER BY test_date DESC, start_time DESC"
            )
        case "test":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE presentation_method LIKE '{db_content}%'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "file":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE presentation_method LIKE '%{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "screen":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE presentation_method LIKE '%{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "R&B":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE solve_method LIKE '{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "Boosted R&B":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE solve_method LIKE '{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "DLXSudoku":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE solve_method LIKE '{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "Random walk":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE solve_method LIKE '{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "Cake Algorithm":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE solve_method LIKE '{db_content}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "date":
            cursor.execute(
                f"""SELECT rowid, * FROM statistics WHERE test_date LIKE '{target}'
                ORDER BY test_date DESC, start_time DESC"""
            )
        case "delete":
            cursor.execute(f"DELETE FROM statistics WHERE rowid = {int(target)}")
            db_conn.commit()
        case "drop":
            cursor.execute(f"DROP TABLE {target}")
            db_conn.commit()
        case _:
            sys.exit("Unexpected situation. Quitting...")

    if db_content not in ("delete", "drop", "save"):
        db = cursor.fetchall()
        formatting = [
            "d",  # rowid
            "",  # presentation method
            "",  # solve method
            "",  # date
            "",  # time
            ".3f",  # duration
            ",d",  # puzzles
            ",d",  # solutions
            ".7f",  # avg solve time
            ".0%",  # solutions ratio
        ]
        print(
            tabulate.tabulate(
                db, headers=names, tablefmt="simple", intfmt=",", floatfmt=formatting
            )
        )
    db_conn.close()


def termination(db_conn: object) -> None:
    """
    Terminates the program via sys.exit()

    :param db_conn: SQLite3 connection object
    """

    miscellaneous.clear_screen()
    db_conn.close()
    sys.exit("Terminating program...\n")


def conn_to_db(db_name: str) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Returns a cursor of DB object. DB name "stats.db"

    :return: DB cursor object
    :rtype: SQLite3 object
    """

    db_conn = sqlite3.connect(db_name)
    cursor = db_conn.cursor()

    return cursor, db_conn


def write_to_db(
    presentation_method: str,
    solve_method: str,
    test_date: object,
    start_time: str,
    duration_time: float,
    puzzles_read: int,
    solutions_found: int,
    avg_solve_time: float,
    db_name: str,
) -> None:
    """
    Establishes a SQLite DB if there is no DB called "stats.db",
    or creates the table called "statistics" if there is none.
    Writes data to the DB.

    :param presentation_method: Type of data presentation method. Available test or tofile
    :param solve_method: Algo name used to solve given dataset
    :param test_date: Date of execution
    :param start_time: Time at which the test has started
    :param duration_time: Operation duration time
    :param puzzles_read: How many puzzles there were in the dataset
    :param solutions_found: How many puzzles were solved
    :param avg_solve_time: Average time needed to solve one puzzle using given method
    :param db_name: A string representing db name
    """

    file_present = validateops.validate_file(db_name)
    db_conn = sqlite3.connect(db_name)
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='statistics'"
    )
    table_present = cursor.fetchone()[0]

    # Create a DB file and a table if conditions are met.
    if not file_present or not table_present:
        cursor.execute(
            """CREATE TABLE statistics(
            presentation_method TEXT,
            solve_method TEXT,
            test_date TEXT,
            start_time TEXT,
            duration_time REAL,
            puzzles_read INTEGER,
            solutions_found INTEGER,
            avg_solve_time REAL,
            solutions_ratio REAL)"""
        )
    solutions_ratio = solutions_found / puzzles_read

    # Entries to be added to DB.
    entries = (
        (
            presentation_method,
            solve_method,
            test_date,
            start_time,
            duration_time,
            puzzles_read,
            solutions_found,
            avg_solve_time,
            solutions_ratio,
        ),
    )

    # Add the data
    cursor.execute("INSERT INTO statistics VALUES(?,?,?,?,?,?,?,?,?)", entries[0])
    db_conn.commit()
    db_conn.close()


def setup_path():
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    sys.path.append(main_dir)
