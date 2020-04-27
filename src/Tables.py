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
            ([TransactionID] INT UID PRIMARY KEY, [TransDate] date, [MonthID] integer, [TransDesc] varchar, [TransVal] money)''')

c.execute('''CREATE TABLE MONTH
            ([MonthID] INT UID PRIMARY KEY, [MonthDate] date, [NumTrans] int, [StartBal] money, [EndBal] money)''')

conn.commit()

if conn:
    conn.close()