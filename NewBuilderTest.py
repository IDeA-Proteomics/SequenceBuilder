import SampleList
import SequenceBuilder
import datamodel
import json

def main():

    
    with open("instrument_data.json") as jf:
        datamodel.instrument_data = json.load(jf)

    sample_list = SampleList.SampleList()
    sample_list.readFile(r'C:\IDeA_Scripts\TestData\BothnerB_022823_SampleList.xlsx')
    positions = datamodel.position_list[:56]
    print("-----------------------")
    builder = SequenceBuilder.SequenceBuilder()
    sequence = builder.build(sample_list, positions, 
        instrument="Exploris2",
        method= "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DIA_12mz_15k_60min_5ulLoad_10ulLoop_052423",
        blanks= 20,
        qc= True, 
        pool_well= 'BH12',
        gpf= False,
        random= False,
        inj_vol= 8,
        test= True
    )

    builder.outputSequence()


if __name__ == '__main__':
    main()