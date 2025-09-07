
import SequenceSettings
from SequenceBuilder import *
from idea_utils import SampleListReader

import pandas as pd
import tkinter as tk
from tkinter import messagebox
import json

class DataModel():

    def __init__(self):

        self.settings = SequenceSettings.AppSettings()

        self.row_labels = "ABCDEFGH"
        # self.position_list = [f"{a}{b}{c}" for a in "RGB" for b in "ABCDEFGH" for c in range(1, 13)]
        self.instrument_data = {}
        self.load_instrument_data()

        self.list_reader = None
        self.sample_frame = None

        self.project_loaded = False

        self.options = {
            'pool':tk.IntVar(value=1),
            'gpf':tk.IntVar(value=0),
            'random':tk.IntVar(value=0),
            'pre_qc':tk.IntVar(value=1),
            'post_qc':tk.IntVar(value=1),
            'pre_blank':tk.IntVar(value=1),
            'post_blank':tk.IntVar(value=1),
            'test_sample':tk.StringVar(value="None"),
            'blank_every':tk.StringVar(value="0"),
            'instrument':tk.StringVar(value=self.settings.default_instrument),
            'method':tk.StringVar(value="None"),
            'diadda':tk.StringVar(value="DIA"),
            'selected_tray':tk.StringVar(value = self.settings.default_tray),
            'start_position':tk.StringVar(value = ""),
            'pool_position':tk.StringVar(value="")
        }

        self.setOption('start_position', self.getTrayPositions(self.getOption('selected_tray'))[0])
        self.setOption('pool_position', self.getTrayPositions(self.getOption('selected_tray'))[-1])

        self.sample_list_path_var = tk.StringVar(value = "")      
        self.project_name_var = tk.StringVar(value = "")

        self.combo_vals = []
        self.pool_vals = []

        self.getAvailablePositions()  ## The app needs the lists for combo boxes

        self.sequence_builder = SequenceBuilder(self)


        return
    
    def load_instrument_data(self):
        with open("instrument_data.json") as jf:
            self.instrument_data = json.load(jf)
        return
    
    def save_instrument_data(self):
        with open("instrument_data.json", 'w') as jf:
            json.dump(self.instrument_data, jf, indent=4)
        return

    
    def onCreateSampleList(self, file_name):
        self.sequence_builder.outputSequence(file_name)
        return
    
    def openSampleList(self, file_name):
        try:
            self.list_reader = SampleListReader.SampleListReader(file_name)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading sample list: \n\n{e}")
            return
        self.sample_list_path_var.set(self.list_reader.path)
        self.project_name_var.set(self.list_reader.project_name)
        ## save original order 
        self.sample_frame = self.list_reader.sample_frame.reset_index(names='order')
        ## randomize
        self.sample_frame = self.sample_frame.sample(frac=1).reset_index(drop=True)
        ##  resort and save the random order
        self.sample_frame = self.sample_frame.sort_values(by='order').reset_index(names='random')
        self.project_loaded = True
        self.sequence_builder.buildSequence()
        return
    
    def randomize(self):
        if self.project_loaded:
            if self.getOption('random'):
                ## rerandomize whenever option goes from 0 to 1
                self.sample_frame.drop('random', axis=1, inplace=True)
                self.sample_frame = self.sample_frame.sample(frac=1).reset_index(drop=True)
                self.sample_frame = self.sample_frame.reset_index(names='random')
        return
    
    def refreshSequence(self):
        return self.sequence_builder.buildSequence()        

    def getOption(self, key):
        return self.options[key].get()
    
    def setOption(self, key, val):
        self.options[key].set(val)
        return
    
    def getOptionVar(self, key):
        return self.options[key]

    # @property
    # def sample_frame(self):
    #     return self.list_reader.sample_frame if self.list_reader is not None else None    
    
    # @property
    # def sample_method(self):
    #     return self.getOption('method')

    @property
    def sample_list_path(self):
        if self.project_loaded:
            return self.sample_list_path_var.get()
        return None

    @property
    def sorted_list(self):
        if self.sample_frame is not None:
            return self.sample_frame.sort_values(by='order')['id'].tolist()
        return []

    @property
    def sample_list(self):
        if self.sample_frame is not None:
            if self.getOption('random') == 1:
                return self.sample_frame.sort_values(by='random')['id'].tolist()
            else:
                return self.sample_frame.sort_values(by='order')['id'].tolist()            
        return []

        
    @property
    def project_name(self):
        return self.project_name_var.get()    
    
    @property
    def sample_count(self):
        if self.project_loaded:
            return len(self.sample_list)
        else:
            return 0
    
    # @property
    # def selected_instrument(self):
    #     return self.instrument_var.get()
    
    # @property
    # def diadda(self):
    #     return self.diadda_selection_var.get()

    @property
    def instrument_list(self):
        return self.instrument_data.keys()

    def getInstrumentData(self, key):
        return self.instrument_data[self.getOption('instrument')][key]
    
    @property
    def method_list(self):
        return self.getInstrumentData('methods')[self.getOption('diadda')]
    
    # @property
    # def selected_tray(self):
    #     return self.selected_tray_var.get()
    
    # @property
    # def start_position(self):
    #     return self.start_position_var.get()
    
    # @property
    # def pool_position(self):
    #     return self.pool_position_var.get()
    
    @property
    def tray_list(self):
        return self.getInstrumentData('trays')
    
    # @property
    # def blank_every(self):
    #     return int(self.blank_every_var.get())
    
    
    def getTrayPositions(self, tray):        
        return [f"{tray}{self.getInstrumentData('tray_separator')}{row}{str(pos)}" for row in self.row_labels for pos in range(1,13)]
    
    
    def onInstrumentSelection(self):
        ### TODO:  This is janky  Figure out a better way to update the start position string based on separator
        sp = self.getOption('start_position')
        t = sp[:1]
        p = sp[2:] if ':' in sp else sp[1:]
        self.setOption('start_position',f"{t}{self.getInstrumentData('tray_separator')}{p}")
        self.setOption('method',self.method_list[0] if self.method_list else "None")
        return
    
    def handleTraySelection(self):
        self.setOption('start_position', self.getOption('selected_tray') + self.getOption('start_position')[1:])        
        self.setOption('pool_position', self.getOption('selected_tray') + self.getOption('pool_position')[1:])
        return
    
    def getAvailablePositions(self):
        self.pos_choices = self.getTrayPositions(self.getOption('selected_tray'))
        self.combo_vals = self.pos_choices[:97-self.sample_count]
        # self.combo.config(values = self.combo_vals)
        if self.sample_count < 96:
            self.pool_vals = [i for i in self.pos_choices if i not in self.getSamplePositions()]
        else:
            second_tray = 'B' if self.getOption('selected_tray') == 'G' else 'G'
            second_tray_list = self.getTrayPositions(second_tray)
            self.pool_vals = [i for i in self.pos_choices + second_tray_list if i not in self.getSamplePositions()]

            if self.sample_count >192:
                third_tray = 'R'
                third_tray_list = self.getTrayPositions(third_tray)
                self.pool_vals = [i for i in self.pos_choices + second_tray_list + third_tray_list if i not in self.getSamplePositions()]
        # self.pool_combo.config(values = self.pool_vals)
        if self.getOption('pool_position') not in self.pool_vals:
            self.setOption('pool_position', self.pool_vals[-1])

        return
    
    def getSamplePositions(self):

        pos_list = self.getTrayPositions(self.getOption('selected_tray'))
        idx = pos_list.index(self.getOption('start_position'))

        if self.sample_count > 96:

            second_tray = 'B' if self.getOption('selected_tray')[:1] == 'G' else 'G'

            second_tray_list = self.getTrayPositions(second_tray)

            pos_list = pos_list + second_tray_list
        
            if self.sample_count > 192:

                third_tray = 'R'

                third_tray_list = self.getTrayPositions(third_tray)

                pos_list = pos_list + third_tray_list
        
        return pos_list[idx:idx+self.sample_count]
    

    def getSequenceDisplay(self):

        df = self.sequence_builder.sequence

        rv = ["{:>3}| {:>5}| {:>24} | {:<5} | {:>24} |\n".format(r[0],r[1],r[2],r[3],r[4]) 
              for r in zip(df.index, df['Sample ID'], df['File Name'], df['Position'] , df['Instrument Method'])]
        
        return rv



    





