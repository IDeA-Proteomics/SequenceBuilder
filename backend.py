import pandas as pd
import openpyxl
import os

import frontend

class SampleList():

    def __init__(self, front):
        self.front = front
        self.path = "~/Automate/BothnerB_022823_SampleList.xlsx"
        self.abs_path = os.path.abspath(self.path)
        self.project_name = "BothnerB_022823"

        self.data = pd.read_excel(self.path, engine='openpyxl')
        self.list = pd.DataFrame(data=self.data[['sample number', 'sample name']].values, columns=['number', 'name'])
        self.list['method'] = "None"
        self.list['position'] = "NA"

        self.sequence = pd.DataFrame(
            columns=[
                'Sample Type' , 
                'File Name' , 
                'Sample ID' , 
                'Path' , 
                'Instrument Method' , 
                'Process Method' , 
                'Calibration File' , 
                'Position' , 
                'Inj Vol' , 
                'Level' , 
                'Sample Wt' , 
                'Sample Vol' , 
                'ISTD Amt' , 
                'Dil Factor' , 
                'L1 Study' , 
                'L2 Client' , 
                'L3 Laboratory' , 
                'L4 Company' , 
                'L5 Phone' , 
                'Comment' , 
                'Sample Name'
                ],
                index=(range(self.getSampleCount()))
            )

        return
    
    def buildSequence(self):

        self.sequence['File Name'] = self.project_name + '/' + self.list['name']
        self.sequence['Sample ID'] = self.list['number']
        self.sequence['Path'] = "C:/Data/" + self.project_name 
        self.sequence['Instrument Method'] = self.getMethod()

        self.sequence['Sample Name'] = self.list['name']
        print(self.sequence)

        return
    
    def reBuildList(self):

        self.list['position'] = self.front.getSamplePositions()

        return
    
    def getMethod(self):
        return self.front.getMethod()
    
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
        

if (__name__ == "__main__"):
    frontend.showSeqFE()
        
    
        
    
