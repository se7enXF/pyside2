# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: Slot.py
@Time: 2020/6/11 15:41
@Introduction: 另一种槽机制
"""

import sys
import random
from PySide2 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "Hello world"]
        self.resize(400, 300)
        self.setWindowTitle('Slot')

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout = QtWidgets.QVBoxLayout()
        # 标签
        self.show_word = QtWidgets.QLabel('Hello world')
        # 设置标签居中
        self.show_word.setAlignment(QtCore.Qt.AlignCenter)
        # 按钮
        self.push_word = QtWidgets.QPushButton('Random word')
        # 设置按钮ObjectName，使用connectSlotsByName必须设定
        self.push_word.setObjectName('push_word')
        # 将标签添加到布局里
        self.center_widget_layout.addWidget(self.show_word)
        # 将按钮添加到布局里
        self.center_widget_layout.addWidget(self.push_word)
        # 将布放置到中心控件上
        self.center_widget.setLayout(self.center_widget_layout)
        # 将中心控件放置到主窗口内
        self.setCentralWidget(self.center_widget)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    # 指定下面的函数是槽函数
    @QtCore.Slot()
    # on_ObjectName_信号 来定义槽函数名
    def on_push_word_clicked(self):
        self.show_word.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
