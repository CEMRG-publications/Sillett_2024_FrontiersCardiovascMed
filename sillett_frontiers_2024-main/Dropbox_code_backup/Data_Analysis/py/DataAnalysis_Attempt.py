import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('/home/csi20local/Data/RG_CT_Cases/CT-CRT-05/MT-HiRes-Normal-Distance-Results.csv',
	sep = ' ', index_col = 0)

data = df.to_numpy().flatten()

plt.boxplot(data)
plt.show()