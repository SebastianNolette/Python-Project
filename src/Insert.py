'''
Created on Apr 27, 2020

@author: canilson
'''
import tkinter as tk
import tkinter.ttk as tk
import sqlite3
import sys
from ID.py import SetTransID() as SetTransID
from ID.py import SetMonthID() as SetMonthID

def Insert(): 
    print("Insert")
        SetTransID
        SetMonthID
        code='''(INSERT INTO TRANSACTIONS (TransactionID, TransDate, MonthID, TransDesc, TransVal)
            VALUES (?,?,?,?,?)'''
        c.execute(code (TransactionID, TransDate, MonthID, TransDesc, TransVal))
    
if conn:
    c.close()