import pandas as pd
import tkinter as tk



instrument_data = {
    'Exploris1' : {
        'name' : 'X1',
        'methods' : {
            'DDA' : [],
            'DIA' : ["C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop\\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221"],
            'QC': "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423",
            'blank': "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423",
            'rinse': "C:\\Xcalibur\\methods\\Sawtooth_wash_DDA_30min",
            'end': "C:\\Xcalibur\\methods\\MeOH_Sawtooth__DDA_10min_end_on_80"
        },
        'loop_vol': 10        
    },
    'Exploris2' : {
        'name' : 'X2',
        'methods' : {
            'DDA' : [],
            'DIA' : ["C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop\\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221"],
            'QC': "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423",
            'blank': "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423",
            'rinse': "C:\\Xcalibur\\methods\\Sawtooth_wash_DDA_30min",
            'end': "C:\\Xcalibur\\methods\\Methanol_wash_10min_end_on_90_111523"
        },
        'loop_vol': 10        
    },
    'Eclipse1' : {
        'name' : 'E1',
        'methods' : {
            'DDA' : [],
            'DIA' : [],
            'QC': "",
            'blank': "",
            'rinse': "",
            'end': ""
        },
        'loop_vol': 20        
    },
    'Eclipse2' : {
        'name' : 'E2',
        'methods' : {
            'DDA' : ["C:\\Xcalibur\\methods\\ul_pickup_60minLCMSMS_020224"],
            'DIA' : ["C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_20ulLoop_ulPickup\\DIA_12mz_15k_60min_5ulLoad_20ulLoop_052423"],
            'QC': "C:\\Xcalibur\\methods\\ul_pickup_60minLCMSMS_070723",
            'blank': "C:\\Xcalibur\\methods\\ul_pickup_60minLCMSMS_070723",
            'rinse': "C:\\Xcalibur\\methods\\sawtooth_30min_042722",
            'end': "C:\\Xcalibur\\methods\\Hold_50percent_B_30min_end_at_80percent"
        },
        'loop_vol': 20        
    },
    'Fusion1' : {
        'name' : 'F1',
        'methods' : {
            'DDA' : ["C:\\Xcalibur\\methods\\Fusion_60min_uLpickup_050324"],
            'DIA' : [],
            'QC': "C:\\Xcalibur\\methods\\Fusion_60min_uLpickup_050324",
            'blank': "C:\\Xcalibur\\methods\\Fusion_60min_uLpickup_050324",
            'rinse': "C:\\Xcalibur\\methods\\rinse_20min_Fusion",
            'end': "C:\\Xcalibur\\methods\\Fusion_60min_end_at_80percent"
        },
        'loop_vol': 20        
    },
    'Fusion2' : {
        'name' : 'F2',
        'methods' : {
            'DDA' : ["C:\\Xcalibur\\methods\\Fusion_60min_10uL_041024_uL_pickup"],
            'DIA' : [],
            'QC': "C:\\Xcalibur\\methods\\Fusion_60min_10uL_041024_uL_pickup",
            'blank': "C:\\Xcalibur\\methods\\Fusion_60min_10uL_041024_uL_pickup",
            'rinse': "C:\\Xcalibur\\methods\\Sawtooth_60min_050622",
            'end': "C:\\Xcalibur\\methods\\Fusion_60min_10uL_011323_end_on_80percent"
        },
        'loop_vol': 20        
    },
}




methods = {'Exploris2' : [
    "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop\\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221"
    ]
    ,
    'Exploris1' : [
        "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop\\DIA_12mz_15k_60min_5ulLoad_10ulLoop_031221"
    ]
    ,
    'Eclipse2' : [
        "C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_20ulLoop_ulPickup\\DIA_12mz_15k_60min_5ulLoad_20ulLoop_052423",
        "C:\\Xcalibur\\methods\\ul_pickup_60minLCMSMS_020224"
    ]
    }

rinse_methods = {'Exploris2' : 'C:\\Xcalibur\\methods\\Sawtooth_wash_DDA_30min',
                 'Exploris1' : 'C:\\Xcalibur\\methods\\Sawtooth_wash_DDA_30min',
                 'Eclipse2' : 'C:\\Xcalibur\\methods\\sawtooth_30min_042722',
                 'Fusion1' : 'NO RINSE METHOD',
                 'Fusion2' : 'C:\\Xcalibur\\methods\\Sawtooth_60min_050622'
}

qc_methods = {'Exploris2' : 'C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423',
              'Exploris1' : 'C:\\Xcalibur\\methods\\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423',
              'Eclipse2' : 'C:\\Xcalibur\\methods\\ul_pickup_60minLCMSMS_070723',
              'Fusion1' : 'C:\\Xcalibur\\methods\\Fusion_60min_uLpickup_050324',
              'Fusion2' : 'C:\\Xcalibur\\methods\\Fusion_60min_10uL_041024_uL_pickup'
}

abbrev = {
    'Exploris2': 'X2',
    'Exploris1': 'X1',
    'Eclipse2': 'E2',
    'Fusion2': 'F2',
    'Fusion1': 'F1'
}