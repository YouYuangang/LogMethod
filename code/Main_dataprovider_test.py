#_*_coding:utf-8_*_
'''
作者：Y.G. You
创建时间：2020.10.14
更新时间：2020.10.28
'''
import os.path
import numpy as np
from data_helper_package import rawdata_provider
from data_helper_package import data_preprocesser
from data_helper_package import well_segment_provider
from log_plot_package import simple_log_plot


#项目根目录
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(path,'output')
images_path = os.path.join(output_path,'images')
#创建输出目录
if(os.path.exists(output_path)):
    pass
else:
    os.makedirs(output_path)
if(os.path.exists(images_path)):
    pass
else:
    os.makedirs(images_path)
print("path:"+path)

#测试示范文件
#去掉相应的一对注释查看运行结果是否正常，熟悉接口的使用


'''
#测试提供原始数据的类：rawdata_provider.RawDataProvider
#数据接口测试，入口文件
test = rawdata_provider.RawDataProvider()
#打印有多少口井
print("井数量："+str(test.get_well_count()))
#打印所有井的名字
print("所有井的名称："+str(test.get_well_allnames()))
#获取well116井的AC测井曲线
AC_data = test.get_column_floatData('well116','AC')
#获取well116井每个采样点对应的深度
depth = test.get_well_depthdata('well116')
#画图,未去除无效数据所以图有些奇怪
simple_log_plot.plot_log(depth,AC_data,"depth","AC")
'''

'''
#测试提供地层信息的类：well_segment_provider.WellSegmentProvider
wellsegmentProvider = well_segment_provider.WellSegmentProvider()
#打印well84包含哪些地层
print("well84包含的地层："+str(wellsegmentProvider.get_segmentnames_fromwell("well84")))
#打印well84井龙潭组地层的开始深度
print("well84龙潭组地层的开始深度："+str(wellsegmentProvider.get_segment_startdepth("well84","龙潭组")))
#打印那些包含石炭系地层的井名
print("含有石炭系地层的井："+str(wellsegmentProvider.get_wellnames_contains_segment("石炭系")))
#获取well84井龙潭组地层的AC数据
longtanzu_ac_data = wellsegmentProvider.get_segment_columndata("well84","龙潭组","AC")
#获取well84龙潭组地层的深度数据
depth = wellsegmentProvider.get_segment_depthdata("well84","龙潭组")
simple_log_plot.plot_log(depth,longtanzu_ac_data,"depth","AC")
'''

'''
#测试数据预处理的模块:data_helper_package.data_processer
test = rawdata_provider.RawDataProvider()
print(list(test.wellname_well_headinfo_dict.keys())[0])
#获取well84井AC数据
ac_data = test.get_column_floatData("well116","AC")
#获取well84深度数据
depth = test.get_well_depthdata("well116")
#去除原始数据中的无用数据
data_preprocesser.data_except_invalid(depth,ac_data)
#提取关键点，曲线粗化
depth1,data1 = data_preprocesser.getkeypoint_from_rawdata(depth,ac_data)
print("粗化前的采样点数："+str(len(ac_data)))
print("粗化后的采样点数："+str(len(data1)))
#画出原始曲线和粗化后的曲线
simple_log_plot.plot_2_log(depth1,data1,"depth","AC",depth,ac_data,"depth","AC")
'''

'''
#交汇图测试
rawdataprovider = rawdata_provider.RawDataProvider()
rawac = rawdataprovider.get_column_floatData("well131","ac")
rawrt = rawdataprovider.get_column_floatData("well131","rt")
data_preprocesser.except_invalid_for_multicolumn([rawac,rawrt])
rawac2 = rawdataprovider.get_column_floatData("well90","ac")
rawrt2 = rawdataprovider.get_column_floatData("well90","rt")
data_preprocesser.except_invalid_for_multicolumn([rawac2,rawrt2])
seris1,seris2 = data_preprocesser.preprocess_for_Jaccrad(rawac,rawrt,rawac2,rawrt2)
#绘制两口井的交汇图
simple_log_plot.cross_plot2d_for_2well([rawac,rawrt],[rawac2,rawrt2],xlabel_="AC",ylabel_="SP",wellname1="well116",wellname2="well84")
simple_log_plot.cross_plot2d_for_2well(seris1,seris2,xlabel_="AC",ylabel_="SP",wellname1="well116",wellname2="well84")
'''

