import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_and_init_db():
    create_connection(r"db_commits_files.db")
    conn = sqlite3.connect('db_commits_files.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS commits 
                    (id INTEGER PRIMARY KEY,
                    sha TEXT,
                    date TIMESTAMP,
                    file_name TEXT,
                    author TEXT,
                    changes INT,
                    complexity INT,
                    nloc INT
                    );'''
                   )

def create_file_legacy_complexity_table():
    create_connection(r"db_commits_files.db")
    conn = sqlite3.connect('db_commits_files.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_legacy_complexity(id INTEGER PRIMARY KEY,
                    file_name TEXT,
                    legacy_percentage FLOAT,
                    cog_complexity FLOAT);'''
                   )

def create_auth_db():
    create_connection(r"db_commits_files.db")
    conn = sqlite3.connect('db_commits_files.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS auth_contib
                    (id INTEGER PRIMARY KEY,
                    author TEXT,
                    file_name TEXT,
                    changes INT, 
                    contribution_count INT
                    );'''
                   )

# create_and_init_db()
#
# create_auth_db()
#
# create_file_legacy_complexity_table()
