import pandas as pd
import openpyxl
import os

import frontend

class SampleList():

    def __init__(self, front):
        self.front = front
        self.path = "~/Automate/BothnerB_022823_SampleList.xlsx"
        self.abs_path = os.path.abspath(self.path)
        self.project_name = "Not Yet"

        self.data = pd.read_excel(self.path, engine='openpyxl')
        self.list = pd.DataFrame(data=self.data[['sample number', 'sample name']].values, columns=['number', 'name'])
        self.list['method'] = "None"
        self.list['position'] = "NA"

        return
    
    def reBuildList(self):

        self.list['position'] = self.front.getSamplePositions()

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
        
    
        
    
