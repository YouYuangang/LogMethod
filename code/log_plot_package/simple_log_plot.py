#_*_coding:utf-8_*_
'''
作者：Y.G. You
创建时间：2020.10.14
更新时间：2020.10.28
'''
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from data_helper_package import rawdata_provider
font_dict={'family': 'Times New Roman',
         'weight': 'normal',
         'size': 16,
         }
def plot_log(depth,data,xlabel="default",ylabel="default"):
    meanofdata = np.mean(data)
    plt.figure(figsize=(0.3, 6.5))
    plt.plot(data,depth,color="green", linewidth=0.3, linestyle="-")
    plt.xlim(meanofdata-1.5*abs(meanofdata),meanofdata+1.5*abs(meanofdata))
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    for tick in ax.get_yticklabels():
        tick.set_rotation(-90)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)

    plt.show()

def plot_2_log(depth1,data1,xlabel1,ylabel1,depth2,data2,xlabel2,ylabel2,saveflag=False,filepath=""):
    meanofdata1 = np.mean(data1)
    meanofdata2 = np.mean(data2)
    plt.figure(figsize=(3, 6.5))
    plt.cla()
    plt.subplot(121)
    plt.plot(data1,depth1,color="green", linewidth=0.3, linestyle="--")
    plt.xlim(meanofdata1-2*abs(meanofdata1),meanofdata1+2*abs(meanofdata1))
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    for tick in ax.get_yticklabels():
        tick.set_rotation(-90)
    plt.xlabel(ylabel1)
    plt.ylabel(xlabel1)
    plt.subplot(122)
    plt.plot(data2,depth2,color="green", linewidth=0.3, linestyle="-")
    plt.xlim(meanofdata2-2*abs(meanofdata2),meanofdata2+2*abs(meanofdata2))
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    for tick in ax.get_yticklabels():
        tick.set_rotation(-90)
    plt.xlabel(ylabel2)
    if(saveflag==True):
        plt.savefig(filepath)
        plt.close()
    else:
        plt.show()
#将两口井的交汇图绘制在平面图上，看重叠情况
def cross_plot2d_for_2well(series1,series2,xlabel_ = "default",ylabel_="default",title = "cross plot",wellname1="well1",wellname2="well2",saveflag = False,path=""):
    plt.figure()
    plt.cla()
    x1 = plt.scatter(series1[0],series1[1],c="r")
    x2 = plt.scatter(series2[0],series2[1],c="b")
    plt.xlabel(xlabel_,fontdict=font_dict)
    plt.ylabel(ylabel_,fontdict=font_dict)
    plt.legend((x1,x2),(wellname1,wellname2))
    plt.title(title)
    if(saveflag==True):
        plt.savefig(path)
        plt.close()
    else:
        plt.show()

def correlation_plot_for_2well(depth1,data1,depth2,data2,map,xlabel="default",ylabel="default",title="none",wellname1="well1",wellname2="well2",saveflag = False,filepath=""):
    meanofdata1 = np.mean(data1)
    data2 = [x+3*meanofdata1 for x in data2]
    meanofdata2 = np.mean(data2)

    plt.figure(figsize=(5, 6))
    plt.cla()
    plt.plot(data1,depth1,color="blue", linewidth=0.3, linestyle="--")
    plt.plot(data2,depth2,color="red")
    for i in range(len(map)):
        if i%15 == 0:
            
            index1 = map[i][0]
            index2 = map[i][1]
            print(str(depth1[index1])+","+str(depth2[index2]))
            plt.plot([meanofdata1,meanofdata2],[depth1[index1],depth2[index2]])
    plt.xlim(meanofdata1-2*abs(meanofdata1),meanofdata2+2*abs(meanofdata1))
    plt.ylim(min(min(depth1),min(depth2)),max(max(depth1),max(depth2)))
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    for tick in ax.get_yticklabels():
        tick.set_rotation(-90)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)

    

    if(saveflag==True):
        plt.savefig(filepath)
        plt.close()
    else:
        plt.show()
