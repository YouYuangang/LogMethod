#_*_coding:utf-8_*_
from data_helper_package import rawdata_provider
from log_plot_package import simple_log_plot
from data_helper_package import data_preprocesser
from data_helper_package import well_segment_provider

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


#测试数据预处理的模块:data_helper_package.data_processer
test = rawdata_provider.RawDataProvider()
#获取well84井AC数据
ac_data = test.get_column_floatData("well84","cal")
#获取well84深度数据
depth = test.get_well_depthdata("well84")
#去除原始数据中的无用数据
data_preprocesser.data_except_invalid(depth,ac_data)
#提取关键点，曲线粗化
depth1,data1 = data_preprocesser.getkeypoint_from_rawdata(depth,ac_data)
print("粗化前的采样点数："+str(len(ac_data)))
print("粗化后的采样点数："+str(len(data1)))
#画出原始曲线和粗化后的曲线
simple_log_plot.plot_2_log(depth1,data1,"depth","CAL",depth,ac_data,"depth","CAL")
