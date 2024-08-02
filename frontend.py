import tkinter as tk
from tkinter import ttk
from IDeA_classes import SampleList
import re

### 1 = RED
### 2 - GREEN
### 3 - BLUE

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
        tk.Text.__init__(self, self.parent, height=10, width=50, yscrollcommand=self.scrollbar.set)  
        self.scrollbar.config(command=self.yview)
        

        for name in sample_list.samplenames:
            self.insert(tk.END, name + '\n')
        

        return
    

class SFE_ListFrame(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent    
        tk.Frame.__init__(self, self.parent)

        sfe_list_text = SFE_ListText(self, sample_list)
        sfe_list_text.pack()
        # sfe_list_text.insert(tk.END, "Text Here")

        return
    
    
class SFE_OptionFrame(tk.Frame):

    def __init__(self, parent):

        self.parent = parent
        tk.Frame.__init__(self.parent)

        return
    

class SequenceFrontEnd:

    def __init__(self, parent, sample_list):

        # self.sample_list = sample_list

        self.parent = parent
        self.sample_list = sample_list
        self.tray_selection = tk.StringVar(value = "BLUE")
        self.start_position = tk.StringVar(value = "BA1")

        self.pos_choices = self.getPositionList()

        self.buildUI()
        return
    
    def getPositionList(self):
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        retval = [self.tray_selection.get()[:1] + row + str(pos) for row in rows for pos in range(1,13)]
        return retval


    def handleTraySelection(self):
        initial = self.tray_selection.get()[:1]
        self.start_position.set(initial + self.start_position.get()[1:])
        self.pos_choices = self.getPositionList()
        self.start_well.combo.config(values = self.pos_choices)
        return


    def buildUI(self):

        self.main_frame = tk.Frame(self.parent)
        self.left_frame = tk.Frame(self.main_frame)
        self.right_frame = tk.Frame(self.main_frame)
        self.bottom_frame = tk.Frame(self.parent)

        self.main_frame.pack(side = tk.TOP)
        self.left_frame.pack(side = tk.LEFT)
        self.right_frame.pack(side = tk.LEFT)
        self.bottom_frame.pack(side = tk.TOP)


        self.head = SFE_Head(self.left_frame, self.sample_list)
        self.head.pack(side = tk.TOP, anchor=tk.W)

        self.list_frame = SFE_ListFrame(self.left_frame, self.sample_list)
        self.list_frame.pack()

        self.start_well = LabelAndCombo(self.right_frame, label = "Start Pos", var = self.start_position, choices = self.pos_choices)
        self.start_well.pack()

        self.tray_selector = SFE_TrayPicker(self.right_frame, self.tray_selection, self.handleTraySelection)
        self.tray_selector.pack()

        self.exit_button = tk.Button(self.bottom_frame, text = "Exit", command = self.parent.destroy)
        self.exit_button.pack()

        return




def showSeqFE(sample_list):
    root = tk.Tk()
    front_end = SequenceFrontEnd(root, sample_list)
    root.mainloop()

def main():
    showSeqFE()

if (__name__ == "__main__"):
    main()