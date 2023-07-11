import sqlite3
from cognitive_complexity_upgrade import get_cognitive_complexities
import os


# randomly chosen gone authors
# gone_contributors = ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick']

# connect to database
conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()
counter = 0


def find_currently_exisitng_files(directory):

    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            absolute_path = file
            file_list.append(absolute_path)

    return file_list


# calc the total contribution of all authors in the list for a file
def gone_authors_contrib(gone_contributors, auth_percentage):
    total_contrib_percentage = 0
    for auth_perc in auth_percentage:
        if auth_perc[0] in gone_contributors:
            if auth_perc[1] is not None:
                total_contrib_percentage += auth_perc[1]
    return total_contrib_percentage


# updates file_legacy_complexity table with columns(files, file_name, legacy_percentage, cog_complexity) with all the gathered info
def update_table_tot_legacy_contrib(file, gone_authors_contib, cog_complexity):
    cursor.execute("INSERT INTO file_legacy_complexity (file_name, legacy_percentage, cog_complexity) VALUES (?,?,?)",
                               (file, gone_authors_contib,cog_complexity))
    conn.commit()


# Loops through all directories and subdirectories to find all files
def find_all_files(root_directory, gone_auth):
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
        if counter % 100 == 0:
            print(f'Done {str(counter)} files out of {str(len(file_list))}')

        file = file[0]
        cursor.execute('SELECT author, percentages FROM file_author_contrib WHERE file_name = "%s";' %(file))
        contrib_percentage = cursor.fetchall()
        cog_complexity = get_cognitive_complexities(file, root_directory)


        update_table_tot_legacy_contrib(file, gone_authors_contrib(gone_auth, contrib_percentage), cog_complexity)


# find_all_files("/Users/bojanaarsovska/TDtool/jenkins", ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick'] )
# file_list = (find_currently_exisitng_files(root_directory))
        # for file in file_list:
        #     cursor.execute("SELECT * FROM file_legacy_complexity WHERE file_name LIKE '%%%s';" %(file))
        #     result = cursor.fetchall()
        #     if len(result) is not 0:
        #         print(result)
