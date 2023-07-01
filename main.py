from itertools import islice
import sys
import git
from datetime import datetime
from create_sql_db import *
# from renamed_files import *
from pydriller import *
from pydriller.metrics.process.code_churn import CodeChurn
import read_args_terminal
import calc_gone_author_contributions as calc_gone_author_contributions
import subprocess
import os

# TODO: REMOVE THIS IF EVERYTHING WORKS
# clonning the directory
# repo_url = "https://github.com/jenkinsci/jenkins.git"
# repo = git.Repo.clone_from(repo_url, "jenkins")

ROOT_DIRECTORY = (subprocess.run('pwd', shell=True, capture_output=True, text=True)).stdout
local_repo_path, gone_authors = read_args_terminal.read_args_terminal()

# connect to database
conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()

# create database
# create_and_init_db()

# open the local repository
repo = git.Repo(local_repo_path)
# commits = islice(Repository(local_repo_path).traverse_commits(),3000)

# THIS COULD BE A FORMAT PROBLEM
commits = Repository(local_repo_path).traverse_commits()
# not_found_files = list()



def cal_code_churn(commit_sha, file_name):
    try:
        metric = CodeChurn(path_to_repo= local_repo_path,
                           from_commit= str(commit_sha),
                           to_commit= str(commit_sha))

        files_count = metric.count()
        return files_count[file_name]
    except:
        print(file_name)
        return 0


def update_table_commits():
    for _commit in commits:
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

            # print(cal_code_churn(_commit.hash,com_element.new_path))

# update_table_commits()

def total_code_churn():
    metric = CodeChurn(path_to_repo= local_repo_path,
                       from_commit= '8a0dc230f44e84e5a7f7920cf9a31f09a54999ac',
                       to_commit='c330c7a50ad00925e257dd7cdab3c75e95660f0d')

    files_count = metric.count()
    return metric

# calculates the code churn of files in the given commit
def update_total_code_churn():
    # file_churns = total_code_churn()
    file_churns = total_code_churn().count()
    # files_renamed = total_code_churn().filepath
    # print(file_churns)

    for file in file_churns:
        try:
            cursor.execute('UPDATE file_author_contrib SET total_churn_tool = %s WHERE file_name = "s%s";' %(int(file_churns[file]), file))
            print((file_churns[file], file))
            conn.commit()
        except sqlite3.Error as error:
            print("Error message: {}".format(error))
            # not_found_files.append(file)
            # print(file)

# update_total_code_churn()

calc_gone_author_contributions.find_all_files(ROOT_DIRECTORY, gone_authors)
conn.close()




