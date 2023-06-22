from sonarqube import SonarQubeClient
url = 'http://localhost:9000'
username = "admin"
password = "admin"
sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)

component = sonar.components.get_project_component_and_ancestors("/Users/bojanaarsovska/TDtool/jenkins")
print(component)
