###############################################################
# Modified from https://www.cnblogs.com/rxbook/p/7509530.html #
# 脚本功能：根据视频或照片中的exif信息，按照日期重命名文件名           #
###############################################################
import os
import time
import exifread


MY_DATE_FORMAT = '%Y%m%d_%H%M%S'

# SUFFIX_FILTER = ['.jpg', '.png', '.mpg', '.mp4', '.thm', '.bmp', '.jpeg', '.avi', '.mov']
DELETE_FILTER = ['thumbs.db', 'sample.dat']

VIDEO_LIST = ['.mp4', '.avi', '.mov']
IMAGE_LIST = ['.jpg', '.png', '.mpg', '.thm', '.bmp', '.jpeg']
# SUFFIX_FILTER = VIDEO_LIST + IMAGE_LIST
SUFFIX_FILTER = ['.mp4']


def isFormatedFileName(filename):
     #判断是否已经是格式化过的文件名
     try :
         filename_nopath = os.path.basename(filename)
         f, e = os.path.splitext(filename_nopath)
         time.strptime(f, MY_DATE_FORMAT)
         return True
     except ValueError :
         return False

def isTargetedFileType(filename):
     #根据文件扩展名，判断是否是需要处理的文件类型
     filename_nopath = os.path.basename(filename)
     f, e = os.path.splitext(filename_nopath)
     if e.lower() in SUFFIX_FILTER :
         return True
     else :
         return False

def isDeleteFile(filename):
     #判断是否是指定要删除的文件
     filename_nopath = os.path.basename(filename)
     if filename_nopath.lower() in DELETE_FILTER :
         return True
     else :
         return False

def generateNewFileName(filename):
     #根据照片的拍照时间生成新的文件名（如果获取不到拍照时间，则使用文件的创建时间）
     try :
         if os.path.isfile(filename):
             fd = open(filename, 'rb')
         else :
             raise "[%s] is not a file!\n" % filename
     except :
         raise "unopen file [%s]\n" % filename

     data = exifread.process_file(fd)
     if data :
         #取得照片的拍摄日期
         try :
             t = data['EXIF DateTimeOriginal']
             #转换成 yyyymmdd_hhmmss的格式
             dateStr = str(t).replace(":", "")[: 10] + "_" + str(t)[11:].replace(":", "")
         except :
             pass

     #如果没有取得exif信息，则用图像文件的创建日期作为拍摄日期
     state = os.stat(filename)
     dateStr = time.strftime(MY_DATE_FORMAT, time.localtime(state[-2]))
     dirname = os.path.dirname(filename)
     filename_nopath = os.path.basename(filename)
     f, e = os.path.splitext(filename_nopath)
     if e.lower() in VIDEO_LIST:
         dateStr = 'VID_' + dateStr
     elif e.lower() in IMAGE_LIST:
         dateStr = 'IMG_' + dateStr
     newFileName = os.path.join(dirname, dateStr + e)
     return newFileName

def scandir(startdir):
     #遍历指定目录以及子目录，对满足条件的文件进行改名或删除处理
     os.chdir(startdir)
     for obj in os.listdir(os.curdir):
         if os.path.isfile(obj):
             if isTargetedFileType(obj) and isFormatedFileName(obj) == False :
                 #对满足过滤条件的文件进行改名处理
                 newFileName = generateNewFileName(obj)
                 print("rename[%s] => [%s]" % (obj, newFileName))
                 os.rename(obj, newFileName)
             elif isDeleteFile(obj):
                 #删除制定的文件
                 print("delete[%s]: " % obj)
                 os.remove(obj)
             else :
                 pass
         if os.path.isdir(obj):
             scandir(obj)
             os.chdir(os.pardir)


if __name__ == "__main__" :
     path = r"/Users/jackeroo/Desktop/Photos"
     scandir(path)
