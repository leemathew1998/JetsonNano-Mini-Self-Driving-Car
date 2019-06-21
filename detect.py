from __future__ import division

from models import *
from utils.utils import *
from utils.datasets import *

import os
import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
import cv2
import time
import datetime
import argparse

import torch
from torch.autograd import Variable

parser = argparse.ArgumentParser()
parser.add_argument('--config_path', type=str, default='config/yolov3-tiny.cfg', help='path to model config file')
parser.add_argument('--weights_path', type=str, default='weights/yolov3-tiny.weights', help='path to weights file')
parser.add_argument('--class_path', type=str, default='data/coco.names', help='path to class label file')
parser.add_argument('--conf_thres', type=float, default=0.7, help='object confidence threshold')
parser.add_argument('--nms_thres', type=float, default=0.3, help='iou thresshold for non-maximum suppression')
parser.add_argument('--batch_size', type=int, default=1, help='size of the batches')
parser.add_argument('--n_cpu', type=int, default=2, help='number of cpu threads to use during batch generation')
parser.add_argument('--img_size', type=int, default=416, help='size of each image dimension')
parser.add_argument('--use_cuda', type=bool, default=True, help='whether to use cuda if available')
opt = parser.parse_args()
print(opt)

cuda = torch.cuda.is_available() and opt.use_cuda

# Set up model
model = Darknet(opt.config_path, img_size=opt.img_size)
model.load_weights(opt.weights_path)

if cuda:
    model.cuda()

model.eval() # Set in evaluation mode
classes = load_classes(opt.class_path) # Extracts class labels from file
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

###  GPIO   ###
backmotorinput_1 = 15
backmotorinput_2 = 16
frontmotorinput_1 = 21
frontmotorinput_2 = 22

