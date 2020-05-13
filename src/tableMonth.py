'''
Created on Apr 26, 2020

@author: Sebastian


This will have the monthTable

################################################################################################################################
Notes:
Data in self.datarow is formated As Follows:

self.datarow[Row][0]= MonthID
self.datarow[Row][1]= Year-Month (StrAttribute)
self.datarow[Row][2]= NmbrOfTransactions (StrAttribute)
self.datarow[Row][3]= StartBal (StrAttribute)
self.datarow[Row][4]= Change of Value (StrAttribute) (EndBal-StartBal)

################################################################################################################################

'''

import sys
#from src.CommonCode import conn
import Insert
from datetime import date
today=date.today()
import ID
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3  

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def ImportData():
    
    Lines={}
    
    #global Data
    #MonthDate=str(today.year)+"-"+str(today.month)
    #impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.EndBal
    #    FROM TRANSACTIONS
    #        JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
    #        WHERE MONTH.MonthDate=?'''
    impt='''SELECT * From Month'''
    
    #c.execute(impt,(MonthDate,))
    c.execute(impt,)
    
    Data=c.fetchall()   #Still needs to select from current month.  Use "today.month".
    print(Data)

    for row in Data:
        Lines[row[0]]=[row[1],row[2],row[3],row[4]]
    
    LinesList = sorted(Lines.items(), key = 
             lambda kv:(kv[1], kv[0]))
    
    Income=[]
    
    for i in range(0,len(LinesList)):
        Income.append(int(LinesList[i][1][3])-int(LinesList[i][1][2]))
    print(Income)
    return [LinesList, Income]


