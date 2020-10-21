from . import rawdata_provider
import numpy as np
INVALID_DATA = -99999.0
PRECISION = 0.0001
def is_valid_data(data):
    if(abs(data-INVALID_DATA)>PRECISION):
        return True
    return False
class DataPreprocesser:
    rawDataGetter = rawdata_provider.RawDataProvider()
    def get_column_floatdata(self,wellName,columnName):
        rawdata = self.rawDataGetter.get_column_floatData(wellName,columnName)
        data = [x for x in rawdata if is_valid_data(x)]
        data_aver = np.mean(data)
        print("data len:"+str(len(data))+" aver:"+str(data_aver))
        for i in range(len(rawdata)):
            if is_valid_data(rawdata[i]):
                continue
            else:
                rawdata[i] = data_aver
        return rawdata

