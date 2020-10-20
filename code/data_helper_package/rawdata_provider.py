#_*_coding:utf-8_*_
'''
作者：Y.G. You
创建时间：2020.10.14
'''
import sys
import os.path
import re
'''
RawDataProvider:返回所有井的名字，及对应的曲线名字。根据井的名字和曲线得到某列测井数据
        get_well_count():int 返回有多少口井
        get_well_allnames():返回所有井的名字
        get_well_Headinfo_byName(wellname):返回wellname井的井头信息（数据文本的头信息）
        get_Well_allcolumnnames(wellname):返回wellName井所有的列名（测井曲线名称）
        get_well_startdepth(wellname):返回测井数据开始的深度
        get_well_enddepth(wellname)：返回测井数据结束的深度
        get_column_floatdata_byname(String wellName,String columnName):返回float型数组，wellName井columnName列的数据
        get_segement_column_floatData(self,wellName,columnName,startDepth,endDepth):返回某一深度区间的某列的测井数据
'''
class RawDataProvider:
    #数据的目录
    data_dir=os.path.join(os.path.abspath(__file__),os.pardir,os.pardir,os.pardir,'data')
    #数据目录的文件列表
    filename_list = os.listdir(data_dir)
    #井名与该井文件路径对应关系
    wellname_well_headinfo_dict = {}
    #初始化，得到井文件列表，读取井文件头信息，保存井名与该井文件的路径对应关系
    def __init__(self):
        self.filename_list = os.listdir(self.data_dir)
        for filename in self.filename_list:
            filePath = os.path.join(self.data_dir,filename)
            if(os.path.isfile(filePath)):
                self.__putinto_dict_byfilepath(filePath)
    #返回data目录下有多少口井
    def get_well_count(self):
        return len(self.wellname_well_headinfo_dict)
    #返回所有井的名字
    def get_well_allnames(self):
        names = []
        for key in self.wellname_well_headinfo_dict:
            names.append(str(self.wellname_well_headinfo_dict[key].wellName))
        return names
    def get_well_allcolumn_names(self,wellname):
        well_headinfo = self.wellname_well_headinfo_dict[wellname]
        return well_headinfo.columnNames
    #输出读到的所有井头信息
    
    #根据井名返回井文件的头部信息
    def get_well_Headinfo_byName(self,wellName):
        return self.wellname_well_headinfo_dict[wellName]
    def get_well_startdepth(self,wellName):
        return self.wellname_well_headinfo_dict[wellName].startDepth
    def get_well_enddepth(self,wellName):
        return self.wellname_well_headinfo_dict[wellName].endDepth
    #根据井名与曲线名返回一列数据
    def get_column_floatData(self,wellName,columnName):
        wellHeadInfo = self.wellname_well_headinfo_dict[wellName]
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
        realRowCount = int((wellHeadInfo.endDepth - wellHeadInfo.startDepth)/wellHeadInfo.level)
        return data[0:realRowCount]
     #根据井名，曲线名,开始深度，结束深度，返回一段数据
    def get_segement_column_floatData(self,wellName,columnName,startDepth,endDepth):
        wellHeadInfo = self.wellname_well_headinfo_dict[wellName]
        if startDepth<wellHeadInfo.startDepth or endDepth>wellHeadInfo.endDepth:
            raise Exception("深度范围有误！")
        data = self.get_column_floatData(wellName,columnName)
        startIndex = round((startDepth-wellHeadInfo.startDepth)/wellHeadInfo.level)
        endIndex = round((endDepth-wellHeadInfo.startDepth)/wellHeadInfo.level)
        return data[startIndex:endIndex]
    #得到wellName井的深度列
    def get_well_depthdata(self,wellName):
        data = []
        wellHeadInfo = self.wellname_well_headinfo_dict[wellName]
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
                data.append(float(strList[0]))
                temp = f.readline()
        realRowCount = int((wellHeadInfo.endDepth - wellHeadInfo.startDepth)/wellHeadInfo.level)
        return data[0:realRowCount]
    #得到wellName井某一段的深度列
    def get_segement_well_depthData(self,wellName,startDepth,endDepth):
        wellHeadInfo = self.wellname_well_headinfo_dict[wellName]
        if startDepth<wellHeadInfo.startDepth or endDepth>wellHeadInfo.endDepth:
            raise Exception("深度范围有误！")
        data = self.get_well_depthdata(wellName)
        startIndex = round((startDepth-wellHeadInfo.startDepth)/wellHeadInfo.level)
        endIndex = round((endDepth-wellHeadInfo.startDepth)/wellHeadInfo.level)
        return data[startIndex:endIndex+1]
    #根据行索引获得深度
    def get_depth_byindex(self,wellName,index):
        wellInfo = self.wellname_well_headinfo_dict[wellName]
        depth = wellInfo.startDepth + wellInfo.level*index
        return depth
    #根据深度获得行索引
    def get_index_bydepth(self,wellName,depth):
        wellInfo = self.wellname_well_headinfo_dict[wellName]
        if(depth<wellInfo.startDepth or depth > wellInfo.endDepth):
            return -1
        index = round((depth - wellInfo.startDepth)/wellInfo.level)
        return index
    #私有函数，不用看，根据井文件路径读取头信息，并把井名与文件路径放入字典
    def __putinto_dict_byfilepath(self,filePath):
            wellDataHeadInfo = WellDataHeadInfo()
            with open(filePath,'r',encoding='gbk') as f:
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
            self.wellname_well_headinfo_dict[wellDataHeadInfo.wellName] = wellDataHeadInfo

    def print_info(self):
        for value in self.wellname_well_headinfo_dict:
            print("------------------------------读取到的测井信息------------------------------")
            print("wellName:"+(self.wellname_well_headinfo_dict[value]).wellName)
            print("startDepth:"+str((self.wellname_well_headinfo_dict[value]).startDepth))
            print("endDepth:"+str((self.wellname_well_headinfo_dict[value]).endDepth))
            print("level:"+str((self.wellname_well_headinfo_dict[value]).level))
            print("columnNames:")
            print((self.wellname_well_headinfo_dict[value]).columnNames)
            print("filePath:"+self.wellname_well_headinfo_dict[value].filePath)
            print("------------------------------  结束分割线  ------------------------------")
class WellDataHeadInfo:
    def __init__(self):
        self.wellName = ""
        self.startDepth = 0.0
        self.endDepth = 0.0
        self.level = 0.0
        self.columnNames = []
        self.filePath = ""