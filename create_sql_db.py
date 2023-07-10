import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Database successfully created")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_commits_db(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS commits 
                    (id INTEGER PRIMARY KEY,
                    sha TEXT,
                    date TIMESTAMP,
                    file_name TEXT,
                    author TEXT,
                    changes INT,
                    nloc INT);'''
                   )

def create_file_legacy_complexity_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_legacy_complexity(id INTEGER PRIMARY KEY,
                    file_name TEXT,
                    legacy_percentage FLOAT,
                    cog_complexity FLOAT);'''
                   )

def create_file_auth_contrib(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_author_contrib(id INTEGER PRIMARY KEY,
                    file_name TEXT,
                    author TEXT,
                    auth_churn INT, 
                    total_churn	INT,
                    file_size INT,
                    file_size_x_percentages	FLOAT,
                    percentages	FLOAT,
                    total_churn_tool FLOAT);'''
                   )

def create_auth_contib(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS auth_contib
                    (author TEXT,
                    file_name TEXT,
                    all_files FLOAT);'''
                   )


def create_and_init_db():
    create_connection(r"db_commits_files.db")
    conn = sqlite3.connect('db_commits_files.db')
    cursor = conn.cursor()

    create_commits_db(cursor)
    create_file_legacy_complexity_table(cursor)
    create_file_auth_contrib(cursor)
    create_auth_contib(cursor)
