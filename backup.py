import git
import sqlite3
from datetime import datetime
import sqlite3
from create_sql_db import *

# clonning the directory
# repo_url = "https://github.com/jenkinsci/jenkins.git"
# repo = git.Repo.clone_from(repo_url, "jenkins")

local_repo_path = "/Users/bojanaarsovska/TDtool/jenkins"
repo = git.Repo(local_repo_path)
list_renamed = dict()

# create database
# create_and_init_db()

# connect to database
conn = sqlite3.connect('db_commits_files.db')
cursor = conn.cursor()

# open the local repository
repo = git.Repo(local_repo_path)


# iterate through the commits
for commit in repo.iter_commits():
    # print("Commit:", commit)
    # Iterate through the files in the commit

    for item in commit.stats.files.items():
        file_name = item[0]
        file_changes = item[1]
        # print("File:", file_name)
        # print("Changes:", file_changes)

        diff = commit.diff()
        # print(diff)
        # Iterate through the diffs of the commit

        # print(diff)
        for d in diff:
            if d.renamed:
                print(diff)
                print("Commit:", commit)
                print("File renamed from:", d.a_path)
                print("File renamed to:", d.b_path)
                print("\n")
                # print("commited at: ", commit.committed_date)

        # save commit info to the database
        # cursor.execute("INSERT INTO commits (sha, date, file_name, changes) VALUES (?,?,?,?)",
        #                (commit.hexsha, datetime.fromtimestamp(commit.committed_date), file_name, file_changes))
        conn.commit()

# close connection
conn.close()
