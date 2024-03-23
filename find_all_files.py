import sqlite3
from cognitive_complexity_upgrade import get_cognitive_complexities
import os
from pathlib import Path
from check_if_java_file import check_type_java


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


def former_contributors(cursor):
    cursor.execute("SELECT DISTINCT(author) FROM file_author_contrib;")
    return [item[0] for item in cursor.fetchall()]


def find_currently_existing_files(ROOT_DIRECTORY):

    directory_path = Path(ROOT_DIRECTORY)
    file_list = []

    # Recursive function to traverse directories
    def traverse_dir(current_dir):
        # Iterate over each item in the current directory
        for item in current_dir.iterdir():
            # Skip items that start with '.'
            if item.name.startswith('.'):
                continue

            # If the item is a directory, recurse into it
            if item.is_dir():
                traverse_dir(item)
            # If the item is a file, add it to the file_list
            elif item.is_file():
                if check_type_java(str(item)):
                    relative_path = str(item).replace(ROOT_DIRECTORY, "")
                    file_list.append(relative_path)

    # Start the traversal from the root directory
    traverse_dir(directory_path)
    return file_list

# Calculate the total contribution of all authors in the list for a file
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
        cursor.execute("INSERT INTO file_legacy_complexity (file_name, author, legacy_percentage, cog_complexity) VALUES (?,?,?,?)",
                                   (file, author, contrib, cog_complexity))
        conn.commit()

# Loops through all directories and subdirectories to find all files
def find_all_files(cloned_repo_path, former_contributors, ROOT_DIRECTORY, conn):
    cursor = conn.cursor()
    cloned_repo_path = cloned_repo_path + "/"
    counter = 0

    # if a file does no exist anymore, pyfriller won't find it's size and it returns None, also file_size_x_percentages
    # will be 0, we're not interested in such files
    cursor.execute('DELETE FROM file_author_contrib WHERE file_size = NULL;')
    conn.commit()

    # Finds all the existing files in the repo. This is necessary to ensure that only files that still exist in te repo are shown
    existing_files = find_currently_existing_files(cloned_repo_path)

    for file in existing_files:
        counter += 1
        if counter % 50 == 0:
            print(f'Done {str(counter)} files out of {str(len(existing_files))}')

        # This returns authors and their contribution percentages for each file
        cursor.execute('SELECT author, percentages FROM file_author_contrib WHERE file_name = (?);', (str(file),))

        author_and_percentage = cursor.fetchall()
        cog_complexity = get_cognitive_complexities(file, cloned_repo_path, ROOT_DIRECTORY)
        if cog_complexity < 0:
            return -1
        authors_n_contrib = authors_contrib(former_contributors, author_and_percentage)

        # sometimes authors_n_contrib is empty because the authors of the file are not in the list of former developers
        # print("(gone_contributors, author_and_percentage)", (gone_contributors, author_and_percentage))

        if authors_n_contrib != []:
            update_table_tot_legacy_contrib(file, authors_n_contrib, cog_complexity, conn)

    drop_duplicate_rows(conn)



