import sqlite3
from cognitive_complexity_upgrade import get_cognitive_complexities
import os


# randomly chosen gone authors
# gone_contributors = ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick']

# connect to database
global conn
global cursor
global counter

def drop_duplicate_rows(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE temp_table AS 
    SELECT DISTINCT * FROM file_legacy_complexity
    """)

    # Drop the original table
    cursor.execute("DROP TABLE file_legacy_complexity")

    # Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE temp_table RENAME TO file_legacy_complexity")

    # Commit the changes and close the connection
    conn.commit()


def find_gone_authors(cursor):
    cursor.execute("SELECT DISTINCT(author) FROM file_author_contrib;")
    return [item[0] for item in cursor.fetchall()]

def find_currently_exisitng_files(directory):
    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            absolute_path = file
            file_list.append(absolute_path)

    return file_list


# calculate the total contribution of all authors in the list for a file
# This function will return a dictionary where the keys are the authors and the values are their total contribution percentages.
def authors_contrib(gone_contributors, auth_percentage):
    prev_author = None
    author_contributions = dict()

    for auth_perc in auth_percentage:
        author = auth_perc[0]
        author_contrib_percentage = auth_perc[1]
        # works ^

        if author in gone_contributors:
            if author_contrib_percentage is not None:
                if (prev_author is not None) and prev_author == author:
                    author_contributions[author] += author_contrib_percentage
                else:
                    author_contributions[author] = author_contrib_percentage
    return author_contributions


# updates file_legacy_complexity table with columns(files, file_name, legacy_percentage, cog_complexity) with all the gathered info
# gone_authors_contib
def update_table_tot_legacy_contrib(file, authors_and_contib, cog_complexity, conn):
    cursor = conn.cursor()
    for author, contrib in authors_and_contib.items():
        # print(author, contrib)
        # ^ works

        cursor.execute("INSERT INTO file_legacy_complexity (file_name, author, legacy_percentage, cog_complexity) VALUES (?,?,?,?)",
                                   (file, author, contrib, cog_complexity))
        conn.commit()


# Loops through all directories and subdirectories to find all files
def find_all_files(root_directory, gone_contributors, ROOT_DIRECTORY, conn):
    cursor = conn.cursor()
    root_directory = root_directory + "/"
    counter = 0

    # if a file does no exist anymore, pyfriller won't find it's size and it returns None, also file_size_x_percentages
    # will be 0, we're not interested in such files
    cursor.execute('DELETE FROM file_author_contrib WHERE file_size = NULL;')
    conn.commit()

    # fetch all exisiting files
    cursor.execute('SELECT DISTINCT file_name FROM file_author_contrib;')
    file_list = cursor.fetchall()
    # all files added
    # print(file_list)

    for file in file_list:
        counter += 1
        if counter % 50 == 0:
            print(f'Done {str(counter)} files out of {str(len(file_list))}')

        file = file[0]

        # this returns authors and their contribution percentages for each file, expected output is
        cursor.execute('SELECT author, percentages FROM file_author_contrib WHERE file_name = "%s";' %(file))
        author_and_percentage = cursor.fetchall()
        cog_complexity = get_cognitive_complexities(file, root_directory, ROOT_DIRECTORY)
        authors_n_contrib = authors_contrib(gone_contributors, author_and_percentage)


       # sometimes authors_n_contrib is empty because the authors of the file are not in the list of formed developers
        # print("(gone_contributors, author_and_percentage)", (gone_contributors, author_and_percentage))

        if authors_n_contrib != []:
            update_table_tot_legacy_contrib(file, authors_n_contrib, cog_complexity, conn)

    drop_duplicate_rows(conn)


# find_all_files("/Users/bojanaarsovska/TDtool/jenkins", ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick'] )
# file_list = (find_currently_exisitng_files(root_directory))
        # for file in file_list:
        #     cursor.execute("SELECT * FROM file_legacy_complexity WHERE file_name LIKE '%%%s';" %(file))
        #     result = cursor.fetchall()
        #     if len(result) is not 0:
        #         print(result)


