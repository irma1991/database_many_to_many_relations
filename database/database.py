import sqlite3
from book.book import book
from book.publisher import publisher


def open_connection():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_books_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_title TEXT UNIQUE,
                        author TEXT,
                        publish_date TEXT,
                        publisher TEXT,
                        selling_price REAL)
                    """

        cursor.execute(query)

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)

def create_publishers_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS books (
                        publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        publisher_name TEXT UNIQUE,
                        book_title TEXT,
                        author TEXT,
                        printed_quantity REAL,
                        printing_price REAL)
                    """

        cursor.execute(query)

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)

create_books_table()
create_publishers_table()


def query_database(query, params = None):
    try:
        connection, cursor = open_connection()
        if params:
            cursor.execute(query, params)
            connection.commit()
        else:
            for row in cursor.execute(query):
                print(row)

    except sqlite3.DataError as error:
        print(error)
    finally:
        connection.close()


def create_book(book):
    query = """INSERT INTO books VALUES (? ,?, ?, ?, ?, ?)"""
    params = (book.book_id, book.book_title, book.author, book.publish_date, book.publisher, book.selling_price)
    query_database(query, params)


book1 = book(None, "Pavadinimas", "Autorius", 2015, "Leidejas", 12)

# create_book(book1)


def get_book(book):
    query = """SELECT * FROM books"""
    query_database(query)

get_book(book1)


def update_book(book):
    query = """UPDATE books SET book_title = 'Pavadinimas antras'
    WHERE book_title = (?)"""
    params = (book.book_title,)
    query_database(query, params)


# update_book(book1)


def delete_book(book):
    query = """DELETE FROM books
    WHERE book_id = (?) OR book_title = (?) OR author = (?) OR publish_date = (?) OR publisher = (?) OR selling_price = (?)"""
    params = (book.book_id, book.book_title, book.author, book.publish_date, book.publisher, book.selling_price)
    query_database(query, params)


# delete_book(book1)

def create_publisher(publisher):
    query = """INSERT INTO books VALUES (? ,?, ?, ?, ?, ?)"""
    params = (publisher.publisher_id, publisher.publisher_name, publisher.book_title, publisher.author, publisher.printed_quantity, publisher.printing_price)
    query_database(query, params)


publisher1 = publisher(None, "Leidejo vardas", "Knygos pavadinimas", "Autorius", 2000, 6)

# create_publisher(publisher1)


def get_publisher(publisher):
    query = """SELECT * FROM publishers"""
    query_database(query)

# get_publisher(publisher1)


def update_publisher(publisher):
    query = """UPDATE publishers SET publisher_name = 'Leidejo vardas antras'
    WHERE publisher_name = (?)"""
    params = (publisher.publisher_name,)
    query_database(query, params)


# update_publisher(publisher1)


def delete_publisher(publisher):
    query = """DELETE FROM publishers
    WHERE publisher_id = (?) OR publisher_name = (?) OR book_title = (?) OR author = (?) OR printed_quantity = (?) OR printing_price = (?)"""
    params = (publisher.publisher_id, publisher.publisher_name, publisher.book_title, publisher.author, publisher.printed_quantity, publisher.printing_price)
    query_database(query, params)


# delete_publisher(publisher1)

def create_junction_table():
    try:
        connection = sqlite3.connect("books.db")
        connection_cursor = connection.cursor()
        connection_cursor.execute("""CREATE TABLE IF NOT EXISTS junction (
                                                    first_id int,
                                                    second_id int,
                                                    FOREIGN KEY (first_id) REFERENCES books(book_id),
                                                    FOREIGN KEY (second_id) REFERENCES publishers(publisher_id)
                                                    )""")
        connection.commit()

    except sqlite3.DataError as error:
        print(error)

    finally:
        connection.close()

create_junction_table()

def insert_junction(book, publisher):
    insert_table_junction_query = """INSERT INTO junction (first_id, second_id)
                                        SELECT(SELECT book_id FROM books WHERE book_title=(?)), 
                                        (SELECT publisher_id FROM publishers WHERE publisher_name=?)"""
    param = (book, publisher)
    query_database(insert_table_junction_query, param)


insert_junction(book1.book_title, publisher1.publisher_name)

def get_junction():
    query = """SELECT * FROM junction JOIN book ON junction.first_id = book.book_id 
    JOIN publishers ON junction.second_id = publisher.publisher_id"""

    query_database(query)


get_junction()