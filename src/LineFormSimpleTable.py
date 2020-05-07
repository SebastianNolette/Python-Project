'''
Created on Apr 26, 2020

@author: Sebastian
'''

import tkinter as tk
import tkinter.ttk as ttk
import sqlite3  

def ImportData():
    
    """
    Actually Writing Select Statement to get this information will go here
    This is just how I plan on organizing the information    
    """
        
    month = [2,2020,2000,3000]
    
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
    
    LinesList = sorted(Lines.items(), key = 
             lambda kv:(kv[1], kv[0]))
    #print(LinesList)
    #print(LinesList[0][1][1])
    
    
    SumMoney=[month[3]+LinesList[0][1][1]]
    
    for i in range(1,len(LinesList)):
        SumMoney.append(SumMoney[i-1]+LinesList[i][1][1])
    print(SumMoney)
    return [LinesList, SumMoney]

ImportData()


class SimpleTable(ttk.Frame):
    def __init__(self, parent, rows=4, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        ttk.Frame.__init__(self, parent)
        #Number of Columns in table
        self.columns=5        
        
        Data=ImportData()
        print(Data)
        #Number of Data Rows
        self.rows=len(Data[0])
        #print(Data[0][0][1])
        
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
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
    # This will be used to update Data
    def EnterData(self,RowNumber):
        print(str(RowNumber) + str(self.datarow[RowNumber]))
        
        # Maybe we can detect if there is a TransID @self.datarow[RowNumber][0]
        #If there isn't one or it is -1, then we could make an insert statement instead.
        
        
        
    
        
    
    def refreshTable(self):
        Data=ImportData()
        for row in range(self.rows):
             self.datarow[row][0]=Data[0][row][0]
             self.datarow[row][1]=Data[0][row][1][0]
             self.datarow[row][2]=Data[0][row][1][1]
             self.datarow[row][3]=Data[1][row]
             self.datarow[row][4]=Data[0][row][1][2]     
    
    
    #This function adds a row to the Table
    def addRow(self):
        self.rows+=1
        current_row=[]
        current_row_data=[]
        
        row=self.rows-1
        for column in range(5):
            if column == 0:
                button = tk.Button(self, text="Insert Row %s" % (row), 
                               borderwidth=0, command= lambda i=row: self.EnterData(i),bd=2) # lambda is needed to send values
                button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append(-1)
                current_row.append(button) 
            elif column == 3:
                StringVariable= tk.StringVar()
                StringVariable.set(self.datarow[row-1][3].get())
                label = tk.Label(self, textvariable=StringVariable, 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row_data.append("")
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
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

              
        
        Table = SimpleTable(self, 20,5)
        Table.pack(side=tk.LEFT, fill=tk.X)
        Table.set(1,1,"Hello, world")
        myCanvas=tk.Canvas
        
        Table.addRow()
        
        
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
        ttk.Button(self, text="Insert", command=self.InsertRow).grid(column=2, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit).grid(column=4, row = 2,sticky=tk.E)    
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    
    def DeleteRow(self):
        print("Delete")     
    
    def InsertRow(self):
        print("Insert")
        
        
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
       
