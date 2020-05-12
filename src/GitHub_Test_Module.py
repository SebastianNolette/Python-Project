'''
Created on Apr 21, 2020
@author: Sebastian
'''

import sqlite3
from src.CommonCode import conn
import sys
from datetime import date
today=date.today()

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()
MonthID=100
MonthDate=str(today.year)+"-"+str(today.month)
NumTrans=1
StartBal=0
EndBal=55


code='''SELECT * FROM MONTH'''
c.execute(code)
datadata=c.fetchall()

print(datadata)
if conn:
    conn.close()