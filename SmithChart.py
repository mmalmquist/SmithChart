#!/usr/bin/python
import tkinter


class SmithChart():
    def __init__(self):
        frame = tkinter.Tk()  # Create the frame
        frame.title('Smith Chart')
        lab1 = tkinter.Label(frame, text='Hello World1').grid(row=0, column=0, sticky='E', padx=10, pady=20)
        lab2 = tkinter.Label(frame, text='Hello World2').grid(row=0, column=1, sticky='W', padx=10, pady=20)
        lab3 = tkinter.Label(frame, text='Hello World3').grid(row=1, column=0, sticky='N', padx=10, pady=20)
        lab4 = tkinter.Label(frame, text='Hello World4').grid(row=1, column=1, sticky='S', padx=10, pady=20)
        # Add stuff to the frame
        frame.mainloop()  # Opens the frame?

a = SmithChart()

"""
from Tkinter import *
def roll(): pass
def links(): pass
def create(): pass
root=Tk()
root.title("CIME")

rows = 0
def create_detail_frame():
    global rows
    step = LabelFrame(root,text="Enter Details:")
    step.grid(row=rows, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
    Label(step,text="Competitors",font = "Arial 8 bold italic").grid(row=0,sticky='E', padx=5, pady=2)
    Label(step,text="Keywords",font = "Arial 8 bold italic").grid(row=1,sticky='E', padx=5, pady=2)
    Label(step,text="Project Name",font = "Arial 8 bold italic").grid(row=2,sticky='E', padx=5, pady=2)
    e1 = Entry(step)
    e2 = Entry(step)
    e3 = Entry(step)
    e1.grid(row=0,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    e2.grid(row=1,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    e3.grid(row=2,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    Button(step,text ="Search Words",width=10,font = "Arial 8 bold    italic",activebackground="red",command=roll).grid(row=3,column=0,sticky=W,pady=4,padx=5)
    Button(step,text="Google Search",width=10,font = "Arial 8 bold italic",command=links).grid(row=3,column=2,sticky=W,pady=4,padx=5)
    Button(step,text="Extraxt Text",width=10,font = "Arial 8 bold italic",command = create).grid(row=3,column=4,sticky=W,pady=4,padx=5)
    rows += 1

    # Reposition text, scroll
    #scr.grid_forget()
    #tex.grid_forget()
    #scr.grid(row=rows, padx=1, column=7, rowspan=15, columnspan=1, sticky=NS)
    #tex.grid(row=rows,column=1)

    # Reposition text, scroll
    scr.grid(row=rows)
    tex.grid(row=rows)

tex = Text(master=root)
scr=Scrollbar(root,orient =VERTICAL,command=tex.yview)
scr.grid(row=1, padx=1, column=7, rowspan=15, columnspan=1, sticky=NS)
tex.grid(row=1,column=1)
tex.config(yscrollcommand=scr.set,font=('Arial', 8, 'bold', 'italic'))

Button(root, text='Add detail frame', command=create_detail_frame).grid(row=0, column=7)
create_detail_frame()

mainloop()
"""
