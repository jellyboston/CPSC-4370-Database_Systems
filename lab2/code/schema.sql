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
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    street VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100)
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
    year INTEGER,
    PRIMARY KEY (book_id, edition_number),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);

CREATE TABLE student_phone (
    student_id INTEGER NOT NULL,
    phone_number VARCHAR(20) NOT NULL,

    PRIMARY KEY (student_id, phone_number),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE borrows (
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    check_out_date DATE NOT NULL,
    due_date DATE,
    return_date DATE,

    PRIMARY KEY (book_id, student_id, check_out_date),
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);
