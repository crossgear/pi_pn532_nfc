import tkinter as tk
import time

def Draw():
    global text

    frame=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame.place(x=10,y=10)
    text=tk.Label(frame,text='HELLO')
    text.pack()

def Refresher():
    global text
    text.configure(text=time.asctime())
    root.after(1000, Refresher) # every second...

root=tk.Tk()
Draw()
Refresher()
root.mainloop()