GPIO.setup(backmotorinput_1,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(backmotorinput_2,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(frontmotorinput_1,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(frontmotorinput_2,GPIO.OUT, initial=GPIO.LOW)
def forward():
    GPIO.output(backmotorinput_1,GPIO.HIGH)
    GPIO.output(backmotorinput_2,GPIO.LOW)

def backward():
    GPIO.output(backmotorinput_1,GPIO.LOW)
    GPIO.output(backmotorinput_2,GPIO.HIGH)

def stop():
    GPIO.output(backmotorinput_1,GPIO.LOW)
    GPIO.output(backmotorinput_2,GPIO.LOW)

def left():
    GPIO.output(frontmotorinput_1,GPIO.LOW)
    GPIO.output(frontmotorinput_2,GPIO.HIGH)

def right():
    GPIO.output(frontmotorinput_1,GPIO.HIGH)
    GPIO.output(frontmotorinput_2,GPIO.LOW)

def center():
    GPIO.output(frontmotorinput_1,GPIO.LOW)
    GPIO.output(frontmotorinput_2,GPIO.LOW)

stop()
center()
###   SH04   ###
echo_left = 37
trig_left = 38
echo_right = 11
trig_right = 12
echo_front = 35
trig_front = 36
GPIO.setup(trig_left, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_left, GPIO.IN)
GPIO.setup(trig_right, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_right, GPIO.IN)
GPIO.setup(trig_front, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_front, GPIO.IN)

def sr04_left():
    start = time.time()
    GPIO.output(trig_left, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_left, GPIO.LOW)
    t1 = time.time()
    while not GPIO.input(echo_left):
        pass
    while GPIO.input(echo_left):
        pass
    t2 = time.time()
    return (t2-t1)*34300/2

def sr04_right():
    start = time.time()
    GPIO.output(trig_right, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_right, GPIO.LOW)
    t1 = time.time()
    while not GPIO.input(echo_right):
        pass
    while GPIO.input(echo_right):
        pass
    t2 = time.time()
    return (t2-t1)*34300/2

def sr04_front():
    start = time.time()
    GPIO.output(trig_front, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_front, GPIO.LOW)
    t1 = time.time()
    while not GPIO.input(echo_front):
        pass
    while GPIO.input(echo_front):
        pass
    t2 = time.time()
    return (t2-t1)*34300/2

print(sr04_right())
assert 1==2
### -----   ###
print ('\nPerforming object detection:')
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Cannot capture source"

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

mid_frame_start = width/3
mid_frame_end = width*2/3
frames = 0
skip = 1
inner_skip = 1
while cap.isOpened():
    frames += 1
    ret, frame = cap.read()
    if frames % skip == 0:
        input_test = Frame_Pre(frame)
        input_imgs = Variable(input_test.type(Tensor))        
        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, 80, opt.conf_thres, opt.nms_thres)
        pad_x = max(frame.shape[0] - frame.shape[1], 0) * (opt.img_size / max(frame.shape))
        pad_y = max(frame.shape[1] - frame.shape[0], 0) * (opt.img_size / max(frame.shape))
        unpad_h = opt.img_size - pad_y
        unpad_w = opt.img_size - pad_x
        if detections[0] is not None:
            unique_labels = detections[0][:, -1].cpu().unique()
            n_cls_preds = len(unique_labels)
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections[0]:
                box_h = ((y2 - y1) / unpad_h) * frame.shape[0]
                box_w = ((x2 - x1) / unpad_w) * frame.shape[1]
                y1 = ((y1 - pad_y // 2) / unpad_h) * frame.shape[0]
                x1 = ((x1 - pad_x // 2) / unpad_w) * frame.shape[1]
                center_point_x = x1 + box_w/2
                center_point_y = y1 + box_h/2
                class_ = classes[int(cls_pred)]
                if center_point_x > mid_frame_start and center_point_x < mid_frame_end:
                    if class_ == 'car' or class_ == 'truck' or class_ == 'bus':
                        print('have a car !!!')
                        left_distan = sr04_left()
                        right_distan = sr04_right()
                        front_distan = sr04_front()
                        if front_distan < 50:
                            stop()
                            print('    something in the front!!!')
                        else:
                            forward()
                        if left_distan <= 40 and right_distan <=40:
                            center()
                            print('    front have a car but left and right have not enough distans!!!')
                        elif left_distan > 40 and right_distan <= 40:
                            left()
                            time.sleep(0.40)
                            center()
                            right()
                            time.sleep(0.2)
                            center()
                            print('    forward and turn left!!!')
                        elif left_distan <= 40 and right_distan > 40:
                            right()
                            time.sleep(0.40)
                            center()
                            left()
                            time.sleep(0.2)
                            center()
                            print('    forward and turn right!!!')
                        else:
                            left()
                            time.sleep(0.40)
                            center()
                            right()
                            time.sleep(0.2)
                            center()
                            print('    both path can go auto choice left!!!')
                    elif class_ == 'person' or class_ == 'bicycle':
                        print('have a person!!!!')
                        left_distan = sr04_left()
                        right_distan = sr04_right()
                        #front_distan = sr04_front()
                        #if front_distan < 50:
                        #    stop()
                        #    print('    something in the front!!!')
                        #else:
                        #    forward()
                        if left_distan <= 40 and right_distan <=40:
                            #center()
                            print('    front have a person but left and right have not enough distans!!!')
                        elif left_distan > 40 and right_distan <= 40:
                            #left()
                            #time.sleep(0.40)
                            #center()
                            #right()
                            #time.sleep(0.2)
                            #center()
                            print('    forward and turn left!!!')
                        elif left_distan <= 40 and right_distan > 40:
                            #right()
                            #time.sleep(0.40)
                            #center()
                            #left()
                            #time.sleep(0.2)
                            #center()
                            print('    forward and turn right!!!')
                        else:
                            #left()
                            #time.sleep(0.40)
                            #center()
                            #right()
                            #time.sleep(0.2)
                            #center()
                            print('    both path can go auto choice left!!!')
                else:
                    print('have object but not in the mid!!!')
                    if frames % inner_skip == 0:
                        right_distan = sr04_right()
                        left_distan = sr04_left()
                        front_distan = 100 #sr04_front()
                        #if front_distan < 50:
                        #    stop()
                        #    print('    front have not enough distan!!!')
                        #else:
                        #    forward())
                        if right_distan >= 100:
                            print('    go right a bit!!!')
                            #right()
                            #time.sleep(0.40)
                            #center()
                            #left()
                            #time.sleep(0.2)
                            #center()
                        else:
                            if left_distan >= 100:
                                print('    go left a bit !!!')
                                #left()
                                #time.sleep(0.40)
                                #center()
                                #right()
                                #time.sleep(0.2)
                                #center()
                            else:
                                #center()
                                print('    forward but both way have no distan to turn')
        else:
            print('no object in this frame')
            if frames % inner_skip == 0:
                right_distan = 100 #sr04_right()
                left_distan = 100 #sr04_left()
                front_distan = 100   #sr04_front()
                #if front_distan < 50:
                #    stop()
                #    print('    front have not enough distan!!!')
                #else:
                #    forward()
                if right_distan >= 100:
                    print('    go right a bit!!!')
                    #right()
                    #time.sleep(0.2)
                    #center()
                    #left()
                    #time.sleep(0.1)
                    #center()
                else:
                    if left_distan >= 100:
                        print('    go left a bit !!!')
                        #left()
                        #time.sleep(0.2)
                        #center()
                        #right()
                        #time.sleep(0.1)
                        #center()
                    else:
                        #center()
                        print('    forward but both way have no distan to turn')
    else:
        continue
