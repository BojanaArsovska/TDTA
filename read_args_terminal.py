import argparse
import re
import subprocess
import os


def clone_git_repo(git_link):
    try:
        # The command line command to clone the git repository
        command = f'git clone {git_link}'
        subprocess.check_call(command, shell=True)
        print(f'Git repository {git_link} cloned successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error: {str(e)}')

def extract_names_from_txt(txt_path):
    with open(txt_path, 'r') as file:
        data = file.read()

    # This pattern assumes names are capitalized and consist of two words
    pattern = r'[A-Z][a-z]+ [A-Z][a-z]+'
    names = re.findall(pattern, data)

    return names

def get_cloned_dir_abs_path(git_link):
    # Extract repository name from the git link
    repo_name = git_link.split('/')[-1].split('.git')[0]

    # Get absolute path of the cloned directory
    abs_path = os.path.join(os.getcwd(), repo_name)

    return abs_path


def parsing_dir_name_through_args(args):

    # Get the current working directory
    current_dir = os.getcwd()

    # URL of the repo
    repo_url = args.git
    #todo take the param that fetches the arguments

    # Get the name of the repo from the URL
    repo_name = repo_url.split("/")[-1].split(".")[0]

    # Construct the full path to the cloned repo
    repo_dir = os.path.join(current_dir, repo_name)
    return repo_name


def read_args_terminal():
    parser = argparse.ArgumentParser(description='Process link to a repository and a txt file of ex employee authors (Name Surname).')
    parser.add_argument('-g', '--git', type=str, help='Link to the git repository.')
    parser.add_argument('-fd', '--txt', type=str, help='Path to the former_developers.txt file.')

    args = parser.parse_args()
    cloned_dir_name = parsing_dir_name_through_args(args)

    # Change directory to script's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Clone the git repository
    clone_git_repo(args.git)

    # Get the absolute path of the cloned directory
    cloned_dir_abs_path = get_cloned_dir_abs_path(args.git)
    print(f'Cloned directory absolute path: {cloned_dir_abs_path}')

    if args.txt is None:
        gone_authors = None
    else:
        abs_txt_path = os.path.abspath(args.txt)
        gone_authors = extract_names_from_txt(abs_txt_path)

    return cloned_dir_abs_path, gone_authors, cloned_dir_name

