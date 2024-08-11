import pandas as pd
import openpyxl
import os

class SampleList():

    def __init__(self):
        self.path = "~/Automate/BothnerB_022823_SampleList.xlsx"
        self.abs_path = os.path.abspath(self.path)
        self.project_name = "Not Yet"

        self.data = pd.read_excel(self.path, engine='openpyxl')
        self.list = self.data[['sample number', 'sample name']].copy()

        self.list['method'] = "No_Method_Selected"

        return
    
    def getSampleCount(self):
        return len(self.data)
    
    def getData(self, data, index):
        return self.list[data][index]
    
    def getSampleName(self, index):
        if index < self.getSampleCount():
            return self.list['sample name'][index]
        else:
            return ""
        
    def getSampleNumber(self, index):
        if index < self.getSampleCount():
            return self.list['sample number'][index]
        else:
            return 'X'
        
    
        
    
