```markdown

# How to run the tool
1. CLone this directory
2. Open a terminal window and navigate to the cloned repository
3. Make a txt file that contains a list of names and surnames of gone authors, no comma separation
3. Run the following command in the terminal:
   ``` bash
   python3 main.py -g  <link to a repository you want to analyse> -t <txt file>
   ```
> command
   

# PMD and PyDriller Installation Guide

This document guides you through the installation of PMD, PyDriller, and some necessary Python modules, along with an explanation of the database tables created by the tool.

## Prerequisites

Before you can install PMD, PyDriller, and other Python modules, make sure your system has:

1. **Java:** PMD requires Java to run. If you haven't installed it yet, you can download and install the latest version of Java from the official Oracle website.
2. **Python and pip:** PyDriller and other modules are Python libraries and can be installed via pip. Make sure you have both Python and pip installed on your system.

## Installing PMD

PMD is an open-source static source code analyzer. Follow these steps to install it:

1. Download the latest PMD .zip file from the official [PMD GitHub Releases page](https://github.com/pmd/pmd/releases).
2. Extract the .zip file to your desired location.
3. Add the `bin` directory from the extracted PMD folder to your system's PATH. 
   
   For Windows:
   - Search for 'Environment Variables' in your system search.
   - Click on 'Edit the system environment variables'.
   - In the System Properties window that opens, click on 'Environment Variables'.
   - In the Environment Variables window, under System Variables, scroll until you find 'Path' and select it.
   - Click on 'Edit'.
   - In the Edit Environment Variable window, click on 'New' and paste the path of the `bin` folder.
   - Click 'OK' on all windows to save the changes.
   
   For macOS/Linux:
   - Open Terminal.
   - Open the bash profile with the command `nano ~/.bash_profile` for Mac or `nano ~/.bashrc` for Linux.
   - Add the line `export PATH=$PATH:/path-to-pmd-bin-directory` to the end of the file.
   - Save and close the file (Ctrl+X, then Y, then Enter).
   - Enter the command `source ~/.bash_profile` for Mac or `source ~/.bashrc` for Linux to refresh the profile.
4. Verify your installation by running `pmd` in your command prompt or terminal. If PMD is correctly installed, this will not return an error.

## Installing PyDriller

PyDriller is a Python framework for mining software repositories. To install it, follow these steps:

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

## Database Tables for the Tool

The tool creates several tables in the database to store data related to the analyzed repositories. Below is an explanation of each table and its columns:

### commits

Stores a row for each file name in a single commit. 

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key |
| sha | TEXT | The commit SHA |
| date | TIMESTAMP | The commit date |
| file_name | TEXT | The file's name |
| author | TEXT | The commit's author |
| changes | INT | The changes made in the commit (lines added or removed) |
| nloc | INT | The number of lines of code in the file |

### file_author_contrib

Stores the contributions of each author to each file.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key |
| file_name | TEXT | The file's name |
| author | TEXT | The author's name |
| auth_churn | INT | The number of lines that the author contributed to the file's code churn |
| total_churn | INT | The total lines of code churn in the file |
| file_size | INT | The file's size |
| file_size_x_percentages | FLOAT | The file size multiplied by the percentage contribution of the author |
| percentages | FLOAT | The percentage of total churn contributed by the author |
| total_churn_tool | FLOAT | The calculated churn by the tool |

### file_legacy_complexity

Stores the percentage of legacy code for each file.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key |
| file_name | TEXT | The file's name |
| legacy_percentage | FLOAT | The percentage of the file's code considered as legacy code |
| cog_complexity | FLOAT | The file's cognitive complexity |

### author_contrib

Stores the association of an author with all the files they have contributed to in the repository.

| Column | Type | Description |
| --- | --- | --- |
| author | TEXT | The author's name |
| sum(file_size_x_percentages) | FLOAT | The sum of the product of the file size and the author's percentage contribution for all files |
| all_files | FLOAT | The sum of sizes of each file that the author contributed to |

The corresponding SQL queries to create and update these tables are available in the original document provided.


Remember to replace `/path-to-pmd-bin-directory` with the actual path to your PMD bin directory.

 This tool only analyses the commits done on a branch that is locally cloned with the repository. If you'd like to analyse multiple branches, you must clone them locally.

``` 

```diff
-  WARNING: This tool only analyses the commits done on a branch that is locally cloned with the repository. If you'd like to analyse multiple branches, you must clone them locally.

```



