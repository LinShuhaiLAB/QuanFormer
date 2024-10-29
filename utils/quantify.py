import os
import numpy as np
from scipy.integrate import trapz
from utils.io_utils import time_master


@time_master
def quantify(mzml, prediction, info):
    area = []
    count = len(mzml[0]) - 1
    for i, (path, scores, box) in enumerate(prediction):
        dir = os.path.dirname(path)
        index = i // count
        index2 = i % count
        rt = mzml[index][0]
        max_rt = max(rt)
        intensity = mzml[index][index2 + 1]
        name = info.loc[index2, 'Compound Name']
        mz = info.loc[index2, 'mz']
        true_rt = info.loc[index2, 'RT']

        if len(scores) > 0:
            for j in range(len(scores)):
                score = scores[j][0]
                left_bound = box[j][0]
                right_bound = box[j][2]
                # 40: the left padding of the img
                # 400: width of the box
                # 12.5: the padding of the coordinate
                # 15: the right padding of the img
                # 25 : 2 * 12.5
                if true_rt - 1 < 0:
                    windows_size = true_rt + 1
                    left = (left_bound - 50) / (400 - 50 - 30) * windows_size
                    right = (right_bound - 50) / (400 - 50 - 30) * windows_size
                elif true_rt + 1 > max_rt:
                    windows_size = max_rt - true_rt + 1
                    left = (left_bound - 50) / (400 - 50 - 30) * windows_size + true_rt - 1
                    right = (right_bound - 50) / (400 - 50 - 30) * windows_size + true_rt - 1
                else:
                    windows_size = 2
                    left = (left_bound - 50) / (400 - 50 - 30) * windows_size + true_rt - 1
                    right = (right_bound - 50) / (400 - 50 - 30) * windows_size + true_rt - 1

                mask = (rt >= left) & (rt <= right)
                filter_x = rt[mask]
                filter_y = intensity[mask]
                point_count = max_consecutive(filter_y)
                max_intensity = max(filter_y)
                max_index = filter_y.argmax()
                max_x = filter_x[max_index]
                area.append((dir, name, mz, true_rt, left, right, max_x, max_intensity, trapz(filter_y, filter_x), score, point_count))
        else:
            area.append((dir, name, mz, true_rt, 0, 0, 0, 0, 0, 0, 0))
    return area


def max_consecutive(arr):
    greater_than_zero = arr > 0
    diff = np.diff(greater_than_zero.astype(int))
    starts = np.where(diff == 1)[0] + 1
    ends = np.where(diff == -1)[0] + 1

    if greater_than_zero[0]:
        starts = np.insert(starts, 0, 0)
    if greater_than_zero[-1]:
        ends = np.append(ends, len(arr))

    if len(starts) == len(ends) == 0:
        max_c = 0
    else:
        max_c = np.max(ends - starts)
    return max_c