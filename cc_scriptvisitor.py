from mccabe import get_code_complexity

# Set the path to the Java file
file_path = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/jenkins/model/Jenkins.java"

# Read the file and extract the code
with open(file_path, "r") as f:
    code = f.read()

# Calculate the cyclomatic complexity of the code
complexity = get_code_complexity(code)

print(f"The cyclomatic complexity of {file_path} is {complexity}.")



# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/model/FreeStyleBuild.java"
# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/jenkins/model/Jenkins.java"
# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/tasks/Maven.java"
