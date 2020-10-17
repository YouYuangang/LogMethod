#_*_coding:utf-8_*_
from data_helper_module import rawdata_provider
from log_plot import simple_log_plot
from data_helper_module import data_preprocesser
#数据接口测试，入口文件
test = rawdata_provider.RawDataProvider()
#打印有多少口井
print("井数量："+str(test.get_well_count))
#打印所有井的名字
print(test.get_well_allnames())
#获取well116井的AC测井曲线
AC_data = test.get_column_floatData('well116','AC')
print("采样点数："+str(len(AC_data)))
depth = test.get_well_depthdata('well116')
#画图测试
#simple_log_plot.plot_log(depth,AC_data)

data_preprocesser = data_preprocesser.DataPreprocesser()
AC_data2 = data_preprocesser.get_column_floatdata('well116','AC')
print(AC_data2[-10:-1])
simple_log_plot.plot_log(depth,AC_data2)
