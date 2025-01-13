import pandas as pd
import os



class SequenceBuilder(object):

    def __init__(self, datamodel):
        self.datamodel = datamodel

        
        
        self.pool_count = 0
        self.blank_count = 0
        self.rinse_count = 0
        self.qc_count = 0

        self.data_path = "D:\\Data"

        self.buildSequence()

        return
    
    def addToSequence(self, line):
        self.sequence.loc[len(self.sequence)] = line
        return
    
    def createLine(self, filename, sample_id, path, method, position, inj_vol, sample_name):
        line = {}
        line['Sample Type'] = 'Unknown'
        line['File Name'] = filename
        line['Sample ID'] = sample_id
        line['Path'] = path
        line['Instrument Method'] = method
        line['Position'] = position
        line['Inj Vol'] = inj_vol
        line['Sample Name'] = sample_name
        return line
    
    def createRinse(self, which=None):
        if which is None:
            self.rinse_count += 1
        return self.createLine(f"Rinse_{which if which is not None else self.rinse_count}", 
                          f'R{self.rinse_count}', 
                          self.data_path, 
                          self.datamodel.getInstrumentData('methods')['rinse'], 
                          'G1', 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          f'Rinse_{which if which is not None else self.rinse_count}'
                          )
    
    def createBlank(self, which=None):
        if which is None:
            self.blank_count += 1
        return self.createLine(f"Blank_{which if which is not None else self.blank_count}", 
                          f'R{self.blank_count}', 
                          self.data_path, 
                          self.datamodel.getInstrumentData('methods')['blank'], 
                          'G1', 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          f'Blank_{which if which is not None else self.blank_count}'
                          )
    
    def createEnd(self):
        return self.createLine("End", 
                          'E', 
                          self.data_path, 
                          self.datamodel.getInstrumentData('methods')['end'], 
                          'G1', 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          "End"
                          )
    
    def createPool(self):
        return self.createLine(f'{self.project_name}_Pool_{self.pool_count}', 
                          f'Pool_{self.pool_count}', 
                          self.data_path, 
                          self.datamodel.getOption('method'), 
                          self.datamodel.getOption('pool_position'), 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          f'Pool_{self.pool_count}'
                          )
    
    def createQC(self, which=None):
        if which is None:
            self.qc_count += 1
        return self.createLine("QC_"+ self.datamodel.getInstrumentData('name') +"_JJN3_iRT_" + ("pre_" if which == "pre" else "post_" if which == "post" else ('mid_' + str(self.qc_count) + '_')) + self.datamodel.project_name + "_DDA", 
                            f'QC{self.qc_count}' if which is None else f'QC_{which}', 
                            self.data_path, 
                            self.datamodel.getInstrumentData('methods')['QC'],
                            f"R{self.datamodel.getInstrumentData('tray_separator')}A1", 
                            str(self.datamodel.getInstrumentData('loop_vol')), 
                            f'QC_{self.qc_count}' if which is None else f'QC_{which}'
                            )

    
    def createSample(self, sample_name, sample_number, position):
        return self.createLine(f"{self.datamodel.project_name}_{str(sample_name)}", 
                            str(sample_number), 
                            self.data_path, 
                            self.datamodel.getOption('method'),
                            position, 
                            str(self.datamodel.getInstrumentData('loop_vol')), 
                            str(sample_name)
                            )





    
    def buildSequence(self):
            
        self.data_path = "D:\\" + self.datamodel.project_name
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
            )
        
        ###  Get sample_frame and add column for positions
        # sample_frame = self.datamodel.sample_frame
        positions = dict(zip(self.datamodel.sorted_list, self.datamodel.getSamplePositions()))
        # sample_frame['position'] = sample_frame['id'].map(positions)

        ###  Check for test sample and add it
        ts = self.datamodel.getOption('test_sample')                
        if ts != "None":
            self.addToSequence(self.createSample(ts+'_TEST', 'T', positions[ts]))

        ###  pre-blank
        if self.datamodel.getOption('pre_blank'):
            self.addToSequence(self.createBlank(which='pre'))
        
        ###  pre-qc
        if self.datamodel.getOption('pre_qc'):
            self.addToSequence(self.createQC(which='pre'))
            self.addToSequence(self.createBlank(which='pre-q'))

        ###  Samples       
        for i, s in enumerate(self.datamodel.sample_list):  ## sample_list will be randomized by datamodel if necessary
            self.addToSequence(self.createSample(s, i, positions[s]))

        ###  post-qc
        if self.datamodel.getOption('post_qc'):
            self.addToSequence(self.createBlank(which='post-q'))
            self.addToSequence(self.createQC(which='post'))

        ###  post-blank
        if self.datamodel.getOption('post_blank'):
            self.addToSequence(self.createBlank(which='post'))
        

        return
    

    




