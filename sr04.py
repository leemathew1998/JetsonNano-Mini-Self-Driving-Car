import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO
import time

echo_left = 40
trig_left = 38
echo_right = 31
trig_right = 32
GPIO.setmode(GPIO.BOARD)                         # 设置模式
GPIO.setup(trig_left, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_left, GPIO.IN)
GPIO.setup(trig_right, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_right, GPIO.IN)
GPIO.cleanup()
def sr04_left():
    GPIO.output(trig_left, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_left, GPIO.LOW)
    t1 = time.time()
    while GPIO.input(echo_left):
        pass
    t2 = time.time()
    return (t2-t1)*340*100/2

def sr04_right():
    GPIO.output(trig_right, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_right, GPIO.LOW)
    t1 = time.time()
    while GPIO.input(echo_right):
        pass
    t2 = time.time()
    return (t2-t1)*340*100/2

def left_detect():
    distan = 0
    for i in range(2):
        distan += sr04_left()
        time.sleep(0.1)
    return distan/2

def right_detect():
    distan = 0
    for i in range(2):
        distan += sr04_right()
        time.sleep(0.1)
    return distan/2

GPIO.cleanup()

