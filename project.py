import tqdm

import argparse
import datetime
import re
import sys
import time

import helpers.dbops as dbops
import helpers.fileops as fileops
import helpers.gridops as gridops
import helpers.miscellaneous as miscellaneous
import helpers.printops as printops
import helpers.solvers as solvers
import helpers.validateops as validateops


def main():
    """
    Main wrapper function containing all logic and loops.
    """



    # Consts
    DB_NAME = "stats.db"
    miscellaneous.clear_screen()

    # Create args using argparse
    args, parser = argparse_logic()

    # Checks if at least one of two needed arguments is present
    wanted_args = {
        key: val
        for key, val in vars(args).items()
        if key == "filename" or key == "statistics"
    }
    if not any(wanted_args.values()):
        print(
            "usage: Sudoku solver [-h] [-m M] [-f FN] [-s] [-c] [-st] [-p | -tf | -t]\n"
        )
        print(
            "[-f FN] [-st] <- One of these is a must. Use -h or --help to see more details\n"
        )
        sys.exit()

    # Checks if this is True
    if args.statistics:
        show_stats(DB_NAME)
    elif not validateops.validate_file(args.filename):
        miscellaneous.clear_screen()
        print(
            f"File '{args.filename}' doesn't exist. Check spelling or extension correctness.\n"
            f"Try using -h or --help flags to see more details\n"
        )
        sys.exit()
    sudoku_data = fileops.read_file(args.filename, args.solutions)
    if args.tests:
        test_pipeline(args, sudoku_data, DB_NAME)

    #  Stats section
    num_of_ops = 0
    dt_obj = datetime.datetime.now()
    cur_date = dt_obj.date()
    cur_time = dt_obj.time().strftime("%H:%M:%S")
    if args.tofile:
        presentation_method = "to file"
    else:
        presentation_method = "to screen"
    solutions_found = 0
    tstart = time.time()

    # Main block
    progress = args.tofile
    for entry in tqdm.tqdm(sudoku_data, desc="Testing...") if progress else sudoku_data:
        base_grid = gridops.make_grid(entry)
        if args.print:
            print("PUZZLE")
            print(gridops.print_grid(base_grid))
        match args.method:
            case 1:
                # Recursion and backtracking
                name = "R&B"
                free_fields = solvers.list_of_free_fields(base_grid)
                solution_status = solvers.bact_r_solve(base_grid, free_fields)
                solution = base_grid[:]
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 2:
                # Boosted recursion and backtracking
                name = "Boosted R&B"
                solution_status = solvers.boost_bact_r_solve(
                    base_grid, solvers.scan_for_valid_vals(base_grid)
                )
                solution = base_grid[:]
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 3:
                # Dlxsudoku module from PyPl
                name = "DLXSudoku"
                solution = solvers.dlxsudoku_module(entry)
                if "0" not in solution:
                    solution_status = True
                else:
                    solution_status = False
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 4:
                # Random walk...
                name = "Random walk"
                solution_status = solvers.random_walk(base_grid)
                solution = base_grid[:]
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 5:
                # Cake algorithm
                name = "Cake algorithm"
                solution = solvers.cake_algo(base_grid)
                solution_status = solution
                solution = base_grid[:]
                num_of_ops += 1
                solutions_found += 1
            case _:
                sys.exit("No such algorithm implemented, please check your input")
        if args.print:
            print("SOLUTION")
            print(gridops.print_grid(solution))
        if args.compare:
            if args.solutions:
                comparison = miscellaneous.compare(solution, entry)
                if args.print:
                    print(
                        f"Generated solution identical to provided one? -> {comparison}"
                    )
                if args.tofile:
                    fileops.write_to_file(entry, solution, name, comparison)
        else:
            if args.tofile:
                fileops.write_to_file(entry, solution, name)
    tstop = time.time()

    # Some more stats
    telapsed = tstop - tstart
    avg_op_time = telapsed / num_of_ops

    # Write stats to db
    dbops.write_to_db(
        presentation_method,
        name,
        str(cur_date),
        str(cur_time),
        telapsed,
        num_of_ops,
        solutions_found,
        avg_op_time,
        DB_NAME,
    )

    # Print stats to screen
    if args.tofile or args.print:
        print()
        print(f"{'Method of presentation':<22}{': ':<}{presentation_method}")
        print(f"{'Solve method name':<22}{': ':<}{name}")
        print(f"{'Test date':<22}{': ':<}{cur_date}")
        print(f"{'Test start time':<22}{': ':<}{cur_time}")
        print(f"{'Test duration time':<22}{': ':<}{telapsed:.8f}")
        print(f"{'Puzzles read':<22}{': ':<}{num_of_ops:,}")
        print(f"{'Solutions found':<22}{': ':<}{solutions_found:,}")
        print(f"{'Avg. solve time':<22}{': ':<}{avg_op_time:.8f}\n")
        sys.exit("Program has ended.\n")


