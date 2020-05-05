'''
Created on Apr 27, 2020

@author: canilson
'''
import tkinter as tk
import tkinter.ttk as tk
import sqlite3
import sys
import ID

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def Insert(): 
    print("Insert")
    ID.SetTransID()
    TransDate=input("Date: ")
    ID.SetMonthID
    TransDesc=input("Description")
    TransVal=int(input("Value: "))
    NumTrans=+1
    EndBal=TransVal
    transinsert='''INSERT INTO TRANSACTIONS (TransactionID, TransDate, MonthID, TransDesc, TransVal)
                    VALUES (?,?,?,?,?)'''
    monthinsert='''UPDATE MONTH 
                    SET NumTrans=?
                    SET EndBal=?
                    WHERE MonthID=?'''
    c.execute(transinsert, (ID.SetTransID, TransDate, ID.SetMonthID, TransDesc, TransVal,))
    c.execute(monthinsert, (NumTrans, EndBal, ID.SetMonthID,))
    conn.commit