import pandas as pd
import openpyxl
from openpyxl import load_workbook
import os
import re

import frontend

class SampleList():

    def __init__(self, front, filename):
        self.front = front
        # self.path = "~/Automate/BothnerB_022823_SampleList.xlsx"
        self.path = filename

        self.abs_path = os.path.abspath(self.path)

        split_name = self.abs_path.split('\\')[-1]
        proj_pattern = r'([^/]+_\d{6}.*)(?=_SampleList\.xlsx)'
        match = re.match(proj_pattern, split_name)

        self.project_name = match.group(1) if match else "Bad Name"

        ####  Examine XLS file.  Find row with headers and last sample (first empty after samples)

        wb = load_workbook(self.abs_path, data_only=True)
        sh = wb.worksheets[0]

        self.head_row = None
        self.last_row = None
        for i in range(1, sh.max_row + 1):
            if self.head_row == None and sh.cell(row = i, column=1).value == "sample number":
                self.head_row = i
            if all([cell.value is None for cell in sh[i]]):
                if self.head_row != None and i > self.head_row:
                    self.last_row = i
                    break
        if self.last_row == None:
            self.last_row = sh.max_row + 1


        self.data = pd.read_excel(self.abs_path, engine='openpyxl', skiprows=self.head_row - 1, nrows=(self.last_row - self.head_row))
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
    
    def reBuildSequence(self):
        self.sequence['Sample Type'] = "Unknown"
        self.sequence['File Name'] = self.project_name + '/' + str(self.list['name'])
        self.sequence['Sample ID'] = self.list['number']
        self.sequence['Path'] = "C:/Data/" + self.project_name 
        self.sequence['Instrument Method'] = self.getMethod()
        self.sequence['Position'] = self.list['position']
        self.sequence['Inj Vol'] = "10.0"

        self.sequence['Sample Name'] = self.list['name']
        # print(self.sequence)

        return
    
    def outputSequence(self):
        self.reBuildSequence()
        template = "Bracket Type = 4\n{}"
        with open('C:\\Automate\\sequence.csv', 'wb') as fp:
            fp.write(template.format(self.sequence.to_csv(index=False)).encode("utf-8"))
    
    def reBuildList(self):

        self.list['position'] = self.front.getSamplePositions()

        return
    
    def getMethod(self):
        return self.front.getMethod()
    
    def getSampleCount(self):
        return len(self.data)
    
    def getSequenceCount(self):
        return len(self.sequence)

    def getListData(self, data, index):
        return self.list[data][index]
     
    def getSequenceData(self, data, index):
        return self.sequence[data][index]
    
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
        
    
        
    
