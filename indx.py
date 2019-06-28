from tkinter import *
import tkinter as tk
import sqlite3
from threading import Thread
from tkinter import messagebox, ttk
import pandas as pd
import sqlalchemy

root=tk.Tk()
root.title('hey')
root.configure(background="powder blue")
textin=StringVar()
textinn=StringVar()
appLabel = tk.Label(root, text="WELCOME TO SEARCH SHELL", fg="#06a099", width=40)
appLabel.config(font=("Sylfaen", 30))
appLabel.grid(row=0, columnspan=2, padx=(30,30), pady=(30, 0))

search_byLabel = tk.Label(root, text="Search By", width=40, anchor='w')\
    .grid(row=1, column=0, padx=(30,0), pady=(30, 0))
detailLabel = tk.Label(root, text="Enter Detail", width=40, anchor='w')\
    .grid(row=2, column=0, padx=(30,0))
runLabel = tk.Label(root, text="Run Script", width=40, anchor='w')\
    .grid(row=3, column=0, padx=(30,0))
viewLabel = tk.Label(root, text="View All Record", width=40, anchor='w')\
    .grid(row=4, column=0, padx=(30,0))

#searchEntry = tk.Entry(root,textvar="textin")
detailEntry = tk.Entry(root,textvar="textinn")
combo = ttk.Combobox(root,
                            values=[
'BOOK_ID','NAME','PRICE','NB_IN_STOCK','URL_IMG','PRODUCT_CATEGORY','RATING'
                                    ])

combo.grid(row=1, column=1, padx=(0,50), pady=(30, 20))

#searchEntry.grid(row=1, column=1, padx=(0,50), pady=(30, 20))
detailEntry.grid(row=2, column=1, padx=(0,50), pady = 20)

database = sqlite3.connect("new_Data.db")
cursor=database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS BOOK1(BOOK_ID INTEGER,NAME TEXT,PRICE INTEGER,NB_IN_STOCK TEXT,"
               "URL_IMG  TEXT,PRODUCT_CATEGORY TEXT,RATING TEXT)")
database.commit()

class ThreadedTask(Thread):
    def __init__(self, value):
        Thread.__init__(self)
        self.value = value

  ## defining work to perform during thread
    def run(self):
        database = sqlite3.connect("new_Data.db")
        if (self.value == "load"):
            data = pd.read_csv('books_data.csv')
            data.info()
            data = data.set_index('BOOK_ID')
            print(data.head())
            data.to_sql("BOOK1", database, if_exists="append")
            messagebox.showinfo("Success", "Done writing files to the database")
        elif(self.value=="show"):
            database = sqlite3.connect("new_Data.db")
            cursor = database.cursor()
            try:
                cursor= cursor.execute("SELECT * FROM BOOK1")
                messagebox.showinfo("Success", "fetching data wait for a moment plss")
                createNewFrame(cursor)
            except sqlite3.OperationalError:
                print("Cannot save this bookssss")
                return ("No record found")
        else:
            database = sqlite3.connect("new_Data.db")
            cursor = database.cursor()
            try:
              searches = combo.get()
              print(searches)

              details =detailEntry.get()
              print(details)
              cursor1 = cursor.execute("SELECT * FROM BOOK1 WHERE "+searches+" =" +"'"+str(details)+"'"+";")
              print(cursor1)

              createNewFrame(cursor1)
            except sqlite3.OperationalError:
                print("Cannot save this bookssss")
                return ("No record found")




def createNewFrame(cursor):
    displayWindow = tk.Tk()

    displayHeading = tk.Label(displayWindow, text="Displaying web scrapped data.")
    displayHeading.pack()

    ## using tree view
    treeview = ttk.Treeview(displayWindow)

    treeview["columns"] = (1, 2, 3, 4, 5, 6,7)
    treeview.heading(1, text="NAME")
    treeview.heading(2, text="PRICE")
    treeview.heading(3, text="NB_IN_STOCK")
    treeview.heading(4, text="URL_IMAGE")
    treeview.heading(5, text="PRODUCT CATEGORY")
    treeview.heading(6, text="RATING")

    i = 0
    for row in cursor:
        treeview.insert('',i,text=str(i+1), values=(row[1],row[2],row[3],row[4],row[5],row[6]))
        i = i + 1

    treeview.pack()
    displayWindow.mainloop()






def load_data():
    messagebox.showinfo("Info", "Writing file's content to the sql.")
    try:
        ## start thread process to load data from csv file to sql table
        ThreadedTask("load").start()
    except (sqlite3.ProgrammingError, sqlite3.OperationalError, sqlalchemy.exc.ArgumentError, pd.io.sql.DatabaseError) as error:
        messagebox.showerror("Error", "Error while writing file contents")
        print(error)

def show_data():

    messagebox.showinfo("Info","SHOWING DATA")
    try:
        ## start thread process to load data from csv file to sql table
        ThreadedTask("show").start()
    except (sqlite3.ProgrammingError, sqlite3.OperationalError, sqlalchemy.exc.ArgumentError, pd.io.sql.DatabaseError) as error:
        messagebox.showerror("Error", "Error while writing file contents")
        print(error)


def search_data():

    messagebox.showinfo("Info", "Searching DATA")
    try:
        ## start thread process to load data from csv file to sql table
        ThreadedTask("search").start()
    except (
    sqlite3.ProgrammingError, sqlite3.OperationalError, sqlalchemy.exc.ArgumentError, pd.io.sql.DatabaseError) as error:
        messagebox.showerror("Error", "Error while writing file contents")
        print(error)





button = tk.Button(root, text="SEARCH", command=lambda : search_data())
button.grid(row=1, column=1, padx=(200,20), pady=(30, 20))


displayButton = tk.Button(root, text="RUN ", command=lambda :load_data())
displayButton.grid(row=3, column=1, padx=(0,50), pady=(30, 20))


displayButton = tk.Button(root, text="VIEW ALL ", command=lambda :show_data())
displayButton.grid(row=4, column=1, padx=(0,50), pady=(30, 20))



root.mainloop()