# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       jsonlistvalue.py
time:       2019/7/1 上午10:34

description: 


"""

import logging.config
import logging
import os
import json

with open('./config.json', 'r') as f:
    config_dict=json.load(f)

logging.config.dictConfig(config_dict)

logger = logging.getLogger(__name__)

if not os.path.exists('./logs/') and not os.path.exists('./logs/mysite.log'):
    os.mkdir('./logs/')
    os.mknod('./logs/mysite.log')

if __name__ == '__main__':
    for i in range(0, 1000):
        logger.info("log what: " + str(i))
