# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       test.py
time:       2019/6/2 上午2:38

description: 


"""

import tensorflow as tf

a = tf.constant([2])

b = tf.constant([3])

config = tf.ConfigProto(inter_op_parallelism_threads=8)

with tf.Session(config=config) as sess:
    print(sess.run(a + b))
