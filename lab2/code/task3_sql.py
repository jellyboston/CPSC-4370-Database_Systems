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
    sql = f"""
    SELECT book.title, COUNT(borrows.book_id) AS "Borrowed Count"
    FROM book JOIN borrows USING (book_id)
    GROUP BY book.book_id, book.title
    ORDER BY "Borrowed Count" DESC 
    LIMIT 5;
    """

    with DatabaseConnection() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
    return results

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
    # Need to calculate duration = return_date - checkout_out_date
    # Take average of that
    sql = f"""
    SELECT
        to_char(date_trunc('month', check_out_date), 'YYYY-MM') AS month,
        COUNT(*) AS "total borrowed",
        ROUND(
          AVG((return_date - check_out_date)) FILTER (WHERE return_date IS NOT NULL)
        , 2) AS avg_duration
    FROM borrows
    GROUP BY date_trunc('month', check_out_date)
    HAVING COUNT(*) FILTER (WHERE return_date IS NOT NULL) > 0
    ORDER BY date_trunc('month', check_out_date) ASC;
    """
    with DatabaseConnection() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
    return results


def task_3_3():
    '''
    combined join (
        # From author
        author_id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL

        # From book
        book_id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        publisher_id INTEGER,             
        author_id INTEGER NOT NULL,     
        FOREIGN KEY (author_id)    REFERENCES author(author_id),
        FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)

        # From publisher
        publisher_id SERIAL PRIMARY KEY,
        publisher_name VARCHAR(100) NOT NULL
    )
    
    '''
    """
    Identify publishers that frequently collaborate with specific authors,
    where "frequent collaboration" means publishers that have published more
    than three books by the same author.
    """
    # TODO: Implement me
    sql = f"""
    SELECT
        p.publisher_name AS publisher,
        a.name           AS author,
        COUNT(DISTINCT b.book_id) AS collaboration_count
    FROM publisher AS p
        JOIN book      AS b ON p.publisher_id = b.publisher_id
        JOIN author    AS a ON a.author_id    = b.author_id
    GROUP BY
        p.publisher_name,
        a.name
    HAVING
        COUNT(DISTINCT b.book_id) > 3  
    ORDER BY
        collaboration_count DESC;
    """
    with DatabaseConnection() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return results


if __name__ == '__main__':
    pass
