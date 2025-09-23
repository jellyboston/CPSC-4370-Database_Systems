#### Startup Commands
```bash
conda activate 4370
docker start cpsc437-postgres-1
```

Create a new database in the PostgreSQL container:
```bash
docker exec -i cpsc437-postgres-1 psql -U admin -d default_database -c "CREATE DATABASE library"
```

Ensure user has all privileges on the database:
```bash
docker exec -i cpsc437-postgres-1 psql -U admin -d library -c "GRANT ALL PRIVILEGES ON DATABASE library TO admin"
```

To query the database:
```bash
docker exec -it cpsc437-postgres-1 psql -U admin -d {db}
```

---
#### Notes from tasks1
```python
'''
Step 1 - Strong Entities
book(book_id, title)
publisher(publisher_id, publisher_name)
author(author-id, name)
student(student_id, student_name, street, city, state, phone_number) Q: How to flatten phone_number?

Step 2 - Weak Entities
book_edition(book_id, edition_number)

Step 3 - Representation of Relationship Sets (following the cardinality relation rules; see text)

--S1--
book(book_id PK, title)
BookEdition(book_id PK/FK, edition_number PK, year)
CREATE TABLE book_edition(
    book_id     INT,
    edition_number  INT,
    year    INT,
    PRIMARY KEY (book_id, edition_number),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);

--S2--
book(book_id PK, title, publisher_id FK) => allow to be null if partial
CREATE TABLE book (
    book_id      INT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    publisher_id INT,   -- FK to publisher

    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);
publisher(publisher_id PK, publisher_name)
CREATE TABLE publisher (
    publisher_id   INT PRIMARY KEY,
    publisher_name VARCHAR(100) NOT NULL
);

--S3--
book(book_id PK, title, publisher_id FK, author_id FK) 
CREATE TABLE book (
    book_id      INT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    publisher_id INT,         -- NULL allowed unless Book has total participation in Book→Publisher
    author_id    INT NOT NULL, -- total participation in Book→Author

    FOREIGN KEY (author_id)    REFERENCES author(author_id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);


author(author_id PK, name)
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    name VARCHAR(100)
)

--S4--
CREATE TABLE book (
    book_id      INT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    publisher_id INT,         
    author_id    INT NOT NULL,

    FOREIGN KEY (author_id)    REFERENCES author(author_id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id),
);

borrows(book_id PK/FK, student_id PK/FK, due_date, check_out_date, return_date)
CREATE TABLE borrows(
    book_id INT,
    student_id INT,
    due_date DATE,
    check_out_date DATE,
    return_date DATE,

    PRIMARY KEY (book_id, student_id, check_out_date),
    FOREIGN KEY(book_id) REFERENCES book(book_id),
    FOREIGN KEY(student_id) REFERENCES student(student_id)
);

CREATE TABLE student (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100),
    street VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
);

CREATE TABLE student_phone (
    student_id   INT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    PRIMARY KEY (student_id, phone_number),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

'''

'''
Summary
M:N → always new table with both keys + attributes.

1:N or N:1 → FK goes to the “many” side.

1:1 → FK goes to the total side (or new table if both partial).

Relationship attributes → always live in the table created for the relationship (if M:N or separate relation is needed).

Total participation → safe to add FK without NULLs. Partial → avoid FKs that would be NULL-heavy.
'''
```