# class OldSequenceBuilder(object):

#     def build(self, instrument_data, samples, project_name, positions, instrument=None, method=None, blanks=0, qc=False, pool_well=None, gpf=False, inj_vol=2, test=False):

#         self.instrument_data = instrument_data
#         self.samples = samples
#         self.project_name = project_name
#         self.sample_count = len(self.sample_list)        
#         self.path = "D:\\" + self.project_name
#         self.method = method
#         self.instrument = instrument
#         self.inj_vol = inj_vol
#         self.pool_well = pool_well
#         self.test = test
#         self.blanks = blanks
#         self.qc = qc
#         self.gpf = gpf
#         self.positions = positions

#         self.pool_count = 1
#         self.blank_count = 1
#         self.rinse_count = 1
#         self.qc_count = 1

#         # ###  Randomize samples if necessary and convert to dict
#         # if self.random:
#         #     self.samples = self.sample_list.sample(frac=1).reset_index(names='order').to_dict('index')
#         # else:
#         #     self.samples = self.sample_list.reset_index(names='order').to_dict('records')  

#         ###  Create empty data frame for sequence
#         self.sequence = pd.DataFrame(
#             columns=[
#                 'Sample Type' , 
#                 'File Name' , 
#                 'Sample ID' , 
#                 'Path' , 
#                 'Instrument Method' , 
#                 'Process Method' , 
#                 'Calibration File' , 
#                 'Position' , 
#                 'Inj Vol' , 
#                 'Level' , 
#                 'Sample Wt' , 
#                 'Sample Vol' , 
#                 'ISTD Amt' , 
#                 'Dil Factor' , 
#                 'L1 Study' , 
#                 'L2 Client' , 
#                 'L3 Laboratory' , 
#                 'L4 Company' , 
#                 'L5 Phone' , 
#                 'Comment' , 
#                 'Sample Name'
#                 ],
#             )

#         ###  Stuff before the samples
#         ### Add Test sample if selected
#         if self.test:
#             ###  Find first sample and make test entry
#             for sample in self.samples:
#                 if sample['order'] == 0:
#                     test = sample
#                     test['Sample Type'] = 'Unknown'
#                     test['File Name'] = self.project_name + '_' + str(sample['name']) + '_TEST'
#                     test['Sample ID'] = 'TEST'
#                     test['Path'] = self.path
#                     test['Instrument Method'] = self.method
#                     test['Position'] = self.positions[sample['order']]
#                     test['Inj Vol'] = '2.0'
#                     test['Sample Name'] = sample['name'] + '_TEST'
#                     self.addToSequence(test)
#                     break
#         ### Add blanks and QC if selected
#         self.addToSequence(self.createRinse())
#         self.addToSequence(self.createBlank())
#         self.addToSequence(self.createQC('pre'))
#         self.addToSequence(self.createRinse())
#         self.addToSequence(self.createBlank())

#         ### iterate through samples and add to sequence
#         for i in range(self.sample_count):
#             sample = self.samples[i]
#             ### Add Sample
#             sample['Sample Type'] = 'Unknown'
#             sample['File Name'] = self.project_name + '_' + str(sample['name'])
#             sample['Sample ID'] = str(sample['number'])
#             sample['Path'] = self.path
#             sample['Instrument Method'] = self.method
#             sample['Position'] = self.positions[sample['order']]
#             sample['Inj Vol'] = str(inj_vol)
#             sample['Sample Name'] = str(sample['name'])
#             self.addToSequence(sample)

#             ### If pool selected and time for pool add pool
#             if i == self.sample_count * (self.pool_count / 3):
#                 self.addToSequence(self.createPool())

#             ### If GPF selected and time for GPF add GPF


#             ### if extra blanks check count and add blank
#             if (i+1) % self.blanks == 0:
#                 self.addToSequence(self.createRinse())
#                 self.addToSequence(self.createBlank())
#                 self.addToSequence(self.createQC())
#                 self.addToSequence(self.createRinse())
#                 self.addToSequence(self.createBlank())

