# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       heartbeat.py
time:       2019/7/10 上午10:38

description: 


"""

from kafka import KafkaProducer
from kafka.errors import KafkaError

from multiprocessing import Process, Pool, Manager

import json
import uuid
import datetime
import yaml
import lockfile
import time
import traceback

import logging


def send_heartbeat():

    while True:
        try:
            lock = lockfile.FileLock('./configs/local_config.yaml')
            lock.acquire()
            with open("./configs/local_config.yaml", "r") as f:
                data = f.read()
                local_config = yaml.safe_load(data)
            lock.release()

            print("local_config: ", local_config)

            heartbeat_msg = {
                "msg_id": str(uuid.uuid1()),
                "msg_type": "heartbeat",
                "timestamp": str(datetime.datetime.now()),
                "node_info": {
                    "lnode_id": local_config["lnode_id"],
                    "lnode_name": local_config["lnode_name"]
                },
                "capability_info": local_config["capability_info"]
            }

            producer = KafkaProducer(bootstrap_servers=local_config["bootstrap_servers"])
            msg = json.dumps(heartbeat_msg)
            producer.send('test1', msg.encode())
            producer.close()


            time.sleep(local_config["heartbeat_frequency"])
        except KafkaError as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.apply_async(send_heartbeat, args=())

    pool.close()
    pool.join()
