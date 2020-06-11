# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: struct.py.py
@Time: 2020/6/11 16:58
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
        self.center_widget.setStyleSheet('*{background: Gold; color: Black}')
        # 中心控件布局
        self.center_widget_layout = QtWidgets.QVBoxLayout()
        # 标签
        self.show_word = QtWidgets.QLabel('这是放在中心控件布局中的标签')
        # 设置标签居中
        self.show_word.setAlignment(QtCore.Qt.AlignCenter)
        # 将标签添加到布局里
        self.center_widget_layout.addWidget(self.show_word)
        # 将布放置到中心控件上
        self.center_widget.setLayout(self.center_widget_layout)

        # Dock窗口1
        self.dock = QtWidgets.QDockWidget('这是Dock1的标题')
        self.dock_container = QtWidgets.QWidget()
        self.dock_layout = QtWidgets.QVBoxLayout()
        self.dock_label = QtWidgets.QLabel('这是放在Dock1中的标签')
        self.dock_layout.addWidget(self.dock_label)
        self.dock_container.setLayout(self.dock_layout)
        self.dock.setWidget(self.dock_container)

        # Dock窗口2
        self.dock2 = QtWidgets.QDockWidget('这是Dock2的标题')
        self.dock2_container = QtWidgets.QWidget()
        self.dock2_layout = QtWidgets.QVBoxLayout()
        self.dock2_label = QtWidgets.QLabel('这是放在Dock2中的标签')
        self.dock2_layout.addWidget(self.dock2_label)
        self.dock2_container.setLayout(self.dock2_layout)
        self.dock2.setWidget(self.dock2_container)

        # 设置工具栏
        self.toolBar_top = QtWidgets.QToolBar()
        self.tool_top = QtWidgets.QLabel('这是放在工具栏中的一个标签')
        self.toolBar_top.addWidget(self.tool_top)

        # 将中心控件放置到主窗口内
        self.setCentralWidget(self.center_widget)
        # 将Dock控件放置到主窗口内
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock2)
        # 将工具栏控件放置到主窗口内
        self.addToolBar(self.toolBar_top)

        # 设置状态栏永久显示信息
        self.statusBar_Permanent = QtWidgets.QLabel('这是放在状态栏中的永久标签')
        self.statusBar().addPermanentWidget(self.statusBar_Permanent)
        self.statusBar().setStyleSheet('*{background: Aqua; color: Black}')

        # 设置菜单栏
        self.menu_setup = QtWidgets.QMenu('这是菜单栏中的一个菜单')
        self.menuBar().addMenu(self.menu_setup)
        self.menuBar().setStyleSheet('*{background: Aqua; color: Black}')


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
