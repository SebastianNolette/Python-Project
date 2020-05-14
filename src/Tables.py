'''
Created on Apr 27, 2020

@author: canilson
'''
import sqlite3
import sys



if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

#Create tables
c.execute('''CREATE TABLE TRANSACTIONS
            ([TransactionID] INTEGER PRIMARY KEY NOT NULL, [TransDate] DATE NOT NULL, [MonthID] INTEGER NOT NULL, [TransDesc] VARCHAR NOT NULL, [TransVal] MONEY NOT NULL)''')

c.execute('''CREATE TABLE MONTH
            ([MonthID] INTEGER PRIMARY KEY NOT NULL, [MonthDate] VARCHAR NOT NULL, [NumTrans] INT NOT NULL, [StartBal] MONEY NOT NULL, [EndBal] MONEY NOT NULL)''')

conn.commit()

if conn:
    conn.close()