# -*- coding: utf-8 -*-#
# File:     main.py
# Author:   se7enXF
# Github:   se7enXF
# Date:     2019/2/19
# Note:     使用布局。此程序在之前2讲已有注释，此处为简洁，不再注释

import sys
import os
from glob import glob
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QDir, QTimer
from PySide2.QtGui import QPixmap,QImage
from ui_mainwindow import Ui_MainWindow
import cv2


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.f_type = 0

    def window_init(self):
        self.label.setText("请打开文件")
        self.menu.setTitle("打开")
        self.actionOpen_image.setText("打开图片")
        self.actionOpen_video.setText("打开视频")
        # 按钮使能（否）
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        # 菜单按钮 槽连接 到函数
        self.actionOpen_image.triggered.connect(ImgConfig_init)
        self.actionOpen_video.triggered.connect(VdoConfig_init)
        # 自适应窗口缩放
        self.label.setScaledContents(True)


class ImgConfig:
    def __init__(self):
        window.pushButton.setEnabled(False)
        window.pushButton_2.setEnabled(True)
        window.pushButton_3.setEnabled(True)
        self.files, self.d_file = open_image()
        if not self.files:
            return
        self.n = len(self.files)
        window.pushButton_2.setText("上一张")
        window.pushButton_3.setText("下一张")

        # 获取当前列表文件名
        file_names = []
        for _ in range(self.n):
            (dir_name, full_file_name) = os.path.split(self.files[_])
            file_names.append(full_file_name)
        # 获取当前文件在列表中的位置
        self.counter = file_names.index(self.d_file)
        # 显示当前图片
        direct_show_image(self.files[self.counter])
        # 连接槽函数
        window.pushButton_2.clicked.connect(self.last_img)
        window.pushButton_3.clicked.connect(self.next_img)

    # 上一张
    def last_img(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = self.n-1
        direct_show_image(self.files[self.counter])

    # 下一张
    def next_img(self):
        if self.counter < self.n-1:
            self.counter += 1
        else:
            self.counter = 0
        direct_show_image(self.files[self.counter])


def ImgConfig_init():
    window.f_type = ImgConfig()


def open_image():
    # 打开文件对话框
    file_dir, _ = QFileDialog.getOpenFileName(window.pushButton, "打开图片", QDir.currentPath(),
                                              "图片文件(*.jpg *.png *.bmp);;所有文件(*)")
    # 判断是否正确打开文件
    if not file_dir:
        QMessageBox.warning(window.pushButton, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
        return
    print("读入文件成功")
    # 分离路径和文件名
    (dir_name, full_file_name) = os.path.split(file_dir)
    # 分离文件主名和扩展名
    (file_name, file_type) = os.path.splitext(full_file_name)
    # 获取文件路径下 所有以当前文件扩展名结尾的文件
    files = glob(os.path.join(dir_name, "*{}".format(file_type)))
    return files, full_file_name


def direct_show_image(img):
    # 使用Qt自带的图像格式读取
    pixmap = QPixmap(img)
    # 在label上显示图像
    window.label.setPixmap(pixmap)


def open_video():
    # 打开文件对话框
    file_dir, _ = QFileDialog.getOpenFileName(window.pushButton, "打开视频", QDir.currentPath(),
                                              "视频文件(*.mp4 *.avi );;所有文件(*)")
    # 判断是否正确打开文件
    if not file_dir:
        QMessageBox.warning(window.pushButton, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
        return
    print("读入文件成功")
    # 分离路径和文件名
    (dir_name, full_file_name) = os.path.split(file_dir)
    return file_dir


class VdoConfig:
    def __init__(self):
        window.pushButton.setEnabled(False)
        window.pushButton_2.setEnabled(False)
        window.pushButton_3.setEnabled(False)
        self.file = open_video()
        if not self.file:
            return
        window.label.setText("正在读取请稍后...")

        # 设置时钟
        self.v_timer = QTimer()
        self.cap = cv2.VideoCapture(self.file)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_f = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.v_timer.start(self.fps)

        window.pushButton.setEnabled(True)
        window.pushButton_2.setEnabled(True)
        window.pushButton_3.setEnabled(True)
        window.pushButton.setText("播放")
        window.pushButton_2.setText("快退")
        window.pushButton_3.setText("快进")

        # 连接槽函数
        self.v_timer.timeout.connect(self.show_pic)
        window.pushButton.clicked.connect(self.go_pause)
        window.pushButton_2.pressed.connect(lambda: self.last_img(True))
        window.pushButton_2.clicked.connect(lambda: self.last_img(False))
        window.pushButton_3.pressed.connect(lambda: self.next_img(True))
        window.pushButton_3.clicked.connect(lambda: self.next_img(False))

    def show_pic(self):
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            window.label.setPixmap(QPixmap.fromImage(showImage))

    def show_pic_back(self):
        self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_f-2)
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            window.label.setPixmap(QPixmap.fromImage(showImage))

    # 快退
    def last_img(self, t):
        window.pushButton.setText("播放")
        if t:
            self.v_timer.timeout.disconnect(self.show_pic)
            self.v_timer.timeout.connect(self.show_pic_back)
            self.v_timer.start(self.fps / 2)
        else:
            self.v_timer.timeout.disconnect(self.show_pic_back)
            self.v_timer.timeout.connect(self.show_pic)
            self.v_timer.start(self.fps)

    # 快进
    def next_img(self, t):
        window.pushButton.setText("播放")
        if t:
            self.v_timer.start(self.fps/2)
        else:
            self.v_timer.start(self.fps)

    # 暂停播放
    def go_pause(self):
        if window.pushButton.text() == "播放":
            self.v_timer.stop()
            window.pushButton.setText("暂停")
        elif window.pushButton.text() == "暂停":
            self.v_timer.start(self.fps)
            window.pushButton.setText("播放")


def VdoConfig_init():
    window.f_type = VdoConfig()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.window_init()
    window.show()
    sys.exit(app.exec_())