'''
#查看原始的交会图与映射后的交会图的区别
rawdataprovider = rawdata_provider.RawDataProvider()
wellnamestemp = rawdataprovider.get_well_allnames()
columns = ["AC","RT"]
wellnames = []
for temp in wellnamestemp:
    if rawdataprovider.if_exist_column(temp,columns[0]) and rawdataprovider.if_exist_column(temp,columns[1]):
        wellnames.append(temp)
dict = {}
res = np.zeros((len(wellnames),len(wellnames)))
for i in range(len(wellnames)):
    data1 = rawdataprovider.get_column_floatData(wellnames[i],columns[0])
    data2 = rawdataprovider.get_column_floatData(wellnames[i],columns[1])
    dict[wellnames[i]]=[data1,data2]
for i in range(len(wellnames)):
    for j in range(len(wellnames)):
        if(i==j):
            res[i][j] = 1.0
            continue
        seris1x = dict[wellnames[i]][0]
        seris1y = dict[wellnames[i]][1]
        seris2x = dict[wellnames[j]][0]
        seris2y = dict[wellnames[j]][1]
        seris1 = [seris1x,seris1y]
        seris2 = [seris2x,seris2y]
        data_preprocesser.except_invalid_for_multicolumn(seris1)
        data_preprocesser.except_invalid_for_multicolumn(seris2)
        simple_log_plot.cross_plot2d_for_2well(seris1,seris2,columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[j]+" similarity:")
        seris1,seris2 = data_preprocesser.preprocess_for_Jaccrad_by_reduce(seris1x,seris1y,seris2x,seris2y)
        simple_log_plot.cross_plot2d_for_2well(seris1,seris2,columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[j]+" similarity:")
'''

