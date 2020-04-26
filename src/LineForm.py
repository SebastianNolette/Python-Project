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
            4: ["3/4/2020", 75, "Income3"]}
    
    LinesList = sorted(Lines.items(), key = 
             lambda kv:(kv[1], kv[0]))
    print(LinesList)
    print(LinesList[0][1][1])
    
    
    SumMoney=[month[3]+LinesList[0][1][1]]
    
    for i in range(1,len(LinesList)):
        SumMoney.append(SumMoney[i-1]+LinesList[i][1][1])
    print(SumMoney)


ImportData()

class TableFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        
        Table=tk.Listbox(self)
        Table.grid(column=0, row = 0, columnspan=4)
        Table.insert(tk.END, "a list entry")
        
        for item in ["one", "two", "three", "four"]:
            Table.insert(tk.END, item)
        
        scrollbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        #scrollbar.config(command=tk.select.yview)        
        Table.pack()
        scrollbar.pack()
        


class ButtonFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

        """
        #Create a label
        ttk.Label(self, text="First Name").grid(column=0, row=0, sticky=tk.E)
        ttk.Label(self, text="Last Name").grid(column=0, row=1, sticky=tk.E)
        ttk.Label(self, text="City").grid(column=0, row=2, sticky=tk.E)

        #Create entry field   moved to data_entry
        self.firstName = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.firstName).grid(column=1, row=0)

        self.lastName = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.lastName).grid(column=1, row=1)

        self.city = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.city).grid(column=1, row=2)
        """

        #self.pack(fill=tk.BOTH, expand=True)   
        #Create Clearbutton
        
        '''Both of these buttons have enough space in the column to share the same column in this instance.
        '''
        #Create Savebutton    
        #ttk.Button(self, text="Save", command=self.data_entry).grid(column=1, row = 3,sticky=tk.W)    
        #Create Destroy button
        ttk.Button(self, text="Insert", command=self.exit).grid(column=2, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Delete", command=self.DeleteRow).grid(column=3, row = 2,sticky=tk.E)    
        ttk.Button(self, text="Exit", command=self.exit).grid(column=4, row = 2,sticky=tk.E)    
        
               
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    
    
    def DeleteRow(self):
        print("Delete")     
    
    def InsertRow(self):
        print("Insert")
    
    def clear(self):
        #Define the event listener for the Clear button
        print("First Name", self.firstName.get())
        self.firstName.set("")
        print("Last Name", self.lastName.get())
        self.lastName.set("")
        print("City", self.city.get())
        self.city.set("")

    def exit(self):
        FormLine.destroy()

class GUI(ttk.Frame):
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
       
