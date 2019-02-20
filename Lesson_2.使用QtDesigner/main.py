# -*- coding: utf-8 -*-#
# File:     main.py
# Author:   se7enXF
# Github:   se7enXF
# Date:     2019/2/19
# Note:     使用QtDesigner高效绘制界面，并使用PySide调用

import sys
import random
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow


# 主窗体类
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 定义主窗口
        self.ui = Ui_MainWindow()
        # 绑定主窗口
        self.ui.setupUi(self)
        # 定义字符
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "Hello world"]

        # 添加槽链接
        self.ui.pushButton.clicked.connect(self.magic)
        '''
        关于槽链接，在PySide中调用的格式是：
        发送者.信号.connect(槽函数)
        
        Qt是面向对象的程序设计，只有某个动作才会触发某个效果。使用槽链接的方式，可以实现复杂的操作。
        使用槽链接时，一定要在官方文档查找发送者有哪些信号，例如pushButton有clicked信号可以激活槽链接。
        '''

    def magic(self):
        # 随机选取
        self.ui.label.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
