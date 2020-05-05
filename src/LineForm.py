'''
Created on Apr 26, 2020

@author: Sebastian
'''

import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import sys
from src.CommonCode import conn
import Insert
from datetime import date
today=date.today()


if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def ImportData():
    global Data
    MonthDate=str(today.year)+"-"+str(today.month)
    impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.EndBal
        FROM TRANSACTIONS
            JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
            WHERE MONTH.MonthDate=?'''
    c.execute(impt,(MonthDate,))
    Data=c.fetchall() #Still needs to select from current month.  Use "today.month".

    
    
ImportData()

class TableFrame(ttk.Frame):
    def __init__(self, parent):
        global Table
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        Table=tk.Listbox(self)
        Table.grid(column=0, row = 0, columnspan=4)

       
        '''
        Work on adding each value to it's own column        
        '''
                
        
        for item in Data:
            Table.insert(tk.END, item)
        
        scrollbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        #scrollbar.config(command=tk.select.yview)        
        Table.pack()
        scrollbar.pack()

class ButtonFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")


        #self.pack(fill=tk.BOTH, expand=True)   
        #Create Clearbutton
        
        '''Both of these buttons have enough space in the column to share the same column in this instance.
        '''
        #Create Savebutton    
        #ttk.Button(self, text="Save", command=self.data_entry).grid(column=1, row = 3,sticky=tk.W)    
        #Create Destroy button
        ttk.Button(self, text="Insert", command=self.InsertRow).grid(column=2, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit).grid(column=4, row = 2,sticky=tk.E)    
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    
    def DeleteRow(self):
        delete=map(int,Table.curselection()) #Retrieves value of selected item
        dc=set(delete)  #Converts map value to set value
        di=list(dc) #Converts set value to list
        delcommand='''DELETE FROM TRANSACTIONS WHERE TransactionID=?'''  #Prototype SQL for delete
        c.execute(delcommand, (Table.get(di)[0],))    #Table.get(di) somehow (I did not know it could and therefore do not know how it does) calls the database value of the selected row
        conn.commit()

    def InsertRow(self):
        Insert.Insert()
        
    def exit(self):
        FormLine.destroy()

class GUI(ttk.Frame):
    """
    Multiple Frames are necessary due to grid and Listbox not liking each other
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        frame1= TableFrame(self)
        frame1.pack(fill=tk.BOTH, expand=True)
        
        frame2=ButtonFrame(self)
        frame2.pack(fill=tk.BOTH, expand=True)
        
        
        print("")
    
    
    
        
FormLine= tk.Tk()
FormLine.title("Customer")
FormLine.geometry("525x400")
FinalWindow=GUI(FormLine)
FinalWindow.pack(fill=tk.BOTH, expand=True)
FormLine.mainloop()
if conn:
    conn.close()
