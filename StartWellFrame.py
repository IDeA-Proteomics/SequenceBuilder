

import SequenceSettings as settings
import tkinter as tk
from tkinter import ttk

import datamodel
import json

class TrayPicker(tk.Frame):

    def __init__(self, parent, onChange, initial_val = None):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)
        self.select_var = tk.StringVar()

        buttons = [
            tk.Radiobutton(self, text="", var=self.select_var, value="R", fg='black', bg='red', width = 4, command=onChange),
            tk.Radiobutton(self, text="", var=self.select_var, value="G", fg='black', bg='green', width = 4, command=onChange),
            tk.Radiobutton(self, text="", var=self.select_var, value="B", fg = 'black', bg='blue', width = 4, command=onChange),
            tk.Radiobutton(self, text="", var=self.select_var, value="Y", fg = 'black', bg='yellow', width = 4, command=onChange)
        ]
        for button in buttons:
            button.pack(side = tk.LEFT)
            if button.cget('value') == settings.default_tray if initial_val is None else initial_val:
                button.select()

        return
    
    def get(self):
        return self.select_var.get()
    


class StartWellFrame(tk.Frame):

    def handleTraySelection(self):
        self.start_position.set(self.selected_tray + self.start_position.get()[1:])
        
        self.pool_position.set(self.selected_tray + self.pool_position.get()[1:])
        self.rebuildSelections()
        self.onStartChangeCallback()
        return
    
    def buildSelections(self):
        self.pos_choices = self.getTrayPositions(self.selected_tray)
        self.combo_vals = self.pos_choices[:97-self.count]
        self.combo.config(values = self.combo_vals)
        if self.count < 96:
            self.pool_vals = [i for i in self.pos_choices if i not in self.getSamplePosistions()]
        else:
            second_tray = 'B' if self.selected_tray == 'G' else 'G'
            second_tray_list = self.getTrayPositions(second_tray)
            self.pool_vals = [i for i in self.pos_choices + second_tray_list if i not in self.getSamplePosistions()]
        self.pool_combo.config(values = self.pool_vals)
        if self.pool_position.get() not in self.pool_vals:
            self.pool_position.set(self.pool_vals[-1])

        return
    
    def onChange(self, event = None):
        self.rebuildSelections()
        self.onStartChangeCallback()
        return

    
    def getSamplePosistions(self):

        pos_list = self.getTrayPositions(self.selected_tray)
        idx = pos_list.index(self.start_position.get())

        if self.count > 96:

            second_tray = 'B' if self.tray_selection.get()[:1] == 'G' else 'G'

            second_tray_list = self.getTrayPositions(second_tray)

            pos_list = pos_list + second_tray_list
        
        return pos_list[idx:idx+self.count]
    
    def getPoolWell(self):
        return self.pool_position.get()

    def __init__(self, parent, count, onStartChange):
        self.parent = parent
        self.count = count
        self.onStartChangeCallback = onStartChange
        

        self.pos_choices = self.getTrayPositions(self.selected_tray)
        self.start_position = tk.StringVar(value = self.pos_choices[0])
        self.pool_position = tk.StringVar(value = self.pos_choices[-1])

        tk.Frame.__init__(self, self.parent)

        self.tray_label = tk.Label(self, text="Tray Selection")
        self.tray_label.pack()

        self.tray_picker = TrayPicker(self, self.handleTraySelection)
        self.tray_picker.pack()

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
    
    @property
    def selected_tray(self):
        return self.tray_picker.get()
    
    
    def getTrayPositions(self, tray):        
        return [f"{tray}{datamodel.instrument_data[datamodel.selected_instrument]['tray_separator']}{row}{str(pos)}" for row in datamodel.row_labels for pos in range(1,13)]
    

    def setCount(self, count):
        self.count = count
        self.onChange()

    