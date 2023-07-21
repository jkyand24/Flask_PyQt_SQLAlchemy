import sys
from PySide6.QtWidgets import QApplication,\
    QWidget, QVBoxLayout, QPushButton, QMessageBox
    
#

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Message Box")
        
        layout = QVBoxLayout()
        
        info_button = QPushButton("Info Button")
        info_button.clicked.connect(self.show_info_message)
        
        warning_button = QPushButton("Warning Button")
        warning_button.clicked.connect(self.show_warning_message)
        
        question_button = QPushButton("Question Button")
        question_button.clicked.connect(self.show_question_message)
        
        layout.addWidget(info_button)
        layout.addWidget(warning_button)
        layout.addWidget(question_button)
        
        self.setLayout(layout)
        
    def show_info_message(self):
        QMessageBox.information(self, "Info", "Info Message",
                                QMessageBox.Ok, QMessageBox.Close)
    
    def show_warning_message(self):
        QMessageBox.warning(self, "Warning", "Warning Message",
                                QMessageBox.Ok, QMessageBox.Close)
    
    def show_question_message(self):
        result = QMessageBox.question(self, "Question", "Question Message",
                                QMessageBox.Yes | QMessageBox.No)
        
        if result == QMessageBox.Yes:
            QMessageBox.information(self, "Your answer was...", "Yes..!", QMessageBox.Ok)
        
        else:
            QMessageBox.information(self, "Your answer was...", "No..!", QMessageBox.Ok)
            
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    
    main_window.show()
    
    app.exec()