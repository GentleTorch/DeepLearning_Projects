# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       TestKafkaConsumer.py
time:       2019/7/4 上午10:45

description: 


"""

from kafka import KafkaConsumer
import json


consumer = KafkaConsumer('test1', bootstrap_servers=['localhost:9092'],auto_offset_reset='latest')

for msg in consumer:
    print(msg.topic, msg.partition, msg.offset, msg.key)
    print(msg.value)
    a=json.loads(msg.value)
    print(a)

