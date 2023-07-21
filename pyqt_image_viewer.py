import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow,\
    QPushButton, QVBoxLayout, QFileDialog, \
    QTreeWidget, QTreeWidgetItem, QListWidget,QLabel,QBoxLayout,QWidget,QHBoxLayout
from PySide6 import QtCore, QtGui

#

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Image Viewer")
        
        self.resize(800, 600)
        
        #
        
        self.folder_button = QPushButton("Folder Opening")
        self.folder_button.clicked.connect(self.open_folder_dialog)
        
        self.image_list_widget = QListWidget()
        self.image_list_widget.currentRowChanged.connect(self.display_image)
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['File'])
        
        self.image_label = QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.go_next)
        
        #
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.folder_button)
        left_layout.addWidget(self.image_list_widget)
        left_layout.addWidget(self.tree_widget)
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.back_button)
        right_layout.addWidget(self.next_button)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        #
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        #
        
        self.current_folder = ""
        self.current_images = []
        self.current_index = -1
        
    # 
        
    def open_folder_dialog(self):
        folder_dialog = QFileDialog(self)
        
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        
        folder_dialog.directoryEntered.connect(self.set_folder_path)
        folder_dialog.accepted.connect(self.load_images)
        
        folder_dialog.exec_()
        
    def set_folder_path(self, folder_path):
        self.current_folder = folder_path
        
    def load_images(self):
        self.image_list_widget.clear()
        self.tree_widget.clear()
        
        if self.current_folder:
            self.current_images = []
            self.current_index = -1
            
            image_extensions = (".jpg", ".png", ".jpeg", ".gif", ".bmp")
            
            root_item = QTreeWidgetItem(self.tree_widget, [self.current_folder])
            self.tree_widget.addTopLevelItem(root_item)
            
            for dir_path, _, file_names in os.walk(self.current_folder):
                dir_item = QTreeWidgetItem(root_item, [os.path.basename(dir_path)])
                root_item.addChild(dir_item)
                
                for file_name in file_names:
                    if file_name.lower().endswith(image_extensions):
                        file_item = QTreeWidgetItem(dir_item, [file_name])
                        dir_item.addChild(file_item)
                        
                        file_path = os.path.join(dir_path, file_name)
                        self.current_images.append(file_path)
                        self.image_list_widget.addItem(file_name)
                        
            if self.current_images:
                self.image_list_widget.setCurrentRow(0)
                
    #
                
    def display_image(self, index):
        if 0 <= index < len(self.current_images):
            self.current_index = index
            
            image_path = self.current_images[self.current_index]
            
            pixmap = QtGui.QPixmap(image_path)
            
            scaled_pixmap = pixmap.scaled(self.image_label.size() * 0.9,
                                          QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            
            self.image_label.setPixmap(scaled_pixmap)    
            
    #
    
    def go_back(self):
        if self.current_index > 0:
            self.image_list_widget.setCurrentRow(self.current_index - 1) # 왜인진 모르겠으나 self.current_index가 바뀜
    
    def go_next(self):
        if self.current_index < len(self.current_images) - 1:
            self.image_list_widget.setCurrentRow(self.current_index + 1)
            
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = ImageViewer()
    
    window.show()
    
    app.exec()