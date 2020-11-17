import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
import pywt
from sklearn.decomposition import PCA
import similarity
import pickle

sys.path.append(r'code')
from data_helper_package import rawdata_provider
from data_helper_package import data_preprocesser
from data_helper_package import well_segment_provider
#设置画图中文输出

if sys.platform == 'darwin':
    font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
elif sys.platform == 'win32':
    font = FontProperties(fname='c:/window/fonts/sinsum.ttc')
else:
    pass
xdata = []
ydata = []
wells = []
columname = "GR"

def get_cr( x_set, y_set ):
    cr = []
    for i in range(len(x_set) -1 ):
        x,y = x_set[i+1] - x_set[i], y_set[i+1] - y_set[i]
        #length = math.sqrt(x*x + y*y)
        #x,y = x/length, y/length
        cr.append(np.array([x,y]))
    return cr

def diff(one, two,tmp_cos):
    one_len, two_len = len(one),len(two)
    db = np.zeros((one_len, two_len))
    one_lenth, two_lenth =0,0
    #计算出两条直线长度
    for i in range(0, one_len):
        one_lenth += np.linalg.norm(one[i])
    for j in range(0, two_len):
        two_lenth += np.linalg.norm(two[j])
    #计算db[0][0]
    if( np.dot( one[0]/np.linalg.norm(one[0]), two[0]/np.linalg.norm(two[0]) ) > tmp_cos ):
        if(one_lenth < two_lenth):
            db[0][0] = np.linalg.norm(one[0])
        else:
            db[0][0] = np.linalg.norm(two[0])
    else:
        db[0][0] = 0
    #计算db[i][0]
    for i in range(1,one_len):
        if( np.dot( one[i]/np.linalg.norm(one[i]), two[0]/np.linalg.norm(two[0]) ) > tmp_cos ):
                db[i][0] = max(db[i-1][0], min( np.linalg.norm(one[i]), np.linalg.norm(two[0]) ))
        else:
            db[i][0] = db[i-1][0]
    #计算db[0][j]
    for j in range(1,two_len):
        if( np.dot( one[0]/np.linalg.norm(one[0]), two[j]/np.linalg.norm(two[j]) ) > tmp_cos ):
                db[0][j] = max(db[0][j-1], min( np.linalg.norm(one[0]), np.linalg.norm(two[j])) )
        else:
            db[0][j] = db[0][j-1]
    #计算db[i][j]
    for i in range(1,one_len):
        for j in range(1,two_len):
            if ( np.dot( one[i]/np.linalg.norm(one[i]), two[j]/np.linalg.norm(two[j]) ) > tmp_cos ):
                    db[i][j] = max( db[i-1][j-1] + min(np.linalg.norm(one[i]),np.linalg.norm(two[j])), db[i-1][j], db[i][j-1] )
            else:
                db[i][j] = max( db[i-1][j-1] , db[i-1][j], db[i][j-1] )
    #返回相似线段长度
    if(one_lenth < two_lenth):
        return np.max(db)/one_lenth
    else:
        return np.max(db)/two_lenth

