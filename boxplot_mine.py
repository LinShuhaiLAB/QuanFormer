import pandas as pd
from matplotlib import pyplot as plt
from matplotlib_venn import venn2


def filter_duplicate(ms_path, benchmark_path):
    df_ms = pd.read_csv(ms_path)
    df_ms = df_ms[['Image_Path', 'Compound Name', 'Retention Time', 'Area']]
    df_QE = pd.read_csv(benchmark_path)
    merged_df = pd.merge(df_ms, df_QE, on='Compound Name')

    grouped = merged_df.groupby('Compound Name')
    num_unique = merged_df['Image_Path'].nunique()

    drop = []
    for a, b in grouped:
        if len(b) > num_unique:
            grouped_ = b.groupby('Image_Path')
            for x, y in grouped_:
                diff = abs(y.iloc[:]['Retention Time'] - y.iloc[:]['RT'])
                min_diff_index = diff.idxmin()
                other_index = diff.index[diff.index != min_diff_index]
                drop.append(other_index)

    indices_to_remove = [item for sublist in [i.tolist() for i in drop if len(i) > 0] for item in sublist]

    single_df = merged_df.drop(indices_to_remove, axis=0)
    return single_df


def post_process(old_df, benchmark_path, number, rt_tolerance):
    old_df = old_df[['Image_Path', 'Compound Name', 'Retention Time', 'Area']]

    df_new = old_df.pivot(index='Compound Name', columns='Image_Path', values=['Retention Time', 'Area'])

    df_new.columns = [f'{col[1]}_{col[0]}' for col in df_new.columns]

    df_new.reset_index(inplace=False)

    df_QE = pd.read_csv(benchmark_path)
    merged_df = pd.merge(df_new, df_QE, on='Compound Name')

    for col in merged_df.columns[1:number]:
        merged_df[col] = abs(merged_df[col] - merged_df['RT'])

    merged_df = merged_df[(merged_df.iloc[:, 1:number] <= rt_tolerance).all(axis=1)]
    print(merged_df.shape)

    return merged_df


def plot_boxplot(df, name, type, precision, n='fc'):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 1, 1])
    graph = ax.boxplot(
        [
            df[df["Compound concentration ratio"] == "1/16"].loc[:, n],
            df[df["Compound concentration ratio"] == "1/4"].loc[:, n],
            df[df["Compound concentration ratio"] == "1/2"].loc[:, n],
            df[df["Compound concentration ratio"] == "1/1"].loc[:, n],
            df[df["Compound concentration ratio"] == "2/1"].loc[:, n],
            df[df["Compound concentration ratio"] == "4/1"].loc[:, n],
            df[df["Compound concentration ratio"] == "16/1"].loc[:, n],
        ],
        vert=True,
        patch_artist=True,
        labels=["Gd1", "Gd2", "Gd3", "Gdm", "Gd4", "Gd5", "Gd6"],
        sym='*'
    )

    colors = ['pink', 'lightblue', 'lightgreen']
    for patch, color in zip(graph['boxes'], colors):
        patch.set_facecolor(color)
    plt.tight_layout()

    ax.set_xticklabels(ax.get_xticklabels(), fontsize=14)
    plt.yscale('log', base=2)
    import numpy as np
    plt.ylim(1 / 2**6,  2**6)
    ax.set_yticklabels([int(1 * np.log2(y)) for y in ax.get_yticks()], fontsize=18)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=18)
#     plt.savefig(f"{type}+{name}+{precision}.png", dpi=300, bbox_inches="tight")
    plt.show()
    # plt.close()



def compute_average_and_cv(group_name, column_names, df):

    try:
        group_columns = [f'{column_name}' for column_name in column_names]

        relevant_data = df.select_dtypes(include='number')[group_columns]

        avg = relevant_data.mean(axis=1)
        std = relevant_data.std(axis=1)

        cv = std.where(std != 0, 0) / avg * 100

        return {'AVG': avg, 'CV': cv}
    except Exception as e:
        print(f"Error processing group {group_name}: {e}")
        return {}


