#_*_coding:utf-8_*_
import sys
import os.path
import re
'''
作者：Y.G. You
创建时间：2020.10.14
得到所有井的名字，及对应的曲线名字
根据井的名字和曲线得到某列测井数据
'''
class RawDataGetter:
    def __init__(self):
        self.data_parDir = os.path.abspath(os.path.join(sys.path[0],os.pardir))
        self.data_dir = os.path.join(self.data_parDir,'data')
        self.filename_list = os.listdir(self.data_dir)
        self.wellName_filepath_dict = {}
        for filename in self.filename_list:
            filePath = os.path.join(self.data_dir,filename)
            self.putinto_dict_byfilePath(filePath)

    def get_well_count(self):
        print(self.data_dir)
        return len(self.filename_list)
    
    def putinto_dict_byfilePath(self,filePath):
            wellDataHeadInfo = WellDataHeadInfo()
            with open(filePath,'r',encoding='gbk') as f:
                wellDataHeadInfo = WellDataHeadInfo()
                #名字
                linStr = f.readline().strip('\n')
                strList1 = re.split('=| ',linStr)
                strList = [x.strip() for x in strList1 if x.strip()!='']
                
                wellDataHeadInfo.wellName = strList[1]
                #开始深度
                linStr = f.readline().strip('\n')
                strList1 = re.split('=| ',linStr)
                strList = [x.strip() for x in strList1 if x.strip()!='']
                
                wellDataHeadInfo.sartDepth = float(strList[1])
                #结束深度
                linStr = f.readline().strip('\n')
                strList1 = re.split('=| ',linStr)
                strList = [x.strip() for x in strList1 if x.strip()!='']
                wellDataHeadInfo.endDepth = float(strList[1])
                #采样率
                linStr = f.readline().strip('\n')
                strList1 = re.split('=| ',linStr)
                strList = [x.strip() for x in strList1 if x.strip()!='']
                wellDataHeadInfo.level = float(strList[1])
                #各列的名字
                linStr = f.readline().strip('\n')
                strList1 = re.split('=| |,',linStr)
                strList = [x.strip() for x in strList1 if x.strip()!='']
                for i in range(1,len(strList)):
                    wellDataHeadInfo.columnNames.append(strList[i])
            wellDataHeadInfo.filePath = filePath
            self.wellName_filepath_dict[wellDataHeadInfo.wellName] = wellDataHeadInfo
    def printInfo(self):
        for value in self.wellName_filepath_dict:
            print("wellName:"+(self.wellName_filepath_dict[value]).wellName)
            print("columnNames:")
            print((self.wellName_filepath_dict[value]).columnNames)
            print("filePath:"+(self.wellName_filepath_dict[value]).filePath)
class WellDataHeadInfo:
    def __init__(self):
        self.wellName = ""
        self.sartDepth = 0.0
        self.endDepth = 0.0
        self.level = 0.0
        self.columnNames = []
        self.filePath = ""