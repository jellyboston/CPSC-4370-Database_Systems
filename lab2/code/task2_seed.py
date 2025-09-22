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

# Fixed seed pools
PUBLISHER_VALUES = ['Charlie', 'Beta', 'Alpha']
AUTHOR_VALUES = ['Gibran', 'Twain', 'King', 'Tolstoy', 'Rowling', 'Orwell', 'Dickens']
STUDENT_NAMES = ['Alice', 'Bob', 'Cathy', 'David', 'Eve']
STUDENT_STREETS = ['Main St', 'Maple Ave', 'Elm St', 'Pine Rd']
STUDENT_CITIES = ['New Haven', 'Hartford', 'Stamford']
STUDENT_STATES = ['CT', 'NY', 'MA']

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
    reset_db_seed() # for testing
    
    # Publisher data
    publisher_attr = ['publisher_name']
    simple_seed(publisher_attr, PUBLISHER_VALUES, 'publisher', NUM_PUBLISHERS)

    # Author data
    author_attr = ['name']
    simple_seed(author_attr, AUTHOR_VALUES, 'author', NUM_AUTHORS)

    # Book data
    publisher_ids = query_ids("publisher", "publisher_id") # extract foreign keys
    author_ids = query_ids("author", "author_id")
    seed_books(NUM_BOOKS, publisher_ids, author_ids)

    # Book edition data
    book_ids = query_ids("book", "book_id")
    seed_book_edition(book_ids)

    # Student registration data
    seed_student(NUM_STUDENTS, STUDENT_NAMES, STUDENT_STREETS, STUDENT_CITIES, STUDENT_STATES)
    student_ids = query_ids("student", "student_id")
    seed_student_phones(student_ids)


'''
DRY function for seeding the publisher and author tables with single attributes.

Returns: None
'''    
def simple_seed(attr, values, table_name, COUNT):
    assert COUNT >= 0
    for name in random.choices(values, k=COUNT):
        # no repeats -> small sample allows for deterministic debugging
        database_actions.execute_insert(table_name, attr, (name,))

        # store publisher_id for sanity testing
        # publisher_fields.append(query_id(name, publisher_fields)

def query_ids(table: str, id_col: str):
    """
    Return a flat list of integer IDs from the given table/column.
    Uses a whitelist for table/column names, since psycopg2 cannot
    parameterize identifiers (only values).
    """
    sql = f"SELECT {id_col} FROM {table} ORDER BY {id_col};"

    with database_actions.connection as cursor:
        cursor.execute(sql)                 # no values to parametrize here
        rows = cursor.fetchall()            # [(1,), (2,), ...]
        return [r[0] for r in rows]         # -> [1, 2, ...]
    
def seed_books(n, publisher_ids, author_ids):
    for i in range(n):
        title = f"Book #{i+1}"                      
        pub_id = random.choice(publisher_ids)       
        auth_id = random.choice(author_ids)
        database_actions.execute_insert(
            "book",
            ("title", "publisher_id", "author_id"),
            (title, pub_id, auth_id)
        )

# Tie each book to an edition.
def seed_book_edition(n, id):
    for i in range(n):
        book_id = random.choice(id)
        edition_number = f"Book #{i+1}"
        year = random.int()
        database_actions.execute_insert(
            "book_edition",
            ("book_id", "edition_number", "year"),
            (book_id, edition_number, year)
        )  

def seed_book_edition(book_id, min_yr = 1900, max_yr = 2025):
    EDITION_NUMBER = 1 # just for testing
    for id in book_id:
        year = random.randint(min_yr, max_yr)
        database_actions.execute_insert(
            "book_edition",
            ("book_id", "edition_number", "year"),
            (id, EDITION_NUMBER, year)
        )

def seed_student(n, student_names, student_streets, student_cities, student_states):
    for i in range(n):
        name, street = random.choice(student_names), random.choice(student_streets)
        city, state = random.choice(student_cities), random.choice(student_states)
        database_actions.execute_insert(
            "student",
            ("student_name", "street", "city", "state"),
            (name, street, city, state)
        )

def seed_student_phones(student_ids, min_phones=1, max_phones=3):
    for sid in student_ids:
        k = random.randint(min_phones, max_phones)  # how many phones for this student
        numbers = set()  # avoid duplicate numbers for same student
        for _ in range(k):
            # Generate a random phone like "203-555-1234"
            phone = f"{random.randint(200, 999)}-555-{random.randint(1000, 9999)}"
            while phone in numbers:
                phone = f"{random.randint(200, 999)}-555-{random.randint(1000, 9999)}"
            numbers.add(phone)

            database_actions.execute_insert(
                "student_phone",
                ("student_id", "phone_number"),
                (sid, phone)
            )



def reset_db_seed():
    sql = """
    TRUNCATE
        borrows,
        student_phone,
        book_edition,
        book,
        student,
        author,
        publisher
    RESTART IDENTITY CASCADE;
    """
    with database_actions.connection as cursor:
        cursor.execute(sql)

if __name__ == '__main__':
    seed_database()
