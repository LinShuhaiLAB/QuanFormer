import pickle
import pandas as pd
import matplotlib.pyplot as plt

with open('xic_list.pkl', 'rb') as f:
    xic_list_load = pickle.load(f)

areas = pd.read_csv('resources/example/peak-output/area.csv')
benchmark_rt = areas['Retention Time'].mean()

rt_list = []
intensity_list = []

for index, row in areas.iterrows():
    value = row['Retention Time']
    diff = value - benchmark_rt
    left = value - 1 - diff
    right = value + 1 - diff
    rt = xic_list_load[0][0]
    intensity = xic_list_load[0][1]
    mask = (rt > left) & (rt < right)
    rt_list.append(rt[mask])
    intensity_list.append(intensity[mask])

for i in range(int(len(rt_list)/2)):
    if len(rt_list[0]) != len(intensity_list[i]):
        intensity_list[i] = intensity_list[i][:len(rt_list[0])]

    plt.plot(rt_list[0], intensity_list[i], color='blue', alpha=0.5)
    plt.plot(rt_list[0], intensity_list[i+int(len(rt_list)/2)], color='red', alpha=0.5)

plt.show()

