import os
import subprocess
from radon.complexity import cc_visit
from radon.cli.tools import iter_filenames

# Define the path to the root directory to search for Java code
ROOT_DIRECTORY = '/Users/bojanaarsovska/TDtool/jenkins/'

# Loop through all directories and subdirectories
def get_congnitive_complexities(filepath):
    total_file_complexity = 0
    method_complexity = 0

    # Calculate the cyclomatic complexity of the Java file
    cmd = 'PATH=$PATH:$HOME/pmd-bin-7.0.0-rc1/bin/; pmd check -f text -R $HOME/TDtool/cogcomp.xml -d ' + str(ROOT_DIRECTORY+filepath)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # '' == result.stdout when the tool cannot find the complexity
    if '' != result.stdout:
        total_file_complexity = 0
        output = result.stdout
        output = output.splitlines()
        for line in output:
            method_complexity = line[(line.index(' of ') + 4) : (line.index(' of ') + 6) ]
            method_complexity = ''.join(filter(str.isdigit, method_complexity))
            total_file_complexity += int(method_complexity)
    return total_file_complexity
