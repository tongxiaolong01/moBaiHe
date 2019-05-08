import traceback, sys, xlrd, xlwt, re, os, atx, time
from xlutils.copy import copy

__all__ = ['UiPlus']

TIMEOUT = 20

class UiPlus(object):
    def __init__(self, pkg = None, act = None,se = None):
        self.app = atx.connect(se)
        self.packageName = pkg
        self.activity = act

    
    def setpkg(self, pkg):
        self.packageName = pkg
        

    def setactivity(self, act):
        self.activity = act
    
    def start_app(self, stop=True):
        '''
        Start application

        Args:
            - package_name (string): like com.example.app1
            - activity (string): optional, activity name
            - stop: force stop the target app before starting the activity

        Returns time used (unit second), if activity is not None
        '''
        activity=self.activity
        return self.app.start_app(self.packageName, activity, stop)

    def close_app(self, clear=False):
        '''
        Stop application

        Args:
            package_name: string like com.example.app1
            clear: bool, remove user data

        Returns:
            None
        '''
        self.app.stop_app(self.packageName, clear)
        
    def findpic(self, imgName, raw = True, minpoint = 20, confidence=0.8, timeout = TIMEOUT):
        '''
        if raw is True, find raw img, fast, need same size, color, shape, confidence the bigger the more similar,
        the value is little than 1.
        
        if raw is not False, use sift find image, could manage scale, but slow, around 0.5s, minpoint the bigger 
        the more similar, the max value depands on the picture.
        
        take screenshot takes 0.3s
        '''
        pos = None
        st = time.time()
        while time.time() - st < timeout:
            if not raw:                
                pos = self.img_pos(imgName,"sift")
                if pos and pos[1][0] > minpoint:
                    return pos[0]
            else:
                pos = self.img_pos(imgName,"template")
                if pos and pos[1] > confidence:
                    return pos[0]
        return None

    def img_pos(self, imgName, algorithm):
        """Check if image position in screen

        Args:
            - imgName: Image file name or opencv image object

        Returns:
            None or FindPoint, For example:

            FindPoint(pos=(20, 30), method='tmpl', confidence=0.801, matched=True)

            Only when confidence > self.image_match_threshold, matched will be True

        Raises:
            TypeError: when image_match_method is invalid
        """
        return self.app.exists(imgName, method=algorithm)

    def click_img(self, imgName):
        pos = self.findpic(imgName)
        self.click(pos[0],pos[1])

    def click(self, x, y):
        self.app.click(x, y)
        
    def drag(self, sx, sy, ex, ey, duration=0.5):
        self.app.drag(sx, sy, ex, ey, duration=0.5)
        
    def double_click(self, x, y):
        self.app.double_click(x,y)
        
    def long_click(self, x, y, duration=None):
        self.app.long_click(x, y, duration=None)
        
    def swipe(self, fx, fy, tx, ty, duration=0.5):
        self.app.swipe(fx, fy, tx, ty, duration=0.5)
        
    def screenShot(self, filename=None):
        """
        Image format is JPEG

        Args:
            filename (str): saved filename
            format (string): used when filename is empty. one of "pillow" or "opencv"

        Raises:
            IOError, SyntaxError

        Examples:
            screenshot("saved.jpg")
            screenshot().save("saved.png")
            cv2.imwrite('saved.jpg', screenshot(format='opencv'))
        """
        time_str = time.strftime('_%m%d_%H%M', time.localtime(time.time()))
        self.app.screenshot(".\\screenshot\\" + filename + time_str + ".png")
        return time_str
        
    def screen_on(self):
        self.app.screen_on()
        
    def screen_off(self):
        self.app.screen_off()
        
    def press(self, key):
        '''
        home,back;left;right;up;down;center;menu;search;enter;delete ( or del);recent (recent apps);volume_up
        volume_down;volume_mute;camera;power
        press('home')
        '''
        self.app.press(key)
        
    def xpath(self, path):
        self.app.xpath(path)

    def _uiwarp(self, **kwargs):
        '''
        resourceId=None, text=None, className=None, description=None,
        textContains, textMatches, textStartsWith,descriptionContains,descriptionMatches,
        focused,selected,resourceIdMatches,index
        ''' 
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']
            del(kwargs['timeout'])
        else:
            timeout = TIMEOUT
        st = time.time()
        while time.time() - st < timeout:
            try:
                el = self.app(**kwargs)
                if el.exists():
                    return el
                else:
                    time.sleep(0.01)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                print(kwargs)
        return None


    def findIdText(self, idname, textname, timeout=TIMEOUT):
        return self._uiwarp(resourceId=idname,text=textname, timeout=timeout)
    def findText(self, textname, timeout=TIMEOUT):
        return self._uiwarp(text=textname, timeout=timeout)
    def findId(self, idname, timeout=TIMEOUT):
        return self._uiwarp(resourceId=idname, timeout=timeout)

        # instance 为相同元素的目标个数

    def findIds(self, idname, instance, Timeout):
        return self._uiwarp(resourceId=idname, instance=instance, timeout=Timeout)

    def findClassText(self, classname, textname, timeout=TIMEOUT):
        return self._uiwarp(className=classname,text=textname, timeout=timeout)

    def clickId(self, idname, timeout=TIMEOUT):
        el = self.findId(idname, timeout)
        if el:
            time.sleep(1)
            el.click()
        else:
            raise Exception("click id error {}".format(idname))

    def writeToExcel(self, data, filename, sheetname):
        if os.path.exists(filename):
            self.writeOldExcel(data, filename, sheetname)
        else:
            self.writeNewExcel(data, filename, sheetname)

    def writeNewExcel(self, data, filename, sheetname):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(sheetname, cell_overwrite_ok=True)
        l = len(data)
        for i in range(l):
            worksheet.write(0, i, str(data[i]))
        workbook.save(filename)

    def writeOldExcel(self, data, filename, sheetname):
        oldWb = xlrd.open_workbook(filename)
        newWb = copy(oldWb)
        if sheetname in oldWb.sheet_names():
            rows = oldWb.sheet_by_name(sheetname).nrows
            newWs = newWb.get_sheet(sheetname)
        else:
            newWs = newWb.add_sheet(sheetname, cell_overwrite_ok=True)
            rows = 0
        l = len(data)
        for i in range(l):
            newWs.write(rows, i, str(data[i]))
        newWb.save(filename)    
        
    def clickElTime(self, el=None, checkId=None, checkText=None, reg=None, pos=None, img=None):
        checkEl = None
        retry = 10 
        time.sleep(1)
        if el or pos:
            if pos:
                x, y = pos
                self.click(x, y)
            else:
                el.click()
            start_time = time.time()
            while retry > 0:                
                if checkText:
                    checkEl = self.findIdText(checkId, checkText)
                elif checkId != None:
                    print("check id", checkId)
                    checkEl = self.findId(checkId)
                else:
                    checkEl = self.findpic(img)
                if checkEl:
                    rt_time = time.time() - start_time
                    if not reg:
                        return str(round(rt_time,2))
                    else:
                        m = re.search(reg, checkEl.get_text())
                        if m:
                            return str(round(rt_time,2))
                        else:
                            retry -= 1
                            continue
                else:
                    return 'false'
            retry -= 10
        else:
            print("clickElTime el id error", checkId)
        return 'false'
    
    def input(self, s):
        self.app.uiautomator.set_fastinput_ime(True)
        self.app.uiautomator.send_keys(s)
        self.app.uiautomator.set_fastinput_ime(True)
        
    def m1_input(self):
        self.press('right')
        time.sleep(1)
        self.press('right')
        time.sleep(1)        
        self.press('enter')
        
    def m2_input(self, s):
        for c in s:
            print('click')
            self.click_img('img/' + c + '.png')
            time.sleep(0.5)




    """"
        根据初始位置，行数和位置偏移量
        返回【元素：位置】字典
        el--所定位元素列表
        start_x，start_y为所定位的初始位置
        shift_x,y为元素间的偏移量
        rows为行数
    """

    def set_elements_dict(self,el,start_X,start_Y,shift_X=0,shift_Y=0,rows = 0,):
        result = {}
        for i in range(0,len(el)):
            Y_times = int(i/rows)
            X_times = int(i%rows)
            X = start_X+shift_X*X_times
            Y = start_Y+ shift_Y*Y_times
            result[el[i]] = [X,Y]

        return result
    def click_element_searchkeyboard(self,str):
        el = ["A","B","C","D","E","F","G","H","I","J",
                   "K","L","M","N","O","P","Q","R","S",
                   "T","U","V","W","X","Y"," ","123","Z"]

        dict = self.set_elements_dict(el,90,180,60,50,5)

        if str in dict.keys():
            v=dict.get(str)
            print(v)
            self.click(v[0],v[1])
        else:
            print('该元素不在自定义元素数组内')


    #         点击01盒子的频道
    def click_element_channel(self,el,str):
        # el = ["推荐","会员超时","都挺好","动漫","教育","游戏",
        #       "音乐","体育健身","4K高清","家庭专区"
        #         ]
        line = []
        new_line = []
        dict = self.set_elements_dict(el,150,90,140,0,8)
        for i in range(8,len(el)):
             line.append(el[i])

        if str in  line:

            aborad = dict.get(el[7])

            self.click(aborad[0],aborad[1])
            time.sleep(2)
            # el = [ "都挺好", "动漫", "教育", "游戏",
            #       "音乐", "体育健身", "4K高清", "家庭专区"
            #       ]

            for l in range(2, len(el)):
                new_line.append(el[l])
            dict = self.set_elements_dict(new_line, 150, 90, 140, 0, 8)
            print(dict,"------")
        if str in dict.keys():
            v=dict.get(str)
            self.click(v[0],v[1])
# 是否展示ID
    def nodisplay_id(self,id):
     print(str(self._uiwarp(resourceId=id, timeout=0.01)))
     for i in range(0,2000):

        if  self._uiwarp(resourceId=id, timeout=0.01)!=None:
            time.sleep(0.01)
            continue
        else:
            return True
     return False

if __name__ == '__main__':
        ui= UiPlus(None)
        el = ["A","B","C","D","E","F","G"]
        ui.set_elements_dict(el,1,1,1,1,4)