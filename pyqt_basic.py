import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox, QMessageBox

# 1.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("버튼을 만들어봤어요")
        
        self.resize(500, 500)
        
        self.button = QPushButton("클릭", self)
        
        self.button.clicked.connect(self.buttonClicked)
        
        self.button.setGeometry(50, 50, 200, 50)
        
    def buttonClicked(self):
        print("버튼 클릭 되었습니다.")
        
if __name__ == "__main__":
    app = QApplication(sys.argv) # sys.argv: ['지금 이 py 파일의 경로']
    
    window = MainWindow()
    
    window.show()
    
    sys.exit(app.exec()) # sys.exit(): 코드를 즉시 중단
        # 여기서는 app.exec() = 0
        
# 2.

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()
label = QLabel("안녕하세요.")

layout.addWidget(label)
window.setLayout(layout)

window.resize(500, 500)

window.show()

app.exec() # 이 코드에서 모든게 실행되는듯?. 뜬 창을 닫아야 다음 코드로 넘어감

# 3. line edit

app = QApplication([])

window = QWidget()
line_edit = QLineEdit()
layout = QVBoxLayout()

layout.addWidget(line_edit)
window.setLayout(layout)

window.resize(500, 500)

window.show()

app.exec()

# 4. button

app = QApplication([])

window = QWidget()
button = QPushButton("버튼!")
layout = QVBoxLayout()

layout.addWidget(button)
window.setLayout(layout)

window.resize(500, 500)

window.show()

app.exec()

# 5. check box

app = QApplication()

window = QWidget()
checkbox = QCheckBox("동의합니다!")
layout = QVBoxLayout()

layout.addWidget(checkbox)
window.setLayout(layout)

window.resize(500, 500)

window.show()

app.exec()

# 6. message box

app = QApplication()

message_box = QMessageBox()

message_box.setWindowTitle("타이틀")
message_box.setText("텍스트")

message_box.exec()