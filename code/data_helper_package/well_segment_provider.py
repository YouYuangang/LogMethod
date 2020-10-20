#_*_coding:utf-8_*_
'''
作者：Y.G. You
创建时间：2020.10.14
'''
import os
import re
from .rawdata_provider import RawDataProvider
'''
WellSegmentProvider类，根据井名提供该井的地层信息；根据井名和地层信息提供某一列测井数据
        get_segmentnames_fromwell(wellname):
        返回一个列表，为该井所有的地层名

        if_exist_segment(wellname,segmentname):
        返回布尔型值，判断wellname井是否含有segmentname地层

        get_segment_columndata(wellname,segmentname,columnname)
        返回浮点值列表，wellname井的segmentname地层的columnname测井数据

        get_segment_depthdata(wellname,segmentname)
        返回浮点值列表，wellname井segementname地层的每个采样点对应的深度

        get_wellnames_contains_segment(segmentname)
        返回井名的列表，那些含有segmentname地层的井会被返回

        get_segment_startdepth(wellname,segment)
        返回一个浮点值，表示wellname井segment地层的开始深度

        get_segment_enddepth(wellname,segment)
        返回一个浮点值，表示wellname井segment地层的结束深度

        get_segment_colorstring(wellname,segment)
        返回一个字符串，表示wellname井segment地层应该用什么颜色表示
'''
class WellSegmentProvider:
    rawdata_provider = RawDataProvider()
    wellname_segments_dict = {}
    segment_dir = ""
    filelist = []
    def __init__(self):
        segment_dir = os.path.join(os.path.abspath(__file__),os.pardir,os.pardir,os.pardir,'data','segmentInfo')
        filelist = os.listdir(segment_dir)
        for filename in filelist:
            wellname = filename.strip(".txt")
            filepath = os.path.join(segment_dir,filename)
            self.__putinto_wellsegments_dict(wellname,filepath)
    def __putinto_wellsegments_dict(self,wellname,filepath):
        segments = SegmentsInfo()
        self.__putinto_segments_dict(filepath,segments)
        
        self.wellname_segments_dict[wellname] = segments
    def __putinto_segments_dict(self,filepath,segments):
        with open(filepath,'r',encoding='gbk') as f:
            #print("读取："+filepath)
            f.readline()
            f.readline()
            rawstr = f.readline().strip("\n")
            while(rawstr!=""):
                str_subspace = re.sub(" +"," ",rawstr)
                strlist = str_subspace.split(" ")
                name = strlist[0]
                startdepth = float(strlist[1])
                enddepth = float(strlist[2])
                colorstring = strlist[4]
                segmentinfo = SegmentInfo()
                segmentinfo.startdepth = startdepth
                segmentinfo.enddepth = enddepth
                segmentinfo.colorstring = colorstring
                segments.name_info_dict_ofsegment[name] = segmentinfo
                rawstr = f.readline().strip("\n")
    def get_segmentnames_fromwell(self,wellname):
        segments_dict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
        names = []
        for segmentname in segments_dict:
            names.append(segmentname)
        return names
    def if_exist_segment(self,wellname,segmentname):
        segments_dict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
        for segmentname_dict in segments_dict:
            if segmentname_dict==segmentname:
                return True
        return False
    def get_segment_columndata(self,wellname,segmentname,columnname):
        data = self.rawdata_provider.get_column_floatData(wellname,columnname)
        segmentinfo = (self.wellname_segments_dict[wellname].name_info_dict_ofsegment)[segmentname]
        startindex = self.rawdata_provider.get_index_bydepth(wellname,segmentinfo.startdepth)
        endindex = self.rawdata_provider.get_index_bydepth(wellname,segmentinfo.enddepth)
        return data[startindex:endindex+1]
    def get_segment_depthdata(self,wellname,segmentname):
        segmentinfo = (self.wellname_segments_dict[wellname].name_info_dict_ofsegment)[segmentname]
        startindex = self.rawdata_provider.get_index_bydepth(wellname,segmentinfo.startdepth)
        endindex = self.rawdata_provider.get_index_bydepth(wellname,segmentinfo.enddepth)
        data = self.rawdata_provider.get_well_depthdata(wellname)
        return data[startindex,endindex+1]
    def get_wellnames_contains_segment(self,segmentname):
        names = []
        for wellname in self.wellname_segments_dict:
            segmentsdict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
            if segmentname in segmentsdict.keys():
                names.append(wellname)
            else:
                continue
        return names
    def get_segment_startdepth(self,wellname,segmentname):
        segmentsdict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
        return segmentsdict[segmentname].startdepth
    def get_segment_enddepth(self,wellname,segmentname):
        segmentsdict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
        return segmentsdict[segmentname].enddepth
    def get_segment_colorstring(self,wellname,segmentname):
        segmentsdict = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
        return segmentsdict[segmentname].colorstring
    def print_info(self):
        print("------------------------------读取到的地层信息------------------------------")
        for wellname in self.wellname_segments_dict:
            print("井名："+ wellname)
            segments = self.wellname_segments_dict[wellname].name_info_dict_ofsegment
            for segmentname in segments:
                print("地层名称："+segmentname)
                segmentinfo = segments[segmentname]
                segmentinfo.print_info()
            print("\n")
        print("------------------------------ 地层信息结束 ------------------------------")
class SegmentInfo:
    def __init__(self):
        self.startdepth = 0.0
        self.enddepth = 0.0 
        self.colorstring = ""
    def print_info(self):
        print("开始深度"+str(self.startdepth))
        print("结束深度:"+str(self.enddepth))
        print("颜色控制字符串:"+self.colorstring)
class SegmentsInfo:
    def __init__(self):
        self.name_info_dict_ofsegment = {}



            