'''
Script to convert area-strains-4.csv to area-strains-4.vec file (need to create it as a txt file on the way)
'''

import pandas as pd

# Read in csv file
df = pd.read_csv('area-strains-4.csv')

# Drop redundant col with cell indices
df_drop = df.drop(labels='Unnamed: 0', axis=1)

# Save cleaner dataframe
df_drop.to_csv('area-strains-4-TEST.txt', header=None, index=None, sep=' ')

