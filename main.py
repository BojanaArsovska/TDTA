import sys
import os
import shutil
from itertools import islice
import git
from create_sql_db import *
from pydriller import *
from pydriller.metrics.process.code_churn import CodeChurn
import read_args_terminal
from results_fetcher import get_data_from_db
from find_all_files import former_contributors, find_all_files
import subprocess
import sqlite3
import pandas as pd
import xlsxwriter
from check_if_java_file import check_type_java
from pathlib import Path
import warnings


def find_currently_exisitng_files(directory):

    directory_path = Path(directory)
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
                item.replace(ROOT_DIRECTORY, '')
                file_list.append(str(item))

    # Start the traversal from the root directory
    traverse_dir(directory_path)
    return file_list




def get_commit_shas():
    repo = git.Repo(cloned_repo_path)
    # with n you can specify how many commit you want to be analysed
    n = 5000

    # get the list of all commit SHAs in the master branch
    commit_shas = [commit.hexsha for commit in repo.iter_commits('master')]
    print("commit_shas", commit_shas, "\n")

    if len(commit_shas) >= n:
        # Get the nth commit SHA
        nth_commit_sha = commit_shas[-n]
    else:
        print(f"The repository has fewer than {n} commits.")
        # if the repo is shorter than the specified num of commits n, then that's its n'th commit
        nth_commit_sha = commit_shas[len(commit_shas) -1]

    # get the first and last commit SHAs
    # first commit is the last and last commit is the first item in the list FIFO order
    first_commit_sha = commit_shas[-1]
    last_commit_sha = commit_shas[0]

    return first_commit_sha, last_commit_sha, nth_commit_sha


def cal_code_churn(commit_sha, file_name):
    try:
        metric = CodeChurn(path_to_repo=cloned_repo_path,
                           from_commit=str(commit_sha),
                           to_commit=str(commit_sha),
                           add_deleted_lines_to_churn=True) #design decision
        files_count = metric.count()
        return files_count[file_name]

    except:
        print("Removed file from this repo", file_name)
        return 0


# THIS FUNCTION IS A DUPLICATE BUT MIGHT BE USEFUL
# you can specify the range of commits for analysing
# def find_all_commits_from_first_to_nth():
#     first_commit, last_commit, nth_commit_sha = get_commit_shas()
#     print("first_commit, last_commit, nth_commit_sha", first_commit, last_commit, nth_commit_sha)
#
#     # CodeChurn is a pydriller thing
#     metric = CodeChurn(path_to_repo=cloned_repo_path,
#                        from_commit=first_commit,
#                        to_commit=nth_commit_sha)
#     return metric


def update_table_commits(commits):
    counter = 0
    for _commit in commits:

        counter += 1
        for com_element in _commit.modified_files:
            # the same way we are checking is a file is java file, we could have been testing if iot is in the repository still or it has been removed
            # while this sounds like a good plan, the problem is that we can't know if the file has been renamed later, so by default file that has one name
            # gets renamed later, will be classified as unexisiting file and will not be added to the database
            if check_type_java(com_element.filename):
                if com_element.change_type.name == "RENAME":
                    cursor.execute('UPDATE commits SET file_name = (?) WHERE file_name = (?);', (com_element.new_path, com_element.old_path))
                    conn.commit()

                # Here we delete all the files from the database that were deleted in the repository
                elif com_element.change_type.name == "DELETE":
                    cursor.execute('DELETE from commits WHERE file_name = (?);', (str(com_element.old_path),))
                    conn.commit()

                else:
                    # every file has a new path property when it appears for the first time in a the commits and a old part property which is None
                    # this property gets updated every time a file is modified
                    # when the file is modified, old path becomes new path and new path stays the same
                    # when a file is renamed the new path becomes and old path and the old path variable takes the path of the renamed file
                    # if the modification type is delete
                    # then the new path property becomes None and the old path takes the value from the new path
                    #
                    if com_element.new_path is not None:
                        cursor.execute(
                            "INSERT INTO commits (sha, date, file_name, author, changes, nloc) VALUES (?,?,?,?,?,?)",
                            (_commit.hash, _commit.committer_date, com_element.new_path, _commit.author.name,
                             cal_code_churn(_commit.hash, com_element.new_path), com_element.nloc))

                    else:
                        cursor.execute(
                            "INSERT INTO commits (sha, date, file_name, author, changes, nloc) VALUES (?,?,?,?,?,?)",
                            (_commit.hash, _commit.committer_date, com_element.old_path, _commit.author.name,
                             cal_code_churn(_commit.hash, com_element.old_path), com_element.nloc))
            else:
                continue
            conn.commit()

        # todo: remove this
        if counter % 100 == 0:
            print(counter)


