import os.path

import pandas as pd




def calculate_mz_range(mz, ppm=25):
    mz_min = mz * (1 - ppm / 1e6)
    mz_max = mz * (1 + ppm / 1e6)
    return mz_min, mz_max


def merge_peakonly_with_feature(df_peakonly, df_feature, rt_tolerance=0.5):
    df_feature["RT_min"] = df_feature["RT"] - rt_tolerance
    df_feature["RT_max"] = df_feature["RT"] + rt_tolerance
    df_feature['mz_min'], df_feature['mz_max'] = zip(*df_feature['mz'].apply(calculate_mz_range))

    filtered_df = pd.DataFrame()
    for index, feature_row in df_feature.iterrows():
        mz_min, mz_max = feature_row['mz_min'], feature_row['mz_max']
        rt_min, rt_max = feature_row['RT_min'], feature_row['RT_max']
        temp_df = df_peakonly[
            (df_peakonly['mz_mean'] >= mz_min) &
            (df_peakonly['mz_mean'] <= mz_max) &
            (df_peakonly['rt'] >= rt_min) &
            (df_peakonly['rt'] <= rt_max)
            ]

        if not temp_df.empty:
            temp_df.loc[:, 'feature_index'] = index
            filtered_df = pd.concat([filtered_df, temp_df])

    merged_df = pd.merge(filtered_df, df_feature, left_on='feature_index', right_index=True, how='left')

    columns_to_drop = ['peak_label', 'mz_mean', 'rt', 'rt_min', 'rt_max', 'mz_width', 'RT_min', 'RT_max', 'mz_min',
                       'mz_max', 'feature_index']
    merged_df.drop(columns=columns_to_drop, inplace=True)

    duplicates = merged_df[merged_df.duplicated(subset='Compound Name', keep=False)]
    max_duplicates = duplicates.sort_values(by=['Compound Name', merged_df.columns[0]],
                                            ascending=[True, False]).drop_duplicates(subset='Compound Name',
                                                                                     keep='first')
    non_duplicates = merged_df[~merged_df.duplicated(subset='Compound Name', keep=False)]
    result = pd.concat([max_duplicates, non_duplicates])
    result = result.drop_duplicates()
    return result


if __name__ == '__main__':
    path = "D:/ms-peakonly-main/peakonly_results/peakonly_QE"

    raw_path = os.path.join(path, "QESB1.csv")
    output_path = os.path.join(path, "solved_QESB1.csv")

    df_peakonly = pd.read_csv(raw_path)
    df_feature = pd.read_csv("D:/QuanFormer-main/data/FeatureQE.csv")
    result = merge_peakonly_with_feature(df_peakonly, df_feature)

    result.to_csv(output_path, index=False)