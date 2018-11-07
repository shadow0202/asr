# -*- coding: utf-8 -*-
"""
# @Author  : huxw 
# @Update  : 2018/11/2 14:13 
# @Software: PyCharm

计算文件数量工具

"""

import os
from sys import argv

totalSize = 0
fileNum = 0
dirNum = 0
fn_list = []
count = 0


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return dirs,files

def visitDir(path):
    global totalSize
    global fileNum
    global dirNum
    global fn_list
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        # print(sub_path)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1  # 统计文件数量
            totalSize = totalSize + os.path.getsize(sub_path)  # 文件总大小
            a = sub_path.split('\\')
            len = a.__len__()
            file_name = a[len - 1 ]
            # print file_name
            fn_list.append(file_name)

        elif os.path.isdir(sub_path):
            dirNum = dirNum + 1  # 统计文件夹数量
            visitDir(sub_path)  # 递归遍历子文件夹


def sizeConvert(size):  # 单位换算
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        return str(size / G) + 'G Bytes'
    elif size >= M:
        return str(size / M) + 'M Bytes'
    elif size >= K:
        return str(size / K) + 'K Bytes'
    else:
        return str(size) + 'Bytes'


def main(path):
    if not os.path.isdir(path):
        print('Error:"', path, '" is not a directory or does not exist.')
        return
    visitDir(path)


def output(path):
    # print('The total size of ' + path + ' is:' + sizeConvert(totalSize))
    # print('The total number of files in ' + path + ' is:', fileNum)
    # print('The total number of directories in ' + path + ' is:', dirNum)
    global fn_list
    global count
    print('The total number of distinct in ' + path + ' is:', set(fn_list).__len__())
    if fn_list.__len__() != 0:
        fn_list = []
        return 1
    else:
        fn_list = []
        return 0


if __name__ == '__main__':
    path = argv[1]
    dirs1,files = file_name(path)
    print dirs1
    count = 0
    real = 0
    for d1 in dirs1:
        dirs2, files = file_name(path + '\\' + d1)
        for d2 in dirs2:
            count += 1
            main(path + '\\' + d1 + '\\' +d2)
            null_or_not = output(path + '\\' + d1 + '\\' +d2)
            real += null_or_not

    print(real, count, 'percent: {:.2%}'.format(real / count))
