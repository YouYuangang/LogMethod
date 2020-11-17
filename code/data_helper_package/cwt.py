import matplotlib.pyplot as plt
import numpy as np
import pywt
import pywt.data
from data_helper_package import rawdata_provider
from data_helper_package.data_preprocesser import fill_invaliddata_use_aver

#获取well116井中的AC特性数据
RawDataProvider = rawdata_provider.RawDataProvider()
ac_data = RawDataProvider.get_column_floatData("well116","AC")
depth = RawDataProvider.get_well_depthdata("well116")
#对well116井中的AC特性数据做预处理，将无效值用总体有效平均值代替
fill_invaliddata_use_aver(ac_data)

sampling_rate = 13000 #采样频率
fc = pywt.central_frequency('cgau8')#中心频率
print("fc中心频率cgau8"+str(fc))
totalscal = 1000
cparam = 2 * fc * totalscal
scales = cparam/np.arange(totalscal,1,-1)

#原信号的深度和AC信号图像
plt.subplot(2,1,1)
plt.xlabel('depth(m)')
plt.ylabel('AC')
plt.plot(depth,ac_data)

#打印CWT的种类
print(pywt.wavelist(kind='continuous'))

#小波变换
[cwtmatr,frequencies]=pywt.cwt(ac_data,scales,'gaus8',1.0/8)
energe = abs(cwtmatr)
print(energe.shape)
plt.figure(0)
plt.plot(energe[0,:])

print("max:"+str(energe.max()))
print("min:"+str(energe.min()))
#小波变换后的图像显示
plt.figure(1)
plt.subplot(2,1,2)
plt.xlabel('depth(m)')
plt.ylabel('AC-frequency(Hz)')
plt.contourf(depth,frequencies,np.log(energe))
plt.colorbar()
plt.show()
