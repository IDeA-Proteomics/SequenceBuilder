import pandas as pd
import tkinter as tk

position_list = [f"{a}{b}{c}" for a in "RGB" for b in "ABCDEFGH" for c in range(1, 13)]

instrument_data = {}

