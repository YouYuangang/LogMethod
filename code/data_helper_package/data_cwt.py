import matplotlib.pyplot as plt
import numpy as np
import pywt

import pywt.data
import rawdata_provider
from data_preprocesser import fill_invaliddata_use_aver

#获取well116井中的GR特性数据
RawDataProvider = rawdata_provider.RawDataProvider()
ac_data = RawDataProvider.get_column_floatData("well116","GR")
depth = RawDataProvider.get_well_depthdata("well116")

#对well116井中的GR特性数据做预处理，将无效值用总体有效平均值代替
fill_invaliddata_use_aver(ac_data)
sampling_rate = 8000 #采样频率
fc = pywt.central_frequency('mexh')#中心频率，cgau8对应的中心频率是0.7
print(fc)
totalscal = 10000#totalscal为想要分析的频率个数
cparam = 2 * fc * totalscal
scales = cparam/np.arange(totalscal,1,-1)

#原信号的深度和GR信号图像
plt.subplot(2,1,1)
plt.xlabel('depth(m)')
plt.ylabel('GR')
plt.plot(depth,ac_data)

#打印CWT的种类
print(pywt.wavelist(kind='continuous'))

#小波变换
[cwtmatr,frequencies]=pywt.cwt(ac_data,scales,'mexh',1/sampling_rate)
print(frequencies)
for i in range(len(frequencies)):
    if frequencies[i]>1:
        frequencies[i]=0
#小波变换后的图像显示
plt.subplot(2,1,2)
plt.xlabel('depth(m)')
plt.ylabel('GR-frequency(Hz)')
plt.contourf(depth,frequencies,abs(cwtmatr))
plt.colorbar()
plt.show()
