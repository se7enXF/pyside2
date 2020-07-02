# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: subwindow.py
@Time: 2020/7/1 15:58
@Introduction: 
"""


import sys
import random
from PySide2 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "Hello world"]
        self.resize(1024, 768)
        self.setWindowTitle('Main window struct')

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout = QtWidgets.QVBoxLayout()
        # 标签
        self.show_word = QtWidgets.QLabel('Hello world')
        self.show_word.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.select = QtWidgets.QPushButton('Click to open sub-window1')
        self.select.setObjectName('subwindow')
        self.select2 = QtWidgets.QPushButton('Click to open sub-window2')
        self.select2.setObjectName('subwindow2')
        # 将标签添加到布局里
        self.center_widget_layout.addWidget(self.show_word)
        self.center_widget_layout.addWidget(self.select)
        self.center_widget_layout.addWidget(self.select2)
        # 将布放置到中心控件上
        self.center_widget.setLayout(self.center_widget_layout)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget)

        # 初始化子窗口
        self.subwindow = SubWindow1(parent=self)
        self.subwindow2 = SubWindow2()
        # 连接子窗口的自定义信号和槽函数
        self.subwindow2.signal_.connect(self.on_sub2_signal_)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)


    @QtCore.Slot()
    def on_subwindow_clicked(self):
        self.subwindow.show()

    @QtCore.Slot()
    def on_subwindow2_clicked(self):
        self.subwindow2.show()

    def on_sub2_signal_(self, num):
        self.show_word.setText(random.choice(self.hello))


class SubWindow1(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        第一种传参的方法：
            1. 为了避免一些问题的出现，避免所有变量重复定义
            2. 子窗口调用主窗口变量，要用 self.parent().window().[控件]
            3. 主窗口中初始化子窗口要指定parent为自己
            4. 主窗口直接可以调用子窗口变量
        :param parent:
        """
        super(SubWindow1, self).__init__(parent=parent)

        self.setWindowTitle('Sub window')
        self.setFixedSize(600, 250)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget_sub = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout_sub = QtWidgets.QVBoxLayout()
        # 按钮
        self.select_sub = QtWidgets.QPushButton('Click to change word in MainWindow')
        self.select_sub.setObjectName('words')
        # 将标签添加到布局里
        self.center_widget_layout_sub.addWidget(self.select_sub)
        # 将布放置到中心控件上
        self.center_widget_sub.setLayout(self.center_widget_layout_sub)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget_sub)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.Slot()
    def on_words_clicked(self):
        self.parent().window().show_word.setText(random.choice(self.parent().window().hello))


class SubWindow2(QtWidgets.QMainWindow):
    signal_ = QtCore.Signal(int)

    def __init__(self, parent=None):
        """
        第二种传参的方法，自定义信号：
            1. 此方法不用指定parent，主窗口和子窗口是独立的
            2. 子窗口中，要在def init 函数之前定义信号，函数中通过[自定义信号].emit()来发出信号
            3. 主窗口中，初始化子窗口后要连接信号
            4. 信号的槽函数参数和发出新信号的类型要一致
        :param parent:
        """
        super(SubWindow2, self).__init__(parent=parent)

        self.setWindowTitle('Sub window')
        self.setFixedSize(600, 250)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget_sub = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout_sub = QtWidgets.QVBoxLayout()
        # 按钮
        self.select_sub = QtWidgets.QPushButton('Click to change word in MainWindow')
        self.select_sub.setObjectName('words')
        # 将标签添加到布局里
        self.center_widget_layout_sub.addWidget(self.select_sub)
        # 将布放置到中心控件上
        self.center_widget_sub.setLayout(self.center_widget_layout_sub)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget_sub)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.Slot()
    def on_words_clicked(self):
        self.signal_.emit(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
