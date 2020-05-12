'''
Created on Apr 26, 2020

@author: Sebastian


This will have the monthTable

################################################################################################################################
Notes:
Data in self.datarow is formated As Follows:

self.datarow[0]= MonthID
self.datarow[1]= Year-Month (StrAttribute)
self.datarow[2]= NmbrOfTransactions (StrAttribute)
self.datarow[3]= StartBal (StrAttribute)
self.datarow[4]= Change of Value (StrAttribute) (EndBal-StartBal)

################################################################################################################################'''





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

        print("Insert")
        
        # Getting Data from the datarows
        TransDateCheck=self.datarow[RowNumber][1].get()
        print(TransDateCheck)
        TransDateCheck=TransDateCheck.split('-')
        print(TransDateCheck)
        #sets TransDesc and TransVal
        TransDesc=self.datarow[RowNumber][4].get()
        TransVal=int(self.datarow[RowNumber][2].get())   
        # Old values
        #TransDesc=input("Description: ")
        #TransVal=int(input("Value: "))       
        
        #gets date string
        TransYear=TransDateCheck[0]
        TransMonth=int(TransDateCheck[1])
        if TransMonth<10: #adds zero to numbers less than 10
            TransMonth="0"+str(TransMonth)
        TransDay=int(TransDateCheck[2])
        if TransDay<10:
            TransDay="0"+str(TransDay)
        TransDate=str(TransYear)+"-"+str(TransMonth)+"-"+str(TransDay)
        #gets NumTrans and EndBal for update
        findMonthID='''SELECT MonthID, NumTrans, EndBal, StartBal FROM MONTH WHERE MonthDate=?'''
        MonthDate=str(today.year)+"-"+str(today.month)
        c.execute(findMonthID, (MonthDate,))
        MonthData=c.fetchone()
        MonthID=MonthData[0]
        

        #updates EndBal based off of TransVal
        #EndBal=MonthData[2]+TransVal
        
        # Same Button Does both Update and Insert
        if self.datarow[RowNumber][0] ==-1:
            #gets random TransactionID
            TransactionID=ID.SetTransID()
            TransactionID=ID.TransactionID
            transinsert='''INSERT INTO Month (MonthDate, NumTrans, StartBal,EndBalance)
                            VALUES (?,0,?,?)'''
            c.execute(transinsert, (MonthDate, StartBal, StartBal,))
            
        else:
            TransactionID=self.datarow[RowNumber][0]
            
            #NumTransSQL=
            #c.execute(NumTransSQL,(,))
            #NumTrans=
            
            transinsert='''UPDATE TRANSACTIONS SET TransDate=?, MonthID=?, TransDesc=?, TransVal=?
                            WHERE TransactionID=?'''           
            NumTrans=MonthData[1]
            # Delta= Change 
            # New End Balanece= Old Value + deltaTransVal
            # DeltaTransVal= NewTransVal-OldTransVal
            # OldTransVal= SumOfVal - LastSumOfVal { int(self.datarow[RowNumber][3].get())+int(self.datarow[RowNumber-1][3].get()) }
            # This is the resulting monstrosity
            if RowNumber ==0:
                EndBal=MonthData[2]+TransVal-int(self.datarow[RowNumber][3].get())+int(MonthData[3])    
            else:    
                EndBal=MonthData[2]+TransVal-int(self.datarow[RowNumber][3].get())+int(self.datarow[RowNumber-1][3].get())
        
        monthinsert='''UPDATE MONTH SET NumTrans=?, EndBal=? WHERE MonthID=?'''

        c.execute(transinsert, (TransDate, MonthID, TransDesc, TransVal, TransactionID,))
        c.execute(monthinsert, (NumTrans, EndBal, MonthID,))
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
                # Unfinished
                if column == 0:
                    button = tk.Button(self, text="Update", 
                                 borderwidth=0, command= lambda i=row: self.EnterData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button)
                # Unfinished
                elif column == 1:
                    button = tk.Button(self, text="View", 
                                 borderwidth=0, command= lambda i=row: self.ViewData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button) 
                # Unfinished
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
            
            print(Data[0][row])
            print(Data[1][row])
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
                current_row_data.append("-1")
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
            elif column >3:
                StringVariable= tk.StringVar()
                if column==5:
                    StringVariable.set("")
                else:

                    StringVariable.set("")
                    
                entry = tk.Entry(self, textvariable=StringVariable,
                             borderwidth=0, width=10)
                entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(entry)
                current_row_data.append(StringVariable)
        
        
        # Data Row Holds [MonthID, MonthID, Month ID, MonthMonth, MonthYear, StartingIncome, Income
        self.datarow.append(current_row_data)
        self._widgets.append(current_row)

class TableFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

              
        
        self.Table = SimpleTable(self, 20,5)
        self.Table.pack(side=tk.LEFT, fill=tk.X)
        #Table.set(1,1,"Hello, world")
        myCanvas=tk.Canvas
        
        #self.Table.addRow()
        
        
        '''
        Work on adding each value to it's own column        
        '''  
        scrollbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        #scrollbar.config(command=ttk.select.yview)        
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
       