def diff_x(one, two,tmp_cos):
    one_len, two_len = len(one),len(two)
    db = np.zeros((one_len, two_len))
    one_lenth, two_lenth =0,0
    #计算出两条直线长度
    for i in range(0, one_len):
        one_lenth += one[i][0]
    for j in range(0, two_len):
        two_lenth += two[j][0]
    #计算db[0][0]
    if( np.dot( one[0]/np.linalg.norm(one[0]), two[0]/np.linalg.norm(two[0]) ) > tmp_cos ):
            db[0][0] = min(one[0][0],two[0][0])
    else:
        db[0][0] = 0
    #计算db[i][0]
    for i in range(1,one_len):
        if( np.dot( one[i]/np.linalg.norm(one[i]), two[0]/np.linalg.norm(two[0]) ) > tmp_cos ):
                db[i][0] = max(db[i-1][0], min( one[i][0], two[0][0] ))
        else:
            db[i][0] = db[i-1][0]
    #计算db[0][j]
    for j in range(1,two_len):
        if( np.dot( one[0]/np.linalg.norm(one[0]), two[j]/np.linalg.norm(two[j]) ) > tmp_cos ):
                db[0][j] = max(db[0][j-1], min( one[0][0], two[j][0]) )
        else:
            db[0][j] = db[0][j-1]
    #计算db[i][j]
    for i in range(1,one_len):
        for j in range(1,two_len):
            if ( np.dot( one[i]/np.linalg.norm(one[i]), two[j]/np.linalg.norm(two[j]) ) > tmp_cos ):
                    db[i][j] = max( db[i-1][j-1] + min(one[i][0], two[j][0]), db[i-1][j], db[i][j-1] )
            else:
                db[i][j] = max( db[i-1][j-1] , db[i-1][j], db[i][j-1] )
    #返回相似线段长度
    if(one_lenth < two_lenth):
        return np.max(db)/one_lenth
    else:
        return np.max(db)/two_lenth

        '''
        wavename = 'cgau8'
        totalscal = 256
        fc = pywt.central_frequency(wavename)
        cparam = 2 * fc * totalscal
        scales = cparam / np.arange(totalscal,1,-1)
        wt_data = ac_data.copy()
        [a,b] = pywt.cwt(wt_data, scales,wavename, 1.0/64)
        '''

def InitAndProcess_Cr(Init_Depth,Init_Value,Process_Depth,Process_Value,wellname):
    plt.figure("{}号井 原始图像及Douglas-Peuker图像 -- {}".format(wellname,columname), figsize=(5,10))
    plt.ylabel(u"深度",FontProperties=font)
    plt.gca().invert_yaxis()                                                                                                                                                                                                                                                                                                                                          
    plt.xlabel(columname)
    plt.gca().xaxis.set_ticks_position('top')
    plt.plot(  Init_Value, Init_Depth, label = "init")
    plt.plot( Process_Value, Process_Depth, label = "Douglas-Peuker")
    plt.legend()
    #plt.savefig("{}号井 原始图像及Douglas-Peuker图像--{}.jpg".format(wellname,columname))
    #plt.show()
    plt.close()

def Get_Cr_PointSet(wells,Seg = None):
    i=0
    for well in wells:
        try:
            ac_data = RawData.get_column_floatData(well, columname)
            depth = RawData.get_well_depthdata(well)
        except:
            continue
            #depth = np.arange(0,len(ac_data)).tolist()
        '''
        
        if(Seg.if_exist_segment(well, "龙潭组")):
            ac_data = Seg.get_segment_columndata(well, "龙潭组", "ac")
            depth = Seg.get_segment_depthdata(well,"龙潭组")
        else:
            continue
        '''
        
        #if well in ["well96","well121","well94","well90"]:
        #    continue
        tmp = depth[0]
        for j in range(len(depth)):
            depth[j] -= tmp
        data_preprocesser.data_except_invalid(depth,ac_data)
        x,y = data_preprocesser.getkeypoint_from_rawdata(depth,ac_data)
        InitAndProcess_Cr(depth,ac_data,x,y,well + "龙潭组")
        xdata.append(x)
        ydata.append(y)

        i+=1
        if(i == 21):
            break

    return xdata,ydata

def Cul_Similarity():
    result = np.zeros((len(ydata),len(ydata)))
    i=1.5
    tmp1,tmp2 = np.array([100-i,100+i])/np.linalg.norm(np.array([100-i,100+i])), np.array([100+i,100-i])/np.linalg.norm(np.array([100+i,100-i]))
    tmp_cos = np.dot(tmp1,tmp2)
    ( "tmp_cos = {}".format(tmp_cos))
    for i in range(len(ydata)):
        for j in range(i,len(ydata)):
            result[j][i] = result[i][j] = diff(cr[i],cr[j], tmp_cos) #+ diff_x(cr[i],cr[j], tmp_cos))/2
        result = np.around( result, decimals = 3 )

    for i in range( result.shape[0] ):
        print( result[i],end = "\n\n" )
    return result

