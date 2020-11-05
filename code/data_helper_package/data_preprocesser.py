#_*_coding:utf-8_*_
'''
作者：Y.G. You
创建时间：2020.10.14
更新时间：2020.10.28
'''
import rawdata_provider
import numpy as np
'''
is_valid_data(data):返回值布尔型，判断数据是否是有效值
data_except_invalid(depth,data):无返回值，删除数据中的无效值
keep_key_point(depth,data,start,end,threshold)：无返回值，只留下数据中的关键采样点
filter_by_threepoint(data,times)：无返回值，三点平滑处理
getkeypoint_from_rawdata(depth,data)
返回值为两个列表depth,data,对数据做了三个预处理操作包括：去除无效值，平滑处理，曲线粗化
'''
INVALID_DATA = -99999.0
INVALID_DATA2 = -1000.0
PRECISION = 0.0001
logstream = open("logmethod_log.txt", "w")
#判断数据是否有效
def is_valid_data(data):
    if(abs(data-INVALID_DATA)>PRECISION and data>INVALID_DATA2):
        return True
    return False
#对数据原地做三点平滑处理
def filter_by_threepoint(data,times):
    if len(data)<3:
        return data
    if times<1:
        return data
    for i in range(0,times):
        for j in range(1,len(data)-1):
            data[j]=data[j-1]*0.2+data[j]*0.6+data[j+1]*0.2
#对单列数据删除数据无效的采样点
def data_except_invalid(*args):
    if(len(args)==1):
        data = args[0]
        j=0
        for i in range(len(data)):
            if(is_valid_data(data[i])):
                data[j]= data[i]
                j+=1
        del data[j:]
    elif(len(args)==2):
        depth = args[0]
        data = args[1]
        j=0
        for i in range(len(data)):
            if( is_valid_data(data[i])):
                data[j], depth[j] = data[i], depth[i]
                j+=1
        del data[j:]
        del depth[j:]
#对多列数据删除数据无效的采样点
def except_invalid_for_multicolumn(datas,depth=None):
    index = 0
    columncount = len(datas)
    pointcount = len(datas[0])
    for i in range(pointcount):
        flag = True
        for j in range(columncount):
            data = datas[j]
            temp = data[i]
            if(is_valid_data(temp)==False):
                flag = False
                break
        if(flag == True):
            for k in range(columncount):
                datas[k][index] = datas[k][i]
            if(depth!=None):
                depth[index] = depth[i]
            index = index+1
        else:
            continue
    for k in range(columncount):
        del(datas[k][index:])
#对具有无效数据的采样点，用平均值代替，并不删除
def fill_invaliddata_use_aver(data):
    dataT = data.copy()
    data_except_invalid(dataT)
    aver = np.mean(dataT)
    for i in range(len(data)):
        if is_valid_data(data[i]):
            continue
        else:
            data[i] = aver
#保留关键点
def keep_key_point(depth,data,start,end,threshold):
    ydata = data
    xdata = depth
    if(start>=end):
        return
    keypoint_index = -1
    max_dist = threshold
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
#对单列数据，去除无效值，平滑，取关键点。DTW预处理
def getkeypoint_from_rawdata(depth,data):
    depthT = depth.copy()
    dataT = data.copy()
    data_except_invalid(depthT,dataT)
    filter_by_threepoint(dataT,20)
    threshold = np.mean(dataT)/10.0
    keep_key_point(depthT,dataT,0,len(dataT)-1,threshold)
    data_except_invalid(depthT,dataT)
    return depthT,dataT
#为了方便数重叠的点，又不错位点的分布，两个系列的X一起归约到0-100
def preprocess_for_Jaccrad(seris1x,seris1y,seris2x,seris2y):
    seris1x_ = seris1x.copy()
    seris1y_ = seris1y.copy()
    seris2x_ = seris2x.copy()
    seris2y_ = seris2y.copy()
    except_invalid_for_multicolumn([seris1x_,seris1y_])
    except_invalid_for_multicolumn([seris2x_,seris2y_])
    #得到相对平均值的振幅
    seris1x_[:] = seris1x_[:]-np.mean(seris1x_)
    seris1y_[:] = seris1y_[:]-np.mean(seris1y_)
    seris2x_[:] = seris2x_[:]-np.mean(seris2x_)
    seris2y_[:] = seris2y_[:]-np.mean(seris2y_)
    transer_to_0_100([seris1x_,seris2x_])
    transer_to_0_100([seris1y_,seris2y_])
    return [seris1x_,seris1y_],[seris2x_,seris2y_]
    #for i in range(len(datas)):
        #filter_by_threepoint(datas[i],10)