# Calculates the code churn of files in the given commit
def update_total_code_churn():
    # file_churns = total_code_churn()
    # file_churns = total_code_churn().count()
    # files_renamed = total_code_churn().filepath
    # print(file_churns)


    sql_commands = [
        """
        INSERT INTO file_author_contrib (file_name, author, auth_churn, file_size) 
        SELECT file_name, author, SUM(changes) AS SCORE, nloc 
        FROM commits 
        GROUP BY file_name, author;
        """,

        """
        DELETE from file_author_contrib where file_name ='';
        """,

        """
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_table AS
        SELECT file_name, author, SUM(changes) as total_changes
        FROM commits
        GROUP BY file_name, author;
        """,

        """
        UPDATE file_author_contrib
        SET auth_churn = (
            SELECT total_changes
            FROM temp_table
            WHERE 
                file_author_contrib.file_name = temp_table.file_name AND 
                file_author_contrib.author = temp_table.author
        );
        """,

        """
        DROP TABLE temp_table;
        """,

        """
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_table AS
        SELECT file_name, SUM(changes) as total_changes
        FROM commits
        GROUP BY file_name;
        """,

        """
        UPDATE file_author_contrib
        SET total_churn = (
            SELECT total_changes
            FROM temp_table
            WHERE 
                file_author_contrib.file_name = temp_table.file_name
        );
        """,

        """
        DROP TABLE temp_table;
        """,

        """
        UPDATE file_author_contrib SET percentages = CAST(auth_churn AS float) / CAST(total_churn AS float);
        """,

        """
        UPDATE file_author_contrib
        SET file_size = (
          SELECT MAX(file_size)
          FROM file_author_contrib f_a
          WHERE file_author_contrib.file_name = f_a.file_name
        );
        """,

        """
        UPDATE file_author_contrib SET file_size_x_percentages = CAST(percentages as float) * CAST(file_size as float);
        """
    ]

    for command in sql_commands:
        cursor.execute(command)

    conn.commit()


def rm_db(database):
    if os.path.exists(database):
        try:
            os.remove(database)
        except Exception as e:
            print(f"Error removing: {e}")
    else:
        print(f"{database} does not exist in the current directory.")


def virtualize_db():
    conn = sqlite3.connect("db_commits_files.db")
    tables = ['commits','auth_contib', 'file_author_contrib', 'file_legacy_complexity']

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter('database_tables_visualizer.xlsx', engine='xlsxwriter') as writer:
        for table in tables:
            # Read the table content into a DataFrame
            df = pd.read_sql_query(f"SELECT * from {table}", conn)

            # Write the DataFrame to an Excel sheet
            df.to_excel(writer, sheet_name=table, index=False)
    conn.close()
    print("Excel file has been created successfully!")

def invalid_pmd():
    result = subprocess.run("pmd", shell=True, capture_output=True, text=True)
    return ("pmd: command not found" in result.stderr)


if __name__ == "__main__":

    if invalid_pmd():
        print("An error has occurred while running the pmd command. Ensure that pmd is installed properly on the system by following the instructions on installing pmd in the README.md")
        exit()

    # Suppressing sqlite3 warning about datetime objects by ignoring DeprecationWarning messages related to the sqlite3 module's default datetime adapter arising from indirect usage within other libraries
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    database = "db_commits_files.db"

    cloned_repo_path, former_developers, cloned_dir_name = read_args_terminal.read_args_terminal()

    # the db is being deleted at the beginning and later remade
    rm_db(database)

    ROOT_DIRECTORY = os.getcwd()

    # connect to database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # create database
    create_and_init_db()

    # open the local repository
    repo = git.Repo(cloned_repo_path)

    # The 5000 value limits the number of commits for analysing
    # The var commits is an array of el that contains data about each commit, 1 el = 1 commit
    commits = islice(Repository(cloned_repo_path).traverse_commits(), 5000)
    # To remove the limit on the number of commits traversed, uncomment the line below and comment the line above
    # commits = Repository(local_repo_path).traverse_commits()

    update_table_commits(commits)
    update_total_code_churn()

    if former_developers is None:
        former_developers = former_contributors(cursor)

    if find_all_files(cloned_repo_path, former_developers, ROOT_DIRECTORY, conn) == -1:
        print("The analysis will be discontinued due to an error.")
        conn.close()
        rm_db(database)
        exit()

    get_data_from_db(cursor)
    conn.close()
    virtualize_db()

