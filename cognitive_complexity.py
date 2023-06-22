import os
import subprocess
from radon.complexity import cc_visit
from radon.cli.tools import iter_filenames

# Define the path to the root directory to search for Java code
ROOT_DIRECTORY = '/Users/bojanaarsovska/TDtool/jenkins'

# Loop through all directories and subdirectories
def get_congnitive_complexities():
    total_file_complexity = 0
    method_complexity = 0
    file = ''

    for dirpath, dirnames, filenames in os.walk(ROOT_DIRECTORY):
        for file in filenames:
            if file.endswith('.java'):
                # Calculate the cyclomatic complexity of the Java file
                filepath = os.path.join(dirpath, file)
                cmd = 'PATH=$PATH:$HOME/pmd-bin-7.0.0-rc1/bin/; pmd check -f text -R $HOME/TDtool/cogcomp.xml -d ' + str(filepath)
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                if '' != result.stdout:
                    total_file_complexity = 0
                    print(filepath)
                    output = result.stdout
                    print(output)
                    output = output.splitlines()
                    for line in output:
                        method_complexity = line[(line.index(' of ') + 4) : (line.index(' of ') + 6) ]
                        method_complexity = ''.join(filter(str.isdigit, method_complexity))
                        total_file_complexity += int(method_complexity)
                    print(total_file_complexity)
                    print()
    return file, total_file_complexity

print(get_congnitive_complexities())

                # print(result.stdout)
                # print(result.stderr)
                # if (hi == 10):
                #     exit(0)

# result = subprocess.run('alias pmd="$HOME/pmd-bin-7.0.0-rc1/bin/pmd"', shell=True, check=True, capture_output=True, text=True)
# print(result)

# print(subprocess.run('echo $PATH', shell=True, check=True, capture_output=True, text=True))
# print(subprocess.run('PATH=$PATH:$HOME/pmd-bin-7.0.0-rc1/bin/; echo $PATH; pmd --help', shell=True, check=False, capture_output=True, text=True))
# print(subprocess.run('echo $PATH', shell=True, check=True, capture_output=True, text=True))
# cmd = 'pmd check -f text -R category/java/design.xml/CognitiveComplexity -d /Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/tasks/LogRotator.java'
# result = (subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True))
# print(result)

# print(subprocess.run('ls', shell=True, capture_output=True, text=True).stdout)
#
# from mccabe import ScriptVisitor
#
# # Set the path to the Java file
# file_path = "/path/to/java/file.java"
#
# # Read the file and extract the code
# with open(file_path, "r") as f:
#     code = f.read()
#
# # Initialize a new ScriptVisitor object
# visitor = ScriptVisitor()
#
# # Parse the code and calculate the cyclomatic complexity
# visitor.preorder_parse(code)
# complexity = visitor.complexity()
#
# print(f"The cyclomatic complexity of {file_path} is {complexity}.")
