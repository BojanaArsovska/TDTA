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
from find_all_files import find_gone_authors, find_all_files
import time_script
import subprocess
import sqlite3
import pandas as pd
import xlsxwriter
from check_if_java_file import check_type_java

# this is never called for some reason

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
            if check_type_java(com_element.filename):
                if com_element.change_type.name == "RENAME":
                    cursor.execute('UPDATE commits SET file_name = "s%s" WHERE file_name = "s%s";' % (
                        com_element.new_path, com_element.old_path))
                else:
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
            print("filename of file added", com_element.filename)
            conn.commit()

        # todo: remove this
        if counter % 100 == 0:
            print(counter)




# calculates the code churn of files in the given commit
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


def rm_cloned_repo_and_db(database):
    if os.path.exists(database):
        try:
            os.remove(database)
            print(f"{database} has been removed.")

        except Exception as e:
            print(f"Error removing: {e}")

    else:
        print(f"{database} does not exist in the current directory.")


def virtualize_db():

    # Connect to the SQLite database
    conn = sqlite3.connect("db_commits_files.db")

    # List of your table names
    tables = ['commits','auth_contib', 'file_author_contrib', 'file_legacy_complexity']


    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter('database_tables_visualizer.xlsx', engine='xlsxwriter') as writer:
        for table in tables:
            # Read the table content into a DataFrame
            df = pd.read_sql_query(f"SELECT * from {table}", conn)

            # Write the DataFrame to an Excel sheet
            df.to_excel(writer, sheet_name=table, index=False)

    # Close the database connection
    conn.close()

    print("Excel file has been created successfully!")



if __name__ == "__main__":


    database = "db_commits_files.db"

    # should be changed to lead to the path of the clonned repo which is the tool
    # ROOT_DIRECTORY = (subprocess.run('pwd', shell=True, capture_output=True, text=True)).stdout
    cloned_repo_path, gone_authors, cloned_dir_name = read_args_terminal.read_args_terminal()

    # the db is being deleted at the beginning and later remade for testing purposes
    rm_cloned_repo_and_db(database)

    ROOT_DIRECTORY = os.getcwd()

    # connect to database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # create database
    create_and_init_db()

    # open the local repository
    repo = git.Repo(cloned_repo_path)

    # if you want to limit the number of commits for analysing, you can specify the value
    # the var commits is an array of el that contain data about each commit, 1 el = 1 commit
    commits = islice(Repository(cloned_repo_path).traverse_commits(), 5000)
    # otherwise use this command
    # commits = Repository(local_repo_path).traverse_commits()

    #################### UNIT TEST ###############
    # # -check if all commits are captured
    # for commit in commits:
    #     print(commit.author.name)
    # for com in commits:
    #     print(com.hash)

    update_table_commits(commits)
    update_total_code_churn()

    if gone_authors is None:
        gone_authors = find_gone_authors(cursor)




    find_all_files(cloned_repo_path, gone_authors, ROOT_DIRECTORY, conn)
    get_data_from_db(cursor)
    conn.close()
    virtualize_db()
    # rm_cloned_repo_and_db(database, cloned_dir_name)