#         ### Add end QC and Blanks
#         self.addToSequence(self.createRinse())
#         self.addToSequence(self.createBlank())
#         self.addToSequence(self.createQC('post'))
#         self.addToSequence(self.createRinse())
#         self.addToSequence(self.createBlank())

                
#         ### return the sequence frame    
#         return self.sequence

#     def addToSequence(self, sample):
#         self.sequence.loc[len(self.sequence)] = sample
#         return



#     def createPool(self):
#         pool = {}
#         pool['Sample Type'] = 'Unknown'
#         pool['File Name'] = f'{self.project_name}_Pool_{self.pool_count}'
#         pool['Sample ID'] = f'Pool_{self.pool_count}'
#         pool['Path'] = self.path
#         pool['Instrument Method'] = self.method
#         pool['Position'] = self.pool_well
#         pool['Inj Vol'] = str(self.inj_vol)
#         pool['Sample Name'] = f'Pool_{self.pool_count}'
#         self.pool_count += 1
#         return pool


#     def createBlank(self):
#         blank = {}
#         blank['Sample Type'] = 'Unknown'
#         blank['File Name'] = f'Blank_{self.blank_count}'
#         blank['Sample ID'] = f'B{self.blank_count}'
#         blank['Path'] = self.path
#         blank['Instrument Method'] = self.instrument_data[self.instrument]['methods']['blank']
#         blank['Position'] = 'G1'
#         blank['Inj Vol'] = str(self.instrument_data[self.instrument]['loop_vol'])
#         blank['Sample Name'] = f'Blank_{self.blank_count}'
#         self.blank_count += 1
#         return blank

#     def createQC(self, which=None):
#         qcrun = {}
#         qcrun['Sample Type'] = 'Unknown'
#         qcrun['File Name'] = "QC_"+ self.instrument_data[self.instrument]['name'] +"_JJN3_iRT_" + ("pre_" if which == "pre" else "post_" if which == "post" else ('mid_' + str(self.qc_count) + '_')) + self.project_name + "_DDA"
#         qcrun['Sample ID'] = f'QC{self.qc_count}' if which is None else f'QC_{which}'
#         qcrun['Path'] = self.path
#         qcrun['Instrument Method'] = self.instrument_data[self.instrument]['methods']['QC']
#         qcrun['Position'] = 'RA1'
#         qcrun['Inj Vol'] = str(self.instrument_data[self.instrument]['loop_vol'])
#         qcrun['Sample Name'] = f'QC_{self.qc_count}' if which is None else f'QC_{which}'
#         if which is None:
#             self.qc_count += 1
#         return qcrun

#     def createRinse(self):
#         rinse = {}
#         rinse['Sample Type'] = 'Unknown'
#         rinse['File Name'] = f"Rinse_{self.rinse_count}"
#         rinse['Sample ID'] = f'R{self.rinse_count}'
#         rinse['Path'] = self.path
#         rinse['Instrument Method'] = self.instrument_data[self.instrument]['methods']['rinse']
#         rinse['Position'] = 'G1'
#         rinse['Inj Vol'] = str(self.instrument_data[self.instrument]['loop_vol'])
#         rinse['Sample Name'] = f'Rinse_{self.rinse_count}'
#         self.rinse_count += 1
#         return rinse

#     def createEnd(self):
#         end = {}
#         end['Sample Type'] = 'Unknown'
#         end['File Name'] = "End"
#         end['Sample ID'] = 'E'
#         end['Path'] = self.path
#         end['Instrument Method'] = self.instrument_data[self.instrument]['methods']['end']
#         end['Position'] = 'G1'
#         end['Inj Vol'] = str(self.instrument_data[self.instrument]['loop_vol'])
#         end['Sample Name'] = 'End'
#         return end

#     def outputSequence(self, path):
#         template = "Bracket Type=4,\n"
#         fname = "{}\\{}_Injection_Sequence.csv".format(os.path.dirname(path), self.project_name)
#         iname = "{}_Injection_Sequence.csv".format(self.project_name)
#         # fname = self.front.askSaveAsName(os.path.dirname(self.abs_path), iname)
#         if not fname:
#             fname = "{}\\{}_Injection_Sequence.csv".format(os.path.dirname(path), self.project_name)
#         with open(fname, 'w') as fp:
#             fp.write(template)
#         self.sequence.to_csv(fname, index=False, mode='a')
#         # self.front.onExit()
        
#         return


