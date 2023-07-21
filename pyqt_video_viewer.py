import sys
import cv2
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout,\
    QFileDialog, QLabel, QApplication, QSizePolicy, QWidget, QStatusBar
from PySide6 import QtGui

class VideoViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Video Viewer")
        
        self.resize(800, 600)
        
        #
        
        self.open_file_button = QPushButton("Open File", self)
        self.open_file_button.clicked.connect(self.open_file_dialog)
        
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_video)
        
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_video)
        
        self.capture_button = QPushButton("Capture", self)
        self.capture_button.clicked.connect(self.capture_frame)
        
        self.view_video_label = QLabel(self)
        self.view_video_label.setAlignment(Qt.AlignCenter)
        self.view_video_label.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)
        
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.capture_button.setEnabled(False)
        
        #
        
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.open_file_button)
        main_layout.addWidget(self.play_button)
        main_layout.addWidget(self.stop_button)
        main_layout.addWidget(self.capture_button)
        main_layout.addWidget(self.view_video_label)
        
        #
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        #
        
        self.video_path = ""
        self.video_width = 720
        self.video_height = 640
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_next_frame)
        self.paused = False
        self.capture = None
        self.current_frame = 0
        self.capture_count = 0
        
        os.makedirs("./data", exist_ok=True)
        
    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mov *.mkv)")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles() # selected_files: ['비디오 파일의 경로']
            
            if selected_files:
                self.video_path = selected_files[0]
                
                self.status_bar.showMessage(f"Video Path: {self.video_path}")
                
                self.play_button.setEnabled(True)
        
    def play_video(self):
        if self.video_path:
            # 아래 if문은 Stop 이후 다시 Play를 눌렀을 때 실행됨
            
            if self.paused:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            
            # 아래 else문은 맨 처음 Play를 눌렀을 때 실행됨
                """
            맨 처음 video를 open하면, 기본적으로 self.paused == False이므로, 이 else문 안에 들어와, video capture가 시작됨
            그 이후에는, "play_video 실행됨" AND "self.paused == False"인 경우가 없어, 이 else문 안에 들어올 일이 없음 
                self.paused == False, 맨 처음 Play를 눌러 play_video 실행 --> Play Button, play_video Disabled
                이때, play_video를 Enable할 방법은, 먼저 stop_video를 실행하는 것밖에 없음
                --> Stop을 눌러 stop_video 실행 --> Play Button, play_video Enabled, self.paused == True
                """
                
            else: 
                self.capture = cv2.VideoCapture(self.video_path)
                
            self.paused = False
                
            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.capture_button.setEnabled(True)
            
            self.timer.start(42) # start()는 interval time [ms]를 파라미터로 받음. 1000ms / 24frame ~ 42로 임의 설정했음
        
    def stop_video(self):
        self.timer.stop()
        
        self.paused = True
        
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
    def capture_frame(self):
        ret, frame = self.capture.read()
        
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resize = self.resize_frame(frame_rgb)
            
            h, w, _ = frame_resize.shape
            
            if w > 0 and h > 0:
                video_name = os.path.splitext(os.path.basename(self.video_path))[0]
                image_name = f"{video_name}_{self.capture_count:04d}_image.png"
                image_path = os.path.join("./data/", image_name)
                
                cv2.imwrite(image_path, frame_resize)
                
                self.capture_count += 1
                
                self.status_bar.showMessage(f"Capture Done: {image_path}")
        
    def display_next_frame(self):
        if self.video_path:
            ret, frame = self.capture.read()
            
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resize = self.resize_frame(frame_rgb)
                
                h, w, _ = frame_resize.shape
                
                if w > 0 and h > 0:
                    frame_image = QtGui.QImage(frame_resize, w, h,
                                               QtGui.QImage.Format_RGB888)
                    
                    pixmap = QtGui.QPixmap.fromImage(frame_image)
                    
                    self.view_video_label.setPixmap(pixmap)
                    
                    self.view_video_label.setScaledContents(True)
                    
                    self.current_frame += 1
                
            else:
                self.timer.stop()
                
    def resize_frame(self, frame):
        h, w, _ = frame.shape
        
        if (w > self.video_width) or (h > self.video_height):
            w_ratio = self.video_width / w
            h_ratio = self.video_height / h
            
            if w_ratio < h_ratio:
                frame = cv2.resize(frame, (self.video_width, int(w_ratio * h)))
                
            else:
                frame = cv2.resize(frame, (int(h_ratio * w), self.video_height))
            
        return frame
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = VideoViewer()
    
    window.show()
    
    app.exec()