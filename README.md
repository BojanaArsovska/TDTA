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



Sure, here is how the information can be added to the document.

```markdown
## Database Tables for the Tool

The tool creates the following tables in the database:

### Commits

This table contains a row for each `file_name` in a single commit. By default, total churn is calculated as added lines - deleted lines, hence it can sometimes be negative. 

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key for the table |
| sha | TEXT | The commit SHA |
| date | TIMESTAMP | The date of the commit |
| file_name | TEXT | The name of the file |
| author | TEXT | The author of the commit |
| changes | INT | The changes made in the commit (number of lines added or deleted) |
| nloc | INT | Number of lines of code in the file |

For each file in a commit in the repo, an entry in the table is created. This entry stores the file name and the commit specifications (sha, date, author), as well as file edits in that commit: lines added/removed. Moreover, it stores the number of lines of code in the file.

### File_author_contrib

This table stores the contributions of each author in this file.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key for the table |
| file_name | TEXT | The name of the file |
| author | TEXT | The author of the commit |
| auth_churn | INT | The number of lines that the author has contributed towards the code churn of this file |
| total_churn | INT | Total lines of code churn in the file |
| file_size | INT | The size of the file |
| file_size_x_percentages | FLOAT | The file size multiplied by the percentage contribution of the author |
| percentages | FLOAT | The percentage of total churn contributed by the author |
| total_churn_tool | FLOAT | Calculated churn by the tool |

The table was created and updated with several SQL queries, which can be found in the original document provided.

### File_legacy_complexity

This table contains all the file names and the amount of legacy code they contain in terms of percentages.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key for the table |
| file_name | TEXT | The name of the file |
| legacy_percentage | FLOAT | The percentage of the file's code that is considered legacy code |
| cog_complexity | FLOAT | Cognitive complexity of the file |

Those percentages have been calculated from the contribution (line of codes written vs all the lines in the file) of the authors that have been specified in the list of gone authors (`gone_authors.txt`).

### Author_contrib

This table contains entries that associate an author to all the files they have made a contribution towards in the repository.

| Column | Type | Description |
| --- | --- | --- |
| author | TEXT | The author of the commit |
| sum(file_size_x_percentages) | FLOAT | The sum of the product of the file size and the author's percentage contribution for all files |
| all_files | FLOAT | The sum of sizes of each file that this author has made a contribution towards |

The table contains entries that associate an author with the sum of percentages of contribution towards each file in the repo. Then in another column, it associates the author with the sum of sizes of each file that this author has made a contribution towards. These two columns are relevant for later on calculating the amount of contribution calc in percentages based on sum(file_size_x_percentages)/sum(file_size). The table was created and updated with several SQL queries, which can be found in the original document provided.
```

You may want to further edit the descriptions of the columns and tables to match your tool's functionality as closely as possible.
