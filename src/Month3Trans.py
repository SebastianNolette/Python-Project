'''
Created on May 11, 2020

@author: canilson
'''
import sys
#from src.CommonCode import conn
import Insert
from datetime import date
today=date.today()
import ID
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import sqlite3  

if sys.platform=="win32":
    DB_File="Name.db"
    
conn=sqlite3.connect(DB_File)

c=conn.cursor()

def ImportData(MonID):
    
    Lines={}
    
    global Data
    global LinesList
    #MonthDate=str(today.year)+"-"+str(today.month)
    #MonthDate1=str(today.year)+"-"+str(today.month-1)
    print(MonID)
    #MonthDate2=str(today.year)+"-"+str(today.month-2)
    md='''SELECT MonthDate FROM MONTH WHERE MonthID=?'''
    c.execute(md, (MonID,))
    MonthRow=c.fetchone()
    MonthYear=MonthRow[0][0]+MonthRow[0][1]+MonthRow[0][2]+MonthRow[0][3]
    MonthMonth=MonthRow[0][5]
    MonthYear=int(MonthYear)
    print(MonthYear)
    MonthMonth=int(MonthMonth)
    MonthMonth+=1
    MonthList=[]
    for i in range (3):
        MonthMonth=MonthMonth-1
        if MonthMonth<=0:
            MonthMonth=12+MonthMonth
            MonthYear-=1
        MonthDate=str(MonthYear)+"-"+str(MonthMonth)
        MonthList.append(MonthDate)
        print(MonthDate)
    print(MonthList)
    impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.EndBal
        FROM TRANSACTIONS
            JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
            WHERE MONTH.MonthDate=? OR MONTH.MonthDate=? OR MONTH.MonthDate=?'''
    #impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.StartBal
    #    FROM TRANSACTIONS
    #        JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
    #        WHERE MONTH.MonthID=?'''
    
    #c.execute(impt,(MonthDate,))
    c.execute(impt,(MonthList[0],MonthList[1],MonthList[2],))
    
    
    Data=c.fetchall()   #Still needs to select from current month.  Use "today.month".
    print(Data)

    for row in Data:
        Lines[row[0]]=[row[1],row[3],row[2]]
    
    LinesList = sorted(Lines.items(), key = 
             lambda kv:(kv[1], kv[0]))
#    print(LinesList)
    #print(LinesList[0][1][1])
    
    
    SumMoney=[int(Data[0][4])+int(LinesList[0][1][1])]
    
    for i in range(1,len(LinesList)):
        SumMoney.append(SumMoney[i-1]+LinesList[i][1][1])
    #print(SumMoney)
    return [LinesList, SumMoney]



