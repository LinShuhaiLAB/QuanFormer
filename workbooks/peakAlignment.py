import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


with open('xic_list3.pkl', 'rb') as f:
    xic_list_load = pickle.load(f)

areas = pd.read_csv("D:/example/output452/area.csv")
benchmark_rt = areas['Retention Time'].mean()

rt_list = []
intensity_list = []

for index, row in areas.iterrows():
    value = row['Retention Time']
    diff = value - benchmark_rt
    left = value - 1 - diff
    right = value + 1 - diff

    rt = xic_list_load[index][0]
    intensity = xic_list_load[index][1]

    value_index = np.argmin(np.abs(rt - value))
    # 确保左右各有500个数据点
    left_start = value_index - 250
    right_end = value_index + 250

    rt_masked = rt[left_start:right_end]
    intensity_masked = intensity[left_start:right_end]

    rt_list.append(rt_masked)
    intensity_list.append(intensity_masked)

# 确保所有 intensity_list 元素的长度与 rt_list[0] 一致
target_length = 500
for i in range(len(intensity_list)):
    current_length = len(intensity_list[i])
    if current_length > target_length:
        l = (current_length - target_length) // 2
        intensity_list[i] = intensity_list[i][:target_length]

    elif current_length < target_length:
        pad_length = target_length - current_length
        intensity_list[i] = intensity_list[i].tolist() + [0] * pad_length

sigma = 2  # 高斯平滑的标准差，可以根据需要调整

for i in range(int(len(rt_list) / 2)):
    # 对 intensity_list 进行高斯平滑
    smoothed_intensity_bc = gaussian_filter1d(intensity_list[i], sigma=sigma)
    smoothed_intensity_hd = gaussian_filter1d(intensity_list[i + int(len(rt_list) / 2)], sigma=sigma)

    plt.plot(rt_list[0], smoothed_intensity_bc, color='#212190', alpha=0.5, label='BC' if i == 0 else "")
    plt.plot(rt_list[0], smoothed_intensity_hd, color='#ed3131', alpha=0.5, label='HD' if i == 0 else "")



plt.legend()
# plt.show()
plt.savefig('D:/example/output452/452.pdf')

