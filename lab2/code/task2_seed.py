"""
Seeding library database. No other imports may be used.
"""

import random
from datetime import datetime, timedelta

from database_actions import database_actions


def seed_database():
    """
    Insert data for 3 publishers.
    Add 20 authors.
    Create 200 book entries.
    Tie each book to an edition.
    Register 100 students.
    Record 500 borrow transactions, associating books with students.
    """
    # TODO: Implement me
    pass


if __name__ == '__main__':
    seed_database()
