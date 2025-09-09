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
                          self.datamodel.getInstrumentData('blank_loc'), 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          f'Rinse_{which if which is not None else self.rinse_count}'
                          )
    
    def createBlank(self, which=None):
        if which is None:
            self.blank_count += 1
        return self.createLine(f"Blank_{which if which is not None else self.blank_count}", 
                          f'B{self.blank_count}', 
                          self.data_path, 
                          self.datamodel.getInstrumentData('methods')['blank'], 
                          self.datamodel.getInstrumentData('blank_loc'), 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          f'Blank_{which if which is not None else self.blank_count}'
                          )
    
    def createEnd(self):
        return self.createLine("End", 
                          'E', 
                          self.data_path, 
                          self.datamodel.getInstrumentData('methods')['end'], 
                          self.datamodel.getInstrumentData('blank_loc'), 
                          str(self.datamodel.getInstrumentData('loop_vol')), 
                          "End"
                          )
    
    def createPool(self):
        self.pool_count += 1
        return self.createLine(f'{self.datamodel.project_name}_Pool_{self.pool_count}', 
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
                            self.datamodel.getInstrumentData('qc_path'), 
                            self.datamodel.getInstrumentData('methods')['QC'],
                            self.datamodel.getInstrumentData('qc_loc'), 
                            str(self.datamodel.getInstrumentData('loop_vol')), 
                            f'QC_{self.qc_count}' if which is None else f'QC_{which}'
                            )

    
    def createSample(self, sample_name, sample_number, position, volume=None):
        volume = volume if volume is not None else self.datamodel.getInstrumentData('loop_vol')
        return self.createLine(f"{str(sample_name)}", 
                            str(sample_number), 
                            self.data_path, 
                            self.datamodel.getOption('method'),
                            position, 
                            str(volume), 
                            str(sample_name)
                            )





    
    def buildSequence(self):
        self.pool_count = 0
        self.blank_count = 0
        self.rinse_count = 0
        self.qc_count = 0
            
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
            self.addToSequence(self.createSample(ts+'_TEST', 'T', positions[ts], 2.0))
        
        ###  pre-qc
        if self.datamodel.getOption('pre_qc'):
            self.addToSequence(self.createRinse(which='pre-qc'))
            self.addToSequence(self.createBlank(which='pre-qc'))
            self.addToSequence(self.createQC(which='pre'))

        ###  pre-blank
        if self.datamodel.getOption('pre_blank'):
            self.addToSequence(self.createRinse(which='pre'))
            self.addToSequence(self.createBlank(which='pre'))

        ###  Samples       
        for i, s in enumerate(self.datamodel.sample_list):  ## sample_list will be randomized by datamodel if necessary
            self.addToSequence(self.createSample(s, i, positions[s]))
            ### if time for pool
            if(self.datamodel.getOption('pool')):
                if i+1 == int(self.datamodel.sample_count * ((self.pool_count + 1) / 3)):
                    self.addToSequence(self.createPool())
            ### if time for extra blank
            if int(self.datamodel.getOption('blank_every')) != 0:
                if (i+1) % (int(self.datamodel.getOption('blank_every'))) == 0:
                    self.addToSequence(self.createRinse())
                    self.addToSequence(self.createBlank())

        ###  post-qc
        if self.datamodel.getOption('post_qc'):
            self.addToSequence(self.createRinse(which='post-qc'))            
            self.addToSequence(self.createBlank(which='post-qc'))
            self.addToSequence(self.createQC(which='post'))

        ###  post-blank
        if self.datamodel.getOption('post_blank'):
            self.addToSequence(self.createRinse(which='post'))
            self.addToSequence(self.createBlank(which='post'))

        ###  end method
        self.addToSequence(self.createEnd())
        

        return self.sequence
    
    def outputSequence(self, filename):
        template = "Bracket Type=4,\n"
        if not filename:
            return
        with open(filename, 'w') as fp:
            fp.write(template)
        self.sequence.to_csv(filename, index=False, mode='a')
        
        return

    

