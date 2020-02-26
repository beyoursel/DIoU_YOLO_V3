
# _*_ coding:utf-8 _*_
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
 
# sets=[('myData', 'train'),('myData', 'val'), ('myData', 'test')]  # 根据自己数据去定义
sets=[('myData', 'train'),('myData', 'val')]  # 根据自己数据去定义


class2id = {'face':0,"unmask":0,"nomask":0,"wrongmask":0,"mask":1,"face_mask":1,"rightmask":1}
# classes = ["plane", "boat", "person"] # 根据自己的类别去定义
 
 
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
 
def convert_annotation(year, image_id):
    in_file = open('./Annotations/%s.xml'%(image_id))
    out_file = open('./labels/%s.txt'%(image_id), 'w')
    # print(in_file)
    tree=ET.parse(in_file)
    root = tree.getroot()
    # 有些标注没有size
    # size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    temp_img = cv2.imread('./JPEGImages/%s.jpg'%(image_id))
    print(image_id)
    img_sp = temp_img.shape
    h = img_sp[0]#height(rows) of image
    w = img_sp[1]#width(colums) of imag
 
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls_ = obj.find('name').text
        if cls_ not in list(class2id.keys()):
            print("没有该label: {}".format(cls_))
            continue
        cls_id = class2id[cls_]
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        # print(bb)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
 
wd = getcwd()
 
for year, image_set in sets:
    if not os.path.exists('./labels/'):
        os.makedirs('./labels/')
    image_ids = open('./ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('./%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/JPEGImages/%s.jpg\n'%(wd, image_id))  # 写了train或val的list
        convert_annotation(year, image_id)
    list_file.close()


# labels/标注数据有了
# train val的list数据也有了
