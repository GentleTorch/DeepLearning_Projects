# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       test.py
time:       2019/8/6 下午6:44

description: 


"""

from multiprocessing import Process, Pool, Manager, Pipe
import os
import time
import sys


def sub_send_msg(sender):
    print('-' * 30)
    print('current pid: ', os.getpid(), ' parent pid: ', os.getppid())
    pid = os.getpid()
    try:
        print('send msg')
        sender.send([1, 'hello', pid])
        time.sleep(2)
        ack_info = sender.recv()
        print('after send, ack_info: ', ack_info)
    finally:
        sender.close()


def sub_recv_msg(receiver):
    try:
        print('#' * 30)
        print('current pid: ', os.getpid(), ' parent pid: ', os.getppid())

        msg = receiver.recv()
        print('recv msg: ', msg)
        if msg[0] == 10:
            cmd = 'kill -9 ' + str(msg[-1])
            os.system(cmd)
        receiver.send('I have receive msg')
    except:
        print('Error occurred: ', sys.exc_info())
    finally:
        receiver.close()
        print('over')


def worker(a, b):
    print('current pid: ', os.getpid(), ' parent pid: ', os.getppid())
    try:
        print('worker: ', a + b)
        pool = Pool(processes=4)
        for i in range(1):
            sender, receiver = Pipe()
            pool.apply_async(func=sub_send_msg, args=(sender,))
            pool.apply_async(func=sub_recv_msg, args=(receiver,))

        pool.close()
        pool.join()

    finally:
        print('end of worker...')


print(os.getpid())
p = Process(target=worker, args=(1, 2))
p.start()
p.join()
