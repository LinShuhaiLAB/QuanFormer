# import pickle
# import pandas as pd
# import matplotlib.pyplot as plt
#
# with open('xic_list.pkl', 'rb') as f:
#     xic_list_load = pickle.load(f)
#
# areas = pd.read_csv('resources/example/peak-output/area.csv')
# benchmark_rt = areas['Retention Time'].mean()
#
# rt_list = []
# intensity_list = []
#
# for index, row in areas.iterrows():
#     value = row['Retention Time']
#     diff = value - benchmark_rt
#     left = value - 1 - diff
#     right = value + 1 - diff
#     rt = xic_list_load[0][0]
#     intensity = xic_list_load[0][1]
#     mask = (rt > left) & (rt < right)
#     rt_list.append(rt[mask])
#     intensity_list.append(intensity[mask])
#
# for i in range(int(len(rt_list)/2)):
#     if len(rt_list[0]) != len(intensity_list[i]):
#         intensity_list[i] = intensity_list[i][:len(rt_list[0])]
#
#     plt.plot(rt_list[0], intensity_list[i], color='blue', alpha=0.5)
#     plt.plot(rt_list[0], intensity_list[i+int(len(rt_list)/2)], color='red', alpha=0.5)
#
# plt.show()
#
#
list=[[[0.01,0,0.03,0.04,0,0.06,0.07,0.08,0.09,0.1],[1,2,3,4,5,6,7,8,9,10]],
      [[0.11,0,0.13,0.14,0,0.16,0.17,0.18,0.19,0.2],[11,12,13,14,15,16,17,18,19,20]]]

print(list[0][0])
result = []
for sublist in list:
    i, mz = sublist
    new_i = [item for item in i if item!= 0]
    new_mz = [mz[idx] for idx, value in enumerate(i) if value!= 0]
    result.append([new_i, new_mz])
print('--')
print(result)
#
# # import matplotlib.pyplot as plt
# # x = [1,2,3,4,5]
# # y1 = [0,1,2,3,0]
# # y2 = [0,0,4,3,0]
# # y3 = [0,1,4,1]
# #
# # plt.plot(x,y1,label= 's1')
# # plt.plot(x,y2,label= 's2')
# # plt.plot(x,y3,label= 's3')
# #
# # plt.legend()
# # plt.title('mutiple')
# # plt.xlabel('x')
# # plt.ylabel('y')
# # plt.show()
#
#
#
#