#为了方便数重叠的点，又不错位点的分布，两个系列的X一起缩小两倍，取整
def preprocess_for_Jaccrad_by_reduce(seris1x,seris1y,seris2x,seris2y):
    seris1x_ = seris1x.copy()
    seris1y_ = seris1y.copy()
    seris2x_ = seris2x.copy()
    seris2y_ = seris2y.copy()
    except_invalid_for_multicolumn([seris1x_,seris1y_])
    except_invalid_for_multicolumn([seris2x_,seris2y_])
    seris1x_[:] = seris1x_[:]-np.mean(seris1x_)
    seris1y_[:] = seris1y_[:]-np.mean(seris1y_)
    seris2x_[:] = seris2x_[:]-np.mean(seris2x_)
    seris2y_[:] = seris2y_[:]-np.mean(seris2y_)
    reduce_to_times_less([seris1x_,seris2x_])
    reduce_to_times_less([seris1y_,seris2y_])
    return [seris1x_,seris1y_],[seris2x_,seris2y_]
    #for i in range(len(datas)):
        #filter_by_threepoint(datas[i],10)
#根据映射后的分布算面积，一格的面积为1
def compute_acquaintance_byarea_100(seris1,seris2):
    mat1 = np.zeros((100,100))
    for i in range(len(seris1[0])):
        index1 = seris1[0][i]
        index2 = seris1[1][i]
        mat1[index1,index2] = mat1[index1,index2] + 1
    mat2 = np.zeros((100,100))
    for i in range(len(seris2[0])):
        index1 = seris2[0][i]
        index2 = seris2[1][i]
        mat2[index1,index2] = mat2[index1,index2] + 1
    overlap_count = 0
    all_count = 0
    for i in range(100):
        for j in range(100):
            if(max(mat1[i][j],mat2[i][j])>1):
                all_count = all_count + 1
            if(min(mat1[i][j],mat2[i][j])>1):
                overlap_count = overlap_count+1
    return float(overlap_count)/all_count
#根据缩小后的分布算面积，一格的面积为1
def compute_acquaintance_byarea_reduce(seris1,seris2):
    
    maxx = int(max(max(seris1[0]),max(seris2[0])))+1
    maxy = int(max(max(seris1[1]),max(seris2[1])))+1
    mat1 = np.zeros((maxx,maxy))
    for i in range(len(seris1[0])):
        index1 = round(seris1[0][i])
        index2 = round(seris1[1][i])
        mat1[index1,index2] = mat1[index1,index2] + 1
    mat2 = np.zeros((maxx,maxy))
    for i in range(len(seris2[0])):
        index1 = round(seris2[0][i])
        index2 = round(seris2[1][i])
        mat2[index1,index2] = mat2[index1,index2] + 1
    overlap_count = 0
    all_count = 0
    #除去点太少的区域
    for i in range(maxx):
        for j in range(maxy):
            if(mat1[i,j]<3):
                mat1[i,j] = 0
            if(mat2[i,j]<3):
                mat2[i,j] = 0
    for i in range(maxx):
        for j in range(maxy):
            #temp = str(mat1[i][j])+" "
            #logstream.write(temp)
            if(max(mat1[i][j],mat2[i][j])>0):
                all_count = all_count + 1
            if(if_mat1_mat2_i_j_neighbor(i,j,mat1,mat2)):
                overlap_count = overlap_count+1
        #logstream.write("\n")
    return float(overlap_count)/all_count
def if_mat1_mat2_i_j_neighbor(i,j,mat1,mat2):
    row = np.size(mat1,0)
    col = np.size(mat1,1)
    res1 = mat1[i,j]
    if(res1<=0):
        return False
    for ii in range(i-1,i+2):
        for jj in range(j-1,j+2):
            if(ii>=0 and ii<row and jj>= 0 and jj< col):
                if(mat2[ii,jj]>0):
                    mat2[ii,jj] = 0
                    return True

#将分布空间映射到100*100
def transer_to_0_100(datas):
    minvalue = min(np.min(datas[0]),np.min(datas[1]))
    maxvalue = max(np.max(datas[0]),np.max(datas[1]))
    for i in range(len(datas[0])):
        datas[0][i] = round((datas[0][i]-minvalue)/(maxvalue-minvalue)*99.0)
    for i in range(len(datas[1])):
        datas[1][i] = round((datas[1][i]-minvalue)/(maxvalue-minvalue)*99.0)
#将分布空间等比缩小某个倍数
def reduce_to_times_less(datas):
    minvalue = min(np.min(datas[0]),np.min(datas[1]))
    maxvalue = max(np.max(datas[0]),np.max(datas[1]))
    maxgap = (maxvalue-minvalue)/3.0
    for i in range(len(datas[0])):
        datas[0][i] = round((datas[0][i]-minvalue)/(maxvalue-minvalue)*maxgap)+0.0
    for i in range(len(datas[1])):
        datas[1][i] = round((datas[1][i]-minvalue)/(maxvalue-minvalue)*maxgap)+0.1
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