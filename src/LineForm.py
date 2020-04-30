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
import datetime as date


if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def ImportData():
    global Data
    impt='''SELECT TransDate, TransVal, TransDesc FROM TRANSACTIONS'''
    c.execute(impt)
    Data=c.fetchall()

    
    
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
                
        
        for item in Data[0]:
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
        delete=map(int,Table.curselection())
        dc=set(delete)
        di=list(dc)
        delcommand='''(DELETE * FROM TRANSACTIONS WHERE TransVal=?)'''
        c.execute(delcommand(Table.get(di)))
    
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
