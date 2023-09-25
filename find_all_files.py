import sqlite3
from cognitive_complexity_upgrade import get_cognitive_complexities
import os


# randomly chosen gone authors
# gone_contributors = ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick']

# connect to database
conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()
counter = 0

def drop_duplicate_rows():
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
def authors_contrib(gone_contributors, auth_percentage):
    total_contrib_percentage = 0
    prev_author = None
    author_contributions = []

    for auth_perc in auth_percentage:
        author = auth_perc[0]
        percent_contrib_author = auth_perc[1]

        if author in gone_contributors:
            if percent_contrib_author is not None:
                if prev_author is not None and prev_author != author:
                    # Store the total contribution of the previous author
                    author_contributions.append((prev_author,total_contrib_percentage))
                    # Reset the total contribution for the new author
                    total_contrib_percentage = 0

                total_contrib_percentage += auth_perc[1]
                prev_author = author


    return author_contributions
    # if author_contributions is [] thant menas the name fo the author if that file was not found in the list of gone authors
# This function will return a dictionary where the keys are the authors and the values are their total contribution percentages. The function keeps track of the previous author and when it detects a change in the author, it stores the total contribution of the previous author and resets the total contribution for the new author.


# updates file_legacy_complexity table with columns(files, file_name, legacy_percentage, cog_complexity) with all the gathered info
# gone_authors_contib
def update_table_tot_legacy_contrib(file, gone_authors_contib, cog_complexity):

    for author_contrib in gone_authors_contib:
        try:
            author, contrib = author_contrib
        except:
            print("author_contrib", author_contrib)
        # gone_authors_contib are now This function will return a dictionary where the keys are the authors and the values are their total contribution percentages. The function keeps track of the previous author and when it detects a change in the author, it stores the total contribution of the previous author and resets the total contribution for the new author.
        # cursor.execute("ALTER TABLE file_legacy_complexity ADD COLUMN author text")
        cursor.execute("INSERT INTO file_legacy_complexity (file_name, author, legacy_percentage, cog_complexity) VALUES (?,?,?,?)",
                                   (file, author, contrib, cog_complexity))
        conn.commit()


# Loops through all directories and subdirectories to find all files
def find_all_files(root_directory, gone_contributors, ROOT_DIRECTORY):
    # print("gone_contributors find all files",gone_contributors)
    root_directory = root_directory + "/"
    counter = 0

    # if a file does no exist anymore, pyfriller won't find it's size and it returns None, also file_size_x_percentages
    # will be 0, we're not interested in such files
    cursor.execute('DELETE FROM file_author_contrib WHERE file_size = NULL;')
    conn.commit()

    # fetch all exisiting files
    cursor.execute('SELECT DISTINCT file_name FROM file_author_contrib;')
    file_list = cursor.fetchall()

    for file in file_list:
        counter += 1
        if counter % 50 == 0:
            print(f'Done {str(counter)} files out of {str(len(file_list))}')

        file = file[0]

        # the biggest optimization ive done in my life
        # Check if the file ends with .java
        print("checking if this ends in .java", file)
        if not file.endswith('.java'):
            print("no \n ")
            continue  # Skip to the next iteration if the file is not a .java file
        else:
            print("yes \n ")

        cursor.execute('SELECT author, percentages FROM file_author_contrib WHERE file_name = "%s";' %(file))

        contrib_percentage = cursor.fetchall()
        cog_complexity = get_cognitive_complexities(file, root_directory, ROOT_DIRECTORY)
        # print("print(file, cog_complexity)", file, cog_complexity)
        authors_n_contrib = authors_contrib(gone_contributors, contrib_percentage)

       # sometimes authors_n_contrib is empty because the authors of the file are not in the list of formed developers
        # print("(gone_contributors, contrib_percentage)", (gone_contributors, contrib_percentage))

        # the biggest optimization ive done in my life
        if authors_n_contrib != []:
            update_table_tot_legacy_contrib(file, authors_n_contrib, cog_complexity)

        # print("gone_authors_contrib(gone_contributors, contrib_percentage)  ", authors_n_contrib(gone_contributors, contrib_percentage))
    drop_duplicate_rows()


# find_all_files("/Users/bojanaarsovska/TDtool/jenkins", ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick'] )
# file_list = (find_currently_exisitng_files(root_directory))
        # for file in file_list:
        #     cursor.execute("SELECT * FROM file_legacy_complexity WHERE file_name LIKE '%%%s';" %(file))
        #     result = cursor.fetchall()
        #     if len(result) is not 0:
        #         print(result)


