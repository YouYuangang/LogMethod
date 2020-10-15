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
    #数据的目录的父目录
    data_parDir=""
    #数据的目录
    data_dir = ""
    #数据目录的文件列表
    filename_list = []
    #井名与该井文件路径对应关系
    wellName_filepath_dict = {}
    #初始化，得到井文件列表，读取井文件头信息，保存井名与该井文件的路径对应关系
    def __init__(self):
        self.data_parDir = os.path.abspath(os.path.join(sys.path[0],os.pardir))
        self.data_dir = os.path.join(self.data_parDir,'data')
        self.filename_list = os.listdir(self.data_dir)
        self.wellName_filepath_dict = {}
        for filename in self.filename_list:
            filePath = os.path.join(self.data_dir,filename)
            if(os.path.isfile(filePath)):
                self.putinto_dict_byfilePath(filePath)
    #返回data目录下有多少口井
    def get_well_count(self):
        return len(self.wellName_filepath_dict)
    #返回所有井的名字
    def get_allwell_names(self):
        names = []
        for key in self.wellName_filepath_dict:
            names.append(str(self.wellName_filepath_dict[key].wellName))
        return names
    #根据井文件路径读取头信息，并把井名与文件路径放入字典
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
                wellDataHeadInfo.startDepth = float(strList[1])
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
    #输出读到的井头信息
    def printInfo(self):
        for value in self.wellName_filepath_dict:
            print("wellName:"+(self.wellName_filepath_dict[value]).wellName)
            print("startDepth:"+str((self.wellName_filepath_dict[value]).startDepth))
            print("endDepth:"+str((self.wellName_filepath_dict[value]).endDepth))
            print("level:"+str((self.wellName_filepath_dict[value]).level))
            print("columnNames:")
            print((self.wellName_filepath_dict[value]).columnNames)
            print("filePath:"+self.wellName_filepath_dict[value].filePath)
            print("------------------------------------------------------------")
    def get_floatData_fromColumn(self,wellName,columnName):
        wellHeadInfo = self.wellName_filepath_dict[wellName]
        data = []
        allcolumn_names =[x.upper() for x in wellHeadInfo.columnNames]
        toRead_index = allcolumn_names.index(columnName.upper())+1
        with open(wellHeadInfo.filePath,'r',encoding='gbk') as f:
            #跳过文件头部信息
            for i in range(7):
                f.readline()
            #全部转为大写
            
            #得到一行的数据列表
            temp = f.readline()
            while temp!="" and temp!="\n":
                strLine = re.sub(" +"," ",temp.strip('\n'))
                strList = strLine.split(" ")
                data.append(float(strList[toRead_index]))
                temp = f.readline()
        return data
class WellDataHeadInfo:
    def __init__(self):
        self.wellName = ""
        self.startDepth = 0.0
        self.endDepth = 0.0
        self.level = 0.0
        self.columnNames = []
        self.filePath = ""


        