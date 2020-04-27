'''
Created on Apr 27, 2020

@author: canilson
'''

import sqlite3
import sys
import random


if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def SetTransID():
    """
    Sets the value of TransactionID to a random integer that does not already exist
    Error: TransactionID is not created if one does not already exist
    """
    global TransactionID
    find='''SELECT TransactionID FROM Transactions'''
    c.execute(find)
    TransIDs=c.fetchall()
    for TransID in TransIDs: #Does not 
        TransactionID=random.randrange(1000,9999)
        if TransactionID==TransID:
            continue
        else:
            break

def SetMonthID():
    """
    Sets the value of MonthID to a random integer that does not already exist
    Error: MonthID is not created if one does not already exist
    """
    global MonthID
    find='''SELECT MonthID FROM Month'''
    c.execute(find)
    MonIDs=c.fetchall()
    for MonID in MonIDs: #Does not 
        MonthID=random.randrange(100,999)
        if MonthID==MonID:
            continue
        else:
            break