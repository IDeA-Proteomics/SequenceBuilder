import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# from IDeA_classes import SampleList
from backend import *
import datamodel
import json

### 1 = RED
### 2 - GREEN
### 3 - BLUE

frame_options = {'highlightbackground':'black' , 'highlightthickness':1}

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

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
        self.rebuildSelections()
        self.onStartChangeCallback()
        return
    
    def rebuildSelections(self):
        self.pos_choices = self.getPositionList()
        self.combo_vals = self.pos_choices[:97-self.count]
        self.combo.config(values = self.combo_vals)
        if self.count < 96:
            self.pool_vals = [i for i in self.pos_choices if i not in self.getSamplePosistions()]
        else:
            second_tray = 'B' if self.tray_selection.get()[:1] == 'G' else 'G'
            second_tray_list = [second_tray + row + str(pos) for row in rows for pos in range(1,13)]
            self.pool_vals = [i for i in self.pos_choices + second_tray_list if i not in self.getSamplePosistions()]
        self.pool_combo.config(values = self.pool_vals)
        if self.pool_position.get() not in self.pool_vals:
            self.pool_position.set(self.pool_vals[-1])

        return
    
    def onStartChange(self, event):
        self.rebuildSelections()
        self.onStartChangeCallback()
        return
    
    def getPositionList(self):
        
        retval = [self.tray_selection.get()[:1] + row + str(pos) for row in rows for pos in range(1,13)]
        return retval
    
    def getSamplePosistions(self):

        pos_list = self.getPositionList()
        idx = pos_list.index(self.start_position.get())

        if self.count > 96:

            second_tray = 'B' if self.tray_selection.get()[:1] == 'G' else 'G'

            second_tray_list = [second_tray + row + str(pos) for row in rows for pos in range(1,13)]

            pos_list = pos_list + second_tray_list
        
        return pos_list[idx:idx+self.count]
    
    def getPoolWell(self):
        return self.pool_position.get()

    def __init__(self, parent, count, onStartChange):
        self.parent = parent
        self.count = count
        self.onStartChangeCallback = onStartChange

        
        self.tray_selection = tk.StringVar(value = "GREEN")
        self.start_position = tk.StringVar(value = "GA1")
        self.pool_position = tk.StringVar(value = "GH12")
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
        self.green_button.select()

        self.start_label = tk.Label(self, text="Start Well")
        self.start_label.pack()

        self.combo = ttk.Combobox(self, textvariable=self.start_position, values=self.pos_choices, state='readonly', width=10)
        self.combo.bind('<<ComboboxSelected>>', self.onStartChange)
        self.combo.pack()   

        self.pool_label = tk.Label(self, text="Pool Well")
        self.pool_label.pack()

        self.pool_combo = ttk.Combobox(self, textvariable=self.pool_position, values=self.pos_choices, state='readonly', width=10)  
        self.pool_combo.bind('<<ComboboxSelected>>', self.onStartChange) 
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

