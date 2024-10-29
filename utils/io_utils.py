import csv
import time
import functools
from pathlib import Path
import pandas as pd
from natsort import natsorted


def time_master(func):
    @functools.wraps(func)
    def wrapper_time_master(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper_time_master


def get_files(path, suffix):
    """
    Read and return paths to all .mzML files in the specified directory and its subdirectories.

    Parameters:
    - files_path (str): The path to the directory where the search should begin.

    Returns:
    - list: A list of Path objects pointing to .mzML files.

    Note:
    - The function does not return anything if no .mzML files are found in the specified directory.
    - Assumes files_path is a valid directory path. No checks are performed for security risks.
    """
    try:
        # Initialize Path object with the provided directory path
        p = Path(path).resolve()

        # Ensure the provided path is a valid directory
        if not p.is_dir():
            raise NotADirectoryError(f"{path} is not a valid directory.")

        # Collect paths to all .mzML files in the directory and its subdirectories
        paths = [path for path in p.rglob(f"*.{suffix}")]
        # Return the collected paths
        return natsorted(paths)

    except FileNotFoundError:
        print(f"The directory {path} does not exist.")
        return []
    except NotADirectoryError as e:
        print(e)
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def validate_file_path(path):
    # Initialize Path object with the provided directory path
    p = Path(path)

    # Ensure the provided path is a valid directory
    if not p.exists():
        raise FileNotFoundError(f"The directory {path} does not exist.")
    if not p.is_file():
        raise ValueError("The provided path is not a file.")


def replace_special_characters(series):

    replaced_series = series.copy()

    for index, value in series.items():
        if isinstance(value, str) and (':' in value or ' ' in value):
            replaced_series[index] = value.replace(":", "_").replace(" ", "_")

    return replaced_series


def read_targeted_features(path):

    validate_file_path(path)

    try:
        data = pd.read_csv(path, encoding_errors='ignore')
        data['Compound Name'] = replace_special_characters(data['Compound Name'])
        data['mz'] = data['mz'].astype(float)
        data['RT'] = data['RT'].astype(float)

        features_info = data[['Compound Name', 'mz', 'RT']].dropna()

        features_info = features_info.sort_values(by=['Compound Name'], key=natsorted)
        return features_info
    except pd.errors.EmptyDataError:
        raise ValueError("The provided CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("There was an error parsing the provided CSV file. Check for formatting issues.")
    except FileNotFoundError:
        raise ValueError("The provided file path does not exist.")
    except ValueError as ve:
        if "provided path" in str(ve):
            raise ValueError("The provided path is not a file.") from ve
        else:
            raise ve


def export_results(area, name):
    csv_file_path = f'{name}'
    # dir, name, mz, true_rt, left, right, max_x, max_intensity, trapz(filter_y, filter_x), score
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image_Path',
                         'Compound Name',
                         'M/Z',
                         'Old RT',
                         'Retention Time',
                         'rt_min',
                         'rt_max',
                         'intensity_max',
                         'Area',
                         'Score',
                         'Point counts'])
        for item in area:
            writer.writerow([str(item[0]),
                             str(item[1]),
                             float(item[2]),
                             float(round(item[3], 3)),
                             float(item[6]),
                             float(item[4]),
                             float(item[5]),
                             float(round(item[7], 3)),
                             float(round(item[8], 3)),
                             float(round(item[9], 3)),
                             int(item[10])])

    print(f"Successfully exported results to {csv_file_path}")