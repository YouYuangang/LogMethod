import os.path
#项目根目录
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(path,'output')
logfilepath = os.path.join(output_path,"logmethod_log.txt")
logstream = open(logfilepath, "w")