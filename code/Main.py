#_*_coding:utf-8_*_
from data_helper_module import rawdata_getter
test = rawdata_getter.RawDataGetter()
wellCount = test.get_well_count()
test.printInfo()