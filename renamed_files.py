import git


# Iterate through the commits
def check_if_renamed(commit):
    # Check if the commit has any file renames
    if commit.stats.renames:
        print("Commit:", commit)
        # Iterate through the file renames in the commit
        for item in commit.stats.renames.items():
            old_file_name = item[0]
            new_file_name = item[1]
            similarity = item[2]
            print("File renamed from:", old_file_name)
            print("File renamed to:", new_file_name)
            print("Similarity:", similarity)
