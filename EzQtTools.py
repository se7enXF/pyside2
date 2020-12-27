# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: EzQtTools.py
@Time: 2020/7/3 12:37
@Introduction: 简便的Qt工具
"""


from PySide2 import QtWidgets, QtCore, QtGui
__NAME__ = 'EzQtTools'


# 快捷生成基础窗口和添加布局控件工具
class EzMainWindow(QtWidgets.QMainWindow):

    def __init__(self,
                 icon=None,
                 title=__NAME__,
                 size=(960, 540),
                 fixed=False,
                 max_window=False,
                 show_statusbar=False,
                 default_layout='V',
                 default_layout_stretch=0,
                 default_layout_margins=9,
                 default_layout_space=9):
        """
        直接生成基础的主窗口，并设置默认布局参数
        :param icon: 窗口图标URL
        :param title: 窗口标题
        :param size: 窗口大小（w，h）
        :param fixed: 窗口大小不可改变？
        :param max_window: 打开窗口后全屏？
        :param default_layout: 默认布局，V表示垂直布局，H表示水平布局
        :param default_layout_stretch: 当前控件在布局中的伸缩量
        :param default_layout_margins: 布局四周的边界量，可以是整数四元组，也可以是一个整数来表示同值的四元组
        :param default_layout_space: 布局中控件之间的间隔量
        """
        super(EzMainWindow, self).__init__()

        self.default_layout = default_layout
        self.default_layout_stretch = default_layout_stretch
        self.default_layout_margins = default_layout_margins
        self.default_layout_space = default_layout_space

        # -- 初始化默认参数 -- #
        if icon and QtCore.QFile.exists(icon):
            icon = QtGui.QIcon(icon)
            self.setWindowIcon(icon)
        self.setWindowTitle(title)
        if fixed:
            self.setFixedSize(size[0], size[1])
        else:
            self.resize(size[0], size[1])
        if max_window:
            self.showMaximized()

        # -- 初始化中心控件 -- #
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # -- 添加菜单栏和状态栏 -- #
        # 菜单栏添加菜单后自动显示
        if show_statusbar:
            self.statusBar().show()

        # -- 在此函数中设置自己的布局控件 -- #
        self.__init__widget()

    def add_layout_widget(self, parent: QtWidgets.QWidget,
                          widget: QtWidgets.QWidget,
                          layout: QtWidgets.QLayout = None,
                          stretch: int = None,
                          margins: [int, list] = None,
                          space: int = None
                          ) -> QtWidgets.QWidget:
        """
        给parent控件上添加widget。当parent首次添加widget，需要指定其布局格式。
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
            current_layout.addWidget(widget)
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

    def status_bar_write(self, words, timeout=0):
        """
        在状态栏上显示信息
        :param keep: 停留时间（毫秒），0表示一致停留直到触发清除或显示信息事件
        :param words: 信息
        """
        self.statusBar().showMessage(words)

    def open_file_dialog(self, default_dir='.', types: list = None) -> str:
        """
        打开文件或文件夹路径并返回
        :param default_dir: 打开文件夹对话框默认的目录
        :param types: 打开文件类型列表，例如 types=['jpg', 'bmp', ...]，当types=None时打开文件夹目录
        :return: dir
        """
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
        在自定义方法中重写该函数以设置自己的布局；
        在中心控件上设置布局，首要布局的parent必须指定为self.central_widget；

        例1：只在中心控件上放置标签
            label = self.add_layout_widget(self.central_widget, QtWidgets.QLabel())
        例2：在中心空间上放置容器，然后在其中添加两个标签
            widget = self.add_layout_widget(self.central_widget, QtWidgets.QWidget())
            label1 = self.add_layout_widget(widget, QtWidgets.QLabel())
            label2 = self.add_layout_widget(widget, QtWidgets.QLabel())
        例3：在中心空间上放置两个容器，然后分别在其中添加标签
            widget1 = self.add_layout_widget(self.central_widget, QtWidgets.QWidget())
            widget2 = self.add_layout_widget(self.central_widget, QtWidgets.QWidget())
            label1 = self.add_layout_widget(widget1, QtWidgets.QLabel())
            label2 = self.add_layout_widget(widget2, QtWidgets.QLabel())
        """
        pass


# 自适应窗口变化的显示图像的标签
class AutoSizeLabel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AutoSizeLabel, self).__init__(parent=parent)

        self.image = QtWidgets.QLabel(self)
        self.image.move(0, 0)
        self.image.setScaledContents(True)
        self.resize(parent.size())

    def SetPixmap(self, pix_img):
        self.image.setPixmap(pix_img)

    def resizeEvent(self, *args, **kwargs):
        self.image.resize(self.size())

    def Clear(self):
        self.image.clear()
