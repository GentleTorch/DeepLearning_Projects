# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       mAP.py
time:       2019/6/5 上午9:15

description:
    we evaluate the performance of object detection algorithm through
    calculating mAP


"""

import os
import glob

import xml.etree.ElementTree as ET
import numpy as np


def parse_xml(filename):
    """
    解析xml, 返回字典信息
    :param filename: xml文件路径
    :return: 需要的信息
    """
    tree = ET.parse(filename)
    objects = []

    for obj in tree.findall("object"):
        obj_struct = {}
        obj_struct["name"] = obj.find("name").text
        # obj_struct["pose"]=obj.find("pose").text
        # obj_struct["truncated"]=int(obj.find("truncated").text)
        # obj_struct["difficult"]=int(obj.find("difficult").text)
        bbox = obj.find("bndbox")
        # print(type(bbox))
        obj_struct["bbox"] = [int(bbox.find("xmin").text),
                              int(bbox.find("ymin").text),
                              int(bbox.find("xmax").text),
                              int(bbox.find("ymax").text)]
        objects.append(obj_struct)

    return objects


def cal_ap(rec, prec):
    mrec = np.concatenate(([0.], rec, [1.]))
    mpre = np.concatenate(([0.], prec, [0.]))

    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    i = np.where(mrec[1:] != mrec[:-1])[0]

    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def eval_od(truthpath, detpath, classname, iou_thresh=0.5):
    """
    评估目标检测, 返回recall, precision
    :param truthpath: 真实的标定框文件夹路径
    :param detpath:   预测的标定框文件夹路径
    :param classname: 物体类别
    :param iou_thresh:iou面积阈值
    :return: recall, precision
    """
    # get the ground truth boxes
    gt_xml_list = glob.glob(truthpath + "*.xml")
    gt_recs = {}
    for filename in gt_xml_list:
        key = filename.split('/')[-1]
        gt_recs[key] = parse_xml(filename)

    class_recs = {}
    npos = 0
    for filename in gt_xml_list:
        key = filename.split('/')[-1]
        R = [obj for obj in gt_recs[key] if obj["name"] == classname]
        bbox = list(x["bbox"] for x in R)
        # difficult=np.array(x["difficult"] for x in R).astype(np.bool)
        # det=[False]*len(R)
        npos = npos + len(bbox)
        class_recs[key] = {"bbox": bbox}
        # "difficult":difficult,
        # "det":det}

    print("Ground Truth: ", class_recs)

    # get the detected results, boxes
    det_xml_list = glob.glob(detpath + "*.xml")
    det_recs = {}
    for filename in det_xml_list:
        key = filename.split('/')[-1]
        det_recs[key] = parse_xml(filename)

    print(det_recs)

    pred_recs = {}
    for filename in det_xml_list:
        key = filename.split('/')[-1]
        R = [obj for obj in det_recs[key] if obj["name"] == classname]
        bbox = list(x["bbox"] for x in R)

        pred_recs[key] = {"bbox": bbox}

    print("Predicted Result: ", pred_recs)

    # calculate the ap, recall
    tp = 0
    fp = 0
    for filename in det_xml_list:
        key = filename.split('/')[-1]
        for det_box in pred_recs[key]["bbox"]:
            if len(det_box) == 0:
                continue
            ovmax = -np.inf
            BBGT = np.array(class_recs[key]["bbox"]).astype(float)
            dt_box = np.array(det_box).astype(float)

            if BBGT.size > 0:
                # print(BBGT)
                ixmin = np.maximum(BBGT[:, 0], dt_box[0])
                iymin = np.maximum(BBGT[:, 1], dt_box[1])
                ixmax = np.minimum(BBGT[:, 2], dt_box[2])
                iymax = np.minimum(BBGT[:, 3], dt_box[3])
                iw = np.maximum(ixmax - ixmin + 1.0, 0.)
                ih = np.maximum(iymax - iymin + 1.0, 0.)
                inters = iw * ih

                uni = (dt_box[2] - dt_box[0] + 1.) * (dt_box[3] - dt_box[1] + 1.0) \
                      + (BBGT[:, 2] - BBGT[:, 0] + 1.0) * (BBGT[:, 3] - BBGT[:, 1] + 1.0) \
                      - inters

                overlaps = inters / uni
                # print(overlaps)
                ovmax = np.max(overlaps)

            if ovmax > iou_thresh:
                tp = tp + 1
            else:
                fp = fp + 1
    print("TP: {}, FP: {}.".format(tp, fp))
    print("Total Ground truth boxes: ", npos)
    rec = 0
    prec = 0
    if npos != 0:
        rec = float(tp) / float(npos)
    if (tp + fp) != 0:
        prec = float(tp) / float(tp + fp)

    return rec, prec


recall, precision = eval_od("./result/truth/", "./result/det/", "05020404")

print(" Recall: {}.\n Precision: {}.".format(recall, precision))
