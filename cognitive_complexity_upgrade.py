import subprocess

# Define the path to the root directory to search for Java code
def get_cognitive_complexities(filepath, root_directory, ROOT_DIRECTORY):
    # counter used for the average
    # total_file_complexity is 0 if it's below the given threshold in the frame
    counter = 0
    total_file_complexity = 0

    # Calculate the cognitive complexity of the Java file
    # Don't forget to write in your thesis how much time parsing this and cutting it and combining it with different sources took.

    cmd = 'PATH=$PATH:$HOME/pmd-bin-7.0.0-rc1/bin/; pmd check -f text -R ' + str(ROOT_DIRECTORY) + '/cogcomp.xml -d ' + str(root_directory + filepath)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # total_file_complexity = Sum (complexities of all methods in a file) / num od methods
    # '' == result.stdout when the tool cannot find the complexity it gives a result one of the 3

    if ' ' != result.stdout and '' != result.stdout and None != result.stdout:
        output = result.stdout
        output = output.splitlines()
        for line in output:
            try:
                # Check if ' of ' is in the line and proceed if it is
                if ' of ' in line:
                    complexity_start_index = line.index(' of ') + 4  # Start index of complexity
                    complexity_end_index = line.find(' ', complexity_start_index)  # End index of complexity
                    if complexity_end_index == -1:  # If no space is found, assume end of line
                        complexity_end_index = len(line)
                    method_complexity = line[complexity_start_index:complexity_end_index]
                    method_complexity = ''.join(filter(str.isdigit, method_complexity))
                    total_file_complexity += int(method_complexity)
                    counter += 1
            except ValueError as e:
                # Handle the exception if ' of ' is not found or any other ValueError
                print(f"An error occurred while processing the line: {line}")
                print(f"Error details: {e}")

    else:
        total_file_complexity = 0

    # print(result)
    if counter is not 0:
        return total_file_complexity/counter
    else:
        return total_file_complexity


