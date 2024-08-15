import pandas as pd
import openpyxl
from openpyxl import load_workbook
import os
import re

import frontend

class SampleList():

    def __init__(self, front, filename):
        self.front = front
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
    
    def buildGPF(self):
        gpf_seq = pd.DataFrame(
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
                index=(range(6))
            )
        
        w = []
        for i in range(1,7):
            mz_start = 300 + (100*i)
            mz_end = 300 + (100*i)
            filename = f'{self.project_name}_GPF6_{i}'
            gpf_method_template = r"C:\Xcalibur\methods\DIA\60min_5ulLoad_10ulLoop\DIA_GPF_{mz_start}_{mz_end}_60min_5ulLoad_10ulLoop_031221"
            meth_name = gpf_method_template.format(mz_start=mz_start, mz_end=mz_end)
            w.append({'Sample Type':'unknown', 
                      'File Name':filename, 
                      'Sample ID':'GPF_' + str(i), 
                      'Path':"C:/Data/" + self.project_name, 
                      'Instrument Method':meth_name,
                      'Inj Vol':'10.0',
                      'Sample Name':"GPF_" + str(i)
                      })
        df = pd.DataFrame.from_records(w,index=range(6))
        return df
    
    def reBuildSequence(self):
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
        if self.front.getRandom() == 1:
            temp_list = self.list.sample(frac=1).reset_index(drop=True)
        else:
            temp_list = self.list
        self.sequence['Sample Type'] = "Unknown"
        self.sequence['File Name'] = [self.project_name + '/' + str(x) for x in temp_list['name']]
        self.sequence['Sample ID'] = temp_list['number']
        self.sequence['Path'] = "C:/Data/" + self.project_name 
        self.sequence['Instrument Method'] = self.getMethod()
        self.sequence['Position'] = temp_list['position']
        self.sequence['Inj Vol'] = "10.0"

        self.sequence['Sample Name'] = temp_list['name']

        halfway = int(len(self.sequence)/2)
        
        if self.front.getGPF() == 1:
            self.sequence = pd.concat([self.sequence.iloc[:halfway], self.buildGPF(), self.sequence.iloc[halfway:]]).reset_index(drop=True)



        return
    
    def outputSequence(self):
        self.reBuildSequence()
        template = "Bracket Type=4,\n"
        fname = "Z:\\David\\{}_Injection_Sequence.csv".format(self.project_name)
        with open(fname, 'w') as fp:
            fp.write(template)
        self.sequence.to_csv(fname, index=False, mode='a')

        
        self.buildGPF()
        return
    
    
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
        
    
        
    
