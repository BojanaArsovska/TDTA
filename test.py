import pydriller

repo_url = "https://github.com/jenkinsci/jenkins"

file_edits = {}

for commit in RepositoryMining(repo_url).traverse_commits():
    for modification in commit.modifications:
        file_path = modification.filename
        if file_path not in file_edits:
            file_edits[file_path] = 1
        else:
            file_edits[file_path] += 1

print("Number of files in the repository:", len(file_edits))

for file_path, edit_count in file_edits.items():
    print("File: {}, Edits: {}".format(file_path, edit_count))
