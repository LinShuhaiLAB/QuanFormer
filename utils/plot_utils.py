from scipy.ndimage import gaussian_filter
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
import os
import bisect


def smooth_xic(inten, rt, sigma):
    if sigma == 0:
        smooth_intensity = inten
        smooth_rt = rt
    else:
        smooth_intensity = gaussian_filter(inten, sigma=sigma)
        smooth_rt = rt
    return smooth_rt, smooth_intensity


def calc_coordinate(info, intensity, rt, k, windows_size=2):
    t_rt = info[k][2]
    lrt = t_rt - windows_size / 2 if t_rt - windows_size / 2 > 0 else 0
    rrt = t_rt + windows_size / 2 if t_rt + windows_size / 2 < rt[-1] else rt[-1]
    lindex = bisect.bisect_left(rt, lrt)
    rindex = bisect.bisect_right(rt, rrt)
    if rindex - lindex >= 0:
        calc_intensity = intensity[lindex:rindex]
        calc_rt = rt[lindex:rindex]
    return calc_intensity, calc_rt


def plot_xic(rt, intensity, name, folder_path):
    fig: Figure = Figure(figsize=(4, 3))

    canvas: FigureCanvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    line, = ax.plot(rt, intensity)
    # ax.set_title(f'{name}')
    # ax.margins(0)

    # 设置y轴的刻度显示为科学计数法
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    ax.yaxis.set_major_formatter(formatter)
    # ax.yaxis.set_major_formatter('{x:.2e}')

    ax.tick_params(axis='y', labelrotation=90)

    fig.tight_layout()
    # file_path_pdf = os.path.join(folder_path, f"{name}.svg")
    # fig.savefig(file_path_pdf, format='svg')

    file_path = os.path.join(folder_path, f"{name}.jpeg")
    canvas.print_jpeg(file_path)
    plt.close()

