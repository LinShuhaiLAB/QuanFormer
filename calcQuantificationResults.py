import numpy as np
import pandas as pd
from compare_fc import read_data, merge_data
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, max_error

def merge_results(*paths):
    dfs = read_data(*paths)
    merged_df = merge_data(*dfs)
    merged_df = merged_df.drop(columns=['Compound Name'])
    return (
        merged_df.iloc[:, [0, 2]].dropna().reset_index(drop=True),
        merged_df.iloc[:, [0, 3]].dropna().reset_index(drop=True),
        merged_df.iloc[:, [0, 4]].dropna().reset_index(drop=True),
        # merged_df.iloc[:, [0, 5]].dropna().reset_index(drop=True)
    )

def calculate_metrics(df):
    mse = mean_squared_error(df.iloc[:, 0], df.iloc[:, 1])
    mae = mean_absolute_error(df.iloc[:, 0], df.iloc[:, 1])
    r2 = r2_score(df.iloc[:, 0], df.iloc[:, 1])
    evs = explained_variance_score(df.iloc[:, 0], df.iloc[:, 1])
    max_err = max_error(df.iloc[:, 0], df.iloc[:, 1])
    return {'MSE': mse, 'MAE': mae, 'R2': r2, 'EVS': evs, 'Max Error': max_err}

if __name__ == '__main__':
    # Figure 3
    path0 = r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\FeatureQEShift.csv"
    path1 = r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\MZMINE3\QEShift_MZ.csv"
    path2 = r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\PEAKDETECTIVE\QEShift_PD.csv"
    # path3 = r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\peakonly\TOF_PO.csv"
    path4 = r"C:\Users\zhangzhengyi\Desktop\temp\1012\data\Mine\QEShift\QEShift_QF.csv"

    # mz, pd_df, po, qf = merge_results(path0, path1, path2, path3, path4)
    mz, pd_df, qf = merge_results(path0, path1, path2, path4)

    # 创建一个空的列表来存储结果
    results = []

    # 计算每个DataFrame的指标并存储到结果列表中
    # for method, df in zip(['MZ', 'PD', 'PO', 'QF'], [mz, pd_df, po, qf]):
    for method, df in zip(['MZ', 'PD', 'QF'], [mz, pd_df, qf]):
        metrics = calculate_metrics(df)
        results.append({'Method': method, **metrics})

    # 将结果列表转换为DataFrame
    results_df = pd.DataFrame(results)

    # 打印结果
    print(results_df)

    # 保存结果到CSV文件
    results_df.to_csv('results_qeshift.csv', index=False)



