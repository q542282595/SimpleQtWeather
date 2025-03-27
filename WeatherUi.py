import json
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsScene


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 370)
        MainWindow.setMinimumSize(QtCore.QSize(420, 370))
        MainWindow.setMaximumSize(QtCore.QSize(420, 370))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 421, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(30, 20))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.province_combobox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.province_combobox.setMaximumSize(QtCore.QSize(130, 16777215))
        self.province_combobox.setObjectName("province_combobox")
        self.horizontalLayout.addWidget(self.province_combobox)
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(30, 20))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.city_combobox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.city_combobox.setObjectName("city_combobox")
        self.horizontalLayout.addWidget(self.city_combobox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.MainView = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        self.MainView.setObjectName("MainView")
        self.verticalLayout_2.addWidget(self.MainView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def loadjson(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def update_city_combobox(self, province_index):
        # 清空市下拉框
        self.city_combobox.clear()

        # 获取当前选中的省
        selected_province = self.province_combobox.itemText(province_index)

        # 填充市数据
        if selected_province in self.data:
            self.city_combobox.addItems(self.data[selected_province])
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LinkWeather"))
        self.label_3.setText(_translate("MainWindow", "省:"))
        self.label_2.setText(_translate("MainWindow", "市:"))
        self.label_4.setText(_translate("MainWindow", "心知天气ApiKey："))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        #print(f'{self.MainView.width()},{self.MainView.height()}')
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 418, 320)
        self.MainView.resetTransform()
        self.MainView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.MainView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.MainView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 加载 JSON 数据
        self.MainView.setScene(self.scene)
        self.data = self.loadjson('ChinaCitys.json')

        # 填充省下拉框
        self.province_combobox.addItems(self.data.keys())

        # 连接信号与槽
        self.province_combobox.currentIndexChanged.connect(
            lambda index: self.update_city_combobox(index)
        )
