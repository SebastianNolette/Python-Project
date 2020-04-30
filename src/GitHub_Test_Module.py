'''
Created on Apr 21, 2020
@author: Sebastian
'''
import sqlite3
import sys
from datetime import date
today=date.today()

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()
MonthID=122
MonthDate=today
NumTrans=1
StartBal=0
EndBal=55
print(MonthDate)

code='''INSERT INTO MONTH (MonthID, MonthDate, NumTrans, StartBal, EndBal) VALUES (?,?,?,?,?)'''
c.execute(code, (122,today,1,0,55,))
month=c.fetchall()
print(month)

if conn:
    conn.close()