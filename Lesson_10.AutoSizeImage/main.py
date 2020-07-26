# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-Mail: FeiXue@nuaa.edu.cn
@File: main.py
@Time: 2020/7/24 22:32
@Introduction: 图变大小跟随窗口变化
"""

from EzQtTools import *
import sys
import cv2
from PySide2.QtCore import QTimer, Signal
from PySide2.QtGui import QPixmap, QImage, QCursor


class MainWindow(EzMainWindow):

    def __init__(self, **kwargs):
        EzMainWindow.__init__(self, **kwargs)
        self.__init__widget()

    def __init__widget(self):
        # up, down
        self.image_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), stretch=1)
        self.control_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), stretch=0)

        # image
        self.image = self.add_layout_widget(self.image_area, ImageLabel(self.image_area))
        # progress widget
        self.progress = self.add_layout_widget(self.control_area, QtWidgets.QWidget())
        # control widget
        self.control = self.add_layout_widget(self.control_area, QtWidgets.QWidget())

        # button in control
        self.back = self.add_layout_widget(self.control, QtWidgets.QPushButton('快退'), QtWidgets.QHBoxLayout())
        self.play = self.add_layout_widget(self.control, QtWidgets.QPushButton('播放'))
        self.next = self.add_layout_widget(self.control, QtWidgets.QPushButton('快进'))
        self.back.setEnabled(False)
        self.play.setEnabled(False)
        self.next.setEnabled(False)

        # progress area
        self.progress_bar = self.add_layout_widget(self.progress, QtWidgets.QSlider(QtCore.Qt.Horizontal), QtWidgets.QHBoxLayout())
        self.progress_text = self.add_layout_widget(self.progress, QtWidgets.QLabel('00:00:00/00:00:00'))
        self.progress_bar.setEnabled(False)

        # menubar
        self.open = QtWidgets.QMenu('打开')
        self.menuBar().addMenu(self.open)
        # menu
        self.open_video = QtWidgets.QAction('打开视频')
        self.open.addAction(self.open_video)

        # video player
        self.video_player = Video()

        # connections
        self.open_video.triggered.connect(self.open_video_play)
        self.video_player.signal_image_show.connect(self.show_image_label)
        self.back.clicked.connect(lambda: self.video_player.play(1))
        self.back.pressed.connect(lambda: self.video_player.play(-2))
        self.next.clicked.connect(lambda: self.video_player.play(1))
        self.next.pressed.connect(lambda: self.video_player.play(2))
        self.play.clicked.connect(self.play_or_pause)
        self.video_player.signal_play_done.connect(self.reset_all)
        self.progress_bar.sliderMoved.connect(self.slider_move)
        self.progress_bar.sliderPressed.connect(lambda: self.video_player.play(0))
        self.progress_bar.sliderReleased.connect(lambda: self.video_player.play(1))
        self.image.signal_speed_changed.connect(self.speed_changed)

    # open file and load video into Opencv
    def open_video_play(self):
        video_path = self.open_file_dialog(default_dir='', types=['mp4', 'flv', 'avi'])
        if video_path:
            self.video_player.load(video_path)
            self.video_player.play(1)
            self.play.setText('暂停')

            self.back.setEnabled(True)
            self.play.setEnabled(True)
            self.next.setEnabled(True)
            self.progress_bar.setEnabled(True)

            max_frame = self.video_player.total_f
            self.progress_bar.setMaximum(max_frame)
            self.progress_text.setText(f'{self.video_player.now_time()}/{self.video_player.total_time()}')

    # show QPixmap into autosize label
    def show_image_label(self, img: QPixmap):
        if img:
            self.image.SetPixmap(img)
            self.progress_text.setText(f'{self.video_player.now_time()}/{self.video_player.total_time()}')
            self.progress_bar.setValue(self.video_player.current_f)

    def play_or_pause(self):
        if self.play.text() == '播放':
            self.video_player.play(1)
            self.play.setText('暂停')
        else:
            self.video_player.play(0)
            self.play.setText('播放')

    def reset_all(self):
        self.video_player.play(0)
        self.video_player.cap = None
        self.video_player.current_f = 0
        self.video_player.total_f = 0
        self.video_player.fps = 0
        self.back.setEnabled(False)
        self.play.setEnabled(False)
        self.next.setEnabled(False)
        self.progress_bar.setEnabled(False)
        self.play.setText('播放')
        self.progress_text.setText('00:00:00/00:00:00')
        self.progress_bar.setValue(self.video_player.current_f)
        self.image.Clear()

    def slider_move(self, pos: int):
        self.video_player.move_to(pos)
        self.video_player.current_f = pos
        self.progress_text.setText(f'{self.video_player.now_time()}/{self.video_player.total_time()}')
        self.video_player.read_next_frame()

    def speed_changed(self, speed: int):
        if speed == 0:
            self.video_player.play(0.5)
        else:
            self.video_player.play(speed)


class ImageLabel(AutoSizeLabel):
    """
    这里为了打开AutoSizeLabel的鼠标右键菜单，重写了它的某些事件。
    如果不使用右键菜单，可以将主窗口函数中的
    self.image = self.add_layout_widget(self.image_area, ImageLabel(self.image_area))
    替换为
    self.image = self.add_layout_widget(self.image_area, AutoSizeLabel(self.image_area))
    """
    signal_speed_changed = Signal(int)

    def __init__(self, *args, **kwargs):
        super(ImageLabel, self).__init__(*args, **kwargs)

        # setup context menu
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # define menu
        self.contextMenu = QtWidgets.QMenu(self)
        self.opt1 = self.contextMenu.addAction('0.5倍速播放')
        self.opt2 = self.contextMenu.addAction('1倍速播放')
        self.opt3 = self.contextMenu.addAction('2倍速播放')
        self.opt4 = self.contextMenu.addAction('4倍速播放')
        self.contextMenu.triggered.connect(self.menuSlot)
        self.contextMenu.sizeHint()

    def contextMenuEvent(self, *args, **kwargs):
        print(QCursor.pos(), self.contextMenu.size())
        self.contextMenu.popup(QCursor.pos())

    def menuSlot(self, act):
        act_text = act.text()
        speed = int(act_text[0])
        self.signal_speed_changed.emit(speed)


class Video(QtCore.QObject):

    signal_image_show = Signal(QPixmap)
    signal_play_done = Signal()

    def __init__(self):
        super(Video, self).__init__()

        self.v_timer = QTimer()
        self.v_timer.timeout.connect(lambda: self.play(1))
        self.cap = None
        self.current_f = 0
        self.total_f = 0
        self.fps = 0

    def load(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        assert self.cap, f"Open file {video_path} error."
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_f = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.v_timer.start(int(1000 / self.fps))

    def play(self, play_speed: float):
        """
        :param play_speed: 0停止，1正常速度播放，-1，正常速度后退
        :return:
        """
        if not self.cap:
            return

        if play_speed == 0:
            self.v_timer.stop()
        elif play_speed > 0:
            self.v_timer.timeout.disconnect()
            self.v_timer.timeout.connect(self.read_next_frame)
            self.v_timer.start(int(1000 / self.fps) / play_speed)
        elif play_speed < 0:
            self.v_timer.timeout.disconnect()
            self.v_timer.timeout.connect(self.__read_last_frame)
            self.v_timer.start(int(1000 / self.fps) / abs(play_speed))

    def move_to(self, pos):
        if pos < self.total_f:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)

    def read_next_frame(self):
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            next_pixmap = QPixmap.fromImage(showImage)
            self.signal_image_show.emit(next_pixmap)
            self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        else:
            self.signal_play_done.emit()

    def __read_last_frame(self):
        self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_f-2)
        return self.read_next_frame()

    def __frame_time(self, frame_n: int) -> str:
        sec = int(frame_n/self.fps)
        c_time = f"{int(sec/3600):02d}:{int((sec % 3600)/60):02d}:{int(sec % 60):02d}"
        return c_time

    def total_time(self) -> str:
        return self.__frame_time(self.total_f)

    def now_time(self) -> str:
        return self.__frame_time(self.current_f)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(icon='icon.png', title='播放器', default_layout_margins=2, default_layout_space=2)
    window.show()
    sys.exit(app.exec_())
