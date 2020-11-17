from data_helper_package import rawdata_provider
from data_helper_package import data_preprocesser
from log_plot_package import simple_log_plot
from data_helper_package import fastdtw
rawdata_getter = rawdata_provider.RawDataProvider()
#需要分析的井
wellname_to_analysis = rawdata_provider.RawDataProvider().get_well_allnames()
#需要分析的曲线
columnname_to_analysis = "GR"
depths = []
datas = []

depths_keypoint = []
datas_keypoint = []

for i in range(len(wellname_to_analysis)):
    depth = rawdata_getter.get_well_depthdata(wellname_to_analysis[i])
    data = rawdata_getter.get_column_floatData(wellname_to_analysis[i],columnname_to_analysis)
    data_preprocesser.fill_invaliddata_use_aver(data)

    depth_key,data_key= data_preprocesser.getkeypoint_from_rawdata(depth,data)
    depths.append(depth)
    datas.append(data)

    depths_keypoint.append(depth_key)
    datas_keypoint.append(data_key)
    print("len_depth:"+str(len(depth_key)))
    print("len_data:"+str(len(data_key)))
    #simple_log_plot.plot_2_log(depths_keypoint[i],datas_keypoint[i],"depth","data",depths[i],datas[i],"depth1","data2")

info_1 = data_preprocesser.get_rake_ratio_and_linelen(depths_keypoint[0],datas_keypoint[0])
for i in range(len(wellname_to_analysis)):
    info_2 = data_preprocesser.get_rake_ratio_and_linelen(depths_keypoint[i],datas_keypoint[i])
    distance,list = fastdtw.fastdtw(info_1,info_2)
    simple_log_plot.correlation_plot_for_2well(depths_keypoint[0],datas_keypoint[0],depths_keypoint[i],datas_keypoint[i],map=list,xlabel="depth",ylabel=columnname_to_analysis)





