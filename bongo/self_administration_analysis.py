# import necessary dependencies
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
#from PIL import ImageTk, Image
#from matplotlib import pyplot as plt
import numpy as np 
import pandas as pd
import re
from datetime import datetime, timedelta

from behaviour import Med_PC_Data_Extractor


# create GUI window
root = Tk()
# app name
root.title('Substance Seeking')
# window size
root.geometry("600x200")
# change app ico
#root.iconbitmap("dopamine.ico")
root.configure(background='#dae5e5')
#photo = tkinter.PhotoImage(file = 'gene.png')
#root.wm_iconphoto(False, photo)

# buttons menu
menu_bar = tkinter.Label(root,bg= "#788181", borderwidth=0,height=2,width=1000)
menu_bar.place(x=0,y=0)

global bg, window
bg = 0
window = 50
  

def open_action():

    '''function for open button to select desired file'''
    
    # opening file label
    wait_label_1 = tkinter.Label(root, text="Opening file. Please wait", font=("Comic Sans MS",30), fg="black", bg= "#9BF753", borderwidth=1,relief="solid")
    wait_label_1.place(x=100,y=100)
    #loading_label = display_gif("loading.gif",g_x=700,g_y=200)
    #loading_label.place(x=700,y=200)
    global file, opened_label

    # create variable for opened file path
    text_var = tkinter.StringVar()
    text_var.set("")
    # opening file dialog
    #opened_file = askopenfilename(filetypes=[("Text files", "*.txt"), ("Text files", "*.csv"), ("Excel files", ".xlsx")])
    opened_file = askopenfilename()

    file = open(opened_file, "r")

    
    # set file path to label content
    text_var.set(opened_file)
    opened_label = tkinter.Label(root, textvariable=text_var, font=("Arial",7), fg="black",width=70)
    opened_label.config(bg= "#E3E4FA", fg= "black",borderwidth=1, relief="solid")
    opened_label.place(x=10,y=33)
    
    #set calculate button state to active
    calculate_button.config(state="normal")
    wait_label_1.destroy()



    
def calculate_action():
    
    ''' function for calculate button'''

    extractor = Med_PC_Data_Extractor(file)

    global boxes
    boxes = extractor.extract_data(file)
    
    # change buttons state to active
    s_data_button.config(state="normal")

def save_data(data):
    
    ''' function for saving calculated data to a new file'''

    # dialog for choosing saving path
    saved_path = asksaveasfilename(filetypes=[("Excel files", ".xlsx"), ("Text files", ".csv")], defaultextension='.xlsx')

    # change data type to pandas Data Frame
    arr = pd.DataFrame(data)

    # save data to excel or text file in accordance to user choice
    if saved_path.endswith(".xlsx"):
        arr.to_excel(saved_path, index=False)
    else:
        arr.to_csv(saved_path, index=False)

    # label informing about successful saving
    save_label = tkinter.Label(root, text="Data saved", font=("Comic Sans MS",30), fg="black", bg= "#9BF753", borderwidth=1,relief="solid")
    save_label.place(x=200,y=100)


# main part of the program

# y value for placing buttons
button_y = 3

# button for saving data
s_data_button = tkinter.Button(root, text="Save data", width=15, command=lambda:save_data(boxes))
s_data_button.config(state="disabled")
s_data_button.place(x=290, y=button_y)

# button for calculating data
calculate_button = tkinter.Button(root, text="Calculate", width=15, command=calculate_action)
calculate_button.config(state="disabled")
calculate_button.place(x=150, y=button_y)

# button for opening file
open_button = tkinter.Button(root, text="Open", width=15, command=open_action)
open_button.place(x=10, y=button_y)

# method that runs main part of the program
root.mainloop()

# close file at the end
file.close()

boxes