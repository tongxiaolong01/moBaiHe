# coding=utf-8
import uiautomator2 as u2
import cv2
import os
import time
import uiplus


# 剧集最新的集数
JUJI = 29
# 设置FLAG的值0、1、2；默认为0，如果有更新，更新1次设置为1；更新2次设置为2；1到2的时间为更新周期。
FLAG = 0
# 记录更新间隔时间
INTERVAL_TIME = 0
# 记录第一次更新时间
FirstUpdateTime = 0
# 记录第二次更新时间
SecondUpdateTime = 0


def getDevicesList():
    command='adb devices'
    output = os.popen(command)
    for line in output.readlines():
        if '5555' in line:
            print(line)
        else:
            output=os.popen('adb connect 192.168.1.130')

def timeStyle(timestamp):
    time_Now = int(timestamp)
    time_local = time.localtime(time_Now)
    dt = time.strftime("%Y-%m-%d %H-%M-%S", time_local)
    return dt


# 保存图像
def imageSave(myfileName, nTime):
    my_file = 'updateResult\i' + myfileName + timeStyle(nTime) + '.jpg'
    print(timeStyle(nTime))
    if os.path.exists(my_file):
        os.remove(my_file)
    cv2.imwrite(my_file, image)

if __name__=='__main__':
    d = u2.connect("192.168.1.130")
    # image = d.screenshot(format='opencv')
    # st_time = time.time()
    # imageSave('home', st_time)

    print(getDevicesList())





# # 判断是否有更新，当前获取到的电视剧集最新剧集是27
# while d(text=str(JUJI)).exists:
#     if FLAG >= 2:
#         break
#     # time.sleep(10)
#     if d(text=str(JUJI + 1)).exists and FLAG == 0:
#         print("剧集第1次发生更新")
#         FirstUpdateTime = time.time()
#         imageSave('FirstUpdate', FirstUpdateTime)
#         FLAG += 1
#         JUJI += 1
#         if d(text=str(JUJI + 1)).exists:
#             JUJI += 1
#             print("更新了2集")
#         else:
#             print("更新了1集")
#     elif d(text=str(JUJI + 1)).exists and FLAG == 1:
#         print("剧集第2次发生更新")
#         SecondUpdateTime = time.time()
#         imageSave('SecondUpdate', SecondUpdateTime)
#         FLAG += 1
#     else:
#         print("更新率程序正在运行，请勿关闭电脑、电视盒子!!!!!!")

# INTERVAL_TIME = SecondUpdateTime - FirstUpdateTime

# print("更新间隔时间是" + str(INTERVAL_TIME))

print('程序结束')


