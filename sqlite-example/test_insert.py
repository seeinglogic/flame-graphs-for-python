import os
import random
import sqlite3
import string
import sys


DB_NAME = "randomized.db"

def random_name():
    first_names = ["John", "Jane", "Bob", "Alice", "Charlie"]
    last_names = ["Smith", "Johnson", "Doe", "Brown", "Davis"]
    return random.choice(first_names) + " " + random.choice(last_names)

def random_age():
    return random.randint(18, 65)

def random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "example.com", "testmail.com"]
    username = ''.join( random.choices(string.ascii_lowercase, k=8)) 
    return username + "@" + random.choice(domains)


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS random_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')
    return conn, cursor

def insert_random_rows(cursor: sqlite3.Cursor, n: int):
    for _ in range(n):
        name = random_name()
        age = random_age()
        email = random_email()

        cursor.execute(
            "INSERT INTO random_data (name, age, email) VALUES (?, ?, ?)",
            (name, age, email)
        )

def close_db(conn: sqlite3.Connection):
    conn.commit()
    conn.close()


def main(n: int=500000):
    conn, cursor = init_db()
    print(f'Perf testing: Inserting {n} rows of random data into "{DB_NAME}"...')
    insert_random_rows(cursor, n)
    close_db(conn)
    os.unlink(DB_NAME)
    print(f'Deleted "{DB_NAME}"')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
        main(n)
    else:
        main()
