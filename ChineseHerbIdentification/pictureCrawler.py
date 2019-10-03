# a crawler for crawler down baidu pictures  
#*******本脚本运行时需要本机安装 Chrome 浏览器以及Chrome的驱动，同时需要selenium库的支撑********  
from selenium import webdriver   
import time    
import urllib    
from bs4 import BeautifulSoup as bs  
import re    
import os    
#****************************************************  
base_url_part1 = 'https://image.baidu.com/search/index?ct=201326592&z=&tn=baiduimage&ipn=r&word='
base_url_part2 = '&pn=0&istype=2&ie=utf-8&oe=utf-8&cl=2&lm=-1&st=-1&fr=&fmq=&ic=0&se=&sme=&width=0&height=0&face=0'
search_query='冬虫夏草' #检索的关键词，可自行更改  
location_driver='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'#Chrome驱动程序在电脑中的位置  
  
class Crawler:  
    def __init__(self):  
        self.url=base_url_part1+search_query+base_url_part2  
  
    #启动Chrome浏览器驱动  
    def start_brower(self):  
        # 启动Chrome浏览器    
        driver = webdriver.Chrome(location_driver)    
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片  
        driver.maximize_window()    
        # 浏览器打开爬取页面    
        driver.get(self.url)    
        return driver  
  
    def downloadImg(self,driver):    
        foldername = 'dongchongxiacao' #定义文件夹的名字  
        picpath = 'D:\\ImageDownload\\%s' % (foldername)#下载到的本地目录   
        if not os.path.exists(picpath):   #路径不存在时创建一个    
            os.makedirs(picpath)  
        # 记录下载过的图片地址，避免重复下载    
        img_url_dic = {}   
        x = 0    
        #当鼠标的位置小于最后的鼠标位置时,循环执行  
        pos = 0       
        for i in range(5000):    #此处可自己设置爬取范围，本处设置为1，那么不会有下滑出现  
            pos +=500 # 每次下滚500    
            js = "document.documentElement.scrollTop=%d" % pos      
            driver.execute_script(js)    
            time.sleep(2)  
            #获取页面源码  
            html_page=driver.page_source  
            #利用Beautifulsoup4创建soup对象并进行页面解析  
            soup=bs(html_page,"html.parser")  
            #通过soup对象中的findAll函数图像信息提取  
            imglist=soup.findAll('img',{'src':re.compile(r'https:.*\.(jpg|png)')})  
  
            for imgurl in imglist:    
                if imgurl['src'] not in img_url_dic:  
                    target = picpath+'\\dongchongxiacao%s.jpg' % x    
                    #print ('Downloading image to location: ' + target + '\nurl=' + imgurl['src'])  
                    img_url_dic[imgurl['src']] = ''   
                    urllib.request.urlretrieve(imgurl['src'], target)    
                    x += 1    
                      
    def run(self):  
        print ('''''      *************************************  
        **      Welcome to use craw Chinese herb pictures!      **  
        *************************************''')    
        driver=self.start_brower()  
        self.downloadImg(driver)  
        driver.close()  
        print ("Download has finished.")  
  
if __name__ == '__main__':    
    craw = Crawler()   
    craw.run()  