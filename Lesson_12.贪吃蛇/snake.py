# -*- coding: utf-8 -*-
"""
@ author: se7enXF
@ software: PyCharm
@ file: snake.py
@ time: 2021/9/25
@ Note: python3.9 code for Qt Greedy snake
"""

from EzQtTools import *
import sys
import random
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer


class Snake(QtWidgets.QPushButton):
    def __init__(self,
                 parent,
                 icon: str = 'resources/ico.svg',
                 direction: int = 0,
                 size: int = 10,
                 position: QtCore.QPoint = QtCore.QPoint(0, 0)
                 ):
        """
        Using QPushButton as a single snake part, head or body unit
        :param parent:must set up MainWindow as parent for embedding
        :param icon:head or body has different icon, default for body
        :param direction:move direction, WASD for up left down right
        :param size:box size in pixel
        :param position:QPushButton left up corner position
        """
        super().__init__(parent=parent)
        self.__icon = icon
        self.__direction = direction
        self.__size = size
        self.__position = position
        # setup snake body
        self.setFixedSize(QtCore.QSize(self.__size, self.__size))
        self.setIcon(QtGui.QIcon(self.__icon))
        self.setIconSize(QtCore.QSize(self.__size, self.__size))
        self.move(self.__position)
        # set button no border
        self.setFlat(True)
        self.show()

    def direct(self):
        return self.__direction

    def remove(self):
        """
        Hide current unit and delete obj
        :return:
        """
        self.hide()
        self.deleteLater()


