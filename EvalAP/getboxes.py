# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       getboxes.py
time:       2019/6/5 下午3:35

description: 


"""
import glob
import xml.etree.ElementTree as ET


def parse_xml(filename):
    """
    解析xml, 返回字典信息
    :param filename: xml文件路径
    :return: 需要的信息
    """
    tree = ET.parse(filename)
    cnt = 0

    for obj in tree.findall("object"):
        obj_name = obj.find("name").text
        if obj_name == "05020404":
            cnt += 1

    return cnt


file_list = glob.glob("./result/truth/*.xml")
total_boxes = 0
id = 1
for filename in file_list:
    print("------------------------------------------------")
    print("Processing {}: {}.".format(id, filename))
    boxes = parse_xml(filename)
    print("boxes: ", boxes)
    total_boxes += boxes
    id += 1
    print("------------------------------------------------")

print("Total boxes: ", total_boxes)
