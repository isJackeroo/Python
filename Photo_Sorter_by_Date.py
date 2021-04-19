'''
脚本功能：根据照片的exif信息，根据照片拍摄日期信息，按日期创建文件夹，并将对应的照片移动到对应的文件夹中
'''

import os
import sys
from shutil import Error
from shutil import copystat
from shutil import copy2
import exifread
import shutil
#图片所处的绝对路径，其中r表示去掉python的内部转义
PhotoPath = r'/Users/jackeroo/Desktop/Photos'
NewPath = r'/Users/jackeroo/Desktop/.'
#根据传参判断复制的目标地址是否存在如果不存在进行创建，并且执行复制操作
def copy_file(src_file,dst_dir):
   if not os.path.isdir(dst_dir):
      os.makedirs(dst_dir)
   copy2(src_file,dst_dir)

#根据传参判断复制的目标地址是否存在如果不存在进行创建，并且执行移动操作
def move_file(src_file,dst_dir):
   if not os.path.isdir(dst_dir):
      os.makedirs(dst_dir)
   shutil.move(src_file,dst_dir)

#遍历整个图片路径底下的所有文件并获取其拍摄时间，根据拍摄时间进行操作
def walk_file(file_path):
   for root,dirs,files in os.walk(file_path,topdown=False):
      for name in files:
         photo = os.path.join(root,name)
         try:
            with open(photo, 'rb') as img:
               dateStr = str(exifread.process_file(img)['Image DateTime'])
            year = dateStr[0:4]
            month = dateStr[5:7]  #截取月份
            day = dateStr[8:10]   #截取日期，如果只需要精确到月份，可以删除该行及下面代码中的"+day+'日'"
            new_path = NewPath+year+'年/'+year+'年'+month+'月/'+day+'日'
            move_file(photo,new_path)
            print("moved '{}' to '{}'".format(photo,new_path))
         except:
            print("Movement failed. {}".format(photo))
      for name in dirs:
         walk_file(name)
walk_file(PhotoPath)
