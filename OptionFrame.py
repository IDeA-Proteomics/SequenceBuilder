


import tkinter as tk
from tkinter import ttk
from SequenceWidgets import *

import json

class TrayPicker(tk.Frame):

    def __init__(self, parent, textvariable, onChange, initial_val):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)
        self.textvariable = textvariable
        self.onChange = onChange

        self.buttons = [
            tk.Radiobutton(self, text="", var=self.textvariable, value="R", fg='black', bg='red', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="G", fg='black', bg='green', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="B", fg = 'black', bg='blue', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="Y", fg = 'black', bg='yellow', width = 4, command=self.onChange)
        ]
        for button in self.buttons:
            button.pack(side = tk.LEFT)
            if button.cget('value') == initial_val:
                button.select()

        return
    
    def refreshState(self, trays):
        for button in self.buttons:
            if button.cget('value') in trays:
                button.config(state="normal")
            else:
                button.config(state="disabled")
                if button.cget('value') == self.textvariable.get():
                    self.textvariable.set(trays[1])
                    self.onChange()
        return

    


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

        self.pos_choices = self.datamodel.getTrayPositions(self.datamodel.selected_tray)

        tk.Frame.__init__(self, self.parent)

        self.tray_label = tk.Label(self, text="Tray Selection")
        self.tray_label.pack()

        self.tray_picker = TrayPicker(self, self.datamodel.selected_tray_var, self.handleTraySelection, datamodel.settings.default_tray)
        self.tray_picker.pack()

        self.start_label = tk.Label(self, text="Start Well")
        self.start_label.pack()

        self.combo = ttk.Combobox(self, textvariable=self.datamodel.start_position_var, values=self.pos_choices, state='readonly', width=10)
        self.combo.bind('<<ComboboxSelected>>', self.onChange)
        self.combo.pack()   

        self.pool_label = tk.Label(self, text="Pool Well")
        self.pool_label.pack()

        self.pool_combo = ttk.Combobox(self, textvariable=self.datamodel.pool_position_var, values=self.pos_choices, state='readonly', width=10)  
        self.pool_combo.bind('<<ComboboxSelected>>', self.onChange) 
        self.pool_combo.pack()

        self.pool_check = tk.Checkbutton(self, text="Include Pool", variable=self.datamodel.getOptionVar('pool'), onvalue=1, offvalue=0)
        self.pool_check.pack()

        self.gpf_check = tk.Checkbutton(self, text="Include GPF", variable=self.datamodel.getOptionVar('gpf'), onvalue=1, offvalue=0)
        self.gpf_check.pack()

        self.random_check = tk.Checkbutton(self, text="Randomize", variable=self.datamodel.getOptionVar('random'), onvalue=1, offvalue=0, command=self.onRandomChange)
        self.random_check.pack()

        self.blanks_frame = PreAndPostCheck(self, "Add Blanks", self.datamodel.getOptionVar('pre_blank'), self.datamodel.getOptionVar('post_blank'))
        self.blanks_frame.pack()

        self.qc_frame = PreAndPostCheck(self, "Add QC", self.datamodel.getOptionVar('pre_qc'), self.datamodel.getOptionVar('post_qc'))
        self.qc_frame.pack()

        self.add_blanks_label = tk.Label(self, text="Additional Blank every n samples")
        self.add_blanks_label.pack()

        self.add_blanks_combo = ttk.Combobox(self, values=[str(i) for i in range(51)], textvariable=self.datamodel.blank_every_var, state='readonly')
        self.add_blanks_combo.pack()


        self.test_label = tk.Label(self, text="Test Sample")
        self.test_label.pack()

        self.test_combo = ttk.Combobox(self, values=["None"] + self.datamodel.sample_list, textvariable=self.datamodel.test_sample_var, state='readonly', width=30)
        self.test_combo.option_add('*TCombobox*ListBox.Justify', 'right')
        self.test_combo.pack()
         
        return

    def onRandomChange(self):
        if self.onRandomChange:
            self.onRandomChange()