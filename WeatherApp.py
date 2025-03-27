import json
import sys
from datetime import datetime
from logging import exception

import requests
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPixmap, QFont, QLinearGradient, QColor, QPen, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, \
    QGraphicsView, QMessageBox

from WeatherUi import Ui_MainWindow  # 导入生成的 UI 类

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 调用 setupUi 方法设置界面
        self.noKey=True
      #  print(f'{self.MainView.viewport().width()},{self.MainView.viewport().height()}')
        self.city_combobox.currentIndexChanged.connect(lambda:self.queryweather())
        self.pushButton.clicked.connect(lambda:self.addApiKey())

    def drawWeatherIcon(self,weatherCode,x,y,isScaled=False):
            pixmap = QPixmap("WeatherIcon/"+weatherCode+".png")
            if isScaled:
                pixmap=pixmap.scaled(102,102,Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            pixmap_item=self.scene.addPixmap(pixmap)
            pixmap_item.setPos(x,y)
    def drawText(self,text,x,y,fontSize,isAlpha=False,color=Qt.GlobalColor.white):
        text_item = QGraphicsTextItem()
        text_item.setPlainText(text)  # 设置纯文本
        color=QColor(color)
        if isAlpha:
            color.setAlpha(128)
        text_item.setDefaultTextColor(color)  # 设置文字颜色
        text_item.setFont(QFont("微软雅黑", fontSize))  # 设置字体
        text_item.setPos(x, y)  # 设置文字位置
        self.scene.addItem(text_item)
    def setBackground(self,color1,color2,color3):
        gradient=QLinearGradient(0,0,0,320)
        gradient.setColorAt(0,QColor(color1))
        gradient.setColorAt(0.5, QColor(color2))
        gradient.setColorAt(1, QColor(color3))
        self.scene.setBackgroundBrush(gradient)
    def drawLine(self,startx,starty,endx,endy,isAlpha=True,color=Qt.GlobalColor.white):
        line=QGraphicsLineItem()
        line.setLine(startx,starty,endx,endy)
        color=QColor(color)
        if isAlpha:
            color.setAlpha(128)
        pen=QPen(color)
        pen.setWidth(1)
        line.setPen(pen)
        self.scene.addItem(line)
    def addApiKey(self):
        if self.noKey:
            self.api_key=self.lineEdit.text()
            self.lineEdit.setReadOnly(True)
            self.lineEdit.setStyleSheet("background-color: #CCCCCC;")
            self.pushButton.setText("取消")
            self.noKey=False
            self.queryweather()
        else:
            self.lineEdit.setReadOnly(False)
            self.lineEdit.setStyleSheet("")
            self.pushButton.setText("确定")
            self.noKey = True



    def queryweather(self):
        if self.city_combobox.currentText()!="" and not(self.noKey):
            location=self.city_combobox.currentText()
            api_url = f'https://api.seniverse.com/v3/weather/daily.json?key={self.api_key}&location={location}&language=zh-Hans&unit=c&start=0&days=3'
            response=requests.get(api_url)
            data=response.json()
            if  'status' in data:
                QMessageBox.warning(self, "错误",data['status'] )
                self.addApiKey()
                return
            self.updateUI(data)
    def updateUI(self,data):
        self.scene.clear()
        dt=datetime.fromisoformat(data['results'][0]['last_update'])
        last_update = dt.strftime("%H:%M")
        self.setBackground("#2b6ce9", "#5093f4", "#73b9fd")
        self.drawWeatherIcon(data['results'][0]['daily'][0]['code_day'], 20, 40, True)
        self.drawText(data['results'][0]['location']['name'], 0, 0, 12)
        self.drawText(f'{last_update}发布', 80, 5, 8, True)
        self.drawText(f"{data['results'][0]['daily'][0]['high']}°C/{data['results'][0]['daily'][0]['low']}°C", 140, 40, 17)
        self.drawText(data['results'][0]['daily'][0]['text_day'], 170, 100, 15)
        self.drawText(f"{data['results'][0]['daily'][0]['wind_direction']}风 {data['results'][0]['daily'][0]['wind_scale']}级", 280, 45, 12)
        self.drawText(f"降水量 {data['results'][0]['daily'][0]['rainfall']} mm", 280, 75, 12)
        self.drawText(f"相对湿度 {data['results'][0]['daily'][0]['humidity']}%", 280, 105, 12)
        self.drawLine(0, 170, 418, 170)
        print(data['results'][0])
        for v in range(3):
            if v>1:
                self.drawText(self.get_weekday(data['results'][0]['daily'][v]['date']), 45 + v * (140), 175, 12)
            elif v==0:
                self.drawText("今天", 45 + v * (140), 175, 12)
            elif v==1:
                self.drawText("明天", 45 + v * (140), 175, 12)
            self.drawWeatherIcon(data['results'][0]['daily'][v]['code_day'], 40 + v * (140), 205)
            self.drawText(data['results'][0]['daily'][v]['text_day'], 50 + v * (140), 260, 12)
            self.drawText(f"{data['results'][0]['daily'][v]['high']}°C/{data['results'][0]['daily'][v]['low']}°C", 30 + v * (140), 285, 12)
            if v < 2:
                self.drawLine(128 + v * (140), 180, 128 + v * (140), 310)

    def get_weekday(self, date_str):
        """
        查询指定日期是周几

        参数:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"

        返回:
            str: 日期对应的星期几，例如 "周一"、"周二" 等
        """
        # 将字符串转换为日期对象
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # 获取星期几，返回 0-6，0 表示周一
        weekday_num = date_obj.weekday()

        # 定义星期几的名称
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

        # 返回对应的星期几名称
        return weekdays[weekday_num]





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())