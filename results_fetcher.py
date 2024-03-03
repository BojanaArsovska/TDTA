import sqlite3
import pandas as pd

def get_data_from_db(cursor):
    # Execute the first query
    cursor.execute("SELECT author, file_name, SUM(changes) AS SCORE, COUNT(author) AS COUNT FROM commits GROUP BY author, file_name ORDER BY SUM(changes) DESC")
    result1_1 = cursor.fetchall()

# COUNT(*) AS COMMIT_COUNT third column, counts the
    # number of commits for each file_name. The author column
    # has been removed because it cannot be included without
    # also grouping by author or using it within an aggregate
    # function. This query will provide a list of files, the total
    # score of changes for each file, and the total count of commits made
    # to each file, grouped by file_name and ordered by the total score of changes (SCORE) in descending order.
    cursor.execute("SELECT file_name, SUM(ABS(changes)) AS SCORE, COUNT(author) AS COUNT FROM commits GROUP BY file_name ORDER BY SUM(changes) DESC")
    result1_2 = cursor.fetchall()
    # Convert result1 to dataframe for better view
    df1_1 = pd.DataFrame(result1_1, columns=['Author', 'File', 'Number of Edits by <Author>', 'Number of Commits by <Author> which include <File>'])
    df1_2 = pd.DataFrame(result1_2, columns=['File Name', 'Code Churn - Total number of lines added/deleted/edited', 'Author Edits/Commits with the file '])

    # Execute the second query
    cursor.execute("""SELECT * FROM file_legacy_complexity 
                 ORDER BY legacy_percentage AND cog_complexity DESC;""")
    result2 = cursor.fetchall()

    # Convert result2 to dataframe for better view
    df2 = pd.DataFrame(result2, columns=['ID', 'File Name', 'Author', 'Contribution', 'Cognitive Complexity'] )

    # Save the results into CSV files
    df1_1.to_csv('Table 1.1: Individual Authors Contribution to a File.csv', index=False)
    df1_2.to_csv('Table 1.2: Total Contribution to a File.csv', index=False)
    df2.to_csv('Table 2: Legacy and Cognitive Complexity of File.csv', index=False)

    print("\nTable 1.1: Individual Author's Contribution to a File\n",df1_1)
    print("\nTable 1.2: Total Contribution to a File\n",df1_2)
    print("\nTable 2: Legacy and Cognitive Complexity of File\n",df2)