class SFE_SequenceText(tk.Text):

    def __init__(self, parent, sample_list):

        self.parent = parent
        self.sample_list = sample_list
        self.y_scrollbar = tk.Scrollbar(self.parent)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_scrollbar = tk.Scrollbar(self.parent, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Text.__init__(self, self.parent, yscrollcommand = self.y_scrollbar.set, xscrollcommand = self.x_scrollbar.set, wrap='none')
        self.y_scrollbar.config(command = self.yview)
        self.x_scrollbar.config(command = self.xview)

        self.buildSequenceText()

        return
    
    def buildSequenceText(self):

        self.config(state = 'normal')
        self.delete(1.0, tk.END)
        for i in range(self.sample_list.getSequenceCount()):
            self.insert(tk.END, 
                        "{:>3}| {:>8}| {:>40.40}| {:>4} | {:<40.40} | {:<40.40} | {:<5} | {:<5} | {:>20.20} |\n".format(i,
                                                                   str(self.sample_list.getSequenceData('Sample Type', i)),
                                                                   str(self.sample_list.getSequenceData('File Name', i)),
                                                                   str(self.sample_list.getSequenceData('Sample ID', i)),  
                                                                   str(self.sample_list.getSequenceData('Path', i)),
                                                                   str(self.sample_list.getSequenceData('Instrument Method', i)),
                                                                   str(self.sample_list.getSequenceData('Position', i)),
                                                                   str(self.sample_list.getSequenceData('Inj Vol', i)),
                                                                   str(self.sample_list.getSequenceData('Sample Name', i)),
                                                                   )
                                                                   )
        self.config(state = 'disabled')


        return
    


class SFE_ListText(tk.Text):

    def __init__(self, parent, sample_list):

        self.parent = parent
        self.sample_list = sample_list
        self.scrollbar = tk.Scrollbar(self.parent)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Text.__init__(self, self.parent, yscrollcommand=self.scrollbar.set)  
        self.scrollbar.config(command=self.yview)
        
        self.buildListText()
        

        return
    
    def buildListText(self):
        self.config(state = 'normal')
        self.delete(1.0, tk.END)
        for i in range(self.sample_list.getSampleCount()):
            self.insert(tk.END, 
                        "{:>3}| {:>5}| {:>24} | {:<4} | {:>24} |\n".format(i, 
                                                                   str(self.sample_list.getListData('number', i)), 
                                                                   str(self.sample_list.getListData('name', i)), 
                                                                   str(self.sample_list.getListData('position', i)),
                                                                   str(self.sample_list.getListData('method', i))))
        self.config(state = 'disabled')

        return
    
class SFE_MethodChooser(tk.Frame):

    def __init__(self, parent):

        self.parent = parent

        self.methods = ["Method 1", "Method 2", "Method 3"]

        self.method_choice = tk.StringVar(value = self.methods[0])

        tk.Frame.__init__(self, self.parent)

        self.combo = ttk.Combobox(self, textvariable=self.method_choice, values=self.methods, state='readonly', width=100)
        self.combo.pack(side = tk.LEFT, anchor=tk.W)

        return
    
    def getMethod(self):
        return self.combo.get()
    

class SFE_ListFrame(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent    
        tk.Frame.__init__(self, self.parent)

        self.tabs = ttk.Notebook(self)
        self.plate_tab = tk.Frame(self.tabs)
        self.sequence_tab = tk.Frame(self.tabs)

        self.tabs.add(self.plate_tab, text = "Plate")
        self.tabs.add(self.sequence_tab, text = "Sequence")

        self.tabs.pack(fill = tk.BOTH, expand=True)

        self.sfe_list_text = SFE_ListText(self.plate_tab, sample_list)
        self.sfe_list_text.pack(fill=tk.BOTH,expand=True)

        self.sfe_sequence_text = SFE_SequenceText(self.sequence_tab, sample_list)
        self.sfe_sequence_text.pack(fill=tk.BOTH,expand=True)
        return
    
    
class SFE_OptionFrame(tk.Frame):

    def __init__(self, parent):

        self.parent = parent
        tk.Frame.__init__(self.parent)

        return
    

class SequenceFrontEnd:

    def __init__(self, parent):

        self.parent = parent
        self.file_name = filedialog.askopenfilename(initialdir="Z:\\Active_projects")
        self.sample_list = SampleList(self, self.file_name)
        self.pool = tk.IntVar(value=0)
        self.gpf = tk.IntVar(value=0)
        self.random = tk.IntVar(value=0)
        self.addqc = tk.IntVar(value=0)
        self.add_blanks = tk.IntVar(value=0)
        self.instrument = tk.StringVar(value="Exploris2")
        self.diadda_selection = tk.StringVar(value="DDA")

        self.buildUI()
        return
    


    def buildUI(self):

        self.main_frame = tk.Frame(self.parent, **frame_options)
        self.top_frame = tk.Frame(self.main_frame, **frame_options)
        self.body_frame = tk.Frame(self.main_frame, **frame_options)
        self.left_frame = tk.Frame(self.body_frame, **frame_options)
        self.right_frame = tk.Frame(self.body_frame, **frame_options)
        self.bottom_frame = tk.Frame(self.parent, **frame_options)

        self.main_frame.pack(side = tk.TOP, fill=tk.BOTH, expand=True)
        self.top_frame.pack(side = tk.TOP, fill=tk.X, anchor = tk.W)
        self.body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_frame.pack(side = tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side = tk.RIGHT, anchor=tk.N)
        self.bottom_frame.pack(side = tk.TOP)


        self.head = SFE_Head(self.top_frame, self.sample_list)
        self.head.pack(side = tk.LEFT, anchor=tk.W)
        
        self.instrument_frame = tk.Frame(self.top_frame, **frame_options)
        self.instrument_frame.pack(side = tk.RIGHT, anchor=tk.E)

        self.instrument_frame_top = tk.Frame(self.instrument_frame, **frame_options)
        self.instrument_frame_top.pack()

        self.list_frame = SFE_ListFrame(self.left_frame, self.sample_list)
        self.list_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        self.instrument_combo = ttk.Combobox(self.instrument_frame_top, textvariable=self.instrument, values=list(datamodel.instrument_data.keys()), state='readonly', width=20)
        self.instrument_combo.pack(side=tk.LEFT, anchor=tk.NW)

        self.dda_button = tk.Radiobutton(self.instrument_frame_top, text="DDA", var=self.diadda_selection, value="DDA", command=self.onInstrumentChoice)
        self.dia_button = tk.Radiobutton(self.instrument_frame_top, text="DIA", var=self.diadda_selection, value="DIA", command=self.onInstrumentChoice)
        self.dda_button.pack(side=tk.LEFT)
        self.dia_button.pack(side=tk.LEFT)

        self.start_well_picker = SFE_WellPicker(self.right_frame, self.sample_list.getSampleCount(), self.rebuild)
        self.start_well_picker.pack()

        self.pool_check = tk.Checkbutton(self.right_frame, text="Include Pool", variable=self.pool,
                                         onvalue=1, offvalue=0, command=self.rebuild)
        self.pool_check.pack()

        self.gpf_check = tk.Checkbutton(self.right_frame, text="Include GPF", variable=self.gpf, 
                             onvalue=1, offvalue=0, command=self.rebuild)
        self.gpf_check.pack()

        self.random_check = tk.Checkbutton(self.right_frame, text="Randomize", variable=self.random, 
                             onvalue=1, offvalue=0, command=self.rebuild)
        self.random_check.pack()

        self.addqc_check = tk.Checkbutton(self.right_frame, text="Add QC", variable=self.addqc, 
                             onvalue=1, offvalue=0, command=self.rebuild)
        self.addqc_check.pack()

        self.add_blanks_label = tk.Label(self.right_frame, text="Add blank every n runs")
        self.add_blanks_label.pack()
        self.add_blanks_combo = ttk.Combobox(self.right_frame, values=[i for i in range(51)], state='readonly')
        self.add_blanks_combo.current(0)
        self.add_blanks_combo.pack()
        self.add_blanks_combo.bind('<<ComboboxSelected>>', self.rebuild)

        self.method_chooser = SFE_MethodChooser(self.instrument_frame)
        self.method_chooser.pack()

        self.exit_button = tk.Button(self.bottom_frame, text = "Exit", command = self.onExit)
        self.create_button = tk.Button(self.bottom_frame, text="Create", command=self.sample_list.outputSequence)
        self.exit_button.pack(side=tk.LEFT)
        self.create_button.pack()

        self.instrument_combo.bind('<<ComboboxSelected>>', self.onInstrumentChoice)
        self.onInstrumentChoice()
        self.rebuild()

        return
    
    def onExit(self):
        self.parent.destroy()
        with open("instrument_data.json", 'w') as jf:
            json.dump(datamodel.instrument_data, jf, ensure_ascii=False, indent=4 )

    
    def onInstrumentChoice(self, event=None):
        # self.method_chooser.combo.config(values = datamodel.methods[self.instrument.get()])
        meth_list = datamodel.instrument_data[self.instrument.get()]['methods'][self.diadda_selection.get()]
        if not meth_list:
            meth_list = ["NOT SUPPORTED"]
        self.method_chooser.combo.config(values=meth_list)
        self.method_chooser.combo.current(0)
        self.rebuild()
        return
    
    def rebuild(self, event=None):
        self.sample_list.reBuildList()
        self.list_frame.sfe_list_text.buildListText()
        self.sample_list.reBuildSequence()
        self.list_frame.sfe_sequence_text.buildSequenceText()

        return
    
    def getAddBlanks(self):
        return self.add_blanks_combo.get()

    def getSamplePositions(self):
        return self.start_well_picker.getSamplePosistions()
    
    def getPoolWell(self):
        return self.start_well_picker.getPoolWell()
    
    def getMethod(self):
        return self.method_chooser.getMethod()
    
    def getRandom(self):
        return self.random.get()
    
    def getGPF(self):
        return self.gpf.get()
    
    def getPool(self):
        return self.pool.get()
    
    def getAddQC(self):
        return self.addqc.get()
    
    def getInstrument(self):
        return self.instrument.get()
    





def showSeqFE():
    root = tk.Tk()
    root.iconbitmap("IDEA_Logo.ico")
    root.title("IDEA Sequence Builder")
    front_end = SequenceFrontEnd(root)
    root.mainloop()

def main():
    showSeqFE()

if (__name__ == "__main__"):
    main()