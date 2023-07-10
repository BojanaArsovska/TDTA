import subprocess

# ROOT_DIRECTORY = (subprocess.run('pwd', shell=True, capture_output=True, text=True)).stdout
# print(ROOT_DIRECTORY)

# Define the path to the root directory to search for Java code
def get_cognitive_complexities(filepath, root_directory):
    # counter used for the average
    # total_file_complexity is 0 if it's below the given threshold in the frame
    counter = 0
    total_file_complexity = 0

    # Calculate the cognitive complexity of the Java file
    cmd = 'PATH=$PATH:$HOME/pmd-bin-7.0.0-rc1/bin/; pmd check -f text -R $HOME/TDtool/cogcomp.xml -d ' + str(root_directory + filepath)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # total_file_complexity = Sum (complexities of all methods in a file) / num od methods
    # '' == result.stdout when the tool cannot find the complexity it give a result one of the 3
    if ' ' != result.stdout and '' != result.stdout and None != result.stdout:
        output = result.stdout
        output = output.splitlines()
        for line in output:
            counter += 1
            method_complexity = line[(line.index(' of ') + 4) : (line.index(' of ') + 6) ]
            method_complexity = ''.join(filter(str.isdigit, method_complexity))
            total_file_complexity += int(method_complexity)
    else:
        total_file_complexity = 0
    if counter is not 0:
        return total_file_complexity/counter
    else:
        return total_file_complexity
#
#
# get_cognitive_complexities("/Users/bojanaarsovska/TDtool/jenkins", "core/src/main/resources/hudson/maven/MavenModuleSet/configure-entries.jelly")
