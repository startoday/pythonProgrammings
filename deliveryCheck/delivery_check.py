# -*- coding: utf-8 -*-
#so far added delivery company: yuantong, baishi, zhongtong 
import requests
import sys
import re
from datetime import datetime
from PyQt5.QtGui import QIcon  #for basic UI and buttons
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QPushButton


class yuantong():
    def __init__(self):
        self.headers = {
                'Referer': 'http://www.yto.net.cn/tracesimple.html/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko \
                Chrome/75.0.3770.142 Safari/537.36'
                }
        
        self.data = {
                'waybillNo': None}  #the data we need to track down
        
        self.url = 'http://www.yto.net.cn/api/trace/waybill' #the websited for tracking information
        
    def printres(self,res):
        traceNum = res.json()['data'][0]['waybillNo']
        traces = res.json()['data'][0]['traces']
        result = '【圆通快递】' + '\n' + '运单号：' + traceNum + '\n'
        for item in traces:
            time = str(datetime.fromtimestamp(int(item['time']/1000)))
            info = item['info']
            itemstr = time + '\t' + info + '\n'
            result = result + itemstr
        return result
        
    def inquiry(self, Number):
        self.data['waybillNo'] = Number
        res = requests.post(self.url,headers=self.headers,data=self.data)
        result = self.printres(res)
        return result
    
    
class zhongtong():
    def __init__(self):
        self.headers = {
                'Referer': 'https://www.zto.com/express/expressCheck.html?txtBill=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
                }
        
        self.data = {
                'billCode': None}
        
        self.url = 'https://hdgateway.zto.com/WayBill_GetDetail'
        
    def printres(self,res):
        traceNum = res.json()['result']['billCode']
        traces = res.json()['result']['logisticsRecord']
        result = '【中通快递】' + '\n' + '运单号：' + traceNum + '\n'
        for items in traces:
            for item in items:
                time = item['scanDate']
                info = item['stateDescription']
                itemstr = time + '\t' + info + '\n'
                result = result + itemstr
        return result
        
    def inquiry(self, Number):
        self.data['billCode'] = Number
        self.headers['Referer'] = self.headers['Referer'] + str(self.data['billCode'])
        res = requests.post(self.url,headers=self.headers,data=self.data)
        result = self.printres(res)
        return result
        


class baishi():
    def __init__(self):
        self.headers = {
                'Referer': 'http://www.800bestex.com/Bill/Track',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
                }
        
        self.data = {
                'code': None}
        
        self.url = 'http://www.800bestex.com/Bill/Track'
        
    def printres(self,res):
        restext = res.text
        restext_temp = restext[restext.find('运单记录： <span class="font-blue">')+30:]
        traceNum = restext_temp[0:restext_temp.find('<')]
        
        result = '【百世快递】' + '\n' + '运单号：' + traceNum + '\n'
        
        tracestext = restext_temp[restext_temp.find('<tbody>'):restext_temp.find('</tbody>')]
        tracestext = tracestext.split('</tr>')
        for items in tracestext[:-1]:
            items = items.split('<td>')
            time = items[1][0:items[1].find('</td>')]
            trace = items[3][0:items[3].find('</td>')]
            trace = re.sub('<.*?>','',trace)
            result = result + time + '\t' + trace + '\n'
        return result
        
    def inquiry(self, Number):
        self.data['code'] = Number
        res = requests.post(self.url,headers=self.headers,data=self.data)
        result = self.printres(res)
        return result


class Demo(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.setWindowTitle('快递查询')
        self.setWindowIcon(QIcon('data/icon.jpg'))
        self.Label1 = QLabel('运单号')
        self.Label2 = QLabel('快递信息')
        #self.Label1.width = 300
        #self.Label1.height = 50
        #self.Label2.width = 300
        #self.Label2.height = 500
        self.LineEdit1 = QLineEdit()
        self.LineEdit2 = QLineEdit()
        self.inquiryButton1 = QPushButton()
        self.inquiryButton1.setText('查询')
        self.inquiryButton2 = QPushButton()
        self.inquiryButton2.setText('圆通快递')
        self.inquiryButton3 = QPushButton()
        self.inquiryButton3.setText('中通快递')
        self.inquiryButton4 = QPushButton()
        self.inquiryButton4.setText('百世快递')
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.addWidget(self.Label1, 1, 0)
        self.grid.addWidget(self.LineEdit1, 1, 1)
        self.grid.addWidget(self.Label2, 2, 0)
        self.grid.addWidget(self.LineEdit2, 2, 1)
        self.grid.addWidget(self.inquiryButton1, 1, 2)
        self.grid.addWidget(self.inquiryButton2, 2, 2)
        self.grid.addWidget(self.inquiryButton3, 3, 2)
        self.grid.addWidget(self.inquiryButton4, 4, 2)
        self.setLayout(self.grid)
        self.resize(400, 200)
        self.inquiryButton1.clicked.connect(lambda : self.inquiry(api='chaxun'))
        self.inquiryButton2.clicked.connect(lambda : self.inquiry(api='yuantong'))
        self.inquiryButton3.clicked.connect(lambda : self.inquiry(api='zhongtong'))
        self.inquiryButton4.clicked.connect(lambda : self.inquiry(api='baishi'))
        self.yt_inquiry = yuantong()
        self.zt_inquiry = zhongtong()
        self.bs_inquiry = baishi()
        
    def inquiry(self,api='yuantong'):
        Number = self.LineEdit1.text()
        if api == 'chaxun':
            NumLen = len(Number)
            if NumLen == 18:
                results = self.yt_inquiry.inquiry(Number)
            elif NumLen == 15:
                results = self.bs_inquiry.inquiry(Number)
            elif NumLen == 14:
                results = self.zt_inquiry.inquiry(Number)                
        elif api == 'yuantong':
            results = self.yt_inquiry.inquiry(Number)
        elif api == 'zhongtong':
            results = self.zt_inquiry.inquiry(Number)
        elif api == 'baishi':
            results = self.bs_inquiry.inquiry(Number)
        
        self.LineEdit2.setText(results)
        
        
if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = Demo()
	demo.show()
	sys.exit(app.exec_())
    