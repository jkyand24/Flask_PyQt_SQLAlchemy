import sys
from PySide6.QtWidgets import QApplication, QLabel,\
    QVBoxLayout, QLineEdit,QPushButton,QCheckBox,QMessageBox, QWidget
    
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("기본 위젯")
        
        self.label = QLabel("위치 정보를 입력하세요.")
        self.line_edit = QLineEdit()
        self.checkbox = QCheckBox("위치 정보 전달 동의")
        self.send_button = QPushButton("전송")
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)
        
        self.send_button.clicked.connect(self.show_message)
        
    def show_message(self):
        if self.checkbox.isChecked():
            message = self.line_edit.text()
            
            print(f"입력 내용: {message}")
            
        else:
            error_message = "동의 버튼이 클릭되지 않았습니다."
            
            QMessageBox.critical(self, "에러", error_message)
        
        self.line_edit.clear()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    window.show()
    
    sys.exit(app.exec())