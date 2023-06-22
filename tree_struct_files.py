def create_tree(file_path):
    parts = file_path.split("/")
    return {parts[-1]: create_tree_recursive(parts[:-1])} if parts else {}

def create_tree_recursive(parts):
    if not parts:
        return {}
    return {parts[-1]: create_tree_recursive(parts[:-1])}

files = ['/home/user/documents/report.txt', '/home/user/music/song.mp3', '/home/user/images/picture.jpg']
tree = {}
for file in files:
    parts = file.split("/")
    d = tree
    for part in parts[1:]:
        if part not in d:
            d[part] = {}
        d = d[part]
print(tree)
