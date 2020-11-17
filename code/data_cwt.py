import matplotlib.pyplot as plt
import numpy as np
import pywt
import sys
import pywt.data

from data_helper_package import rawdata_provider
from data_helper_package.data_preprocesser import fill_invaliddata_use_aver
from data_helper_package.data_preprocesser import getkeypoint_from_rawdata
import os

#获取所有井的名称
RawDataProvider = rawdata_provider.RawDataProvider()
well_names = RawDataProvider.get_well_allnames()
path0 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
save_path_before = os.path.join(path0,'pic_before')
save_path_after = os.path.join(path0,'pic_after')
central_frequencies = {}

i = 1

#对每个井的每个指标画图
for well in well_names:
    
    if well not in ['well116', 'well118', 'well119', 'well120', 'well121', 'well123', 'well131', 
                    'well52', 'well60', 'well68', 'well77', 'well79', 'well84', 'well90', 'well92', 'well94', 'well95']:
        detecting_names = RawDataProvider.get_well_allcolumn_names(well)#得到这口井的所有测量数据
        well_central_frequency = dict.fromkeys(detecting_names)#先建立一个字典，用于存储这口井的所有指标的中心频率
        central_frequencies[well] = well_central_frequency#再建立一个字典，用于储存所有井的所有指标的中心频率
        
        #创建图片的存储路径
        save_path_each_well_before = os.path.join(save_path_before, well)
        os.mkdir(save_path_each_well_before)
        save_path_each_well_after = os.path.join(save_path_after, well)
        os.mkdir(save_path_each_well_after)
        
        for detecting_name in detecting_names:
            
            ac_data = RawDataProvider.get_column_floatData(well,detecting_name)
            depth = RawDataProvider.get_well_depthdata(well)
            #fill_invaliddata_use_aver(ac_data)#对井中的特性数据做预处理，将无效值用总体有效平均值代替
            
            
            
            new_depth, new_data = getkeypoint_from_rawdata(depth, ac_data)#对数据做了三个预处理操作包括：去除无效值，平滑处理，曲线粗化
            sampling_rate = 8000 #采样频率
            
            #这里构造一个字典，记录这些数据的中心频率
            fc = pywt.central_frequency('mexh')#中心频率，cgau8对应的中心频率是0.7
            well_central_frequency[detecting_name] = fc
            
            filter('nan', new_data)
            if len(new_data)>20:
            
                #绘制原信号图并保存
                pic_str = save_path_each_well_before + '\\' + well + '_' + detecting_name + '.png'
                plt.figure(i)
                plt.plot(new_depth, new_data)
                plt.savefig(pic_str)
                i += 1
                
                #绘制小波变换后的信号图并保存
                totalscal = 10000#totalscal为想要分析的频率个数
                cparam = 2 * fc * totalscal
                scales = cparam/np.arange(totalscal,1,-1)
                # list_of_frequencies = [] 
                # list_of_cwtmatr = []
                [cwtmatr, frequencies]=pywt.cwt(new_data,scales,'mexh',1/sampling_rate)
                pic_str = save_path_each_well_after + '\\' + well + '_' + detecting_name + '-frequency(Hz).png'
                plt.figure(i)
                plt.contourf(new_depth, frequencies, abs(cwtmatr))
                plt.savefig(pic_str)
                i += 1
                if i>=5:
                    plt.close(i-4)




# #对well116井中的GR特性数据做预处理，将无效值用总体有效平均值代替
# fill_invaliddata_use_aver(ac_data)
# sampling_rate = 8000 #采样频率
# fc = pywt.central_frequency('mexh')#中心频率，cgau8对应的中心频率是0.7
# print(fc)
# totalscal = 10000#totalscal为想要分析的频率个数
# cparam = 2 * fc * totalscal
# scales = cparam/np.arange(totalscal,1,-1)

# #原信号的深度和GR信号图像
# plt.subplot(2,1,1)
# plt.xlabel('depth(m)')
# plt.ylabel('GR')
# plt.plot(depth,ac_data)


# #打印CWT的种类
# print(pywt.wavelist(kind='continuous'))

# #小波变换

# [cwtmatr,frequencies]=pywt.cwt(ac_data,scales,'mexh',1/sampling_rate)
# print(frequencies)
# # for i in range(len(frequencies)):
# #     if frequencies[i]>1:
# #         frequencies[i]=0

# #小波变换后的图像显示
# plt.subplot(2,1,2)
# plt.xlabel('depth(m)')
# plt.ylabel('GR-frequency(Hz)')

# plt.contourf(depth,frequencies,abs(cwtmatr))
# plt.colorbar()

# plt.show()
