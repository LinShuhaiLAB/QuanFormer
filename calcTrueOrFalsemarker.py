import pandas as pd
from statsmodels.stats.multitest import multipletests

# use = ['Fold change', 'p-value', 'fc','Compound Name']
df = pd.read_csv(r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\MZMINE3\TOF.csv", encoding_errors='ignore')

from scipy import stats

df['t_statistic'] = 0
df['true p_value'] = 0

# 对每一行进行 t 检验
for index, row in df.iterrows():
    # MZmine 3 QE
    # cols_SA = row[4:9].values.astype(float)
    # cols_SB = row[9:14].values.astype(float)
    # MZmine 3 TOF
    cols_SA = row[4:8].values.astype(float)
    cols_SB = row[8:12].values.astype(float)


    # QE
    # cols_SA = row[2:7].values.astype(float)
    # cols_SB = row[7:12].values.astype(float)

    #TOF
    # cols_SA = row[2:6].values.astype(float)
    # cols_SB = row[6:12].values.astype(float)

    # PeakDetective QE
    # cols_SA = row[3:8].values.astype(float)
    # cols_SB = row[8:13].values.astype(float)

    # # PeakDetective TOF
    # cols_SA = row[3:7].values.astype(float)
    # cols_SB = row[8:12].values.astype(float)

    # Mine TOF
    # cols_SA = row[[1,2,7,8]].values.astype(float)
    # cols_SB = row[3:7].values.astype(float)

    # 进行 t 检验
    t_statistic, p_value = stats.ttest_ind(cols_SA, cols_SB)
    df.at[index, 't_statistic'] = t_statistic
    df.at[index, 'true p_value'] = p_value


# 提取所有行的 p 值
p_values = df['true p_value'].values

# 进行 FDR 校正
fdr_level = 0.05
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=fdr_level, method='fdr_bh')

# 将校正后的 p 值添加到 DataFrame 中
df['corrected_p_value'] = corrected_p_values
df.to_csv(r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\MZMINE3\TOF.csv", index=False)


df1 = df[((df['Fold change'] > 2) | (df['Fold change'] < 0.5)) & (df['p-value'] < 0.05)]
set1 = set(df1['Compound Name'])
df2 = df[((df['fc'] > 2) | (df['fc'] < 0.5)) & (df['corrected_p_value'] < 0.05)]
set2 = set(df2['Compound Name'])
print(len(set1.intersection(set2)))
print(len(set1.union(set2))-len(set1.intersection(set2)))
