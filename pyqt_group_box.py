import sys
from PySide6.QtWidgets import QApplication, QWidget,\
    QVBoxLayout, QBoxLayout, QGroupBox, QPushButton, QLineEdit, QLabel, QHBoxLayout
    
#

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Window Title")
        
        # 
        
        group_box1 = QGroupBox("Group Box 1")
        
        label1 = QLabel("name: ")
        line_edit1 = QLineEdit()
        button1 = QPushButton("Save")
        
        layout1 = QVBoxLayout()
        
        layout1.addWidget(label1)
        layout1.addWidget(line_edit1)
        layout1.addWidget(button1)
        
        group_box1.setLayout(layout1)
        
        #
        
        group_box2 = QGroupBox("Group Box 2")
        
        label2 = QLabel("age: ")
        line_edit2 = QLineEdit()
        button2 = QPushButton("Save")
        
        layout2 = QVBoxLayout()
        
        layout2.addWidget(label2)
        layout2.addWidget(line_edit2)
        layout2.addWidget(button2)
        
        group_box2.setLayout(layout2)
        
        #
        
        layout_main = QVBoxLayout()
        
        layout_main.addWidget(group_box1)
        layout_main.addWidget(group_box2)
        
        self.setLayout(layout_main)
        
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    window.show()
    
    app.exec()