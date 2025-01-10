import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from datamodel import *
from SequenceWidgets import *


frame_options = {'highlightbackground':'black' , 'highlightthickness':1}



class HeaderFrame(tk.Frame):

    def __init__(self, parent, datamodel):

        self.parent = parent
        self.datamodel = datamodel
        tk.Frame.__init__(self, self.parent)

        self.path_label = LabelAndText(self, "Path:", textvariable=self.datamodel.path_var)
        self.path_label.pack(side = tk.TOP, anchor=tk.W)
        self.project_label = LabelAndText(self, "Project:", textvariable=self.datamodel.project_name_var)
        self.project_label.pack(side=tk.TOP, anchor=tk.W)

        return
    
class InstrumentFrame(tk.Frame):

    def __init__(self, parent, datamodel):

        self.parent = parent
        self.datamodel = datamodel
        tk.Frame.__init__(self, self.parent)

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP)
        
        self.instrument_combo = ttk.Combobox(self.top_frame, textvariable=self.datamodel.instrument_var, values=list(self.datamodel.instrument_data.keys()), state='readonly', width=20)
        self.instrument_combo.pack(side=tk.LEFT, anchor=tk.NE)
        self.instrument_combo.bind('<<ComboboxSelected>>', self.onInstrumentChange)

        self.dda_button = tk.Radiobutton(self.top_frame, text="DDA", var=datamodel.diadda_selection_var, value="DDA", command=self.onInstrumentChange)
        self.dia_button = tk.Radiobutton(self.top_frame, text="DIA", var=datamodel.diadda_selection_var, value="DIA", command=self.onInstrumentChange)
        self.dda_button.pack(side=tk.LEFT, anchor=tk.E)
        self.dia_button.pack(side=tk.LEFT, anchor=tk.E)

        self.method_combo = ttk.Combobox(self, textvariable=self.datamodel.method_var, values=self.datamodel.method_list, state='readonly', width=100)
        self.method_combo.pack(side=tk.TOP, anchor=tk.E)

        self.onInstrumentChange()

        return
    
    def onInstrumentChange(self, event=None):
        self.datamodel.onInstrumentSelection()
        self.method_combo.config(values=self.datamodel.method_list)
        return



class SequenceApp():

    def __init__(self, root):

        self.root_window = root
        self.datamodel = DataModel()
        self.datamodel.openSampleList("/home/david/IDeA_Scripts/TestData/LiuY_20241205_01_DDA_SampleList.xlsx")
        self.buildUI()

        return

    def buildUI(self):
        
        self.main_frame = tk.Frame(self.root_window, **frame_options)
        self.top_frame = tk.Frame(self.main_frame, **frame_options)
        self.body_frame = tk.Frame(self.main_frame, **frame_options)
        self.left_frame = tk.Frame(self.body_frame, **frame_options)
        self.right_frame = tk.Frame(self.body_frame, **frame_options)
        self.bottom_frame = tk.Frame(self.root_window, **frame_options)

        self.main_frame.pack(side = tk.TOP, fill=tk.BOTH, expand=True)
        self.top_frame.pack(side = tk.TOP, fill=tk.X, anchor = tk.W)
        self.body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_frame.pack(side = tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side = tk.RIGHT, anchor=tk.N)
        self.bottom_frame.pack(side = tk.TOP)

        self.head = HeaderFrame(self.top_frame, self.datamodel)
        self.head.pack(side = tk.LEFT, anchor=tk.W)

        self.instrument_frame = InstrumentFrame(self.top_frame, self.datamodel)
        self.instrument_frame.pack(side=tk.RIGHT, anchor=tk.E)

        return




def startSequenceApp():

    root = tk.Tk()    
    root.eval('tk::PlaceWindow . center')
    # root.iconbitmap("IDEA_Logo.ico")
    root.title("IDEA Sequence Builder")
    root.geometry("900x900")
    app = SequenceApp(root)
    root.mainloop()


if (__name__ == "__main__"):
    startSequenceApp()

