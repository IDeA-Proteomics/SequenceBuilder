
import SequenceSettings
from idea_utils import SampleListReader

import pandas as pd
import tkinter as tk
import json

class DataModel():

    def __init__(self):

        self.settings = SequenceSettings.AppSettings()

        self.row_labels = "ABCDEFGH"
        # self.position_list = [f"{a}{b}{c}" for a in "RGB" for b in "ABCDEFGH" for c in range(1, 13)]
        self.instrument_data = {}
        with open("instrument_data.json") as jf:
            self.instrument_data = json.load(jf)

        self.list_reader = None
        self.sample_frame = None

        self.project_loaded = False

        self.options = {
            'pool':tk.IntVar(value=1),
            'gpf':tk.IntVar(value=0),
            'random':tk.IntVar(value=1),
            'pre_qc':tk.IntVar(value=1),
            'post_qc':tk.IntVar(value=1),
            'pre_blank':tk.IntVar(value=1),
            'post_blank':tk.IntVar(value=1),
        }

        self.test_sample_var = tk.StringVar(value="None")
        self.blank_every_var = tk.StringVar(value="0")
        self.instrument_var = tk.StringVar(value=self.settings.default_instrument)
        self.method_var = tk.StringVar(value="None")
        self.diadda_selection_var = tk.StringVar(value="DIA")

        self.path_var = tk.StringVar(value = "")      
        self.project_name_var = tk.StringVar(value = "")
        self.count_var = tk.IntVar(value=0)

        self.selected_tray_var = tk.StringVar(value = self.settings.default_tray)

        self.combo_vals = []
        self.pool_vals = []
        self.start_position_var = tk.StringVar(value = self.getTrayPositions(self.selected_tray)[0])
        self.pool_position_var = tk.StringVar(value=self.getTrayPositions(self.selected_tray)[-1])
        self.getAvailablePositions()


        return
    
    def openSampleList(self, file_name):
        self.list_reader = SampleListReader.SampleListReader(file_name)
        self.path_var.set(self.list_reader.path)
        self.project_name_var.set(self.list_reader.project_name)
        self.sample_frame = self.list_reader.sample_frame.reset_index(names='order')
        self.count_var.set(len(self.sample_frame))
        self.project_loaded = True
        return
    
    def randomize(self):
        if self.project_loaded:
            if self.getOption('random'):
                self.sample_frame = self.sample_frame.sample(frac=1).reset_index(drop=True)
            else:
                self.sample_frame = self.sample_frame.sort_values(by='order').reset_index(drop=True)
        return
    
    def getOption(self, key):
        if self.options[key].get() == 0:
            return False
        return True
    
    def getOptionVar(self, key):
        return self.options[key]

    # @property
    # def sample_frame(self):
    #     return self.list_reader.sample_frame if self.list_reader is not None else None    
    
    @property
    def sample_list(self):
        return self.sample_frame['id'].tolist() if self.sample_frame is not None else None

        
    @property
    def project_name(self):
        return self.project_name_var.get()    
    
    @property
    def sample_count(self):
        return self.count_var.get()
    
    @property
    def selected_instrument(self):
        return self.instrument_var.get()
    
    @property
    def diadda(self):
        return self.diadda_selection_var.get()
    
    @property
    def method_list(self):
        return self.instrument_data[self.selected_instrument]['methods'][self.diadda]
    
    @property
    def selected_tray(self):
        return self.selected_tray_var.get()
    
    @property
    def start_position(self):
        return self.start_position_var.get()
    
    @property
    def pool_position(self):
        return self.pool_position_var.get()
    
    @property
    def tray_list(self):
        return self.instrument_data[self.selected_instrument]['trays']
    
    @property
    def blank_every(self):
        return int(self.blank_every_var.get())
    
    
    def getTrayPositions(self, tray):        
        return [f"{tray}{self.instrument_data[self.selected_instrument]['tray_separator']}{row}{str(pos)}" for row in self.row_labels for pos in range(1,13)]
    
    
    def onInstrumentSelection(self):
        ### TODO:  This is janky  Figure out a better way to update the start position string based on separator
        t = self.start_position[:1]
        p = self.start_position[2:] if ':' in self.start_position else self.start_position[1:]
        self.start_position_var.set(f"{t}{self.instrument_data[self.selected_instrument]['tray_separator']}{p}")
        self.method_var.set(self.method_list[0] if self.method_list else "None")
        return
    
    def handleTraySelection(self):
        self.start_position_var.set(self.selected_tray + self.start_position[1:])
        
        self.pool_position_var.set(self.selected_tray + self.pool_position[1:])

        return
    
    def getAvailablePositions(self):
        self.pos_choices = self.getTrayPositions(self.selected_tray)
        self.combo_vals = self.pos_choices[:97-self.sample_count]
        # self.combo.config(values = self.combo_vals)
        if self.sample_count < 96:
            self.pool_vals = [i for i in self.pos_choices if i not in self.getSamplePosistions()]
        else:
            second_tray = 'B' if self.selected_tray == 'G' else 'G'
            second_tray_list = self.datamodel.getTrayPositions(second_tray)
            self.pool_vals = [i for i in self.pos_choices + second_tray_list if i not in self.getSamplePosistions()]
        # self.pool_combo.config(values = self.pool_vals)
        if self.pool_position not in self.pool_vals:
            self.pool_position_var.set(self.pool_vals[-1])

        return
    
    def getSamplePosistions(self):

        pos_list = self.getTrayPositions(self.selected_tray)
        idx = pos_list.index(self.start_position)

        if self.sample_count > 96:

            second_tray = 'B' if self.selected_tray[:1] == 'G' else 'G'

            second_tray_list = self.getTrayPositions(second_tray)

            pos_list = pos_list + second_tray_list
        
        return pos_list[idx:idx+self.sample_count]

    

    

    





