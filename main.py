#把所有图片都reshape到99*99，在该分辨率下找频域亮线条

import cv2
import numpy as np
from math import *
import matplotlib.pyplot as plt
import time


nearby = 3   #统计附近3度范围

#near_scan = [[0]*99 for _ in range(99)] #长宽为99的二维list，其中每个元素是0
#near_scan = [[0]*99]*99   #不能用该方式创建二维list，第二个*99属于浅拷贝，更改一列的list，其他列也会被更改
near_scan = [[[] for _ in range(99)] for _ in range(99)] #长宽为99的二维list，其中每个元素又是一个空list,存储每个像素位置附近有哪些扫描线


for row in range(99):
    for col in range(49, 99):
        if col != 49:
            p = degrees(-atan((row-49)/(col-49)))
        else:
            if row > -49:
                p = 90
            if row < 49:
                p = 90
            if row == 49:
                p = 10000
        #print(p)
        for theta in np.arange(-90, 90, 0.5):
            if abs(p-theta)<=5 or abs(p-(theta+180))<=5 or abs(p-(theta-180))<=5:
                near_scan[row][col].append(theta)


fre_img_path = 'fimg.png'
fre_img = cv2.imread(fre_img_path, 0)

time_star = time.time()
line_angle = [[] for _ in range(360)]    #存储扫描线附近像素灰度值
for row in range(99):
    for col in range(49, 99):
        gray_vale = fre_img[row][col]
        for angle in near_scan[row][col]:
            line_angle[int((angle+90)*2)].append(gray_vale)  #int((angle+90)*2)为angle对应的第几条扫描线

#求均值
line_mean = []
for angle in line_angle:
    line_mean.append(np.mean(angle))
time_end = time.time()

print('扫描耗时：', time_end-time_star, 's')

a_array = np.array(line_mean)
# 获取最大值的索引
print('最大值角度为：', a_array.argmax()/2-90)



x_axis_data = np.arange(-90, 90, 0.5)
plt.plot(x_axis_data, line_mean, 'b*-', alpha=0.5, linewidth=1, label='acc')#'bo-'表示蓝色实线，数据点实心原点标注
## plot中参数的含义分别是横轴值，纵轴值，线的形状（'s'方块,'o'实心圆点，'*'五角星   ...，颜色，透明度,线的宽度和标签 ，
plt.legend()  #显示上面的label
plt.xlabel('theta')    #x_label
plt.ylabel('scan_mean') #y_label
#plt.xlim(0,30)#仅设置y轴坐标范围
plt.gcf().set_size_inches(40,8)
plt.show()






