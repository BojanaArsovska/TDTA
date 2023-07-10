import sys
from itertools import islice
import git
from create_sql_db import *
from pydriller import *
from pydriller.metrics.process.code_churn import CodeChurn
import read_args_terminal
from calc_gone_author_contributions import find_all_files
import subprocess

ROOT_DIRECTORY = (subprocess.run('pwd', shell=True, capture_output=True, text=True)).stdout
local_repo_path, gone_authors = read_args_terminal.read_args_terminal()

# connect to database
conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()

# create database
create_and_init_db()

# open the local repository
repo = git.Repo(local_repo_path)

# if you want to limit the number of commits for analysing, you can specify the value
commits = islice(Repository(local_repo_path).traverse_commits(), 5000)

# otherwise use this command
# commits = Repository(local_repo_path).traverse_commits()



def get_commit_shas():
    repo = git.Repo(local_repo_path)
    n = 5000

    # get the list of all commit SHAs in the master branch
    commit_shas = [commit.hexsha for commit in repo.iter_commits('master')]

    if len(commit_shas) >= n:
        # Get the nth commit SHA
        nth_commit_sha = commit_shas[-n]
    else:
        print(f"The repository has fewer than {n} commits.")
        nth_commit_sha = None


    # get the first and last commit SHAs
    # first commit is the last and last commit is the first item in the list
    first_commit_sha = commit_shas[-1]
    last_commit_sha = commit_shas[0]


    return first_commit_sha, last_commit_sha, nth_commit_sha


def cal_code_churn(commit_sha, file_name):
    try:
        metric = CodeChurn(path_to_repo= local_repo_path,
                           from_commit= str(commit_sha),
                           to_commit= str(commit_sha))
        files_count = metric.count()
        return files_count[file_name]

    except:
        print("Nonexistant file", file_name)
        return 0


def update_table_commits():
    counter = 0
    for _commit in commits:
        counter += 1
        for com_element in _commit.modified_files:
            if com_element.change_type.name == "RENAME":
                cursor.execute('UPDATE commits SET file_name = "s%s" WHERE file_name = "s%s";' %(com_element.new_path, com_element.old_path))
            else:
                if com_element.new_path is not None:
                    cursor.execute("INSERT INTO commits (sha, date, file_name, author, changes, nloc) VALUES (?,?,?,?,?,?)",
                               (_commit.hash, _commit.committer_date, com_element.new_path, _commit.author.name, cal_code_churn(_commit.hash,com_element.new_path), com_element.nloc))
                else:
                    cursor.execute("INSERT INTO commits (sha, date, file_name, author, changes, nloc) VALUES (?,?,?,?,?,?)",
                               (_commit.hash, _commit.committer_date, com_element.old_path, _commit.author.name, cal_code_churn(_commit.hash,com_element.old_path), com_element.nloc))
            conn.commit()

        #todo: remove this
        if counter % 100 == 0:
            print(counter)


update_table_commits()

# you can specify the range of commits for analysing
def total_code_churn():
    first_commit, last_commit, nth_commit_sha = get_commit_shas()
    metric = CodeChurn(path_to_repo= local_repo_path,
                       from_commit= first_commit,
                       to_commit= nth_commit_sha)
    return metric

# calculates the code churn of files in the given commit
def update_total_code_churn():

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

    # Execute each SQL command
    for command in sql_commands:
        cursor.execute(command)

    # Commit your changes
    conn.commit()

update_total_code_churn()
find_all_files(ROOT_DIRECTORY, gone_authors)
conn.close()




