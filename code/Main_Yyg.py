#_*_coding:utf-8_*_
from data_helper_module import rawdata_getter
#数据接口测试，入口文件
test = rawdata_getter.RawDataGetter()
#打印有多少口井
print("井数量："+str(test.get_well_count()))
#打印所有井的名字
print(test.get_allwell_names())
#获取well116井的AC测井曲线
data = test.get_floatData_fromColumn('well116','AC')
print("采样点数："+str(len(data)))
print(data[-67:-1])