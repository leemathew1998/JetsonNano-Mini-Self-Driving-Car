import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO
import time
backmotorinput_1 = 15
backmotorinput_2 = 16
frontmotorinput_1 = 21
frontmotorinput_2 = 22

GPIO.setmode(GPIO.BOARD)                         # 设置模式
GPIO.setup(backmotorinput_1,GPIO.OUT, initial=GPIO.LOW)             # 此端口为输出模式
GPIO.setup(backmotorinput_2,GPIO.OUT, initial=GPIO.LOW)             # 此端口为输出模式
GPIO.setup(frontmotorinput_1,GPIO.OUT, initial=GPIO.LOW)            # 此端口为输出模式
GPIO.setup(frontmotorinput_2,GPIO.OUT, initial=GPIO.LOW)            # 此端口为输出模式

def forward():
    #GPIO.setmode(GPIO.BOARD)                         # 设置模式
    #GPIO.setup(backmotorinput_1,GPIO.OUT)             # 此端口为输出模式
    #GPIO.setup(backmotorinput_2,GPIO.OUT)             # 此端口为输出模式
    GPIO.output(backmotorinput_1,GPIO.HIGH)
    GPIO.output(backmotorinput_2,GPIO.LOW)

def backward():
    #GPIO.setmode(GPIO.BOARD)                         # 设置模式
    #GPIO.setup(backmotorinput_1,GPIO.OUT)             # 此端口为输出模式
    #GPIO.setup(backmotorinput_2,GPIO.OUT)             # 此端口为输出模式
    GPIO.output(backmotorinput_1,GPIO.LOW)
    GPIO.output(backmotorinput_2,GPIO.HIGH)

def stop():
    #GPIO.setmode(GPIO.BOARD)                         # 设置模式
    #GPIO.setup(backmotorinput_1,GPIO.OUT)             # 此端口为输出模式
    #GPIO.setup(backmotorinput_2,GPIO.OUT)             # 此端口为输出模式
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