class MainWindow(EzMainWindow):
    __ticker = QTimer()
    __directions: list[str] = ['w', 'a', 's', 'd']
    __snake: list[Snake] = []
    __h_direction: int = 0
    __enable_key = False
    __candy = None

    def __init__(self,
                 title: str = '贪吃蛇',
                 col_row_num: tuple = (10, 10),
                 icon: str = 'resources/ico.svg',
                 default_len: int = 3,
                 cell_edge: int = 50,
                 step: int = 500,
                 acc_rate: float = 2.,
                 **kwargs):
        """
        Qt MainWindow for snake control
        :param col_row_num: columns, rows, must greater than 5
        :param default_len:start snake length, must greater than 3
        :param cell_edge:snake unit edge size, must  greater than 50
        :param step:snake move interval time, m_second, must  greater than 100
        :param kwargs: other EzMainWindow args
        """
        w_size = list(col_row_num)
        if col_row_num[0] < 10:
            w_size[0] = 10
        if col_row_num[1] < 10:
            w_size[1] = 10
        if cell_edge < 50:
            cell_edge = 50
        w_size = (w_size[0] * cell_edge, w_size[1] * cell_edge)
        EzMainWindow.__init__(self, title=title, size=w_size, icon=icon, fixed=True, **kwargs)
        self.__cell_edge = cell_edge
        self.__col_row_num = col_row_num
        if default_len < 3:
            default_len = 3
        self.__default_len = default_len
        if step < 100:
            step = 100
        self.__step = step
        self.__init__widget()
        self.__ticker.setInterval(self.__step)
        self.__acc_step = int(self.__step / acc_rate)

    def __init__widget(self):
        """
        Init layout and connection
        """
        self.__introduction = QtWidgets.QPushButton('使用“WSAD”对应“上下左右”控制\n贪吃蛇，点击开始游戏！')
        self.add_layout_widget(self.central_widget, self.__introduction)
        self.__introduction.clicked.connect(self.__run)
        self.__ticker.timeout.connect(self.__snake_move)

    def __init_snake(self):
        """
        Init snake head, bodies
        """
        if len(self.__snake) > 0:
            for s in self.__snake:
                s.remove()
        self.__snake = []
        self.__ticker.setInterval(self.__step)
        self.__h_direction = random.choice(range(4))
        max_len_x = self.width() // self.__cell_edge
        max_len_y = self.height() // self.__cell_edge
        pos_x = random.choice(range(self.__default_len + 2, max_len_x - 2)) * self.__cell_edge
        pos_y = random.choice(range(self.__default_len + 2, max_len_y - 2)) * self.__cell_edge
        icon = f'resources/{self.__directions[self.__h_direction]}.svg'
        s = Snake(self, icon, self.__h_direction, self.__cell_edge, QtCore.QPoint(pos_x, pos_y))
        self.__snake.append(s)
        for i in range(self.__default_len - 1):
            self.__add_node()
        if not self.__candy:
            self.__candy = Snake(self, 'resources/candy.svg', size=self.__cell_edge)
        self.__new_candy()

    def __run(self):
        """
        Start move and show snake
        """
        # init snake show
        self.__init_snake()
        self.__introduction.hide()
        # start ticktock for snake moving
        self.__ticker.start()
        # enable key press
        self.__enable_key = True

    def __snake_move(self):
        """
        Body follow head, calculate head new pos
        Eating and crash check
        """
        self.__eat_candy()
        # move tail and body
        n_snake = len(self.__snake)
        for i in range(1, n_snake):
            s2 = self.__snake[n_snake - i]
            s1 = self.__snake[n_snake - i - 1]
            s2.move(s1.pos())
        # move head
        pos = self.__snake[0].pos()
        tmp_snake = Snake(self, direction=self.__h_direction, position=pos)
        h_pos = self.__get_next_head_pos(tmp_snake)
        tmp_snake.remove()
        icon = f'resources/{self.__directions[self.__h_direction]}.svg'
        new_head = Snake(self, icon, self.__h_direction, self.__cell_edge, h_pos)
        old_head = self.__snake[0]
        self.__snake[0] = new_head
        old_head.remove()
        self.__crash_check()

    def __restart(self):
        """
        Reset variables
        :return:
        """
        self.__ticker.stop()
        self.__enable_key = False
        self.__introduction.setText(f'游戏结束！\n得分：{len(self.__snake)}\n点击重新开始游戏！')
        self.__introduction.show()

    def __crash_check(self):
        # head out of window
        if self.__snake[0].x() < 0 or self.__snake[0].y() < 0 \
                or (self.__snake[0].x() + self.__cell_edge) > self.window().width() \
                or (self.__snake[0].y() + self.__cell_edge) > self.window().height():
            self.__restart()
        # head on body
        array_set = []
        for s in self.__snake:
            step_x = s.x() // self.__cell_edge
            step_y = s.y() // self.__cell_edge
            array_set.append(step_y * self.__col_row_num[0] + step_x)
        if array_set[0] in array_set[1:]:
            self.__restart()

    def __add_node(self):
        """
        Add one node based on last node
        """
        next_pos = self.__get_next_tail_pos(self.__snake[-1])
        next_d = self.__snake[-1].direct()
        node = Snake(self, direction=next_d, size=self.__cell_edge, position=next_pos)
        self.__snake.append(node)

    def __get_next_tail_pos(self, snake: Snake) -> QtCore.QPoint:
        """
        Mapping dir_code to next position
        """
        dir_code = snake.direct()
        pos = snake.pos()
        if dir_code == 0:  # up
            next_pos = QtCore.QPoint(pos.x(), pos.y() + self.__cell_edge)
        elif dir_code == 2:  # down
            next_pos = QtCore.QPoint(pos.x(), pos.y() - self.__cell_edge)
        elif dir_code == 1:  # left
            next_pos = QtCore.QPoint(pos.x() + self.__cell_edge, pos.y())
        elif dir_code == 3:  # right
            next_pos = QtCore.QPoint(pos.x() - self.__cell_edge, pos.y())
        else:
            raise ValueError(f'dir_code must in [0, 1, 2, 3], but get {dir_code}')
        return next_pos

    def __get_next_head_pos(self, snake: Snake) -> QtCore.QPoint:
        """
        Switch up and down, left and right
        :param snake: head of snake
        :return: next head position QPoint
        """
        pos = snake.pos()
        direction = (snake.direct() + 2) % 4
        tmp_snake = Snake(self, direction=direction, position=pos)
        pos = self.__get_next_tail_pos(tmp_snake)
        tmp_snake.remove()
        return pos

    def __change_speed(self, speed):
        if speed != self.__ticker.interval():
            self.__ticker.setInterval(speed)
            self.__snake_move()

    def __new_candy(self):
        """
        Random raise a candy in window but not on snake
        Mapping x,y to 1-d array
        :return:
        """
        array_set = list(range(self.__col_row_num[0] * self.__col_row_num[1]))
        for s in self.__snake:
            step_x = s.x() // self.__cell_edge
            step_y = s.y() // self.__cell_edge
            array_set.remove(step_y * self.__col_row_num[0] + step_x)
        pos = random.choice(array_set)
        x_pos = pos % self.__col_row_num[0] * self.__cell_edge
        y_pos = pos // self.__col_row_num[0] * self.__cell_edge
        self.__candy.move(QtCore.QPoint(x_pos, y_pos))

    def __eat_candy(self):
        """
        Judge eating candy
        :return:
        """
        head = self.__snake[0]
        if head.x() == self.__candy.x() and head.y() == self.__candy.y():
            self.__new_candy()
            self.__add_node()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Keep pressing key for accelerating speed, release for normal speed
        :param event:
        :return:
        """
        if event.key() in [Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D] and self.__enable_key:
            new_direction = self.__directions.index(event.text())
            # ignore opposite direction
            if (new_direction + 2) % 4 == self.__h_direction:
                return
            self.__h_direction = new_direction
            if event.isAutoRepeat():
                self.__change_speed(self.__acc_step)
                print(f'{event.text().capitalize()}:accelerate speed')
            else:
                self.__change_speed(self.__step)
                print(f'{event.text().capitalize()}:normal speed')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
