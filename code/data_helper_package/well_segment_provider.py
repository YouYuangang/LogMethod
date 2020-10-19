import os
import re
class SegmentInfo:
    startdepth = 0.0
    enddepth = 0.0 
    colorstring = ""
    def print_info(self):
        print("开始深度"+str(self.startdepth))
        print("结束深度:"+str(self.enddepth))
        print("颜色控制字符串:"+self.colorstring)

class SegmentsInfo:
    name_info_dict_ofsegment = {}
class WellSegmentProvider:
    wellname_segments_dict = {}
    segment_dir = ""
    filelist = []
    def __init__(self):
        self.segment_dir = os.path.join(os.path.abspath(__file__),os.pardir,os.pardir,os.pardir,'data','segmentInfo')
        filelist = os.listdir(self.segment_dir)
        for filename in filelist:
            wellname = filename.strip(".txt")
            filepath = os.path.join(self.segment_dir,filename)
            self.__putinto_wellsegments_dict(wellname,filepath)
    def __putinto_wellsegments_dict(self,wellname,filepath):
        segments = SegmentsInfo()
        self.__putinto_segments_dict(filepath,segments)
        self.wellname_segments_dict[wellname] = segments
    def __putinto_segments_dict(self,filepath,segments):
        with open(filepath,'r',encoding='gbk') as f:
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
#wellsegements = WellSegmentProvider()
#wellsegements.print_info()



            