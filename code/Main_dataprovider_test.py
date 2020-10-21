#_*_coding:utf-8_*_
from data_helper_package import rawdata_provider
from log_plot_package import simple_log_plot
from data_helper_package import data_preprocesser
from data_helper_package import well_segment_provider

#测试rawdata_provider.RawDataProvider
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
#画图测试
simple_log_plot.plot_log(depth,AC_data)


#测试well_segment_provider.WellSegmentProvider
wellsegmentProvider = well_segment_provider.WellSegmentProvider()
#打印well84包含哪些地层
print("well84包含的地层："+str(wellsegmentProvider.get_segmentnames_fromwell("well84")))
#打印well84井龙潭组地层的开始深度
print("well84龙潭组地层的开始深度："+str(wellsegmentProvider.get_segment_startdepth("well84","龙潭组")))
#打印那些包含石炭系地层的井名
print("含有石炭系地层的井："+str(wellsegmentProvider.get_wellnames_contains_segment("石炭系")))
