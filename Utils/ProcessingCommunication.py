# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       ProcessingCommunication.py
time:       2019/7/8 下午3:42

description: 


"""

from multiprocessing import Process, Queue, Pool
# import queue
import multiprocessing
import time


def gen1(que):
    for i in range(0, 1000):
        print("Processing Name: ", multiprocessing.current_process().name)
        que.put((i % 3, i))
        print("gen1: ", que.qsize())


def gen2(que):
    for i in range(1000, 2000):
        print("Processing Name: ", multiprocessing.current_process().name)
        que.put((i % 3, i))
        print("gen2: ", que.qsize())


def consumer1(que):
    for i in range(0, 300):
        print("Processing Name: ", multiprocessing.current_process().name)
        print("consumer1: ", que.get())


def consumer2(que):
    for i in range(0, 500):
        print("Processing Name: ", multiprocessing.current_process().name)
        print("consumer2: ", que.get())


def div(a, b):
    res = a / b
    return res


def on_success(res):
    print("on_success:", res)


def on_error(res):
    print("on_error: ", res)


# p = Process(target=gen1, args=(q,))
# p2 = Process(target=gen2, args=(q,))
#
# p3 = Process(target=consumer1, args=(q,))
# p4 = Process(target=consumer2, args=(q,))

# p.start()
# p2.start()
# p3.start()
# p4.start()
# p.join()
# p2.join()
# p3.join()
# p4.join()

manager = multiprocessing.Manager()
que = manager.Queue()
#
# pool = Pool(processes=4)
# pool.apply_async(gen1, (que,))
# pool.apply_async(gen2, (que,))
# pool.apply_async(consumer1, (que,))
# pool.apply_async(consumer2, (que,))
#
# time.sleep(1)
# pool.close()
# pool.join()

pool = Pool(processes=4)
pool.apply_async(div, (3, 0), callback=on_success, error_callback=on_error)

pool.close()
pool.join()

print(que.qsize())

while not que.empty():
    print(que.get())
