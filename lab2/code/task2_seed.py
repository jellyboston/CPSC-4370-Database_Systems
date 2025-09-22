"""
Seeding library database. No other imports may be used.
"""

import random
from datetime import datetime, timedelta

from database_actions import database_actions

# Seed counts
NUM_PUBLISHERS = 3
NUM_AUTHORS = 20
NUM_BOOKS = 200
NUM_STUDENTS = 100
NUM_BORROWS = 500

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
    # Publisher data
    publisher_attr = ['publisher_name']
    publisher_values = ['Charlie', 'Beta', 'Alpha']
    # publisher_fields = []
    for name in random.sample(publisher_values, NUM_PUBLISHERS):
        # no repeats -> small sample allows for deterministic debugging
        database_actions.execute_insert('publisher', publisher_attr, (name,))
        # store publisher_id for sanity testing
        # publisher_fields.append(query_id(name, publisher_fields)

    # Author data
    

def query_id(name, publisher_fields):
    with database_actions.DatabaseConnection() as cursor:
        cursor.execute(
            """
            SELECT publisher_id, publisher_name
            FROM publisher
            WHERE publisher_name = %s
            LIMIT 1;
            """,
            (name,)  # <- pass params as a tuple
        )
        row = cursor.fetchone()  # (publisher_id, publisher_name)
        if row:
            return row

if __name__ == '__main__':
    seed_database()
