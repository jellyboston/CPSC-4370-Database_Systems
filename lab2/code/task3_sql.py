"""
Each task is a function that returns the result of a SQL query.

No other imports may be used
"""
from database_connection import DatabaseConnection


def task_3_1():
    """
    List the top 5 most borrowed books in the library.

    The result should include the books title and number of times borrowed,
    ranked from most borrowed to least borrowed.
    """
    # TODO: Implement me
    pass


def task_3_2():
    """
    For each month, calculate the total number of books borrowed and the
    average duration (in days) of a borrow.

    - If a book has not been returned yet, it should not be included in
    the average duration.
    - If a book was borrowed in month X and returned in month Y, it should
    be included in the month it was checked out.

    Display the months in a year-month format (YYYY-MM) and order
    by the month ascending.
    """
    # TODO: Implement me
    pass


def task_3_3():
    """
    Identify publishers that frequently collaborate with specific authors,
    where "frequent collaboration" means publishers that have published more
    than three books by the same author.
    """
    # TODO: Implement me
    pass


if __name__ == '__main__':
    pass
