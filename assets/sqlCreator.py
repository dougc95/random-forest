import pyodbc 
# Importing the pyodbc module for database connectivity
def create_table():
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=host.docker.internal,1433;'
                      'Database=Emnist;'
                      'UID=mysql;'
                      'PWD=andres123;')
    # Establishing a connection to the SQL Server database named 'Emnist' on the server 'DESKTOP-IHIVVUV' using a trusted connection

    cursor = conn.cursor()
    # Creating a cursor object that will be used to execute SQL commands on the database

    cursor.execute("CREATE TABLE Test ( a0 int )")
    # Creating a new table named 'Letters_Test' in the 'Emnist' database with a single column named 'a0' of data type `int`.

    conn.commit()
    # Committing the changes made to the database

    for i in range(1,785):
        cursor.execute(f'''
                        ALTER TABLE Test
                        ADD a{i} int;
                    ''')
        # Creating 784 more columns in the 'Letters_Test' table using a loop. 
        # Using the ALTER TABLE command to add a new column to the table for each iteration of the loop, 
        # with column names 'a1' through 'a784'.
        # Using a formatted string to include the column number in the ALTER TABLE statement
        conn.commit()
        # Committing the changes made to the database after each iteration of the loop
