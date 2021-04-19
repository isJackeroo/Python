''' 
代码功能：根据文件的md5值清除重复的文件
'''
import os
import hashlib
import shutil
from tqdm import tqdm

class DuplicateFile(object):
    """
    这是一个对重复文件的处理类
    """

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.duplicate_tuple = self._get_duplicate(path)

    @property
    def show(self):
        """
        显示重复文件
        """
        duplicate, _ = zip(*self.duplicate_tuple)
        print("\n".join(duplicate))
        print(f"\n重复文件共{len(duplicate)}个")
        return None

    @staticmethod
    def md5(filename, block_size=65536):
        """
        :param filename: 文件名
        :param block_size:
        :return: md5值
        """
        hash_ = hashlib.md5()
        with open(filename, "rb") as f:
            for i in iter(lambda: f.read(block_size), b""):
                hash_.update(i)
        return hash_.hexdigest()

    def _get_duplicate(self, path):
        total_files = [(f, os.path.join(root, f)) for root, _, files in os.walk(path) for f in files]
        duplicate_tuple = []
        unique_md5 = []
        with tqdm(total_files, desc="正在扫描中") as bar:
            for i in bar:
                md5_values = self.md5(i[1])
                if md5_values in unique_md5:
                    duplicate_tuple.append(i)
                else:
                    unique_md5.append(md5_values)
                bar.set_description(f"正在扫描中，发现{len(duplicate_tuple)}个重复文件。")
        return duplicate_tuple

    def delete(self):
        """
        删除重复文件
        """
        if self.duplicate_tuple:
            confirm = input("删除后无法恢复，是否继续(y/n)?")
            if confirm in "Yy":
                for file, path in self.duplicate_tuple:
                    print(f"已删除{file}")
                    os.remove(path)
                print("删除完毕")
            else:
                print("已取消")
        else:
            print("没有重复文件")
            return None

    def move(self, new_path):
        """
        剪切重复文件
        """
        if self.duplicate_tuple:
            if not os.path.exists(new_path):
                print(f"{new_path} not exist,正在创建文件夹")
                os.makedirs(new_path)
            print("移动中")
            for file, path in self.duplicate_tuple:
                print(f"正在移动{file}")
                dst = os.path.join(new_path, file)
                shutil.move(path, dst)
            print("移动完毕")
        else:
            print("没有重复文件")
            return None

if __name__ == "__main__":
    src_path="xxx/xxx/xxx"  #输入你要清除重复文件的目录
    dup=DuplicateFile(src_path)
    dup.delete()
