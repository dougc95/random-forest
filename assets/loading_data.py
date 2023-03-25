# Import necessary libraries
import sys
sys.path.append("../")  # Add parent directory to module search path

import pyodbc  # Python module for connecting to SQL Server databases

import pandas as pd  # Data manipulation library
import numpy as np  # Numerical computing library
import matplotlib.pyplot as plt  # Plotting library

import helpers  # Custom helper module

# Connect to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IHIVVUV;'
                      'Database=Emnist;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Read data from SQL Server database
def gatherData():
    train = pd.read_sql_query('SELECT * FROM Classes', conn)  # Read training set from 'Classes' table
    test = pd.read_sql_query('SELECT * FROM TestV', conn)  # Read test set from 'TestV' table
    data = pd.concat([train, test])  # Combine training and test sets

    return data

data = helpers.Loader().run(gatherData, 'Reading Database')  # Load data using custom helper function

# Separate digits from letters
letters = data[data['a784']>=10]  # Select rows where label >= 10 (letters)
digits = data[data['a784']<10]  # Select rows where label < 10 (digits)

# Get matrix and labels for digits and letters
x_letters = np.array(letters.iloc[:,:-1])  # Features (pixels) for letters
y_letters = np.array(letters.iloc[:,-1])  # Labels (letters) for letters

x_digits = np.array(digits.iloc[:,:-1])  # Features (pixels) for digits
y_digits = np.array(digits.iloc[:,-1])  # Labels (digits) for digits

# Create column names for database table
cols = []
builder = helpers.StringBuilder()  # Custom string builder for creating comma-separated lists of values

for i in range(784):
    cols.append(f'a{i}')
cols.append('a784')  # Add label column name
columns = builder.listString(cols)  # Convert list of column names to comma-separated string

# Initialize progress bar
bar = helpers.ProgressBar()

# Insert digit data into 'Digits' table in database
digits_size = digits.shape[0]  # Get number of rows in digit dataset
print('Saving Digits...')
bar.printProgressBar(0, digits_size, prefix = 'Progress:', suffix = 'Complete', length = 50)  # Print progress bar
for i in range(digits_size):
    zero = x_digits[i].reshape((28,28))  # Reshape flattened image to 28x28 matrix
    rotated = np.flip(list(zip(*zero[::-1])), 1)  # Rotate image by flipping vertically and horizontally
    rotated = rotated.flatten().tolist()  # Flatten rotated image and convert to list
    rotated.append(y_digits[i])  # Add label to end of list

    inner = builder.listString(map(str, rotated))  # Convert list of values to comma-separated string
    cursor.execute(f'''
                    INSERT INTO Digits ({columns})  # Insert values into 'Digits' table
                    VALUES ({inner}) ;
                ''')
    bar.printProgressBar(i + 1, digits_size, prefix = 'Progress:', suffix = 'Complete', length = 50)  # Update progress bar
    conn.commit()  # Commit changes to database

# Insert letter data into 'Letters' table in database
letters_size = letters.shape[0]  # Get number of rows in letter
