'''
Created on Apr 27, 2020

@author: canilson
'''
import tkinter as tk
import tkinter.ttk as tk
import sqlite3
import sys
import ID
from datetime import date
today=date.today()

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def Insert(): 
    print("Insert")
    #gets random TransactionID
    TransactionID=ID.SetTransID()
    TransactionID=ID.TransactionID
    #gets date string
    TransYear=input("Year")
    TransMonth=int(input("Month"))
    if TransMonth<10: #adds zero to numbers less than 10
        TransMonth="0"+str(TransMonth)
    TransDay=int(input("Day"))
    if TransDay<10:
        TransDay="0"+str(TransDay)
    TransDate=str(TransYear)+"-"+str(TransMonth)+"-"+str(TransDay)
    #gets NumTrans and EndBal for update
    findMonthID='''SELECT MonthID, NumTrans, EndBal FROM MONTH WHERE MonthDate=?'''
    MonthDate=str(today.year)+"-"+str(today.month)
    c.execute(findMonthID, (MonthDate,))
    MonthData=c.fetchone()
    MonthID=MonthData[0]
    #sets TransDesc and TransVal
    TransDesc=input("Description: ")
    TransVal=int(input("Value: "))
    NumTrans=MonthData[1]+1
    #updates EndBal based off of TransVal
    EndBal=MonthData[2]+TransVal
    
    transinsert='''INSERT INTO TRANSACTIONS (TransactionID, TransDate, MonthID, TransDesc, TransVal)
                    VALUES (?,?,?,?,?)'''
    monthinsert='''UPDATE MONTH 
                    SET NumTrans=?, EndBal=?
                    WHERE MonthID=?'''
    c.execute(transinsert, (TransactionID, TransDate, MonthID, TransDesc, TransVal,))
    c.execute(monthinsert, (NumTrans, EndBal, MonthID,))
    conn.commit()