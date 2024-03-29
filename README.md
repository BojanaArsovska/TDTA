

# How to run the tool
1. Clone this repository in your home directory (on MacOS)
2. Open a terminal window and navigate to the cloned repository
3. Then use the example below to run the tool.
4. In the same directory, if you wish to, you can make a txt file that contains a list of git account names of authors, that have left the company, separated by a new line. This means that the tool will analyse the specified repository and only calculate the legacy and congnitive complexity for file that have been edited by one or more authors that have been specified in your txt file.

```bash
python3 main.py -g  <link to a repository you want to analyse> 
```
Alternatively, run the command with the -fd flag
```bash
python3 main.py -g  <link to a repository you want to analyse> -fd <txt file>
```

Sample
```bash
python3 main.py -g  https://github.com/jenkinsci/jenkins.git -fd gone_authors.txt
```


# How to install all the required libraries:
To install all the required libraries such as SQL, PMD and PyDriller, simply run the following command in your terminal:
```bash
pip3 install -r requirements.txt
```


# How to obtain the results
1. The result are saved in results1.csv and result2.csv
   - In results1.csv, you will find Table 1 which shows the authors contribution of file they have edited. Meaning, it shows how many edits a author - "Author" had done on THAT file in the "Number of Edits". The "Author Edits/Commits on the file" shows how many times THAT author has edited the file in column "File Name".
   - In results2.csv you will find the values for legacy and cognitive complexity of each file by the specified contributors. "Legacy" means owneship percentage that the author has over a file.


# PMD and PyDriller Installation Guide

This document guides you through the installation of PMD, PyDriller, and some necessary Python modules, along with an explanation of the database tables created by the tool.

## Prerequisites

Before you can install PMD, PyDriller, and other Python modules, make sure your system has:

1. **Java:** PMD requires Java to run. If you haven't installed it yet, you can download and install the latest version of Java from the official Oracle website.
2. **Python3 and pip:** PyDriller and other modules are Python libraries and can be installed via pip. Make sure you have both Python3 and pip installed on your system.
3. **Git:** Git may be installed on MacOS and Linux by running `sudo apt install git`.

## Installing PMD

PMD is an open-source static source code analyzer. Follow these steps to install it:

1. Download and unzip the PMD 'pmd-dist-<latest_version>-bin.zip' file from the official [PMD GitHub Releases page](https://github.com/pmd/pmd/releases).
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
   - Run `nano ~/.bashrc` for Linux
   - For Mac, open your shell's start-up file (.zshrc, .bashrc, .profile, etc). Which start-up file to choose depends on the shell envrionment that you are using. For instance, in Z Shell (zsh) you would run the command `nano ~/.zshrc`, in Bash, `nano ~/.bash_profile`. 
   - Add the line `export PATH=$PATH:/path-to-pmd-bin-directory` to the end of the file.
   - Save your changes and close the file.
   - Enter the command `source ~/.your_start-up_file` to refresh the profile (and to load your new path variable).
4. Verify your installation by running `pmd` in your command prompt or terminal. If PMD is correctly installed, this will not return an error.

Important to note: Make sure you add PMD in the correct start-up file, otherwise it will not be added to the path once you restart your shell.

## Installing PyDriller

PyDriller is a Python framework for mining software repositories. To install it, follow these steps:

1. Open your terminal and run the following command:

   ```bash
   pip install PyDriller
   ```
   
   You can verify the installation by running a Python script with the following line:

   ```python
   import pydriller
   ```
   
   If PyDriller is correctly installed, this will not return an error.



### Explanation of the Database Tables Used

The tool creates several tables in the database to store data related to the analyzed repositories. Below is an explanation of each table and its columns:



### commits



| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key |
| sha | TEXT | The commit SHA |
| date | TIMESTAMP | The commit date |
| file_name | TEXT | The file's name |
| author | TEXT | The commit's author |
| changes | INT | The changes made in the commit (lines added or removed) |
| nloc | INT | The number of lines of code in the file |

Stores a row for each file name in a single commit. 


### file_author_contrib



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

Stores the contributions of each author to each file.


### file_legacy_complexity

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key |
| file_name | TEXT | The file's name |
| legacy_percentage | FLOAT | The percentage of the file's code considered as legacy code |
| cog_complexity | FLOAT | The file's cognitive complexity |


Stores the percentage of legacy code for each file.

### author_contrib



| Column | Type | Description |
| --- | --- | --- |
| author | TEXT | The author's name |
| sum(file_size_x_percentages) | FLOAT | The sum of the product of the file size and the author's percentage contribution for all files |
| all_files | FLOAT | The sum of sizes of each file that the author contributed to |

Stores the association of an author with all the files they have contributed to in the repository.
The corresponding SQL queries to create and update these tables are available in main.py .

### Important

Remember to replace `/path-to-pmd-bin-directory` with the actual path to your PMD bin directory.

WARNING: This tool only analyses the commits done on a branch that is locally cloned with the repository. If you'd like to analyse multiple branches, you must clone them locally as well.
