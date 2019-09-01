# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       get_process_result.py
time:       2019/8/14 下午1:37

description: 


"""

from multiprocessing import Process, Pool
import os


def sub(a, b):
    print('sub: ', a, b)
    return a - b


def add(a, b):
    print('pid: ', os.getpid())
    # prc = Process(target=sub, args=(3, 2))
    # prc.start()
    # prc.join()

    return a + b, 3, 4, 5


print('main pid: ', os.getpid())
pool = Pool(processes=1)
result = pool.apply_async(func=add, args=(1, 2)).get()
pool.close()
pool.join()
print(result)
print('ending of main')
