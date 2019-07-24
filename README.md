# Making a self-driving car with Jetson Nano
# The appearance of the final car
![](https://github.com/leemathew1998/JetsonNano-Mini-Self-Driving-Car/blob/master/assets/20190627214116.png)
![](https://github.com/leemathew1998/JetsonNano-Mini-Self-Driving-Car/blob/master/assets/20190627214137.png)
# 超声波传感器HC-SR04 (Ultrasonic Sensor)
![](https://github.com/leemathew1998/JetsonNano-Mini-Self-Driving-Car/blob/master/assets/20190627214029.png)
# L298N模块-驱动直流电机 (Driving DC Motor)
![](https://github.com/leemathew1998/JetsonNano-Mini-Self-Driving-Car/blob/master/assets/20190627213957.png)
# 罗技-170摄像头 (Camera)
![](https://github.com/leemathew1998/JetsonNano-Mini-Self-Driving-Car/blob/master/assets/20190627214053.png)
# 原理 (How to work?)
**在detect.py中，使用了yolov3-tiny的目标检测模型，在Nano上测试可达10帧每秒，把图像三等分，只对中间的目标进行判断。另外左右各有一个超声波传感器检测左右边的距离，然后就是各种判断语句控制电机转向，因为Nano上没有PWM, 也可以再添加一个硬件用来调速。**
**In detect.py, use yolov3-tiny object detection model, test up to 10 frames per second on the Nano. First, divide the image into three equal parts and judge only the middle target. In addition, there is an ultrasonic sensor on each side to detect the distance between the left and right sides.**