def plot_log(df1, type, name, output_path):
    df1 = df1[df1.notnull().all(axis=1)]
    all_columns = df1.columns.tolist()

    if type == 'TOF' or type == 'TOFShift':
        import pandas as pd
        sample_a_columns = [all_columns[i] for i in [-14, -13, -8, -7]]
        sample_b_columns = [all_columns[i] for i in [-12, -11, -10, -9]]
    elif type == 'QE' or type == 'QEShift':
        sample_a_columns = all_columns[-16:-11]
        sample_b_columns = all_columns[-11:-6]

    sample_a_results = compute_average_and_cv('SampleA', sample_a_columns, df1)
    sample_b_results = compute_average_and_cv('SampleB', sample_b_columns, df1)

    df1.loc[:, 'AVG-A'] = sample_a_results['AVG']
    df1.loc[:, 'CV-A'] = sample_a_results['CV']
    df1.loc[:, 'AVG-B'] = sample_b_results['AVG']
    df1.loc[:, 'CV-B'] = sample_b_results['CV']

    df1.loc[:, 'fc'] = df1.loc[:, 'AVG-B'] / df1.loc[:, 'AVG-A']
    df1.loc[:, 'ratio'] = df1.loc[:, 'fc'] / df1.loc[:, 'Fold change']

    df_cleaned = df1[df1.notnull().all(axis=1)]

    precsion = calculate_precision(df_cleaned, name, type)
    print(precsion)
    plot_boxplot(df_cleaned, name, type, precsion)
    df_cleaned = df_cleaned.drop(df_cleaned.columns[1:11], axis=1)
    df_cleaned.to_csv(output_path)


def calculate_precision(df, name, type):
    print(f'{type}+{name}')
    df_filtered = df[(df['ratio'] > 0.8) & (df['ratio'] < 1.2)]
    count = df_filtered.shape[0]
    print(f"precise quantify:{count}")
    print(f"count:{df.shape[0]}",)
    if type == 'TOF' or type == 'TOFShift':
        return round((count/df.shape[0] + df.shape[0] / 970)/2, 3)
    elif type == 'QE' or type == 'QEShift':
        return round((count/df.shape[0] + df.shape[0] / 836)/2, 3)


if __name__ == '__main__':
    PeakFormer_path = 'data/Mine/QE/areas.csv'
    benchmark_path = 'data/FeatureQE.csv'
    output_path = 'data/Mine/QE/post-my-qe.csv'
    type = 'QE'
    df = filter_duplicate(PeakFormer_path, benchmark_path)
    df1 = post_process(df, benchmark_path, 11, 0.5)
    plot_log(df1, type, 'PeakFormer',output_path)

    # PeakFormer_path = 'data/Mine/QEShift/areas.csv'
    # benchmark_path = 'data/FeatureQEShift.csv'
    # output_path = 'data/Mine/QEShift/post-my-qe.csv'
    # type = 'QEShift'
    # df = filter_duplicate(PeakFormer_path, benchmark_path)
    # df1 = post_process(df, benchmark_path, 11, 0.7)
    # plot_log(df1, type, 'PeakFormer', output_path)

    # PeakFormer_path = 'data/Mine/TOF/areas.csv'
    # benchmark_path = 'data/FeatureTOF.csv'
    # output_path = 'data/Mine/TOF/post-my-tof.csv'
    # type = 'TOF'
    # df = filter_duplicate(PeakFormer_path, benchmark_path)
    # df1 = post_process(df, benchmark_path, 9, 0.5)
    # plot_log(df1, type, 'PeakFormer', output_path)

    # PeakFormer_path = 'data/Mine/TOFShift/areas.csv'
    # benchmark_path = 'data/FeatureTOFShift.csv'
    # output_path = 'data/Mine/TOFShift/post-my-tof.csv'
    # type = 'TOFShift'
    # df = filter_duplicate(PeakFormer_path, benchmark_path)
    # df1 = post_process(df, benchmark_path,9,0.5)
    # plot_log(df1, type, 'PeakFormer', output_path)