class SimpleTable(ttk.Frame):
    def __init__(self, parent, MonID, rows=4, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        ttk.Frame.__init__(self, parent)
        #Number of Columns in table
        self.columns=6
              
        self._widgets = []
        self.datarow =[]
        self.refreshTable(MonID)

    # This will be used to update Data
    def GoToMonth(self,RowNumber,MonID):
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
        c.execute(findMonthID, (MonID,))
        MonthData=c.fetchone()
        MonthID=MonthData[0]
        

        #updates EndBal based off of TransVal
        #EndBal=MonthData[2]+TransVal
        
        # Same Button Does both Update and Insert
        if self.datarow[RowNumber][0] ==-1:
            #gets random TransactionID
            TransactionID=ID.SetTransID()
            TransactionID=ID.TransactionID
            transinsert='''INSERT INTO TRANSACTIONS (TransDate, MonthID, TransDesc, TransVal, TransactionID)
                            VALUES (?,?,?,?,?)'''
            NumTrans=MonthData[1]+1
            EndBal=MonthData[2]+TransVal
            
            # Code for the chaning of buttons
            Row=self.rows-1
#            button = tk.Button(self, text="Delete Row %s" % (Row), 
#                               borderwidth=0, command= lambda i=Row: self.DeleteData(i),bd=2) # lambda is needed to send values
            button.grid(row=Row, column=5, sticky="nsew", padx=1, pady=1)
            self._widgets[Row][0].config(text="Update Row %s" %(Row))
            self._widgets[Row].append(button)  
            self.datarow[Row].append(TransactionID)
            
        else:
            TransactionID=self.datarow[RowNumber][0]
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
        self.refreshTable(MonID)

        
    def DeleteData(self,RowNumber,MonID):
        RowID=self.datarow[RowNumber][0] # Takes the ID at the beginning of the RowData. This is the ID
        #get MonthID
        monthid='''SELECT MonthID FROM TRANSACTIONS WHERE TransactionID=?'''
        c.execute(monthid,(RowID,))
        MonthID=c.fetchone()
        print(MonthID[0])
        #gets the NumTrans and EndBal from the MonthID
        numtrans='''SELECT NumTrans, EndBal FROM MONTH WHERE MonthID=?'''
        c.execute(numtrans, (MonthID[0],))
        montranend=c.fetchone()
        NumTrans=montranend[0]-1
        EndBal=montranend[1]
        EndBal=EndBal-int(self.datarow[RowNumber][2].get()) # Takes the string variable of the 3rd item in RowData. This is the Current Balance
        #updates the NumTrans and EndBal from the MonthID
        monthud='''UPDATE MONTH
                SET NumTrans = ?, EndBal = ?
                WHERE MonthID=?'''
        c.execute(monthud, (NumTrans, EndBal, MonthID[0],))
        #Deletes TRANSACTION row using the TransactionID
        delcommand='''DELETE FROM TRANSACTIONS WHERE TransactionID=?'''
        c.execute(delcommand, (RowID,))    #Table.get(di) somehow (I did not know it could and therefore do not know how it does) calls the database value of the selected row
        conn.commit()  
        
        # Refreshes Table
        self.refreshTable()
        

    def refreshTable(self,MonID):
        Data=ImportData(MonID)
        print(Data)
        #Number of Data Rows
        self.rows=len(Data[0])
        monthego='''SELECT TRANSACTIONS.MonthID FROM TRANSACTIONS WHERE TransactionID=?'''
        gregpersona='''SELECT MONTH.MonthDate FROM MONTH WHERE MonthID=?'''
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
                    c.execute(monthego,(str(LinesList[row][0]),))
                    lunarid=c.fetchone()
                    c.execute(gregpersona,(str(lunarid[0]),))
                    caesarsuperego=c.fetchone()
                    caesarsuperego=list(caesarsuperego)
                    button = tk.Button(self, text="Month Date %s" % (caesarsuperego[0],), 
                                 borderwidth=0, command= lambda i=row: self.GoToMonth(i,MonID),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button) 
                elif column == 3:
                    StringVariable= tk.StringVar()
                    StringVariable.set(Data[1][row])
                    label = tk.Label(self, text=StringVariable.get(), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable.get())
                    current_row.append(label)  
                elif column ==5:     
                    current_row.append(button)                                  
                else:
                    StringVariable= tk.StringVar()
                    if column==4:
                        StringVariable.set(Data[0][row][1][column-2])
                    else:
                        StringVariable.set(Data[0][row][1][column-1])
                        
                    entry = tk.Entry(self, width=10, textvariable=StringVariable.get(), state="readonly")
                    entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(entry)
                    current_row_data.append(StringVariable.get())
                    
            self.datarow.append(current_row_data)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

    

class TableFrame(ttk.Frame):
    def __init__(self, parent, MonID):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

              
        
        self.Table = SimpleTable(self, MonID, 20,5)
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
    def __init__(self, parent,MonID):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")


        #self.pack(fill=tk.BOTH, expand=True)   
        #Create Clearbutton
        
        '''Both of these buttons have enough space in the column to share the same column in this instance.
        '''
        #Create Savebutton    
        #ttk.Button(self, text="Save", command=self.data_entry).grid(column=1, row = 3,sticky=tk.W)    
    
        #ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit).grid(column=4, row = 2,sticky=tk.E)    
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
        
    def exit(self):
        FormLine.destroy()

class GUI(ttk.Frame):
    """
    Multiple Frames are necessary due to grid and Listbox not liking each other
    """
    def __init__(self, parent,MonID):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        self.frame1= TableFrame(self,MonID)
        self.frame1.pack(fill=tk.BOTH, expand=True)
        
 
        #ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit)
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    

    # Testing Buttons
        
    def exit(self):
        FormLine.destroy()
        
        
        #frame2=ButtonFrame(self)
        #frame2.pack(fill=tk.BOTH, expand=True)
        
        
        #print("")
    
    
    
def main(MonID):       
    FormLine= tk.Tk()
    FormLine.title("Customer")
    FormLine.geometry("525x400")
    FinalWindow=GUI(FormLine,MonID)
    FinalWindow.pack(fill=tk.BOTH, expand=True)
    FormLine.mainloop()
       
