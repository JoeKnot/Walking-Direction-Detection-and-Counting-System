import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_580=tk.Button(root)
        GButton_580["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_580["font"] = ft
        GButton_580["fg"] = "#000000"
        GButton_580["justify"] = "center"
        GButton_580["text"] = "Open"
        GButton_580.place(x=410,y=390,width=70,height=25)
        GButton_580["command"] = self.GButton_580_command

        GButton_555=tk.Button(root)
        GButton_555["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_555["font"] = ft
        GButton_555["fg"] = "#000000"
        GButton_555["justify"] = "center"
        GButton_555["text"] = "Close"
        GButton_555.place(x=510,y=390,width=70,height=25)
        GButton_555["command"] = self.GButton_555_command

        GButton_467=tk.Button(root)
        GButton_467["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_467["font"] = ft
        GButton_467["fg"] = "#000000"
        GButton_467["justify"] = "center"
        GButton_467["text"] = "Exit"
        GButton_467.place(x=460,y=460,width=70,height=25)
        GButton_467["command"] = root.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