class SimpleTable(ttk.Frame):
    def __init__(self, parent, rows=4, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        ttk.Frame.__init__(self, parent)
        #Number of Columns in table
        self.columns=9  
 
        self._widgets = []
        self.datarow =[]
        self.refreshTable()
    
    # This will be used to update Data
    #Must be edited
    def EnterData(self,RowNumber):
        print(str(RowNumber) + str(self.datarow[RowNumber]))
        print((self.datarow[RowNumber][1].get()))
        print((self.datarow[RowNumber][2].get()))
        print((self.datarow[RowNumber][3].get()))
        print((self.datarow[RowNumber][4].get()))        
        # Maybe we can detect if there is a TransID @self.datarow[RowNumber][0]
        #If there isn't one or it is -1, then we could make an insert statement instead.


        MonthDate=self.datarow[RowNumber][1].get()
        StartBal=self.datarow[RowNumber][3].get()
        #updates EndBal based off of TransVal
        #EndBal=MonthData[2]+TransVal
        
        # Same Button Does both Update and Insert
        if self.datarow[RowNumber][0] ==-1:
            transinsert='''INSERT INTO Month (MonthDate, NumTrans, StartBal,EndBal)
                            VALUES (?,0,?,?)'''
            print(transinsert, MonthDate, StartBal)
            c.execute(transinsert, (MonthDate, StartBal, StartBal,))
        
        else:
            MonthID=self.datarow[RowNumber][0]
            transinsert='''UPDATE MONTH SET MonthDate=?, StartBal=?, 
                            NumTrans=(SELECT Count(TRANSACTIONS.TransactionID) FROM TRANSACTIONS Where TRANSACTIONS.MonthID = MONTH.MonthID), 
                            EndBal=(SELECT SUM(TRANSACTIONS.TransVal) FROM TRANSACTIONS Where TRANSACTIONS.MonthID = MONTH.MonthID) 
                            Where MonthID=?'''''           
            c.execute(transinsert, (MonthDate, StartBal, MonthID,))

        conn.commit()
        self.refreshTable()


    #Must be edited
    def DeleteData(self,RowNumber):
        RowID=self.datarow[RowNumber][0] # Takes the ID at the beginning of the RowData. This is the ID
        print(RowID)
        RowID=str(RowID)
        
        # Deletes the month, and then deletes all transactions attached to the month.
        delmonth='DELETE FROM Month where MonthID=?'
        delMonthTrans=' DELETE FROM TRANSACTIONS where MonthID=?'
        
        c.execute(delmonth, (RowID,))
        c.execute(delMonthTrans, (RowID,))        

        conn.commit()  
        
        # Refreshes Table
        self.refreshTable()
    
    
    
    def ViewData(self,RowNumber):
        print(self.datarow[RowNumber])
        #This Holds MonthID
        RowID=self.datarow[RowNumber][0]  
        # This opens the other Window that holds all the Transactions
        
        
        
    def CopyMonthData(self,RowNumber):
        print(self.datarow[RowNumber])
        RowID=self.datarow[RowNumber][0]     
        NewMonthID=ID.SetMonthID()
        NewMonthID=ID.MonthID
        #This copies the month to another month
        transInsert= 'INSERT INTO TRANSACTIONS (TransDate, MonthID, TransDesc, TransVal) SELECT TransDate, ?, TransDesc, TransVal From Transactions WHERE Transactions.MonthID= ?'
        monthInsert= 'INSERT INTO Month SELECT ?, MonthDate,NumTrans,StartBal,EndBal FROM Month WHERE MonthID= ?'
        c.execute(transInsert, (NewMonthID, RowID,))
        c.execute(monthInsert, (NewMonthID, RowID,))        
        conn.commit()
        
        
        self.refreshTable()
        
    def CompareData(self,RowNumber):
        print(self.datarow[RowNumber])
        #This Holds MonthID
        RowID=self.datarow[RowNumber][0]          
        #This Opens The Third Window
    
    
    def refreshTable(self):
        Data=ImportData()
        print(Data)
        #Number of Data Rows
        self.rows=len(Data[0])
        
        # Removes every Widgets from the table
        for row in self._widgets:
            for col in row:
                col.destroy()
        
        self._widgets = []
        self.datarow =[]
        for row in range(self.rows):
            current_row = []
            current_row_data = []
            for column in range(self.columns):
                if column == 0:
                    button = tk.Button(self, text="Update", 
                                 borderwidth=0, command= lambda i=row: self.EnterData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button)
                elif column == 1:
                    button = tk.Button(self, text="View", 
                                 borderwidth=0, command= lambda i=row: self.ViewData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button) 
                elif column == 2:
                    button = tk.Button(self, text="Copy", 
                                 borderwidth=0, command= lambda i=row: self.CopyMonthData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button)  
                elif column == 3:
                    button = tk.Button(self, text="Compare", 
                                 borderwidth=0, command= lambda i=row: self.CompareData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button)  
                elif column == 7:
                    StringVariable= tk.StringVar()
                    StringVariable.set(Data[1][row])
                    label = tk.Label(self, textvariable=StringVariable, 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable)
                    current_row.append(label)  
                elif column ==8:     
                    button = tk.Button(self, text="Delete Month", 
                                 borderwidth=0, command= lambda i=row: self.DeleteData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button)  
                elif column == 5:
                    StringVariable= tk.StringVar()
                    StringVariable.set(Data[0][row][1][1])
                    label = tk.Label(self, textvariable=StringVariable, 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable)
                    current_row.append(label)  
                
                else:
                    StringVariable= tk.StringVar()
                    if column==5:
                        StringVariable.set(Data[0][row][1][column-4])
                    else:
                        StringVariable.set(Data[0][row][1][column-4])
                        
                    entry = tk.Entry(self, textvariable=StringVariable,
                                 borderwidth=0, width=10)
                    entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(entry)
                    current_row_data.append(StringVariable)
            
            #print(Data[0][row])
            #print(Data[1][row])
            # Data Row Holds [MonthID, MonthID, Month ID, MonthMonth, MonthYear, StartingIncome, Income
            self.datarow.append(current_row_data)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

    
    #This function adds a row to the Table
    def addRow(self):
        self.rows+=1
        current_row=[]
        current_row_data=[]
        
        row=self.rows-1
        current_row = []
        current_row_data = []
        for column in range(self.columns):
            if column == 0:
                button = tk.Button(self, text="Update", 
                             borderwidth=0, command= lambda i=row: self.EnterData(i),bd=2) # lambda is needed to send values
                button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(-1)
                current_row.append(button)
            elif column == 7:
                StringVariable= tk.StringVar()
                StringVariable.set("0")
                label = tk.Label(self, textvariable=StringVariable, 
                             borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(StringVariable)
                current_row.append(label)  
            elif column ==8:     
                # As Nothing is inserted yet, using Refresh Table to remove this Row
                button = tk.Button(self, text="Delete Month", 
                             borderwidth=0, command=self.refreshTable,bd=2) # lambda is needed to send values
                button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append("-1")
                current_row.append(button)  
            elif column == 5:
                StringVariable= tk.StringVar()
                StringVariable.set("0")
                label = tk.Label(self, textvariable=StringVariable, 
                             borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(StringVariable)
                current_row.append(label)                                  
            elif column >3:
                StringVariable= tk.StringVar()
                StringVariable.set("")
                    
                entry = tk.Entry(self, textvariable=StringVariable,
                             borderwidth=0, width=10)
                entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(entry)
                current_row_data.append(StringVariable)
        
        
        # Data Row Holds [MonthID, MonthID, Month ID, MonthMonth, MonthYear, StartingIncome, Income
        self.datarow.append(current_row_data)
        print(self.datarow[row])
        self._widgets.append(current_row)

class TableFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

              
        
        self.Table = SimpleTable(self, 20,5)
        self.Table.pack(side=tk.LEFT, fill=tk.X)
        #Table.set(1,1,"Hello, world")
        self.myCanvas=tk.Canvas(self)
        self.myCanvas.create_window((0,0), window=self.Table, anchor='nw')
        
        self.myCanvas.pack(side=tk.LEFT, fill=tk.X)
        #self.Table.addRow()
        
        
        '''
        Work on adding each value to it's own column        
        '''  
        scrollbar=tk.Scrollbar(self.myCanvas, orient=tk.VERTICAL)
        scrollbar.config(command=self.myCanvas.yview)        
        scrollbar.pack(side=tk.RIGHT)


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
        ttk.Button(self, text="Add Insert Row", command=self.InsertRow).grid(column=2, row = 2,sticky=tk.E)    
        #ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit).grid(column=4, row = 2,sticky=tk.E)    
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)


    def InsertRow(self):
        FormLine.destroy()
        #Insert.Insert()
        #addRow()
        
    def exit(self):
        FormLine.destroy()

class GUI(ttk.Frame):
    """
    Multiple Frames are necessary due to grid and Listbox not liking each other
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        self.frame1= TableFrame(self)
        self.frame1.pack(fill=tk.BOTH, expand=True)
        
        # Testing Buttons
        ttk.Button(self, text="Add Insert Row", command=self.InsertRow)  
        #ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit)
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    

    # Testing Buttons
    def InsertRow(self):
        #FormLine.destroy()
        #Insert.Insert()
        self.frame1.Table.addRow()
        
    def exit(self):
        FormLine.destroy()
        
        
        #frame2=ButtonFrame(self)
        #frame2.pack(fill=tk.BOTH, expand=True)
        
        
        #print("")
    
    
    
        
FormLine= tk.Tk()
FormLine.title("Monthly Income")
FormLine.geometry("600x600")
FinalWindow=GUI(FormLine)
FinalWindow.pack(fill=tk.BOTH, expand=True)
FormLine.mainloop()
       
