import pylint.lint
import os
from pylint import epylint as lint

filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/tasks/Maven.java"

if not os.path.isfile(filename):
    print(f"File {filename} not found")
    exit()

# Run pylint and capture the output
(out, _) = lint.py_run(f"{filename} --enable=W --disable=R,C", return_std=True)
output = out.getvalue()

# Extract the Cyclomatic Complexity value from the output
cc = None
for line in output.split("\n"):
    if line.startswith("Cyclomatic complexity:"):
        cc = int(line.split(":")[1].strip())
        break

if cc is None:
    print("Error: Unable to determine Cyclomatic Complexity from pylint output")
else:
    print(f"The Cyclomatic Complexity of the file is {cc}")
