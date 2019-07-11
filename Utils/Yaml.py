# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       Yaml.py
time:       2019/7/8 下午3:07

description: 


"""

import yaml
import socket


# my_config = {'name': 'lili', 'age': [18, 29]}
# f = open('a.yaml', 'w')
# yaml.dump(my_config, f)
# f.close()
#
# f = open('a.yaml', 'r+')
# data = f.read()
# all_data = yaml.safe_load(data)
# f.close()
# print(type(all_data))
# print('all_data: ', all_data)
# all_data['name'] = 'yamy'
#
# f = open('a.yaml', 'w')
# yaml.dump(all_data, f)
# f.close()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# print(get_host_ip())
ip_addr = get_host_ip()
lnode_id = ip_addr + "_tf_0"
print(lnode_id)

config_yaml = {
    "bootstrap_servers": ["localhost:9092"],
    "heartbeat_frequency": 60,
    "lnode_id": lnode_id,
    "lnode_name": "tf",
    "capability_info": {
        "train_capability": [
            {
                "capability_id": "ssd"
            },
            {
                "capability_id": "yolov3"
            }
        ],
        "detect_capability": []
    }
}

with open("local_config.yaml", "w") as f:
    yaml.dump(config_yaml, f)
