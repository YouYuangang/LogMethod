from dataengine import DataEngine
from datasource import DataSource
from workspace import WorkSpace
from well import Well
from category import Category
from curve1d import Curve1D
from table import Table
from communication import Communication
from datapath import DataPathPaser
from logdata import LogData
from logplot import LogPlot
import numpy as np
import pandas as pd
import fastdtw
import matplotlib.pyplot as plt
import math
import time
import scipy.signal as signal


'''
从第一点开始依次筛选，去除冗余点。
即以第一点为起点，计算第二点至第一点和第三点连线的垂直距离，若此距离大于某阈值，则保留第二点，并将其作为新起点，
计算第三点至第二点和第四点连线的距离；否则，去除第二点，计算第三点至第一点和第四点连线距离，依次类推，直至曲线上最后一点。
 '''


def curve_compress(value_df, value_index):
    lastIndex = -1
    results = []
    count = value_df.shape[0]
    col_df = log_df[log_df.columns[value_index]]
    values = signal.medfilt(col_df, kernel_size=15)

    # threshold = sum(values)/(200*len(values))
    threshold = max(values)/400
    results.append([value_df.index[0], values[value_index]])
    for i in range(count-1):
        if i == 1:
            lastIndex = 0
        else:
            currentIndex = i
            lastEffectiveIndex = lastIndex
            followIndex = i + 1
            dvlf = values[lastEffectiveIndex] - values[followIndex]
            dilf = lastEffectiveIndex - followIndex
            dd = math.sqrt(dvlf * dvlf + dilf * dilf)
            a = dvlf / dd
            b = -dilf / dd
            c = (lastEffectiveIndex * values[followIndex] -
                 followIndex * values[lastEffectiveIndex]) / dd
            d = abs(a * currentIndex + b *
                    values[currentIndex] + c) / math.sqrt(a * a + b * b)

            if d > threshold:
                lastIndex = i
                results.append(
                    [value_df.index[i], values[i]])
    results.append(
        [value_df.index[count-1], values[count-1]])
    return results


def draw(log_df, point_list):
    fig, axes = plt.subplots(
        nrows=1, ncols=log_df.shape[1], figsize=(6, 12), sharey=True)
    fig.subplots_adjust(top=0.9, wspace=0.15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for i, curve_name in enumerate(log_df.columns):
        # axes[i].set_ylim(log_df.index[0], log_df.index[-1])
        axes[i].set_ylim(400, 600)
        axes[i].invert_yaxis()
        axes[i].yaxis.grid(True)
        axes[i].get_xaxis().set_visible(False)
        ax = axes[i].twiny()
        data = log_df[curve_name]
        ax.set_xlim(min(data), max(data))
        ax.spines['top'].set_position(('outward', 0))
        color = 'blue'
        ax.plot(data, log_df.index, color=color, label=curve_name)
        ax.set_xlabel(curve_name, color=color)
        ax.tick_params(axis='x', colors=color)

        depthes = [x[0] for x in point_list[i]]
        values = [x[1] for x in point_list[i]]
        ax.scatter(values, depthes, marker='o',
                   color='R', label='Core')
        ax.grid(False)
    plt.show()


data_engine = DataEngine()
data_engine.initialize()
data_source = DataSource()

data_source.open("D:\cifplusdemo20120913")
wells = data_source.get_workspace("多井测试数据").get_wells()
logdata = LogData()
logplot = LogPlot()
well = wells[1]
print(well.name)
category = well.get_default_category()
curve_names = category.get_curve1d_names_existed(["sp", "ac", "rt"])
curve1ds = category.get_curve1ds(curve_names)
log_df = logdata.read_curve1ds_to_df(curve1ds)
# logplot.draw_curve1d_df(log_df)
# ac_df =log_df['AC']
begin_time = time.time()
# points = [[ac_df.index[i], ac_df.iloc[i]] for i in range(log_df.shape[0])]
point_list = []
for i in range(log_df.shape[1]):
    pts = curve_compress(log_df, i)
    print(len(pts))
    point_list.append(pts)
draw(log_df, point_list)

end_time = time.time()
print("运行时间:%.2f秒" % (end_time-begin_time))
print(log_df.shape[0])


data_engine.release()
