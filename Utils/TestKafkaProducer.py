# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       TestKafka.py
time:       2019/7/4 上午10:34

description: 


"""

from kafka import KafkaProducer
import json
import uuid
import datetime
import yaml

with open("local_config.yaml", "r") as f:
    data = f.read()
    local_config = yaml.safe_load(data)

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

# msg_dict = {
#     "sleep_time": 10,
#     "db_config": {
#         "database": str(10),
#         "host": "xxxx",
#         "user": "root",
#         "password": "root"
#     },
#     "table": "msg",
#     "msg": "Hello World"
# }

producer = KafkaProducer(bootstrap_servers=local_config["bootstrap_servers"])
msg = json.dumps(heartbeat_msg)
producer.send('test1', msg.encode())
producer.close()
