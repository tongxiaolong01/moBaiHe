# coding=utf-8
import os


def getMacAddress():
    command = "adb shell cat /sys/class/net/eth0/address"
    output = os.popen(command)
    for line in output:
        print(line)
        return line
    return str(output)
if __name__ == '__main__':
    print("dadfad" + getMacAddress())
    # ________________________mySmallTest_______________
    # k = 0
    # while k < 1:
    #     # time.sleep(30)
    #     st = time.time()
    #     jiangsuTestCase1.getRAM()
    #     dut=time.time()-st
    #     # time.sleep(30-dut)
    #     print("执行时间"+str(dut))
    #     waitTemp = 30 - dut
    #     print(waitTemp)
    #     time.sleep(waitTemp)
    #     myeddut = time.time()-st
    #
    #     print(myeddut)
    #     k += 1
