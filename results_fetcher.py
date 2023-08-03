import sqlite3
import pandas as pd

def get_data_from_db(cursor):
    # Execute the first query
    cursor.execute("SELECT author, file_name, SUM(changes) AS SCORE, COUNT(author) AS COUNT FROM commits GROUP BY author, file_name ORDER BY SUM(changes) DESC")
    result1 = cursor.fetchall()

    # Convert result1 to dataframe for better view
    df1 = pd.DataFrame(result1, columns=['Author', 'File Name', 'Number of Edits', 'Author Edits/Commits on the file '])

    # Execute the second query
    cursor.execute("""SELECT * FROM file_legacy_complexity 
                 ORDER BY legacy_percentage AND cog_complexity DESC;""")
    result2 = cursor.fetchall()

    # Convert result2 to dataframe for better view
    df2 = pd.DataFrame(result2, columns=['ID', 'File Name', 'Author', 'Legacy', 'Cognitive Complexity'] )

    # Save the results into CSV files
    df1.to_csv('table1.csv', index=False)
    df2.to_csv('table2.csv', index=False)

    print("\nTable 1: Authors Contribution per File\n",df1)
    print("\nTable 2: Legacy and Cognitive Complexity of Each File\n",df2)
