import subprocess
import sqlite3
from cognitive_complexity_upgrade import get_congnitive_complexities


local_repo_path = "/Users/bojanaarsovska/TDtool/jenkins"
# randomly chosen gone authors
gone_contributors = ['stephenconnolly', 'cactusman', 'dwdyer', 'jglick']

conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()

# fetch all exisiting files
cursor.execute('SELECT DISTINCT file_name FROM file_author_contrib;')
file_list = cursor.fetchall()

# calc the total contribution of all authors in the list for a file
def gone_authors_contrib(auth_percentage):
    total_contrib_percentage = 0
    for auth_perc in auth_percentage:
        if auth_perc[0] in gone_contributors:
            total_contrib_percentage += auth_perc[1]
            print(auth_perc[0])
    return total_contrib_percentage

# update the table with all the gathered info
def update_table_tot_legacy_contrib(file, gone_authors_contib, cog_complexity):
    cursor.execute("INSERT INTO file_legacy_complexity (file_name, legacy_percentage, cog_complexity) VALUES (?,?,?)",
                               (file, gone_authors_contib,cog_complexity))
    conn.commit()


for file in file_list:
    file = file[0]
    cursor.execute('SELECT author, percentages FROM file_author_contrib WHERE file_name = "%s";' %(file))
    auth_percentage = cursor.fetchall()
    cog_complexity = get_congnitive_complexities(file)
    update_table_tot_legacy_contrib(file, gone_authors_contrib(auth_percentage), cog_complexity)

# roberto.verdecchia@tiscali.it
# https://github.com/S2-group/ATDx
