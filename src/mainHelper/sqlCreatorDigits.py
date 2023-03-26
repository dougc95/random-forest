import pyodbc 

# Connect to the database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IHIVVUV;'
                      'Database=Emnist;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# Create a Table
cursor.execute("CREATE TABLE Digits ( a0 int )")
conn.commit()

# Add columns to the table
for i in range(1,785):
    cursor.execute(f'''
                    ALTER TABLE Digits
                    ADD a{i} int;

                ''')
    print(f'column {i}')
    conn.commit()