import miscellaneous
import validateops


def confirmation() -> None:
    """
    Confirmation menu for DB drop
    """
    print(
        """
ARE YOU SURE TOU WANT TO DROP TABLE STATISTICS???
THIS IS IRREVERSIBLE PROCESS. ALL DATA WILL BE LOST!!:
    Y. Drop the table
    N. Dont drop the table.

    0. Exit program
    """
    )


def print_other_actions() -> None:
    """
    Other actions menu
    """
    print(
        """
Choose what you want to do:
    1. Drop a record.
    2. Drop the table.
    3. Save DB to file.

    0. Exit program
    B. Get back to previous menu
    """
    )


def print_main_menu() -> None:
    """
    Manin menu
    """
    print(
        """
Choose what you want to do:
    1. Show all stats.
    2. Show stats for given presentation method only.
    3. Show stats for given solve method only.
    4. Show stats for given date.
    5. Other actions.

    0. Exit program.
    """
    )


def print_presentation_method_menu() -> None:
    """
    Presentation by method menu
    """
    print(
        """
Choose presentation method to display stats for:
    1. Test pipeline.
    2. To file.
    3. To screen.

    0. Exit program
    B. Get back to previous menu
    """
    )


def print_solve_menu() -> None:
    """
    Presentation by solve method menu
    """
    print(
        """
Choose solve method to display stats for:
    1. R&B.
    2. Boosted R&B.
    3. DLXSudoku.
    4. Random walk.
    5. Cake Algorithm.

    0. Exit program
    B. Get back to previous menu
    """
    )


def print_date() -> str:
    """
    Returns valid date string if input matches the pattern and adopted conventions for dates.

    :return: A date entered by the user after validation.
    """

    miscellaneous.clear_screen()
    while True:
        picked_date = input("\nEnter date in format YYYY-MM-DD\n\n>>> ")
        validation = validateops.validate_date(picked_date)
        miscellaneous.clear_screen()
        if validation:
            return picked_date
