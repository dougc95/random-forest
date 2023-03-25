# Import necessary packages
from mlxtend.data import loadlocal_mnist
import pandas as pd 
import pyodbc 

def emnist_to_sql():
    # Connect to SQL Server database
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=host.docker.internal,1433;'
                      'Database=Emnist;'
                      'UID=mysql;'
                      'PWD=andres123;')

    # Define cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a list of column names for the MNIST dataset
    cols = []
    for i in range(784):
        cols.append(f'a{i}')

    # Load MNIST test dataset
    x_train, y_train = loadlocal_mnist(
        images_path='dataset/emnist-byclass-test-images-idx3-ubyte', 
        labels_path='dataset/emnist-byclass-test-labels-idx1-ubyte')

    # Create pandas DataFrame with pixel values as columns and label values as a separate column
    train = pd.DataFrame(x_train, columns=cols)
    train['a784'] = pd.DataFrame(y_train)

    # Add label column to list of column names
    cols.append('a784')

    # Define helper function to convert list of strings to comma-separated string
    def listString(lt):
        st = ""
        for i in lt: 
            st += i + ','

        st = st[:-1]
        return st

    # Convert list of column names to comma-separated string and print it
    columns = listString(cols)
    print(columns)

    # Loop over each row in the DataFrame and insert values into SQL Server database using SQL INSERT statements
    for i in range(train.shape[0]):
        # Convert row values to comma-separated string
        inner = listString(map(str, train.loc[i]))    
        # Execute SQL INSERT statement with row values
        cursor.execute(f'''
                        INSERT INTO Test ({columns}) 
                        VALUES ({inner}) ;
                    ''')
        # Print progress
        print(f'column {i}')
        # Commit changes to database
        conn.commit()