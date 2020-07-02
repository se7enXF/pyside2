# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: main.py.py
@Time: 2020/7/1 17:10
@Introduction: 此例只适用于点击链接直接跳转的网页，不适用于点击链接打开新tab或者窗口的网页
"""

import sys
import os
from PySide2 import QtWidgets, QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class EzMainWindow(QtWidgets.QMainWindow):

    def __init__(self,
                 ico=None,
                 title='浏览器',
                 size=(960, 540),
                 fixed=False,
                 full_screen=False,
                 default_layout='V',
                 default_layout_stretch=0,
                 default_layout_margins=9,
                 default_layout_space=9):
        super(EzMainWindow, self).__init__()

        self.default_layout = default_layout
        self.default_layout_stretch = default_layout_stretch
        self.default_layout_margins = default_layout_margins
        self.default_layout_space = default_layout_space

        # -- 初始化默认参数 -- #
        if ico and os.path.isfile(ico):
            self.setWindowIcon(ico)
        self.setWindowTitle(title)
        if fixed:
            self.setFixedSize(size[0], size[1])
        else:
            self.resize(size[0], size[1])
        if full_screen:
            self.setWindowFlag(QtCore.Qt.WindowFullScreen)

        # -- 初始化中心控件 -- #
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # -- 添加菜单栏和状态栏 -- #

        # -- 在此函数中设置自己的布局控件 -- #
        self.__init__widget()

    def add_layout_widget(self, parent, widget, layout=None, stretch=None, margins=None, space=None):
        """
        给parent控件上添加widget。当parent首次添加widget，需要指定其布局格式
        :param parent: 父控件
        :param widget: 当前添加的控件
        :param layout: 布局
        :param stretch: 伸缩量
        :param margins: 边界量
        :param space: 间隔量
        :return: 当前添加的控件
        """

        current_layout = parent.layout()
        if not stretch:
            stretch = self.default_layout_stretch

        if current_layout:
            current_layout.addWidget(widget, stretch=stretch)
        else:
            if not layout:
                if self.default_layout == 'H':
                    layout = QtWidgets.QHBoxLayout()
                else:
                    layout = QtWidgets.QVBoxLayout()
            if not margins:
                margins = self.default_layout_margins
            if not space:
                space = self.default_layout_space

            layout.addWidget(widget, stretch=stretch)
            layout.setSpacing(space)
            parent.setLayout(layout)

            if isinstance(margins, int):
                layout.setContentsMargins(margins, margins, margins, margins)
            else:
                layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])

        return widget

    def status_bar_write(self, words):
        self.statusBar().showMessage(words)

    def open_file_dialog(self, default_dir='.', types=None):
        if types is None:
            src = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             '打开目录',
                                                             default_dir,
                                                             QtWidgets.QFileDialog.ShowDirsOnly)
        else:
            type_str = f'*.{types}'
            if isinstance(types, list):
                type_str = f'*.{types[0]}'
                for t in types[1:]:
                    type_str += f' *.{t}'
            src, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开文件', default_dir, f'File type ({type_str})')

        return src

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
        2. 块1水平分5块
        :return:
        """

        # 首先是从上往下的两个个大区域
        self.default_layout_space = 5
        self.default_layout_margins = 2
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
    window = EzMainWindow()
    window.show()
    sys.exit(app.exec_())
