


import tkinter as tk
from tkinter import ttk
from SequenceWidgets import *

import json    


class OptionFrame(tk.Frame):

    def handleTraySelection(self):
        self.datamodel.handleTraySelection()
        self.onChange()
        return
    
    def buildSelections(self):
        self.tray_picker.refreshState(self.datamodel.tray_list)
        self.datamodel.getAvailablePositions()
        self.combo.config(values = self.datamodel.combo_vals)
        self.pool_combo.config(values = self.datamodel.pool_vals)
        return
    
    def onChange(self, event = None):
        self.buildSelections()
        if self.onStartChangeCallback is not None:
            self.onStartChangeCallback()
        return
    

    def __init__(self, parent, datamodel, onStartChange, onRandom):

        self.parent = parent
        self.datamodel = datamodel
        self.onStartChangeCallback = onStartChange     
        self.onRandomChange = onRandom  

        self.pos_choices = self.datamodel.getTrayPositions(self.datamodel.getOption('selected_tray'))

        tk.Frame.__init__(self, self.parent)

        self.layout_frame = tk.Frame(self, bd=5, highlightbackground="black", highlightthickness=2)
        self.layout_frame.pack(fill=tk.X, pady=5)
        self.layout_label = tk.Label(self.layout_frame, text="Plate Layout", font=(None, 14, 'bold'))
        self.layout_label.pack()
        self.vertical_radio = tk.Radiobutton(self.layout_frame, text="Vertical Plate", font=(None, 12), variable=self.datamodel.getOptionVar('vertical'), value=True, command=self.onChange)
        self.horizontal_radio = tk.Radiobutton(self.layout_frame, text="Horizontal Plate", font=(None, 12), variable=self.datamodel.getOptionVar('vertical'), value=False, command=self.onChange)
        self.vertical_radio.pack()
        self.horizontal_radio.pack()

        self.tray_label = tk.Label(self, text="Tray Selection")
        self.tray_label.pack()

        self.tray_picker = TrayPicker(self, self.datamodel.getOptionVar('selected_tray'), self.handleTraySelection, datamodel.settings.default_tray)
        self.tray_picker.pack()

        self.start_label = tk.Label(self, text="Start Well")
        self.start_label.pack()

        self.combo = ttk.Combobox(self, textvariable=self.datamodel.getOptionVar('start_position'), values=self.pos_choices, state='readonly', width=10)
        self.combo.bind('<<ComboboxSelected>>', self.onChange)
        self.combo.pack()   

        self.pool_label = tk.Label(self, text="Pool Well")
        self.pool_label.pack()

        self.pool_combo = ttk.Combobox(self, textvariable=self.datamodel.getOptionVar('pool_position'), values=self.pos_choices, state='readonly', width=10)  
        self.pool_combo.bind('<<ComboboxSelected>>', self.onChange) 
        self.pool_combo.pack()

        self.pool_check = tk.Checkbutton(self, text="Include Pool", variable=self.datamodel.getOptionVar('pool'), onvalue=1, offvalue=0, command=self.onChange)
        self.pool_check.pack()

        self.gpf_check = tk.Checkbutton(self, text="Include GPF", variable=self.datamodel.getOptionVar('gpf'), onvalue=1, offvalue=0, command=self.onChange)
        self.gpf_check.pack()

        self.random_check = tk.Checkbutton(self, text="Randomize", variable=self.datamodel.getOptionVar('random'), onvalue=1, offvalue=0, command=self.onRandomChange)
        self.random_check.pack()

        self.blanks_frame = PreAndPostCheck(self, "Add Blanks", self.datamodel.getOptionVar('pre_blank'), self.datamodel.getOptionVar('post_blank'), self.onChange)
        self.blanks_frame.pack()

        self.qc_frame = PreAndPostCheck(self, "Add QC", self.datamodel.getOptionVar('pre_qc'), self.datamodel.getOptionVar('post_qc'), self.onChange)
        self.qc_frame.pack()

        self.add_blanks_label = tk.Label(self, text="Additional Blank every n samples")
        self.add_blanks_label.pack()

        self.add_blanks_combo = ttk.Combobox(self, values=[str(i) for i in range(51)], textvariable=self.datamodel.getOptionVar('blank_every'), state='readonly')
        self.add_blanks_combo.pack()
        self.add_blanks_combo.bind('<<ComboboxSelected>>', self.onChange)


        self.test_label = tk.Label(self, text="Test Sample")
        self.test_label.pack()

        combo_vals = [None]
        if self.datamodel.project_loaded:
            combo_vals += self.datamodel.sorted_list
        self.test_combo = ttk.Combobox(self, values=combo_vals, textvariable=self.datamodel.getOptionVar('test_sample'), state='readonly', width=30)
        self.test_combo.pack()
        self.test_combo.bind('<<ComboboxSelected>>', self.onChange)
         
        return
    
    def refreshProject(self):
        combo_vals = [None]
        if self.datamodel.project_loaded:
            combo_vals += self.datamodel.sorted_list
        self.datamodel.setOption('test_sample', "None")
        self.test_combo.config(values=combo_vals)
        self.onChange()
        return

    def onRandomChange(self):
        if self.onRandomChange:
            self.onRandomChange()