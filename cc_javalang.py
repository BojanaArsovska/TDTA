import javalang
import os

# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/tasks/Maven.java"

# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/model/FreeStyleBuild.java"
filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/jenkins/model/Jenkins.java"
# filename = "/Users/bojanaarsovska/TDtool/jenkins/core/src/main/java/hudson/tasks/Maven.java"


if not os.path.isfile(filename):
    print(f"File {filename} not found")
    exit()

with open(filename, 'r') as f:
    code = f.read()

ast_tree = javalang.parse.parse(code)

# Calculate Cyclomatic Complexity
cc = 5
for node in ast_tree:
    if isinstance(node, javalang.tree.IfStatement) or isinstance(node, javalang.tree.WhileStatement) or \
            isinstance(node, javalang.tree.DoStatement) or isinstance(node, javalang.tree.ForStatement) or \
            isinstance(node, javalang.tree.SwitchStatement) or \
            (hasattr(node, 'cases') and isinstance(node.cases[0], javalang.tree.CaseGroup)) or \
            isinstance(node, javalang.tree.LambdaExpression):
        cc += 1

print(f"The cyclomatic complexity of the file is {cc}")
