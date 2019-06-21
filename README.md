# Making a autonomous driving car with Jetson Nano

# 自动驾驶小车
![](./assets/IMG_20190621_232208.jpg)
![](./assets/IMG_20190621_232141.jpg)

# 超声波传感器 HC-SR04
![](./assets/IMG_20190621_230414.jpg)

# L298N模块-驱动直流电机
![](./assets/IMG_20190621_230207.jpg)

# 罗技-170摄像头
![](./assets/IMG_20190621_230530.jpg)

# 原理
**在detect.py中，使用了yolov3-tiny的目标检测模型，在Nano上测试可达10帧每秒，把图像三等分，只对中间的目标进行判断。另外左右各有一个超声波传感器检测左右边的距离，**