'''
#根据AC与RT的交汇根据重叠面积算相似度
rawdataprovider = rawdata_provider.RawDataProvider()
wellnamestemp = rawdataprovider.get_well_allnames()
columns = ["AC","RT"]
wellnames = []
for temp in wellnamestemp:
    if rawdataprovider.if_exist_column(temp,columns[0]) and rawdataprovider.if_exist_column(temp,columns[1]):
        wellnames.append(temp)
dict = {}
res = np.zeros((len(wellnames),len(wellnames)))
for i in range(len(wellnames)):
    data1 = rawdataprovider.get_column_floatData(wellnames[i],columns[0])
    data2 = rawdataprovider.get_column_floatData(wellnames[i],columns[1])
    data_preprocesser.except_invalid_for_multicolumn([data1,data2])
    dict[wellnames[i]]=[data1,data2]
for i in range(len(wellnames)):
    max_similarity = -1
    most_similarity_index = 0
    well_most_similarity = ""
    after_transfer_data1 = []
    after_transfer_data2 = []
    for j in range(len(wellnames)):
        if(i==j):
            res[i][j] = 0.75
            continue
        seris1x = dict[wellnames[i]][0]
        seris1y = dict[wellnames[i]][1]
        seris2x = dict[wellnames[j]][0]
        seris2y = dict[wellnames[j]][1]
        
        seris1,seris2 = data_preprocesser.preprocess_for_Jaccrad(seris1x,seris1y,seris2x,seris2y)
        similarity = data_preprocesser.compute_acquaintance_byarea_100(seris1,seris2)
        if(similarity>max_similarity):
            well_most_similarity = wellnames[j]
            max_similarity = similarity
            most_similarity_index = j
            after_transfer_data1 = seris1
            after_transfer_data2 = seris2
        res[i][j] = similarity
        #展示过程图片
        #simple_log_plot.cross_plot2d_for_2well([seris1x,seris1y],[seris2x,seris2y],columns[0],columns[1],title="cross plot:"+wellnames[i]+" and "+wellnames[j]+",similarity:"+str(round(similarity,3)),wellname1=wellnames[i],wellname2=wellnames[j])
        #simple_log_plot.cross_plot2d_for_2well(seris1,seris2,columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[j]+" similarity:"+str(round(similarity,3)),wellname1=wellnames[i],wellname2=wellnames[j])
    #保存图片结果到文件  
    filepath = os.path.join(output_path,(wellnames[i]+"_"+wellnames[most_similarity_index]+".png" ))
    simple_log_plot.cross_plot2d_for_2well(dict[wellnames[i]],dict[wellnames[most_similarity_index]],columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[most_similarity_index]+" similarity:"+str(round(max_similarity,3)),wellname1=wellnames[i],wellname2=wellnames[most_similarity_index],saveflag=True,path=filepath)
    depth1 = rawdataprovider.get_well_depthdata(wellnames[i])
    data1 = rawdataprovider.get_column_floatData(wellnames[i],columns[1])
    depth2 = rawdataprovider.get_well_depthdata(wellnames[most_similarity_index])
    data2 = rawdataprovider.get_column_floatData(wellnames[most_similarity_index],columns[1])
    data_preprocesser.except_invalid_for_multicolumn([depth1,data1])
    data_preprocesser.except_invalid_for_multicolumn([depth2,data2])
    filepath = os.path.join(output_path,(wellnames[i]+"_"+wellnames[most_similarity_index]+"_curve.png" ))
    simple_log_plot.plot_2_log(depth1,data1,"depth",columns[1],depth2,data2,"depth",columns[1],saveflag=True,filepath=filepath)
    #filepath2 = os.path.join(output_path,(wellnames[i]+"_"+wellnames[most_similarity_index]+"_after_transfer"+".png" ))
    #simple_log_plot.cross_plot2d_for_2well(after_transfer_data1,after_transfer_data2,columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[most_similarity_index]+" similarity:"+str(round(max_similarity,3)),wellname1=wellnames[i],wellname2=wellnames[most_similarity_index],saveflag=True,path=filepath2)    
    print(wellnames[i]+"与"+well_most_similarity+"最相似:"+str(round(max_similarity,3)))
#保存相似矩阵
filepath = os.path.join(output_path,"simality_matrix.txt")
with open(filepath,"w") as f:
    for i in range(len(wellnames)):
        for j in range(len(wellnames)):
            f.write(str(round(res[i][j],3))+" ")
        f.write("\n")
#保存最相似的井
filepath = os.path.join(output_path,"most_similarity.txt")
with open(filepath,"w") as f:
    for i in range(len(wellnames)):
        max_similarity = -1
        well_most_similarity = ""
        for j in range(len(wellnames)):
            if(i == j):
                continue
            similarity = res[i][j]
            if(similarity>max_similarity):
                well_most_similarity = wellnames[j]
                max_similarity = similarity
        f.write(wellnames[i]+" "+well_most_similarity+" 最相似："+str(round(max_similarity,3)))
        f.write("\n")
#相似矩阵的热图
simple_log_plot.plt.figure()
simple_log_plot.plt.cla()
simple_log_plot.plt.imshow(res)
filepath = os.path.join(output_path,"similarity_matrix.png")
simple_log_plot.plt.savefig(filepath)
simple_log_plot.plt.show()
'''


