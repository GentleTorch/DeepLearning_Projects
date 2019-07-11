# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       TestLogConcurrent.py
time:       2019/7/10 下午1:45

description: 


"""
from multiprocessing import Process, Queue, Pool
import multiprocessing
import json
import yaml
import pprint
import logging
import logging.config
import sys


# f = open('./configs/config.json', 'r')
# config = json.load(f)
# f.close()
#
# with open('./configs/log_config.yaml', 'w') as f:
#     yaml.dump(config, f)

def get_log_config():
    """
    get the log configuration
    :return: dict for log
    """
    with open('./configs/log_config.yaml', 'r') as f:
        data = f.read()
        tmp = yaml.safe_load(data)
        print(tmp)
    return tmp


def get_logger():
    """
    get object logger
    :return:
    """
    config = get_log_config()
    logging.config.dictConfig(config)
    logger = logging.getLogger()
    return logger


# this could work
def gen_log_1():
    logger = get_logger()
    name = multiprocessing.current_process().name
    for i in range(0, 1000):
        loginfo = str(sys._getframe().f_code.co_filename) + \
                  ' Line: ' + str(sys._getframe().f_lineno) + " Function: " + str(sys._getframe().f_code.co_name)
        print(loginfo)
        logger.info(name + ' ' + loginfo + ': log what ' + str(i))


if __name__ == '__main__':
    pool = Pool(4)
    for k in range(0, 4):
        pool.apply_async(gen_log_1, args=())
    pool.close()
    pool.join()
