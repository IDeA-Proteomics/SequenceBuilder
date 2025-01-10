
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

        self.pool_var = tk.IntVar(value=1)
        self.gpf_var = tk.IntVar(value=0)
        self.random_var = tk.IntVar(value=1)
        self.addqc_var = tk.IntVar(value=1)
        self.add_blanks_var = tk.IntVar(value=0)
        self.instrument_var = tk.StringVar(value=self.settings.default_instrument)
        self.method_var = tk.StringVar(value="None")
        self.diadda_selection_var = tk.StringVar(value="DIA")

        self.path_var = tk.StringVar(value = "")      
        self.project_name_var = tk.StringVar(value = "")
        self.count_var = tk.IntVar(value=0)

        return
    
    def openSampleList(self, file_name):
        self.list_reader = SampleListReader.SampleListReader(file_name)
        self.path_var.set(self.list_reader.path)
        self.project_name_var.set(self.list_reader.project_name)
        self.count_var.set(len(self.sample_frame))
        return
    

    @property
    def sample_frame(self):
        return self.list_reader.sample_frame if self.list_reader is not None else None    

        
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
    
    
    def onInstrumentSelection(self):
        self.method_var.set(self.method_list[0] if self.method_list else "None")
        return

    

    

    