def show_stats(db_name: str) -> None:
    """
    Main logic loop for CLS menu which gives the user the ability to brow solve stats,
    drop db contents into a csv file, delete entries, or even drop the wole db.

    :param db_name: Name of database file
    """

    file_present = validateops.validate_file(db_name)
    if not file_present:
        sys.exit(
            f"No database file named {db_name} present.\nRun some solve cycles first.\n"
        )
    cursor, db_conn = dbops.conn_to_db(db_name)
    cursor.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='statistics'"
    )
    table_present = cursor.fetchone()[0]
    if not table_present:
        sys.exit("No table with statistics available. Run som solve cycles first.\n")

    # Main menu loop and logic
    while True:
        miscellaneous.clear_screen()
        printops.print_main_menu()
        pick = input(">>> ")
        pattern = re.compile(r"(^[1-5,0]$)")
        if not bool(pattern.match(pick)):
            continue
        miscellaneous.clear_screen()
        match pick:
            case "1":
                dbops.get_data(db_name, "all")
                while True:
                    action = input(
                        "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                    )
                    if action.lower() == "b":
                        break
                    elif action == "0":
                        dbops.termination(db_conn)
            case "2":
                while True:
                    miscellaneous.clear_screen()
                    printops.print_presentation_method_menu()
                    action = input("\n>>> ")
                    match action.lower():
                        case "b":
                            break
                        case "0":
                            dbops.termination(db_conn)
                        case "1":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "test")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "2":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "file")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "3":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "screen")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
            case "3":
                while True:
                    miscellaneous.clear_screen()
                    printops.print_solve_menu()
                    action = input("\n>>> ")
                    match action.lower():
                        case "b":
                            break
                        case "0":
                            dbops.termination(db_conn)
                        case "1":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "R&B")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "2":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "Boosted R&B")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "3":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "DLXSudoku")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "4":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "Random walk")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
                        case "5":
                            miscellaneous.clear_screen()
                            dbops.get_data(db_name, "Cake Algorithm")
                            while True:
                                action = input(
                                    "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                                )
                                if action.lower() == "b":
                                    break
                                elif action == "0":
                                    dbops.termination(db_conn)
            case "4":
                action = printops.print_date()
                miscellaneous.clear_screen()
                dbops.get_data(db_name, "date", action)
                while True:
                    action = input(
                        "\nType 'B' to return to previous menu or '0' to exit.\n>>> "
                    )
                    if action.lower() == "b":
                        break
                    elif action == "0":
                        dbops.termination(db_conn)
            case "5":
                while True:
                    miscellaneous.clear_screen()
                    printops.print_other_actions()
                    action = input("\n>>> ")
                    if not action.isdigit() and action.lower() != "b":
                        continue
                    match action.lower():
                        case "b":
                            break
                        case "0":
                            dbops.termination(db_conn)
                        case "1":
                            miscellaneous.clear_screen()
                            action = input(
                                "\nWhich rowid you want to delete?\n"
                                "Type 'B' to return to previous menu or '0' to exit.\n\n>>> "
                            )
                            if action.lower() == "b":
                                break
                            elif action.lower() == "0":
                                dbops.termination(db_conn)
                            elif len(action) < 1:
                                continue
                            else:
                                dbops.get_data(db_name, "delete", action)
                        case "2":
                            miscellaneous.clear_screen()
                            printops.confirmation()
                            while True:
                                action = input("\n>>> ")
                                match action.lower():
                                    case "b":
                                        break
                                    case "0":
                                        dbops.termination(db_conn)
                                    case "y":
                                        dbops.get_data(db_name, "drop", "statistics")
                                        break
                                    case "n":
                                        break
                        case "3":
                            miscellaneous.clear_screen()
                            fileops.db_to_file(db_name)
                            print("DB copy to csv done.")
                            time.sleep(1)
            case "0":
                dbops.termination(db_conn)
            case _:
                sys.exit(f"Something went wrong. Check what did you input {pick}")


def test_pipeline(
    args: argparse.Namespace, sudoku_data: list[dict[str, str]], db_name: str
) -> None:
    """
    Test pipeline for sudoku algorithms. Elegant way for testing and writing to DB

    :param args: Argparse Namespace
    :param sudoku_data: A dict containing sudoku puzzles and/or solutions
    """

    # Creates stats variables, match case nad execute
    num_of_ops = 0
    dt_obj = datetime.datetime.now()
    cur_date = dt_obj.date()
    cur_time = dt_obj.time().strftime("%H:%M:%S")
    presentation_method = "test pipeline"
    solutions_found = 0
    tstart = time.time()
    for entry in tqdm.tqdm(sudoku_data, desc="Testing..."):
        base_grid = gridops.make_grid(entry)
        match args.method:
            case 1:
                # Recursion and backtracking
                name = "R&B"
                free_fields = solvers.list_of_free_fields(base_grid)
                solution_status = solvers.bact_r_solve(base_grid, free_fields)
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 2:
                # Boosted recursion and backtracking
                name = "Boosted R&B"
                solution_status = solvers.boost_bact_r_solve(
                    base_grid, solvers.scan_for_valid_vals(base_grid)
                )
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 3:
                # Dlxsudoku module from PyPl
                name = "DLXSudoku"
                solution = solvers.dlxsudoku_module(entry)
                if "0" not in solution:
                    solution_status = True
                else:
                    solution_status = False
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 4:
                # Random walk...
                name = "Random walk"
                solution_status = solvers.random_walk(base_grid)
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case 5:
                # Cake algorithm
                name = "Cake algorithm"
                solution = solvers.cake_algo(base_grid)
                solution_status = solution
                num_of_ops += 1
                if solution_status:
                    solutions_found += 1
            case _:
                sys.exit("No such algorithm implemented, please check your input")
    tstop = time.time()
    telapsed = tstop - tstart
    avg_op_time = telapsed / num_of_ops
    dbops.write_to_db(
        presentation_method,
        name,
        str(cur_date),
        str(cur_time),
        telapsed,
        num_of_ops,
        solutions_found,
        avg_op_time,
        db_name,
    )
    if args.tofile or args.tests:
        print()
        print(f"{'Method of presentation':<22}{': ':<}{presentation_method}")
        print(f"{'Solve method name':<22}{': ':<}{name}")
        print(f"{'Test date':<22}{': ':<}{cur_date}")
        print(f"{'Test start time':<22}{': ':<}{cur_time}")
        print(f"{'Test duration time':<22}{': ':<}{telapsed:.8f}")
        print(f"{'Puzzles read':<22}{': ':<}{num_of_ops:,}")
        print(f"{'Solutions found':<22}{': ':<}{solutions_found:,}")
        print(f"{'Avg. solve time':<22}{': ':<}{avg_op_time:.8f}\n")
        sys.exit("Program has ended.\n")


def argparse_logic() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """
    Returns argparse Namespace instance containing all args and flags.
    Assign args after returning or change what is to be returned via this function.

    :raise argparse.ArgumentError: If -m is not an int in specified range
    :return: An object containing names of args provided via cli
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        prog="Sudoku solver",
        description="""Solve sudoku puzzle using multiple methods,
        check statistics about solving process.""",
        epilog="For more information write at pokeplacek@gmail.com. Thank you for using!",
    )
    parser.add_argument(
        "-m",
        "--method",
        metavar="M",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5],
        help="""Type in a number to choose the solver method.
        Input an int in range {1-5}.
        >> 1 << Recursion and backtracking,
        >> 2 << Boosted recursion and backtracking looking ahead for available valid values,
        >> 3 << Dlxsudoku module from PyPl,
        >> 4 << Random walk... Use one very small data samples, preferably just one,
        >> 5 << Cake algorithm.""",
    )
    parser.add_argument(
        "-f",
        "--filename",
        metavar="FN",
        type=str,
        default=False,
        action="store",
        help="""Type in filename with extension containing your data.
        Use csv or text format with header row and data in distinct lines separated with commas.
        Use 0 to point which values are to be found,
        and solution after comma if you have it and want to compare results.
        Stick to puzzle,solution or solution,puzzle data layout when file contains solution.
        Or puzzle only if there is no data to compare to.""",
    )
    parser.add_argument(
        "-s",
        "--solutions",
        action="store_true",
        default=False,
        help="""If you have solutions to your Sudoku puzzle sets,
        provide them in the file itself.""",
    )
    parser.add_argument(
        "-c",
        "--compare",
        action="store_true",
        default=False,
        help="""If you have solutions to compare,
        you can check if solution generated is equal to solution provided.""",
    )
    parser.add_argument(
        "-st",
        "--statistics",
        action="store_true",
        default=False,
        help="""If you have ran som puzzle solving already,
        you can check some stats of conducted operations.""",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--print",
        action="store_true",
        default=False,
        help="""Use for printing solver results on the screen.
        This is the default way of usage.""",
    )
    group.add_argument(
        "-tf",
        "--tofile",
        action="store_true",
        default=False,
        help="""Use for storing solver results to the file named results.csv.""",
    )
    group.add_argument(
        "-t",
        "--tests",
        action="store_true",
        default=False,
        help="""Use for testing solver results. Read effects from database by using '-st' flag.""",
    )
    args = parser.parse_args()
    if not args.tofile:
        args.print = True

    return args, parser


if __name__ == "__main__":
    main()
