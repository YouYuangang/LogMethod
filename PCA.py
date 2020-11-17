import sys
import io
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle

sys.path.append(r'code')
from data_helper_package import rawdata_provider
from data_helper_package import data_preprocesser
from data_helper_package import well_segment_provider

def get_cr( x_set, y_set ):
    cr = []
    for i in range(len(x_set) -1 ):
        x,y = x_set[i+1] - x_set[i], y_set[i+1] - y_set[i]
        #length = math.sqrt(x*x + y*y)
        #x,y = x/length, y/length
        cr.append(np.array([x,y]))
    return cr

data = []
RawData = rawdata_provider.RawDataProvider()
wells = RawData.get_well_allnames()
Seg = well_segment_provider.WellSegmentProvider()

i=0
#读取数据
z = []
for well in wells:
    ac_data = RawData.get_column_floatData(well, "ac")
    if(Seg.if_exist_segment(well, "龙潭组")):
        ac_data = Seg.get_segment_columndata(well, "龙潭组", "ac")
        depth = np.arange(0,len(ac_data),1/8).tolist()
        data_preprocesser.data_except_invalid(depth,ac_data)
        x,y = data_preprocesser.getkeypoint_from_rawdata(depth,ac_data,threshold = 1)
        tmp = []
        for j in range( len(y) - 1 ):
            tmp += list(np.arange( y[j], y[j+1], (y[j+1]-y[j])/(x[j+1]-x[j])/8))
        data.append(tmp)
    i+=1
    if(i == 4):
        break

data_set = np.zeros((10000,1000))
re_set = np.zeros(10000)
for i in range(4):
    for j in range(len(data[i])):
        data_set[i][j] = data[i][j]
        re_set[i] = i

#生成数据
for i in range(4,10000):
    tmp = np.random.randint(0,4)
    re_set[i] = tmp
    for j in range(  data_set.shape[1] ):
        data_set[i][j] = data_set[i][j]
    for j in range(20):
        pos = np.random.randint(1,data_set.shape[1]-1)
        data_set[i][pos] = ((np.random.random()/10) + 0.9) * data_set[i][pos]

test_set = np.zeros((2000,1000))
re_test_set = np.zeros(2000)
for i in range(2000):
    tmp = np.random.randint(0,4)
    re_test_set[i] = tmp
    for j in range(  data_set.shape[1] ):
        test_set[i][j] = data_set[tmp][j]
    for j in range(20):
        pos = np.random.randint(1,test_set.shape[1]-1)
        test_set[i][pos] = ((np.random.random()/10) + 0.9) * test_set[i][pos]

data_w = {'data_set':data_set, 're_set':re_set, 'test_set':test_set, 're_test_set':re_test_set}

file_path = open("data.pkl",'wb')
pickle.dump(data_w,file_path)


