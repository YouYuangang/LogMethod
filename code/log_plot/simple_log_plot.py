import matplotlib.pyplot as plt
import sys
import os
from data_helper_module import rawdata_provider
def plot_log(depth,data):
    plt.figure(figsize=(0.3, 6.5))
    plt.plot(data,depth,color="green", linewidth=0.3, linestyle="-")
    plt.xlim((0,100))
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    for tick in ax.get_yticklabels():
        tick.set_rotation(-90)
    plt.show()