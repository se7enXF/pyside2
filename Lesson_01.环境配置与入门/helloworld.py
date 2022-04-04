# -*- coding: utf-8 -*-#
# File:     helloworld.py
# Author:   se7enXF
# Github:   se7enXF
# Date:     2019/2/19
# Note:     此程序源自Qt官网文档！使用PySide2显示窗口，点击按钮随机显示不同语言的“hello world”

import sys
import random
from PySide2 import QtGui, QtWidgets, QtCore


# 定义主窗口
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 设置主窗口大小
        self.resize(400, 300)
        # 设置主窗口标题
        self.setWindowTitle("hello world")

        # 定义不同语言
        self.hello = ["Hallo Welt", "你好世界！", "Hola Mundo", "Привет мир", "Hello world"]

        # 定义按钮
        self.button = QtWidgets.QPushButton("Click me!")

        # 定义标签
        self.text = QtWidgets.QLabel("Hello World")
        # 文字居中对齐
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        # 定义布局，垂直分布
        self.layout = QtWidgets.QVBoxLayout()

        # 在布局上添加文字
        self.layout.addWidget(self.text)
        # 在布局上添加按钮
        self.layout.addWidget(self.button)
        # 在主窗口上布置布局
        self.setLayout(self.layout)

        # 添加槽链接
        self.button.clicked.connect(self.magic)

    # 定义槽函数
    def magic(self):
        self.text.setText(random.choice(self.hello))


# 以下是主程序入口，格式基本固定，无须修改
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