'''
#根据AC与RT的交汇图，根据重叠采样点算相似度
rawdataprovider = rawdata_provider.RawDataProvider()
wellnamestemp = rawdataprovider.get_well_allnames()
columns = ["AC","DEN"]
wellnames = []
for temp in wellnamestemp:
    if rawdataprovider.if_exist_column(temp,columns[0]) and rawdataprovider.if_exist_column(temp,columns[1]):
        wellnames.append(temp)
dict = {}
res = np.zeros((len(wellnames),len(wellnames)))
for i in range(len(wellnames)):
    data1 = rawdataprovider.get_column_floatData(wellnames[i],columns[0])
    data2 = rawdataprovider.get_column_floatData(wellnames[i],columns[1])
    data_preprocesser.except_invalid_for_multicolumn([data1,data2])
    dict[wellnames[i]]=[data1,data2]
for i in range(len(wellnames)):
    max_similarity = -1
    most_similarity_index = 0
    well_most_similarity = ""
    after_transfer_data1 = []
    after_transfer_data2 = []
    for j in range(len(wellnames)):
        if(i==j):
            res[i][j] = 1.0
            continue
        seris1x = dict[wellnames[i]][0]
        seris1y = dict[wellnames[i]][1]
        seris2x = dict[wellnames[j]][0]
        seris2y = dict[wellnames[j]][1]
        if(len(seris1x)==0 or len(seris1y)==0 or len(seris2x)==0 or len(seris2y)==0):
            continue
        seris1,seris2 = data_preprocesser.preprocess_for_Jaccrad(seris1x,seris1y,seris2x,seris2y)
        similarity = data_preprocesser.compute_acquaintance_byarea_100_weight(seris1,seris2)
        if(similarity>max_similarity):
            well_most_similarity = wellnames[j]
            max_similarity = similarity
            most_similarity_index = j
            after_transfer_data1 = seris1
            after_transfer_data2 = seris2
        res[i][j] = similarity
        #展示过程图片
        #simple_log_plot.cross_plot2d_for_2well([seris1x,seris1y],[seris2x,seris2y],columns[0],columns[1],title="cross plot:"+wellnames[i]+" and "+wellnames[j]+",similarity:"+str(round(similarity,3)),wellname1=wellnames[i],wellname2=wellnames[j])
        #simple_log_plot.cross_plot2d_for_2well(seris1,seris2,columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[j]+" similarity:"+str(round(similarity,3)),wellname1=wellnames[i],wellname2=wellnames[j])
    #保存图片结果到文件  
    filepath = os.path.join(output_path,(wellnames[i]+"_"+wellnames[most_similarity_index]+"_jaccard"+".png" ))
    simple_log_plot.cross_plot2d_for_2well(dict[wellnames[i]],dict[wellnames[most_similarity_index]],columns[0],columns[1],title="cross plot:"+wellnames[i]+" "+wellnames[most_similarity_index]+" similarity_jac:"+str(round(max_similarity,3)),wellname1=wellnames[i],wellname2=wellnames[most_similarity_index],saveflag=True,path=filepath)    
    print(wellnames[i]+"与"+well_most_similarity+"最相似:"+str(round(max_similarity,3)))
#保存相似矩阵
filepath = os.path.join(output_path,"simality_matrix_jac.txt")
with open(filepath,"w") as f:
    for i in range(len(wellnames)):
        for j in range(len(wellnames)):
            f.write(str(round(res[i][j],3))+" ")
        f.write("\n")
#保存最相似的井
filepath = os.path.join(output_path,"most_similarity_jac.txt")
with open(filepath,"w") as f:
    for i in range(len(wellnames)):
        max_similarity = -1
        well_most_similarity = ""
        for j in range(len(wellnames)):
            if(i == j):
                continue
            similarity = res[i][j]
            if(similarity>max_similarity):
                well_most_similarity = wellnames[j]
                max_similarity = similarity
        f.write(wellnames[i]+" "+well_most_similarity+" 最相似："+str(round(max_similarity,3)))
        f.write("\n")
#相似矩阵的热图
simple_log_plot.plt.cla()
simple_log_plot.plt.imshow(res)
filepath = os.path.join(output_path,"similarity_matrix_jac.png")
simple_log_plot.plt.savefig(filepath)
simple_log_plot.plt.show()
'''

