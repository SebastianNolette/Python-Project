'''
Created on Apr 23, 2020

This is code that both windows will be using. 
'''

import sqlite3  



DATABASE= "Name.db"

conn = sqlite3.connect(DATABASE)    
c = conn.cursor() 

