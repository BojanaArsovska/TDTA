Sure! Here is the updated version of the documentation including instructions to install the PyDriller library:

```markdown
# Installing PMD and PyDriller

PMD is an open-source, cross-platform static source code analyzer for Java, JavaScript, PLSQL, XML, and more. PyDriller is a Python framework that helps in the analysis of Git repositories. Here's a quick guide to help you install both PMD and PyDriller on your system.

## Prerequisites

Before you can install PMD and PyDriller, make sure your system has:

1. Java: PMD requires Java to run. If you haven't installed it yet, you can download and install the latest version of Java from the official Oracle website.
2. Python and pip: PyDriller is a Python library, and it can be installed via pip. Make sure you have both Python and pip installed on your system.

## Steps to Install PMD

### 1. Download PMD

The first step to installing PMD is to download the software. You can do this by visiting the [official PMD GitHub page](https://github.com/pmd/pmd) and navigating to the "Releases" tab. 

Here, choose the most recent release and download the .zip or .tar.gz file, depending on your preference.

### 2. Extract the Downloaded File

Once you have the PMD file, extract it to a directory of your choice on your system.

- For Windows users, you can use software like WinZip or WinRAR.
- For Linux and macOS users, you can use the command `tar -xvf [filename]` to extract the .tar.gz file in the terminal.

### 3. Set Up PMD Path

You'll need to add PMD to your system's PATH to run it from any directory. 

For Windows:

1. Search for "Environment Variables" in the system settings.
2. In the system properties window that appears, click on the "Environment Variables" button.
3. In the "System Variables" section, find the PATH variable and click on "Edit".
4. In the edit window, click "New" and add the path to the `bin` directory of your PMD installation.

For Linux/macOS:

Open your terminal and add the following line to your `.bashrc` or `.zshrc` file:

```bash
export PATH=$PATH:/path/to/your/pmd/bin
```
Replace `/path/to/your/pmd/bin` with the actual path to the `bin` directory of your PMD installation. After that, source your `.bashrc` or `.zshrc` file:

```bash
source ~/.bashrc   # If you use bash
source ~/.zshrc    # If you use zsh
```
### 4. Verify the Installation

You can verify if PMD is installed correctly by running the following command in your terminal:

```bash
pmd -version
```
If PMD is correctly installed, this command will output the installed version of PMD.

## Steps to Install PyDriller

1. Go to the [PyDriller page on PyPI](https://pypi.org/project/PyDriller/).
2. Make sure you’re on a page with the latest version.
3. Open your terminal and run the following command:

```bash
pip install PyDriller
```
You can verify the installation by running a Python script with the following line:

```python
import pydriller
```
If PyDriller is correctly installed, this will not return an error.

## PMD Plugins for IDEs

PMD has plugins available for various IDEs like Eclipse, IntelliJ IDEA, NetBeans, etc., which allow you to easily use PMD within the IDE itself. You can find these plugins and their installation guides in the [official PMD documentation](https://pmd.github.io/latest/pmd_userdocs_tools.html). 

Now, you're all set to use PMD and PyDriller for code analysis!
```
Remember to replace the placeholders like `/path/to/your/pmd/bin` with the actual paths on your system.
