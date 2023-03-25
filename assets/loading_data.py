import sys
sys.path.append("../")

import pyodbc

import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt 
import helpers

# Get the Database connection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IHIVVUV;'
                      'Database=Emnist;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# Read Data
def gatherData():
    train = pd.read_sql_query('SELECT * FROM Classes', conn)
    test = pd.read_sql_query('SELECT * FROM TestV', conn)
    data = pd.concat([train, test])

    return data

data = helpers.Loader().run(gatherData, 'Reading Database')

# Separate Digits from letters
letters = data[data['a784']>=10]
digits = data[data['a784']<10]

# Get matrix and labels
x_letters = np.array(letters.iloc[:,:-1])
y_letters = np.array(letters.iloc[:,-1])

x_digits = np.array(digits.iloc[:,:-1])
y_digits = np.array(digits.iloc[:,-1])

# Create Columns 
cols = []
builder = helpers.StringBuilder() 

for i in range(784):
    cols.append(f'a{i}')

cols.append('a784')
columns = builder.listString(cols)

# Get progress bar
bar = helpers.ProgressBar()

# Set Digits 
digits_size = digits.shape[0]
print('Saving Digits...')
bar.printProgressBar(0, digits_size, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i in range(digits_size):
    zero = x_digits[i].reshape((28,28))
    rotated = np.flip(list(zip(*zero[::-1])), 1)
    rotated = rotated.flatten().tolist()
    rotated.append(y_digits[i])

    inner = builder.listString(map(str, rotated))
    cursor.execute(f'''
                    INSERT INTO Digits ({columns}) 
                    VALUES ({inner}) ;
                ''')
    bar.printProgressBar(i + 1, digits_size, prefix = 'Progress:', suffix = 'Complete', length = 50)
    conn.commit()


# Set Letters 
letters_size = letters.shape[0]
print('Saving Letters...')
bar.printProgressBar(0, letters_size, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i in range(letters_size):
    zero = x_letters[i].reshape((28,28))
    rotated = np.flip(list(zip(*zero[::-1])), 1)
    rotated = rotated.flatten().tolist()
    rotated.append(y_letters[i])

    inner = builder.listString(map(str, rotated))
    cursor.execute(f'''
                    INSERT INTO Letters ({columns}) 
                    VALUES ({inner}) ;
                ''')
    bar.printProgressBar(i + 1, letters_size, prefix = 'Progress:', suffix = 'Complete', length = 50)
    conn.commit()