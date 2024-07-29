import argparse
from pathlib import Path
import os
import sys
import openpyxl
import random
import glob 
import shutil
import time
import sys
from IDeA_classes import SampleList

parser = argparse.ArgumentParser()
parser.add_argument("sampleList")

parser2 = argparse.ArgumentParser()
parser2.add_argument("-t", "--tray", default = "G")
parser2.add_argument("-s", "--start_index", default = 0)
parser2.add_argument("-p", "--pool_well", default = "H12")
parser2.add_argument("-m", "--method", default = 1)

#args = parser.parse_args(["SchraderJ_021723_Plasma_SampleList.xlsx"])
args = parser.parse_args()

a = SampleList(args.sampleList)
print(a.project_name)
[print(x) for x in a.samplenames]

arg_test = input("""
Modify methods:
-t --tray         default = "G"
-s --start_index  default = 0
-p --pool_well    default = H12
-m --method       default = 1
""")


if arg_test == "":
  print("Handling blank")
  arg2 = parser2.parse_args(["-t", "G"])

if not arg_test == "":
  arg2 = parser2.parse_args(arg_test.split(" "))
  print(arg2)


#Workout method selection here.
method_dic = {
  "1":[
    r"C:\Xcalibur\methods\DIA\60min_5ulLoad_10ulLoop\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221",
    r"C:\Xcalibur\methods\DIA\60min_5ulLoad_10ulLoop\DIA_GPF_{mz_start}_{mz_end}_60min_5ulLoad_10ulLoop_031221"
  ],
  "2":[
    r"C:\Xcalibur\methods\DIA_60min_5ulLoad\DIA_60min_14mz_5ulLoad_040823",
    r"C:\Xcalibur\methods\DIA_60min_5ulLoad\DIA_GPF_{mz_start}_{mz_end}_60min_14mz_5ulLoad_040823"
  ]
}

class InjectionSequence():
  def __init__(self, project, sample_names, tray, start_index, pool_well):
    self.project_name = project
    self.samples = sample_names
    self.tray = tray
    self.pool_well = pool_well
    self.start_index = int(start_index)
    self.positions = [self.get_position(x) for x in range(self.start_index, self.start_index + len(self.samples))]
    self.position_label = (self.get_position(x) for x in range(self.start_index + len(self.samples)))
    self.DIA_path = r"C:\Xcalibur\methods\DIA\60min_5ulLoad_10ulLoop\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221"
    self.GPF_path = r"C:\Xcalibur\methods\DIA\60min_5ulLoad_10ulLoop\DIA_GPF_{mz_start}_{mz_end}_60min_5ulLoad_10ulLoop_031221"
    self.sample_rows = self._pack_samples()
    self.GPF_rows = self._pack_GPFs()
    self.pool_rows = self._pack_pool_runs()
  
  def __str__(self):
        return f'Injection sequence object with {self.project_name} -tray: {self.tray} -start_index:{self.start_index} -pool_well:{self.pool_well}'
    
  
  def get_position(self, index):
    row = int(index/12)
    row_letter = "ABCDEFGH"[row]
    col = str((index % 12) + 1)
    return(row_letter + col)
  
  def _format_filename(self, project_name, sample_number, sample_name):
    return(f'{project_name}_Sample_{sample_number:02d}_{sample_name}')
  
  def _format_row(self, project_name, sample_name, method, tray, position):
    return(f'Unknown,{sample_name},1,D:\\{project_name},{method},,,{tray}{position},10,,0,0,0,1,,,,,,,\n')

  def _pack_samples(self):
    w = []
    for i,sample in enumerate(self.samples):
      filename = self._format_filename(self.project_name, i + 1, sample)
      w.append(self._format_row(self.project_name, filename, self.DIA_path, self.tray, self.positions[i]))
    return(w)
  
  def _pack_GPFs(self):
    w = []
    for i in range(1,7):
      mz_start = 300 + (100*i)
      mz_end = 400 + (100*i)
      filename = f'{self.project_name}_GPF6_{i}'
      f_method = self.GPF_path.format(mz_start = mz_start, mz_end = mz_end)
      w.append(self._format_row(self.project_name, filename, f_method, self.tray, self.pool_well))
    return(w)
  
  def _pack_pool_runs(self):
    w = []
    for i in range(1,4):
      filename = f'{self.project_name}_Pool_{i}'
      w.append(self._format_row(self.project_name, filename, self.DIA_path, self.tray, self.pool_well))
    return(w)
  
  def write_injection_sequence(self, tail = "", dest = ""):
    line1 = 'Bracket Type=4,,,,,,,,,,,,,,,,,,,,\n'
    line2 = 'Sample Type,File Name,Sample ID,Path,Instrument Method,Process Method,Calibration File,Position,Inj Vol,Level,Sample Wt,Sample Vol,ISTD Amt,Dil Factor,L1 Study,L2 Client,L3 Laboratory,L4 Company,L5 Phone,Comment,Sample Name\n'
    data = list(tuple(self.sample_rows)) #Deep copy
    GPF = self.GPF_rows
    pool = self.pool_rows
    half_index = int(len(data)/2)
    pool_index1 = int(len(data)/3)
    pool_index2 = int(len(data)*2/3)
    for i in range(5, -1, -1):
      data.insert(half_index, GPF[i])
    data.insert(pool_index1, pool[0])
    data.insert(int(len(data)*2/3), pool[1])
    data.append(pool[2])
    if not dest == "":
      dest = dest + "/"
    else:
      dest = os.getcwd() + "/"
    with open(f"{dest}{self.project_name}_Injection_Sequence{tail}.csv", "w") as file:
      file.writelines(line1)
      file.writelines(line2)
      file.writelines(data)
    
    print(f"Wrote {self.project_name}_Injection_Sequence_{tail}.csv using -{self.tray}{self.start_index} -{self.tray}{self.pool_well} ")
    #print(f"Wrote {self.project_name}_Injection_Sequence{tail}.csv to {dest} using {self.tray}{self.positions[0]} and {self.pool_well} as Pool")
    del(data)



substr = "_SampleList"

a = SampleList(args.sampleList)
project_name = a.basename.split(substr)[0]
a2 = InjectionSequence(project_name, a.samplenames, arg2.tray, arg2.start_index, arg2.pool_well)
print(project_name)
[print(x) for x in a.samplenames]
print(a2)
a2.write_injection_sequence("", a.dirname)
random.shuffle(a2.sample_rows)
random.shuffle(a2.sample_rows)
random.shuffle(a2.sample_rows)
a2.write_injection_sequence("_BlockRandomized", a.dirname)
