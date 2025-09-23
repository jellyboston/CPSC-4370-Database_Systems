-- CHANGE: Created parent tables before children to avoid FK dependency errors
-- CHANGE: Keep SERIAL only for PKs (not for FKs in child tables)
-- Child Tables
CREATE TABLE publisher (
    publisher_id SERIAL PRIMARY KEY,
    publisher_name VARCHAR(100) NOT NULL
);

CREATE TABLE author (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL
); 

CREATE TABLE student ( 
    student_id SERIAL PRIMARY KEY NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    street VARCHAR(200),
    city VARCHAR(200),
    state CHAR(2)
); 

-- Parent Tables
CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    publisher_id INTEGER,             
    author_id INTEGER NOT NULL,     
    FOREIGN KEY (author_id)    REFERENCES author(author_id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);

CREATE TABLE book_edition (
    book_id INTEGER NOT NULL,
    edition_number INTEGER NOT NULL,
    year INTEGER NOT NULL,
    PRIMARY KEY (book_id, edition_number),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE
);

CREATE TABLE phone_number ( 
    student_id INTEGER NOT NULL,
    phone_number CHARACTER(100),
    PRIMARY KEY (student_id, phone_number),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE borrows ( 
    book_id INTEGER,
    student_id INTEGER,
    check_out_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,

    PRIMARY KEY (book_id, student_id, check_out_date),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fines (
    fine_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    book_id INT NOT NULL,
    days_overdue INT NOT NULL,
    fine_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);