def Similarity_Set(result):
    re = result>=0.45
    Similarity_Re = []
    for i in range(result.shape[0]):
        tmp = []
        for j in range( result.shape[1]):
            if re[i][j]:
                tmp.append(j)
        Similarity_Re.append(tmp)
        print(tmp)

        plt.figure("{}号井 相似井集合--{}曲线".format(wells[i],columname),figsize=(5,60))
        plt.ylabel(u"相对深度",FontProperties = font) 
        plt.gca().xaxis.set_ticks_position('top')
        plt.gca().invert_yaxis()                                                                                                                                                                                                                                                                                                                                  
        plt.xlabel(columname)
        for k in tmp:#range(len(tmp)):
            plt.plot( ydata[k], xdata[k], label = "{}".format(wells[k]) )
        plt.legend()
        plt.savefig("{}号井 相似井集合--{}曲线.jpg".format(wells[i],columname))
        #plt.show()
        plt.close()
    return Similarity_Re

def union_set( Similarity_Re ):
    for i in range(len(Similarity_Re)):
        for j in range(i + 1,len(Similarity_Re)):
            intersection = list(set(Similarity_Re[i]).intersection(set(Similarity_Re[j])))
            if( 3*len(intersection) >= len(Similarity_Re[i])*2 or  3*len(intersection) >= len(Similarity_Re[j])*2):
                Similarity_Re[j] = list(set(Similarity_Re[i]).union(set(Similarity_Re[j])))
                Similarity_Re[i] = []
                break
    li = list(range( len(Similarity_Re) ))
    li.reverse()
    for i in li:
        if( len(Similarity_Re[i]) == 0):
            Similarity_Re.pop(i)
    return Similarity_Re

def Paint_Similarity_Cr(Similarity_Re):
    i=0
    for tmp in Similarity_Re:
        print(tmp)
        string = ""
        for i in tmp:
            string += wells[i] + "-"
        plt.figure("{}".format(string),figsize=(5,10))
        plt.ylabel(u"相对深度",FontProperties = font) 
        plt.gca().xaxis.set_ticks_position('top')
        plt.gca().invert_yaxis()                                                                                                                                                                                                                                                                                                                                            
        plt.xlabel(columname)
        for k in tmp:#range(len(tmp)):
            plt.plot( ydata[k], xdata[k], label = "{}".format(wells[k]) )
        plt.legend()
        plt.savefig("{}-{}曲线.jpg".format(string,columname))
    #    plt.show()
        plt.close()

def Paint_example_classification(Similarity_Re):
    i = 0
    plt.figure(u"分类示例图",figsize=(7*len(Similarity_Re),60))
    plt.gca().invert_yaxis()
    plt.axis("off")
    for tmp in Similarity_Re:
        plt.plot( (np.array(ydata[min(tmp)]) + 200*i).tolist(), xdata[min(tmp)])
        #plt.annotate("dfhjkdashfjksdahfjksadhfkajdhfjksadh",xy=(1,1), xytext=(0,0)) #(10 + 200*i, 120))
        plt.text(15 + 200*i,100, "\n".join( [str(wells[item]) for item in tmp ] ) , horizontalalignment="left", verticalalignment = "top",fontsize=30)
        i += 1
    plt.savefig("分类示例.jpg")
    #plt.show()
    plt.close()
        

RawData = rawdata_provider.RawDataProvider()
wells = RawData.get_well_allnames()
Seg = well_segment_provider.WellSegmentProvider()

xdata, ydata = Get_Cr_PointSet( wells, Seg )
#得到所有图的曲线
cr = []
for i in range(len(ydata)):
    cr.append( get_cr(xdata[i], ydata[i]) )

#计算相似的结果
result = Cul_Similarity()



'''
file_path = open("tmp.pkl",'wb')
data = {'A_init':result}
pickle.dump(data,file_path)
'''
#求得相似集合
#Similarity_Re = Similarity_Set(result)
#集合合并
#Similarity_Re = union_set( Similarity_Re )
similarity.get_similarityMatrx(result)
X = np.zeros(result.shape)
Similarity_Re = similarity.K_means(result.shape[0],result,X)
#print(re_set)
#print(X)
print("*********************************************")
#绘制各个曲线的相似集合
Paint_Similarity_Cr( Similarity_Re )
#绘制分类
Paint_example_classification(Similarity_Re)
