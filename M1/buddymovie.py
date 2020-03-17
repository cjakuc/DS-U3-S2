import pandas as pd
import os
import sqlite3

df = pd.read_csv('https://github.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/raw/master/module1-introduction-to-sql/buddymove_holidayiq.csv')

# Save the filepath for the DB to a variable
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.sqlite3")

# Intanstiate the connection
connection = sqlite3.connect(DB_FILEPATH)

# Instantiate the cursor
cursor = connection.cursor()

df.to_sql('review',con=connection, if_exists='replace')

# Count how many rows there are - should be 249
count_query = """
SELECT
    count('User ID') as row_count
FROM
    review
"""

count_result = cursor.execute(count_query).fetchone()
print(f"There are {count_result[0]} rows")

# How many users who reviewd at least 100 Nature in the category also 
# reviewed at least 100 in the shopping category?
query2 = """
SELECT
    count('User ID') as user_count
WHERE
    'Nature' >= 100
AND 'Shopping' >= 100;
"""

query2_result = cursor.execute(query2).fetchone()
print(f"There are {query2_result[0]} users who reviewed at least 100 Nature and 100 Shopping")