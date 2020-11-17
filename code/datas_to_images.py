from data_helper_package import rawdata_provider
from data_helper_package import data_preprocesser
from log_plot_package import simple_log_plot
column_names = ["AC","GR","RT"]
data_getter = rawdata_provider.RawDataProvider()
wellnames = data_getter.get_well_allnames()
Depths = []
ACs = []
GRs = []
RTs = []
for i in range(len(wellnames)):
    depth = data_getter.get_well_depthdata(wellnames[i])
    data0 = data_getter.get_column_floatData(wellnames[i],column_names[0])
    data_preprocesser.fill_invaliddata_use_aver(data0)
    data1 = data_getter.get_column_floatData(wellnames[i],column_names[1])
    data_preprocesser.fill_invaliddata_use_aver(data1)
    data2 = data_getter.get_column_floatData(wellnames[i],column_names[2])
    data_preprocesser.fill_invaliddata_use_aver(data2)
    Depths.append(depth)
    data_preprocesser.normalize_bymean(data0)
    data_preprocesser.filter_by_threepoint(data0,20)
    ACs.append(data0)
    data_preprocesser.normalize_bymean(data1)
    data_preprocesser.filter_by_threepoint(data1,20)
    GRs.append(data1)
    data_preprocesser.normalize_bymean(data2)
    data_preprocesser.filter_by_threepoint(data2,20)
    RTs.append(data2)
    #simple_log_plot.plot_log(Depths[i],ACs[i])
    #simple_log_plot.plot_log(Depths[i],GRs[i])
    #simple_log_plot.plot_log(Depths[i],RTs[i])
print("数据读入完成")

for i in range(len(Depths)):
    simple_log_plot.plt.figure(figsize = (14,6))
    simple_log_plot.plt.stackplot(Depths[i],ACs[i],GRs[i],RTs[i],labels=[column_names[0],column_names[1],column_names[2]])
    simple_log_plot.plt.legend()
    simple_log_plot.plt.ylim(0,3)
    simple_log_plot.plt.show()    






