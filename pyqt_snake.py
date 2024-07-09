import sys
import numpy as np

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class Snake_Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.img_width = 40
        self.img_height = 40
        
        self.img = np.zeros((self.img_width,self.img_height), dtype=np.uint8)
        self.p_x = []
        self.p_y = []
        for j in range(8):
            self.p_x.append(10)
            self.p_y.append(10+j)
        self.img[self.p_x,self.p_y] = 255

        self.r_x = np.random.randint(low=1,high=self.img_height,size=1)
        self.r_y = np.random.randint(low=1,high=self.img_width,size=1)
        self.img[self.r_x,self.r_y] = 160

        qtImage = QImage(self.img.data, self.img_width, self.img_height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qtImage)
        pixmap = pixmap.scaled(400, 400)
        
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)

        self.score_label = QLabel("Score = "+str(0))
        self.left_button = QPushButton("Left")
        self.right_button = QPushButton("Right")
        self.top_button = QPushButton("Top")
        self.down_button = QPushButton("Down")

        layout_left_right = QHBoxLayout()
        layout_left_right.addWidget(self.left_button)
        layout_left_right.addWidget(QLabel(""))
        layout_left_right.addWidget(self.right_button)

        layout_top = QHBoxLayout()
        layout_top.addWidget(QLabel(""))
        layout_top.addWidget(self.top_button)
        layout_top.addWidget(QLabel(""))

        layout_down = QHBoxLayout()
        layout_down.addWidget(QLabel(""))
        layout_down.addWidget(self.down_button)
        layout_down.addWidget(QLabel(""))

        layout_left_right = QHBoxLayout()
        layout_left_right.addWidget(self.left_button)
        layout_left_right.addWidget(QLabel(""))
        layout_left_right.addWidget(self.right_button)

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.score_label)
        control_layout.addWidget(QLabel(""))
        control_layout.addLayout(layout_top)
        control_layout.addLayout(layout_left_right)
        control_layout.addLayout(layout_down)
        control_layout.addWidget(QLabel(""))
        control_layout.addWidget(QLabel(""))
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(control_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer to update video frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer_interval = 300  # Default timer interval (100 ms)
        self.timer.start(self.timer_interval)  # Update video frames every 100 ms by default

        self.direction = "right"
        self.top_button.clicked.connect(self.top_direction)
        self.down_button.clicked.connect(self.down_direction)
        self.left_button.clicked.connect(self.left_direction)
        self.right_button.clicked.connect(self.right_direction)
    
    def update_game(self):
        self.img[self.p_x[0],self.p_y[0]] = 0
        self.p_x.pop(0)
        self.p_y.pop(0)

        ### add new point
        if self.direction=="top":
            self.p_x.append(self.p_x[-1]-1)
            self.p_y.append(self.p_y[-1])
        elif self.direction=="down":
            self.p_x.append(self.p_x[-1]+1)
            self.p_y.append(self.p_y[-1])
        elif self.direction=="left":
            self.p_x.append(self.p_x[-1])
            self.p_y.append(self.p_y[-1]-1)
        elif self.direction=="right":
            self.p_x.append(self.p_x[-1])
            self.p_y.append(self.p_y[-1]+1)
        
        if self.p_x[-1]==-1 or self.p_x[-1]==self.img_height or self.p_y[-1]==-1 or self.p_y[-1]==self.img_width:
            self.timer.stop()
            print("Game over!!!")
        else:
            hit_snake = 0
            for j in range(len(self.p_x)-1):
                if self.p_x[-1]==self.p_x[j] and self.p_y[-1]==self.p_y[j]:
                    hit_snake = 1
                    break
            if hit_snake==1:
                self.timer.stop()
                print("Game over!!!")
            else:
                self.img[self.p_x[-1],self.p_y[-1]] = 255

                if self.p_x[-1]==self.r_x and self.p_y[-1]==self.r_y:
                    if self.direction=="top":
                        self.p_x.append(self.p_x[-1]-1)
                        self.p_y.append(self.p_y[-1])
                    elif self.direction=="down":
                        self.p_x.append(self.p_x[-1]+1)
                        self.p_y.append(self.p_y[-1])
                    elif self.direction=="left":
                        self.p_x.append(self.p_x[-1])
                        self.p_y.append(self.p_y[-1]-1)
                    elif self.direction=="right":
                        self.p_x.append(self.p_x[-1])
                        self.p_y.append(self.p_y[-1]+1)
                    self.img[self.p_x[-1],self.p_y[-1]] = 255

                    self.score = self.score + 1
                    self.score_label.setText("Score = "+str(self.score))

                    self.timer_interval = int(0.9*self.timer_interval)  # Default timer interval (100 ms)
                    self.timer.setInterval(self.timer_interval)  # Update video frames every 100 ms by default

                    self.r_x = np.random.randint(low=1,high=self.img_height,size=1)
                    self.r_y = np.random.randint(low=1,high=self.img_width,size=1)
                    self.img[self.r_x,self.r_y] = 160
    
                qtImage = QImage(self.img.data, self.img_width, self.img_height, QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(qtImage)
                pixmap = pixmap.scaled(400, 400)
                self.image_label.setPixmap(pixmap)

    def top_direction(self):
        if self.direction != "down":
            self.direction = "top"
    
    def down_direction(self):
        if self.direction != "top":
            self.direction = "down"

    def left_direction(self):
        if self.direction != "right":
            self.direction = "left"

    def right_direction(self):
        if self.direction != "left":
            self.direction = "right"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Snake_Game()
    player.show()
    sys.exit(app.exec_())