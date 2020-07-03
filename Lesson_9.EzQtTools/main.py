# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: main.py.py
@Time: 2020/7/1 17:10
@Introduction: 此例只适用于点击链接直接跳转的网页，不适用于点击链接打开新tab或者窗口的网页
"""

import sys
from EzQtTools import *
from PySide2.QtWebEngineWidgets import QWebEngineView


class MainWindow(EzMainWindow):

    def __init__(self, **kwargs):
        EzMainWindow.__init__(self, **kwargs)
        self.__init__widget()

    def __init__widget(self):
        """
        界面大概组成如下：

        -------------------------------------
        后退|前进|刷新|主页|      URL
        -------------------------------------
                      显示区域
        -------------------------------------

        根据上述格式，我们从大到小分块构成布局
        1. 垂直分两块
        2. 第一块水平分五块
        :return:
        """

        # 首先是从上往下的两个个大区域
        self.title_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), space=1)
        self.pages_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), stretch=1)

        # 给最上面的区域添加项目
        self.back = self.add_layout_widget(self.title_area, QtWidgets.QPushButton('后退'), QtWidgets.QHBoxLayout())
        self.ford = self.add_layout_widget(self.title_area, QtWidgets.QPushButton('前进'))
        self.refs = self.add_layout_widget(self.title_area, QtWidgets.QPushButton('刷新'))
        self.home = self.add_layout_widget(self.title_area, QtWidgets.QPushButton('主页'))
        self.urls = self.add_layout_widget(self.title_area, QtWidgets.QLineEdit())
        self.goto = self.add_layout_widget(self.title_area, QtWidgets.QPushButton('打开'))

        # 给显示区域添加浏览控件
        self.web_browser = self.add_layout_widget(self.pages_area, QWebEngineView())

        # 定义槽函数
        def open_home():
            url_home = 'https://gitee.com/se7enXF/pyside2'
            self.web_browser.load(QtCore.QUrl(url_home))
            self.urls.setText(url_home)

        def open_last():
            self.web_browser.back()

        def open_next():
            self.web_browser.forward()

        def open_refs():
            self.web_browser.reload()

        def open_goto():
            url = self.urls.text()
            self.web_browser.load(QtCore.QUrl(url))

        def correct_title():
            title = self.web_browser.title()
            self.setWindowTitle(title)

        # connections
        self.home.clicked.connect(open_home)
        self.back.clicked.connect(open_last)
        self.ford.clicked.connect(open_next)
        self.refs.clicked.connect(open_refs)
        self.goto.clicked.connect(open_goto)
        self.urls.returnPressed.connect(open_goto)
        self.web_browser.loadFinished.connect(correct_title)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(title='浏览器', default_layout_margins=2, default_layout_space=2, max_window=True)
    window.show()
    sys.exit(app.exec_())
