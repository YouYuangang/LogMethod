from . import rawdata_provider
import numpy as np
INVALID_DATA = -99999.0
PRECISION = 0.0001
def is_valid_data(data):
    if(abs(data-INVALID_DATA)>PRECISION and data>INVALID_DATA):
        return True
    return False
def filter_by_threepoint(data,times):
    if len(data)<3:
        return data
    if times<1:
        return data
    for i in range(0,times):
        for j in range(1,len(data)-1):
            #data[j]=data[j-1]*0.15+data[j]*0.7+data[j+1]*0.15
            data[j]=data[j-1]*0.2+data[j]*0.6+data[j+1]*0.2

def data_except_invalid(depth,data):
    j=0
    for i in range(len(data)):
        if( is_valid_data(data[i])):
            data[j], depth[j] = data[i], depth[i]
            j+=1
    del data[j:]
    del depth[j:]

def keep_key_point(depth,data,start,end,threshold):
    ydata = data
    xdata = depth
    if(start>=end):
        return
    keypoint_index = -1
    max_dist = max(abs(ydata[end]-ydata[start])/3, threshold )#threshold
    k = ( ydata[end] - ydata[start] ) / ( xdata[end] - xdata[start] )
    b = ( ydata[start] * xdata[end] - ydata[end] * xdata[start] ) / ( xdata[end] - xdata[start] )
    for i in range(start+1,end):
        dist = abs( k * xdata[i] + b - ydata[i] )
        if ( dist > max_dist ):
            max_dist, keypoint_index = dist, i
    if( keypoint_index == -1 ):
        for i in range(start+1,end):
            ydata[i] = INVALID_DATA
        return
    keep_key_point(depth,data,start,keypoint_index,threshold)
    keep_key_point(depth,data,keypoint_index,end,threshold)

def getkeypoint_from_rawdata(depth,data,threshold = 10):
    depthT = depth.copy()
    dataT = data.copy()
    data_except_invalid(depthT,dataT)
    filter_by_threepoint(dataT,20)
    keep_key_point(depthT,dataT,0,len(dataT)-1,threshold)
    data_except_invalid(depthT,dataT)
    return depthT,dataT

class DataPreprocesser:
    rawDataGetter = rawdata_provider.RawDataProvider()
    def get_column_floatdata(self,wellName,columnName):
        rawdata = self.rawDataGetter.get_column_floatData(wellName,columnName)
        data = [x for x in rawdata if is_valid_data(x)]
        data_aver = np.mean(data)
        print("data len:"+str(len(data))+" aver:"+str(data_aver))
        for i in range(len(rawdata)):
            if is_valid_data(rawdata[i]):
                continue
            else:
                rawdata[i] = data_aver
        return rawdata

