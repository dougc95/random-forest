import pyodbc
import pandas as pd
import numpy as np

class Data():

    def loadData(self, db, table):
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IHIVVUV;'
                      f'Database={db};'
                      'Trusted_Connection=yes;')

        data = pd.read_sql_query(f'SELECT * FROM {table}', conn)
        return data

    def getX(self, dataFrame):
        return np.array(dataFrame.iloc[:,:-1])
        
    def getY(self, dataFrame):
        return np.array(dataFrame.iloc[:,-1])
