import pandas as pd

use = ['Fold change', 'p-value', 'fc', 'true p-value','Compound Name']
df = pd.read_csv('data/MZMINE3/TOF.csv', usecols=use, encoding_errors='ignore')

df1 = df[((df['Fold change'] > 2) | (df['Fold change'] < 0.5)) & (df['p-value'] < 0.05)]
set1 = set(df1['Compound Name'])
df2 = df[((df['fc'] > 2) | (df['fc'] < 0.5)) & (df['true p-value'] < 0.05)]
set2 = set(df2['Compound Name'])
print(len(set1.intersection(set2)))
print(len(set1.union(set2))-len(set1.intersection(set2)))