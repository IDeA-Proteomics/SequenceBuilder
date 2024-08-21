import pandas as pd
import tkinter as tk






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
              'Exploris1' : 'C:\\Xcalibur\\methods\DIA\\60min_5ulLoad_10ulLoop_ulPickup\\DDA_60min_5ulLoad_10ulLoop_pickup_071423',
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