import pandas as pd


def filter_duplicate(path, xic_info):
    df_pk = pd.read_csv(path)
    df_pk = df_pk[['Image_Path', 'Compound Name', 'Retention Time', 'Area', 'Point counts']]
    merged_df = pd.merge(df_pk, xic_info, on='Compound Name')

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


def reset_col(old_df, output_path, xic_info):
    old_df = old_df[['Image_Path', 'Compound Name', 'Retention Time', 'Area', 'Point counts']]
    df_new = old_df.pivot(index='Compound Name', columns='Image_Path', values=['Retention Time', 'Area', 'Point counts'])

    df_new.columns = [f'{col[1]}_{col[0]}' for col in df_new.columns]
    df_new.reset_index(inplace=False)

    df_merged = pd.merge(df_new, xic_info, "inner", on='Compound Name')
    parts = output_path.split('/')
    parts[-1] = 'post-' + parts[-1]
    new_path = '/'.join(parts)
    df_merged.to_csv(new_path, index=False)


def post_process(path, xic_info):
    df = filter_duplicate(path, xic_info)
    reset_col(df, path, xic_info)


if __name__ == "__main__":
    post_process("D:/example/output_text/area.csv", "D:/example/test_feature.csv")