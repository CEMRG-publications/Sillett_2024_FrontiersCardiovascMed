## Use this file to save .txt files of rmse for creating plots offline

## See MT_Veri.ipynb

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

## All 30 Cases
all_cases = ['01', '02', '05', '06', '07', '08', '09', '12', '14',
             '15', '16', '17', '18', '21', '24', '27', '28', '29', '30',
             '32', '10', '19', '20', '23', '26', '31', '25', '34']
all_cases = [f"CT-CRT/case{case}" for case in all_cases]
ebr=['EBR/case01', 'EBR/case02']
all_cases=all_cases+ebr

## 20 frame cases
f20_cases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
f20_cases = [f'CT-CRT/case{case_ind}' for case_ind in f20_cases]
ebr=['EBR/case01', 'EBR/case02']
f20_cases = f20_cases + ebr