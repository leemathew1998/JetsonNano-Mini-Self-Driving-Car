import sys
import time
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
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
#forward()
#time.sleep(1)
GPIO.cleanup()
