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
    transinsert='''(INSERT INTO TRANSACTIONS (TransactionID, TransDate, MonthID, TransDesc, TransVal)
                    VALUES (?,?,?,?,?)'''
    monthinsert='''(UPDATE MONTH 
                    SET NumTrans=?
                    SET EndBal=?
                    WHERE MonthID=?)'''
    c.execute(transinsert (TransactionID, TransDate, MonthID, TransDesc, TransVal))
    c.execute(monthinsert (NumTrans, TransVal, MonthID))
if conn:
    c.close()