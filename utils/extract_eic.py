import time

import matplotlib.pyplot as plt
import numpy as np
import pymzml
from pathlib import Path
from joblib import Parallel, delayed
from tqdm import tqdm

from utils.io_utils import time_master
from utils.plot_utils import smooth_xic, plot_xic, calc_coordinate


def get_closest(mzmean, mz, pos):
    if pos == len(mzmean):
        res = pos - 1
    elif pos == 0:
        res = pos
    else:
        res = pos if (mzmean[pos] - mz) < (mz - mzmean[pos - 1]) else pos - 1
    return res


def extract_eic(path, df_info, ppm):
    _ppm = ppm * 1e-6
    flag = 0
    with pymzml.run.Reader(path) as run:
        matrix = np.zeros(((len(df_info)) + 1, run.get_spectrum_count()))
        for i, spec in enumerate(run):
            if spec.ms_level == 1:
                _mzs = spec.mz
                _intensities = spec.i
                if spec.scan_time[1] == 'second':
                    matrix[0, i-flag] = spec.scan_time[0] / 60
                else:
                    matrix[0, i-flag] = spec.scan_time[0]
                for index in range(len(df_info)):
                    f_mz = df_info[index][1]
                    indices = np.searchsorted(_mzs, f_mz)
                    closest = get_closest(_mzs, f_mz, indices)
                    if abs(_mzs[closest] - f_mz) < f_mz * _ppm:
                        matrix[index + 1, i-flag] = _intensities[closest]
                    else:
                        matrix[index + 1, i-flag] = 0
            else:
                flag = flag + 1
        matrix = matrix[:, :len(matrix[0])-flag]
        return matrix


def draw_eic(index, path, df_info, xic_list, args):
    sigma = args.smooth_sigma
    # threshold = args.intensity_threshold
    eic_path = args.images_path

    xic = xic_list[index]
    rt = xic[0]

    compounds_count = len(xic_list[0]) - 1
    table_rt_min = df_info[:, 2].min()
    table_rt_max = df_info[:, 2].max()
    assert table_rt_min > rt.min() and table_rt_max < rt.max(), \
        f"Feature table is not compatible with the EIC. The min acceptable RT is {rt.min()}, the max is {rt.max()}"

    name = path[index].stem
    folder_name = f"{name}"
    current_path = Path.cwd()
    folder = current_path / eic_path / folder_name
    Path(folder).mkdir(parents=True, exist_ok=True)

    for k in range(compounds_count):
        intensity = xic[k + 1]
        name = df_info[k][0]
        calc_intensity, calc_rt = calc_coordinate(df_info, intensity, rt, k)
        # if max(calc_intensity) > threshold:
        smooth_rt, smooth_intensity = smooth_xic(calc_intensity, calc_rt, sigma)
        plot_xic(smooth_rt, smooth_intensity, name, folder)


@time_master
def build(paths, info, plot, args):

    processes_number = args.processes_number
    df_info = info.values
    ppm = args.ppm

    xic_list = Parallel(n_jobs=processes_number)(delayed(extract_eic)(path, df_info, ppm)
                                                 for path in paths)

    if plot:
        if processes_number == 1:
            for i in range(len(xic_list)):
                draw_eic(i, paths, df_info, xic_list, args)
        else:
            (Parallel(n_jobs=processes_number)
             (delayed(draw_eic)(i, paths, df_info, xic_list, args)
              for i in range(len(xic_list))))

    return xic_list
