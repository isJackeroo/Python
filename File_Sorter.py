'''
脚本功能：根据文件类型整理文件，根据FileType归类整理
使用方法：将该脚本放置需要整理的文件夹下，cd到该目录，执行 python3 File_Sorter.py 即可。

'''

import os
import glob
import shutil

'''
@Author: huny
@date: 2021.04.18
@function: 文件整理(按文件类型)
'''

class FileType():
    def __init__(self):
        self.filetype = {
            "图片": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg", ".heif", ".psd",".JPG"],
            "视频": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp",
                   ".mkv"],
            "音频": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3", ".msv", ".ogg", ".oga", ".raw",
                   ".vox", ".wav", ".wma"],
            "文档": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods", ".odt", ".pwi", ".xsn", ".xps", ".dotx",
                   ".docm", ".dox",
                   ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".pdf", ".md", ".xmind"],
            "压缩文件": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".xar", ".zip"],
            "文本": [".txt", ".in", ".out", ".json", "xml", ".log"],
            "程序脚本": [".py", ".html5", ".html", ".htm", ".xhtml", ".c", ".cpp", ".java", ".css", ".sql"],
            "可执行程序": [".exe", ".bat", ".lnk","dmg"],
            "字体文件": [".ttf", ".OTF", ".WOFF", ".EOT"]
        }

    def JudgeFile(self, pathname):
        for name, type in self.filetype.items():
            if pathname in type:
                return name
        return "无法判断类型文件"


class DeskTopOrg(object):
    def __init__(self):
        self.filetype = FileType()

    def Organization(self):
        filepath = input("请输入需要整理的文件夹路径： ")
        paths = glob.glob(filepath + "/*.*")
        print('paths-->', paths)
        for path in paths:
            try:
                if not os.path.isdir(path):
                    file = os.path.splitext(path)
                    filename, type = file
                    print('type-->', type)
                    print("filename-->", filename)
                    print('path-->', path)
                    dir_path = os.path.dirname(path)
                    print('dir_path-->', dir_path)
                    savePath = dir_path + '/{}'.format(self.filetype.JudgeFile(type))
                    print('savePath-->', savePath)
                    if not os.path.exists(savePath):
                        os.mkdir(savePath)
                        shutil.move(path, savePath)
                    else:
                        shutil.move(path, savePath)
            except FileNotFoundError:
                pass
        print("程序执行结束！")


if __name__ == '__main__':
    try:
        while True:
            desktopOrg = DeskTopOrg()
            desktopOrg.Organization()
            print("---->你的文件已经整理完成。")
            a = input('---->请按回车键退出:')
            if a == '':
                break
    except BaseException:
        print("ERROE:路径错误或有重复的文档")
