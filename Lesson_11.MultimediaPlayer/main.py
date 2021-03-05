# -*- coding:utf-8 -*-
"""
@Author: Fei Xue
@E-mail: feixue@nuaa.edu.cn
@File  : main.py.py
@Date  : 2020/10/15
@Info  : 多媒体播放器，支持视频，音频，必须安装本地媒体解码器
         作者使用解码器：https://github.com/Nevcairiel/LAVFilters
"""

from EzQtTools import *
import sys
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtCore import QUrl


class MainWindow(EzMainWindow):

    def __init__(self, **kwargs):
        EzMainWindow.__init__(self, **kwargs)
        self.player_widget = VideoPlayer()
        self.__init__widget()
        self.total_time = 0
        self.now_time = 0
        self.play_rate = 1

    def __init__widget(self):
        # up, down
        self.image_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), stretch=1)
        self.control_area = self.add_layout_widget(self.central_widget, QtWidgets.QWidget(), stretch=0)

        # image
        self.image = self.add_layout_widget(self.image_area, self.player_widget.video_widget)
        # progress widget
        self.progress = self.add_layout_widget(self.control_area, QtWidgets.QWidget())
        # control widget
        self.control = self.add_layout_widget(self.control_area, QtWidgets.QWidget())

        # button in control
        self.back = self.add_layout_widget(self.control, QtWidgets.QPushButton('正常速度'), QtWidgets.QHBoxLayout())
        self.play = self.add_layout_widget(self.control, QtWidgets.QPushButton('播放'))
        self.next = self.add_layout_widget(self.control, QtWidgets.QPushButton('加速播放'))
        self.back.setEnabled(False)
        self.play.setEnabled(False)
        self.next.setEnabled(False)

        # progress area
        self.progress_bar = self.add_layout_widget(self.progress, QtWidgets.QSlider(QtCore.Qt.Horizontal),
                                                   QtWidgets.QHBoxLayout(), space=20)
        self.progress_text = self.add_layout_widget(self.progress, QtWidgets.QLabel('00:00:00/00:00:00'))
        self.progress_bar.setEnabled(False)
        # volume control
        self.volume = self.add_layout_widget(self.progress, QtWidgets.QSlider(QtCore.Qt.Horizontal),
                                             QtWidgets.QHBoxLayout())
        self.volume.setFixedWidth(100)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setSingleStep(1)
        self.volume.setValue(50)

        # menubar
        self.open = QtWidgets.QMenu('打开')
        self.menuBar().addMenu(self.open)
        # menu
        self.open_video = QtWidgets.QAction('打开视频')
        self.open.addAction(self.open_video)

        # connections
        self.open_video.triggered.connect(self.open_video_play)
        self.play.clicked.connect(self.play_or_pause)
        self.progress_bar.sliderMoved.connect(self.img_slider_move)
        self.volume.sliderMoved.connect(self.volume_slider_move)
        self.player_widget.dur_changed.connect(self.auto_set_img_slider_max_pos)
        self.player_widget.pos_changed.connect(self.auto_move_img_slider)
        self.player_widget.state_changed.connect(self.auto_reset_play_end)
        self.back.clicked.connect(self.play_rate_reset)
        self.next.clicked.connect(self.play_rate_raise)

    def open_video_play(self):
        video_path = self.open_file_dialog(default_dir='', types=['mp4', 'flv', 'avi', 'mp3'])
        if video_path:
            self.player_widget.video_widget.show()
            self.player_widget.set_media(video_path)
            self.player_widget.play()

            self.play.setText('暂停')
            self.back.setEnabled(True)
            self.play.setEnabled(True)
            self.next.setEnabled(True)
            self.progress_bar.setEnabled(True)

    def play_or_pause(self):
        if self.play.text() == '暂停':
            self.play.setText('播放')
            self.player_widget.pause()
        else:
            self.play.setText('暂停')
            self.player_widget.play()

    def reset_all(self):
        self.back.setEnabled(False)
        self.play.setEnabled(False)
        self.next.setEnabled(False)
        self.progress_bar.setEnabled(False)
        self.play.setText('播放')
        self.progress_text.setText('00:00:00 / 00:00:00')
        self.progress_bar.setValue(0)
        self.player_widget.video_widget.hide()

    def img_slider_move(self, pos: int):
        self.player_widget.set_pos(pos)

    def volume_slider_move(self, pos: int):
        self.player_widget.set_volume(pos)

    def auto_move_img_slider(self, pos: int):
        self.progress_bar.setValue(pos)
        self.now_time = pos
        now, total = self.calculate_time(self.now_time, self.total_time)
        self.progress_text.setText(f'{now} / {total}')

    def auto_set_img_slider_max_pos(self, dur: int):
        self.progress_bar.setMaximum(dur)
        self.total_time = dur

    def auto_reset_play_end(self, state: int):
        if state == 0:
            self.reset_all()

    def calculate_time(self, now: int, total: int):
        current_sec = now // 1000
        total_seconds = total // 1000
        c_time = "{}:{}:{}".format(int(current_sec/3600), int((current_sec % 3600)/60), int(current_sec % 60))
        t_time = "{}:{}:{}".format(int(total_seconds / 3600), int((total_seconds % 3600) / 60), int(total_seconds % 60))
        return c_time, t_time

    def play_rate_reset(self):
        self.play_rate = 1
        self.player_widget.set_play_rate(self.play_rate)

    def play_rate_raise(self):
        self.play_rate += 1
        self.player_widget.set_play_rate(self.play_rate)


class VideoPlayer(QtWidgets.QWidget):

    dur_changed = QtCore.Signal(int)
    pos_changed = QtCore.Signal(int)
    state_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent=parent)
        """
        需要安装媒体解码器才可以正常使用QMediaPlayer
        作者使用 LAVFilters 来解码视频和音频。 URL：https://github.com/Nevcairiel/LAVFilters
        """
        self.video_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.setVolume(50)

        # 信号连接
        self.video_player.durationChanged.connect(self.__dur_changed)
        self.video_player.positionChanged.connect(self.__pos_changed)
        self.video_player.stateChanged.connect(self.__state_changed)

    def set_media(self, media_path: str):
        media = QMediaContent(QUrl.fromLocalFile(media_path))
        media = QMediaContent(media)
        self.video_player.setMedia(media)

    def set_volume(self, v: int = 50):
        self.video_player.setVolume(v)

    def set_play_rate(self, speed: int = 1):
        self.video_player.setPlaybackRate(speed)

    def set_pos(self, pos: int):
        self.video_player.setPosition(pos)

    def get_max_pos(self):
        return self.video_player.duration()

    def get_now_pos(self):
        return self.video_player.position()

    def get_video_widget(self):
        return self.video_widget

    def pause(self):
        self.video_player.pause()

    def play(self):
        self.video_player.play()

    def __dur_changed(self, dur: int):
        self.dur_changed.emit(dur)

    def __pos_changed(self, pos: int):
        self.pos_changed.emit(pos)

    def __state_changed(self, state: int):
        self.state_changed.emit(state)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(icon='icon.png', title='音视频播放器', default_layout_margins=2, default_layout_space=2)
    window.show()
    sys.exit(app.exec_())
