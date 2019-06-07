# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       voc_ap.py
time:       2019/6/5 下午4:38

description: 


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
        bbox = obj.find("bndbox")
        obj_struct["bbox"] = [int(bbox.find("xmin").text),
                              int(bbox.find("ymin").text),
                              int(bbox.find("xmax").text),
                              int(bbox.find("ymax").text)]
        objects.append(obj_struct)

    return objects


def cal_ap(rec, prec):
    """
    计算 ap值
    :param rec:
    :param prec:
    :return:
    """
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
        npos = npos + len(bbox)
        class_recs[key] = {"bbox": bbox}

    print("Ground Truth: ", class_recs)

    # get the detected results, boxes
    det_xml_list = glob.glob(detpath + "*.xml")
    det_recs = {}
    for filename in det_xml_list:
        key = filename.split('/')[-1]
        det_recs[key] = parse_xml(filename)

    print(det_recs)

    pred_recs = {}
    len_pred_boxes = 0
    for filename in det_xml_list:
        key = filename.split('/')[-1]
        R = [obj for obj in det_recs[key] if obj["name"] == classname]
        bbox = list(x["bbox"] for x in R)
        len_pred_boxes += len(bbox)
        pred_recs[key] = {"bbox": bbox}

    print("Predicted Result: ", pred_recs)

    # calculate the ap, recall
    tp = np.zeros(len_pred_boxes)
    fp = np.zeros(len_pred_boxes)
    i = 0
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
                tp[i] = 1
            else:
                fp[i] = 1
            i += 1

    print("Total Predicted boxes: ", len_pred_boxes)
    print("tp: ", tp)
    print("fp: ", fp)
    fp = np.cumsum(fp)
    tp = np.cumsum(tp)
    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = cal_ap(rec, prec)

    print("cumsum tp: ", tp)
    print("cumsum fp", fp)
    return rec, prec, ap


recall, precision, ap = eval_od("./result/truth/", "./result/det/", "05020404")

print("AP: {}.".format(ap))
