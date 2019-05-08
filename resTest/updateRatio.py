# coding=utf-8
import uiautomator2 as u2
import cv2
import os
import time
import uiplus


# 电视盒子与电脑在同一局域网，IP_ADDRESS为电视盒子的地址，需要根据实际盒子的IP地址进行更新
IP_ADDRESS='192.168.1.130'
#剧集最新的集数,需要根据实际的节目集数来填写
JUJI=31

# 设置FLAG的值0、1；默认为0，如果有更新设置为1。
FLAG=0
#记录更新间隔时间
INTERVAL_TIME=0
#记录第一次更新时间
FirstUpdateTime=0
# 获取设备列表，逻辑有问题
def getDevicesList():
    command='adb devices'
    output = os.popen(command)
    for line in output.readlines():
        if '5555' in line:
            print(line)
            return True
        else:
            command=IP_ADDRESS
            output=os.popen(command)
            return False
            break

def uiautomator2Init():
    command='python -m uiautomator2 init'
    output=os.popen(command)
    for line in output.readlines():
        if 'success' in line:
            print("Uiautomator2 init Success!!")
            return True


def timeStyle(timestamp):
    time_Now = int(timestamp)
    time_local = time.localtime(time_Now)
    dt = time.strftime("%Y-%m-%d %H-%M-%S", time_local)
    return dt
# 保存图像
def imageSave(myfileName,nTime):
    my_file = 'updateResult\i'+myfileName+timeStyle(nTime)+'.jpg'
    print(timeStyle(nTime))
    if os.path.exists(my_file):
        os.remove(my_file)
    cv2.imwrite(my_file, image)

if __name__ == '__main__':
    # if (getDevicesList()==False):
    #     uiautomator2Init()
    d = u2.connect("192.168.1.130")
    image = d.screenshot(format='opencv')
    st_time=time.time()
    imageSave('Start',st_time)
    # 判断是否有更新，当前获取到的电视剧集最新剧集是27



    while d(text=str(JUJI)).exists:
            # 检查网络状态：
            # 检查adb连接状态
            # 检查当前剧集情况，如果没有当前剧集
            if FLAG>=1:
                break
            # time.sleep(10)
            if d(text=str(JUJI+1)).exists and FLAG==0:
                print("剧集第1次发生更新")
                FirstUpdateTime=time.time()
                imageSave('FirstUpdate',FirstUpdateTime)
                FLAG+=1
                JUJI+=1
                if d(text=str(JUJI+1)).exists:
                    JUJI+=1
                    print("更新了2集")
                else:
                    print("更新了1集")
            else:
                print("更新率程序正在运行，请勿关闭电脑、电视盒子!!!!!!")
    print("检测到更新时间是"+str(timeStyle(FirstUpdateTime)))
    print('程序结束')


