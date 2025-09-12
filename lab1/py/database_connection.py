"""
Contains a context manager for a database connection.

Author: Rami Pellumbi
"""
import psycopg2

DB_NAME = "universitydb"  # same name as db you made in the setup
USER = "admin"  # replace with your username if necessary
PASSWORD = "admin"  # replace with your password if necessary
HOST = "localhost"  # replace if you're running postgres on a different host
PORT = "5432"  # default port that postgres listens on - replace if necessary


class DatabaseConnection:
    """
    This class is a context manager for a database connection.
    It automatically establishes a connection to the database when the context is entered
    and closes the connection when the context is exited.

    Example Usage:
    ```
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT * FROM students;')
        results = cursor.fetchall()
        print(results)
    ```
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()
        if self.cursor:
            self.cursor.close()

        if exc_type or exc_val or exc_tb:
            print(f"Error: {exc_type}, {exc_val}, {exc_tb}")
