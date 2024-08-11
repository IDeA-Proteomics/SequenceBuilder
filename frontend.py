import tkinter as tk
from tkinter import ttk
from tkinter import font
# from IDeA_classes import SampleList
from backend import *
import re

### 1 = RED
### 2 - GREEN
### 3 - BLUE

frame_options = {'highlightbackground':'black' , 'highlightthickness':1}

class SFE_TrayPicker(tk.Frame):

    def __init__(self, parent, select_var, command):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)

        self.red_button = tk.Radiobutton(self, text="RED", var=select_var, value="RED", fg='black', bg='red', width = 4, command=command)
        self.green_button = tk.Radiobutton(self, text="GREEN", var=select_var, value="GREEN", fg='black', bg='green', width = 4, command=command)
        self.blue_button = tk.Radiobutton(self, text="BLUE", var=select_var, value="BLUE", fg = 'black', bg='blue', width = 4, command=command)

        self.red_button.pack()
        self.green_button.pack()
        self.blue_button.pack()        

        return

class LabelAndText(tk.Frame):

    def __init__(self, parent, label, text):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)

        self.label = tk.Label(self, text=label)
        self.text = tk.Label(self, text=text)

        self.label.pack(side=tk.LEFT)
        self.text.pack(side=tk.LEFT)

        return
    
class LabelAndCombo(tk.Frame):

    def __init__(self, parent, label, var, choices):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.combo = ttk.Combobox(self.parent, textvariable=var, values=choices, state='readonly')
        self.combo.pack()

        return
    

class SFE_WellPicker(tk.Frame):

    def handleTraySelection(self):
        self.start_position.set(self.tray_selection.get()[:1] + self.start_position.get()[1:])
        
        self.pool_position.set(self.tray_selection.get()[:1] + self.pool_position.get()[1:])
        self.pos_choices = self.getPositionList()
        self.combo.config(values = self.pos_choices)
        self.pool_combo.config(values = self.pos_choices)
        return
    
    
    def getPositionList(self):
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        retval = [self.tray_selection.get()[:1] + row + str(pos) for row in rows for pos in range(1,13)]
        return retval
    

    def __init__(self, parent):
        self.parent = parent

        
        self.tray_selection = tk.StringVar(value = "BLUE")
        self.start_position = tk.StringVar(value = "BA1")
        self.pool_position = tk.StringVar(value = "BH12")
        self.pos_choices = self.getPositionList()

        tk.Frame.__init__(self, self.parent)

        self.tray_label = tk.Label(self, text="Tray Selection")
        self.tray_label.pack()

        self.colorFrame = tk.Frame(self)
        self.colorFrame.pack()

        self.red_button = tk.Radiobutton(self.colorFrame, text="", var=self.tray_selection, value="R", fg='black', bg='red', width = 0, command=self.handleTraySelection)
        self.green_button = tk.Radiobutton(self.colorFrame, text="", var=self.tray_selection, value="G", fg='black', bg='green', width = 0, command=self.handleTraySelection)
        self.blue_button = tk.Radiobutton(self.colorFrame, text="", var=self.tray_selection, value="B", fg = 'black', bg='blue', width = 0, command=self.handleTraySelection)

        self.red_button.pack(side = tk.LEFT)
        self.green_button.pack(side = tk.LEFT)
        self.blue_button.pack(side = tk.LEFT)
        self.blue_button.select()

        self.start_label = tk.Label(self, text="Start Well")
        self.start_label.pack()

        self.combo = ttk.Combobox(self, textvariable=self.start_position, values=self.pos_choices, state='readonly', width=10)
        self.combo.pack()   

        self.pool_label = tk.Label(self, text="Pool Well")
        self.pool_label.pack()

        self.pool_combo = ttk.Combobox(self, textvariable=self.pool_position, values=self.pos_choices, state='readonly', width=10)   
        self.pool_combo.pack()

         
        return
    
    

class SFE_Head(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.path_label = LabelAndText(self, "Path:", sample_list.abs_path)
        self.path_label.pack(side = tk.TOP, anchor=tk.W)

        self.proj_label = LabelAndText(self, "Project:", sample_list.project_name)
        self.proj_label.pack(side=tk.TOP, anchor=tk.W)

        return
    
class SFE_ListText(tk.Text):

    def __init__(self, parent, sample_list):

        self.parent = parent
        self.scrollbar = tk.Scrollbar(self.parent)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # tk.Text.__init__(self, self.parent, height=40, width=100, yscrollcommand=self.scrollbar.set)  
        tk.Text.__init__(self, self.parent, yscrollcommand=self.scrollbar.set)  
        self.scrollbar.config(command=self.yview)
        
        for i in range(sample_list.getSampleCount()):
            self.insert(tk.END, "{:>3}| {:>5}| {:>24}| {:>24}\n".format(i, sample_list.getData('sample number', i), sample_list.getData('sample name', i), sample_list.getData('method', i)))
        
        self.config(state = 'disabled')

        return
    
class SFE_MethodChooser(tk.Frame):

    def __init__(self, parent):

        self.parent = parent

        self.methods = ["Method 1", "Method 2", "Method 3"]

        self.method_choice = tk.StringVar(value = self.methods[0])

        tk.Frame.__init__(self, self.parent)

        self.combo = ttk.Combobox(self, textvariable=self.method_choice, values=self.methods, state='readonly', width=20)
        self.combo.pack(side = tk.LEFT, anchor=tk.W)

        return
    

class SFE_ListFrame(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent    
        tk.Frame.__init__(self, self.parent)

        sfe_list_text = SFE_ListText(self, sample_list)
        sfe_list_text.pack(fill=tk.BOTH,expand=True)
        # sfe_list_text.insert(tk.END, "Text Here")

        return
    
    
class SFE_OptionFrame(tk.Frame):

    def __init__(self, parent):

        self.parent = parent
        tk.Frame.__init__(self.parent)

        return
    

class SequenceFrontEnd:

    def __init__(self, parent):

        self.parent = parent
        self.sample_list = SampleList()
        self.gpf = tk.IntVar(value=0)

        self.buildUI()
        return
    
    def buildSequence(self):

        

        return
    


    def buildUI(self):

        self.main_frame = tk.Frame(self.parent, **frame_options)
        self.left_frame = tk.Frame(self.main_frame, **frame_options)
        self.right_frame = tk.Frame(self.main_frame, **frame_options)
        self.bottom_frame = tk.Frame(self.parent, **frame_options)

        self.main_frame.pack(side = tk.TOP, fill=tk.BOTH, expand=True)
        self.left_frame.pack(side = tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side = tk.RIGHT, anchor=tk.E)
        self.bottom_frame.pack(side = tk.TOP)


        self.head = SFE_Head(self.left_frame, self.sample_list)
        self.head.pack(side = tk.TOP, anchor=tk.W)

        self.list_frame = SFE_ListFrame(self.left_frame, self.sample_list)
        self.list_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        self.start_well_picker = SFE_WellPicker(self.right_frame)
        self.start_well_picker.pack()

        self.gpf_check = tk.Checkbutton(self.right_frame, text="Include GPF", variable=self.gpf, 
                             onvalue=1, offvalue=0)
        self.gpf_check.pack()

        self.method_chooser = SFE_MethodChooser(self.right_frame)
        self.method_chooser.pack()

        self.exit_button = tk.Button(self.bottom_frame, text = "Exit", command = self.parent.destroy)
        self.exit_button.pack()

        return




def showSeqFE():
    root = tk.Tk()
    front_end = SequenceFrontEnd(root)
    root.mainloop()

def main():
    showSeqFE()

if (__name__ == "__main__"):
    main()