'''
Created on Apr 26, 2020

@author: Sebastian
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

def ImportData(MonID):
    
    Lines={}
    
    #global Data
    impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.StartBal
        FROM TRANSACTIONS
            JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
            WHERE MONTH.MonthID=?'''
    #impt='''SELECT TRANSACTIONS.TransactionID, TRANSACTIONS.TransDate,TRANSACTIONS.TransDesc, TRANSACTIONS.TransVal, MONTH.StartBal
    #    FROM TRANSACTIONS
    #        JOIN MONTH ON MONTH.MonthID = TRANSACTIONS.MonthID
    #        WHERE MONTH.MonthID=?'''
    
    c.execute(impt,(MonID,))
    #c.execute(impt,(str("1"),))
    
    
    Data=c.fetchall()   #Still needs to select from current month.  Use "today.month".
    #print(Data)

    for row in Data:
        Lines[row[0]]=[row[1],row[3],row[2]]
    
    '''
    Lines= {1: ["3/1/2020", 100, "Income1"],
            2: ["3/3/2020", 10, "Income2"],
            3: ["3/2/2020", -50, "Payment1"],
            4: ["3/4/2020", 75, "Income3"],
            5: ["3/5/2020", 20, "Income4"],
            6: ["3/7/2020", 10, "Income5"],
            7: ["3/6/2020", -10, "Payment2"],
            8: ["3/8/2020", 15, "Income6"],
            9: ["3/8/2020", 15, "Income6"],
            10: ["3/8/2020", 15, "Income6"],
            11: ["3/1/2020", 100, "Income1"],
            12: ["3/3/2020", 10, "Income2"],
            13: ["3/2/2020", -50, "Payment1"],
            14: ["3/4/2020", 75, "Income3"],
            15: ["3/5/2020", 20, "Income4"],
            16: ["3/7/2020", 10, "Income5"],
            17: ["3/6/2020", -10, "Payment2"],
            18: ["3/8/2020", 15, "Income6"],
            19: ["3/8/2020", 15, "Income6"],
            20: ["3/8/2020", 15, "Income6"]            
            }
    '''
    LinesList = sorted(Lines.items(), key = 
             lambda kv:(kv[1], kv[0]))
    #print(LinesList)
    ##print(LinesList[0][1][1])
    
    if len(LinesList)!= 0:   
        SumMoney=[int(Data[0][4])+int(LinesList[0][1][1])]
    else:
        SumMoney=[]
    
    for i in range(1,len(LinesList)):
        SumMoney.append(SumMoney[i-1]+LinesList[i][1][1])
    ##print(SumMoney)
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
        '''
        Data=ImportData()
        #print(Data)
        #Number of Data Rows
        self.rows=len(Data[0])
        ##print(Data[0][0][1])
        
        
        self._widgets = []
        self.datarow =[]
        for row in range(self.rows):
            current_row = []
            current_row_data = []
            for column in range(self.columns):
                if column == 0:
                    button = tk.Button(self, text="Update Row %s" % (row), 
                                 borderwidth=0, command= lambda i=row: self.EnterData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button) 
                elif column == 3:
                    StringVariable= tk.StringVar()
                    StringVariable.set(Data[1][row])
                    label = tk.Label(self, textvariable=StringVariable, 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable)
                    current_row.append(label)  
                elif column ==5:     
                    button = tk.Button(self, text="Delete Row %s" % (row), 
                                 borderwidth=0, command= lambda i=row: self.DeleteData(i),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button)                                  
                else:
                    StringVariable= tk.StringVar()
                    if column==4:
                        StringVariable.set(Data[0][row][1][column-2])
                    else:
                        StringVariable.set(Data[0][row][1][column-1])
                        
                    entry = tk.Entry(self, textvariable=StringVariable,
                                 borderwidth=0, width=10)
                    entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(entry)
                    current_row_data.append(StringVariable)
                    
            self.datarow.append(current_row_data)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
        '''
    
    # This will be used to update Data
    def EnterData(self,RowNumber,MonID):
        ##print(str(RowNumber) + str(self.datarow[RowNumber]))
        ##print((self.datarow[RowNumber][1].get()))
        #print((self.datarow[RowNumber][2].get()))
        ##print((self.datarow[RowNumber][3].get()))
        ##print((self.datarow[RowNumber][4].get()))        
        # Maybe we can detect if there is a TransID @self.datarow[RowNumber][0]
        #If there isn't one or it is -1, then we could make an insert statement instead.

        ##print("Insert")
        
        # Getting Data from the datarows
        TransDateCheck=self.datarow[RowNumber][1].get()
        ##print(TransDateCheck)
        TransDateCheck=TransDateCheck.split('-')
        ##print(TransDateCheck)
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
        #findMonthID='''SELECT MonthID, NumTrans, EndBal, StartBal FROM MONTH WHERE MonthDate=?'''
        findMonthID='''SELECT MonthID, NumTrans, EndBal, StartBal FROM MONTH WHERE MonthID=?'''
        
        #MonthDate=str(today.year)+"-"+str(today.month)
        #c.execute(findMonthID, (MonthDate,))
        c.execute(findMonthID, (MonID,))
        MonthData=c.fetchone()
        MonthID=MonID
        

        #updates EndBal based off of TransVal
        #EndBal=MonthData[2]+TransVal
        
        # Same Button Does both Update and Insert
        if self.datarow[RowNumber][0] ==-1:
            #gets random TransactionID
            TransactionID=ID.SetTransID()
            #TransactionID=ID.TransactionID
            transinsert='''INSERT INTO TRANSACTIONS (TransDate, MonthID, TransDesc, TransVal, TransactionID)
                            VALUES (?,?,?,?,?)'''
            NumTrans=MonthData[1]+1
            EndBal=MonthData[2]+TransVal
                        
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
        ''' Legacy code to see If I did this right:
        #delete=map(int,Table.curselection()) #Retrieves value of selected item
        #dc=set(delete)  #Converts map value to set value
        #di=list(dc) #Converts set value to list
        '''
        #get MonthID
        monthid='''SELECT MonthID FROM TRANSACTIONS WHERE TransactionID=?'''
        c.execute(monthid,(RowID,))
        MonthID=c.fetchone()
        ##print(MonthID[0])
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
        self.refreshTable(MonID)
        
    
    def refreshTable(self, MonID):
        Data=ImportData(MonID)

        
        #print(Data)
        #print(MonID)
        #Number of Data Rows
        self.rows=len(Data[0])
        #print(self.rows)
        # Removes every Widgets from the table
        for row in self._widgets:
            for col in row:
                col.destroy()
        
        
        self._widgets = []
        self.datarow =[]
        
        if not Data[0]:
            self.addRow(MonID)
            return
        
        for row in range(self.rows):
            current_row = []
            current_row_data = []
            for column in range(self.columns):
                ##print(Data[0][row][0])
                ##print(Data[1][row])
                ##print(Data[])
                if column == 0:
                    button = tk.Button(self, text="Update Row %s" % (row), 
                                 borderwidth=0, command= lambda i=row: self.EnterData(i,MonID),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(Data[0][row][0])
                    current_row.append(button) 
                elif column == 3:
                    StringVariable= tk.StringVar()
                    StringVariable.set(Data[1][row])
                    #print(StringVariable.get())
                    label = tk.Label(self, text=StringVariable.get(), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable)
                    current_row.append(label)  
                elif column ==5:
                    StringVariable=tk.StringVar()
                    StringVariable.set(Data[0][row][0])     
                    button = tk.Button(self, text="Delete Row %s" % (row), 
                                 borderwidth=0, command= lambda i=row: self.DeleteData(i,MonID),bd=2) # lambda is needed to send values
                    button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(button)                                  
                else:
                    StringVariable= tk.StringVar()
                    if column==4:
                        StringVariable.set(Data[0][row][1][column-2])
                        
                        #print(Data[0][row][1][column-2])
                    else:
                        StringVariable.set(Data[0][row][1][column-1])
                        #print(Data[0][row][1][column-1])
                    entry = tk.Entry(self, textvariable=StringVariable,
                                     borderwidth=0, width=10)
                    entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row_data.append(StringVariable)
                    current_row.append(entry)
                    
                
            self.datarow.append(current_row_data)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        #print(self.datarow)
        '''
        Data=ImportData()
        for row in range(len(Data[0])):
             self.datarow[row][0]=(Data[0][row][0])
             self.datarow[row][1].set(Data[0][row][1][0])
             self.datarow[row][2].set(Data[0][row][1][1])
             self.datarow[row][3].set(Data[1][row])
             self.datarow[row][4].set(Data[0][row][1][2]) 
        '''

    
    #This function adds a row to the Table
    def addRow(self,MonID):
        self.rows+=1
        current_row=[]
        current_row_data=[]
        
        row=self.rows-1
        for column in range(5):
            if column == 0:
                button = tk.Button(self, text="Insert Row %s" % (row), 
                               borderwidth=0, command= lambda i=row: self.EnterData(i,MonID),bd=2) # lambda is needed to send values
                button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(-1)
                current_row.append(button) 
            elif column == 3:
                StringVariable= tk.StringVar()
                if (self.datarow):
                    StringVariable.set(self.datarow[row-1][3].get())
                else:
                    StringVariable.set("0")
                label = tk.Label(self, textvariable=StringVariable, 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(StringVariable)
                current_row.append(label)       
            else:
                StringVariable= tk.StringVar()
                StringVariable.set("")                        
                entry = tk.Entry(self, textvariable=StringVariable,
                                 borderwidth=0, width=10)
                entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(entry)
                current_row_data.append(StringVariable)
        
        
        self.datarow.append(current_row_data)
        self._widgets.append(current_row) 

class TableFrame(ttk.Frame):
    def __init__(self, parent,MonID):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

        
        
        self.Table = SimpleTable(self,MonID, 20,5)
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


class GUI(ttk.Frame):
    """
    Multiple Frames are necessary due to grid and Listbox not liking each other
    """
    def __init__(self, parent, MonID):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        self.frame1= TableFrame(self, MonID)
        self.frame1.pack(fill=tk.BOTH, expand=True)
        #print(MonID)
        # Testing Buttons
        ttk.Button(self, text="Add Insert Row", command=lambda i=MonID:self.InsertRow(i))  
        #ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        #ttk.Button(self, text="Exit", command=self.exit)
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    

    # Testing Buttons
    def InsertRow(self,MonID):
        #FormLine.destroy()
        #Insert.Insert()
        self.frame1.Table.addRow(MonID)

        #frame2=ButtonFrame(self)
        #frame2.pack(fill=tk.BOTH, expand=True)
        ##print("")
    
def main(MonID):
    #ImportData(MonID)
    FormLine= tk.Toplevel()
    FormLine.title("Transaction Table")
    FormLine.geometry("525x400")
    

    FinalWindow=GUI(FormLine, MonID)
    FinalWindow.pack(fill=tk.BOTH, expand=True)

    Button=ttk.Button(FormLine, text="Exit", command=FormLine.destroy)
    Button.pack()
    
    
    #FormLine.update()
    #FormLine.mainloop()
