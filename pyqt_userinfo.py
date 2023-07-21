import sys
import csv
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,\
    QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QListWidget
    
# 정보 입력하는 창. InfoWindow로 연결됨
    
class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.age_line_edit = QLineEdit()
        self.gender_line_edit = QLineEdit()
        self.country_line_edit = QLineEdit()
        
        self.view_button = QPushButton("View")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("age: "))
        layout.addWidget(self.age_line_edit)
        
        layout.addWidget(QLabel("gender: "))
        layout.addWidget(self.gender_line_edit)
        
        layout.addWidget(QLabel("country: "))
        layout.addWidget(self.country_line_edit)
        
        layout.addWidget(self.view_button)
        
        self.setLayout(layout)
        
        self.view_button.clicked.connect(self.show_info)
        
    def show_info(self):
        age = self.age_line_edit.text()
        gender = self.gender_line_edit.text()
        country = self.country_line_edit.text()
        
        info_window = InfoWindow(age, gender, country)
        
        info_window.setModal(True)
        
        info_window.exec()
        
# 먼저 정보를 보여준 후, 해당 정보를 저장하는 창. ListWindow로 연결됨

class InfoWindow(QDialog):
    def __init__(self, age, gender, country):
        super().__init__()
        
        self.setWindowTitle("Info")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"age: {age}"))
        layout.addWidget(QLabel(f"gender: {gender}"))
        layout.addWidget(QLabel(f"country: {country}"))
        
        save_button = QPushButton("Save")
        load_button = QPushButton("Load")
        close_button = QPushButton("Close")
        
        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        save_button.clicked.connect(lambda: self.save_info(age, gender, country)) # signal로서 전달되는 parameter가 아닌 경우, lambda를 활용하여 function에 직접 전달해주는듯?
        load_button.clicked.connect(self.load_info)
        close_button.clicked.connect(self.close)
    
    def save_info(self, age, gender, country):
        iden = str(int(time.time()))
        data = [iden, age, gender, country]
        
        try:
            with open("info.csv", 'a', newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                writer.writerow(data)
                
            QMessageBox.information(self, "Success", "Info Saved")
        
        except Exception as e:
            QMessageBox.critical(self, "Failed", str(e))
        
    def load_info(self):
        try:
            with open("info.csv", 'r') as f:
                reader = csv.reader(f)
                
                lines = [line for line in reader]
                
            if len(lines) > 0:
                list_window = ListWindow(lines)
                
                list_window.exec()
            
            else:
                QMessageBox.information(self, "No Information")
                
        except Exception as e:
            QMessageBox.critical(self, "Cannot Load", str(e)) ###
            
# 전체 정보 리스트를 보여주는 창

class ListWindow(QDialog):
    def __init__(self, lines):
        super().__init__()
        
        self.setWindowTitle("Saved Information")
        
        list_widget = QListWidget()
        
        for line in lines:
            item = f"ID {line[0]}, age {line[1]}, gender {line[2]}, country {line[3]}"
            
            list_widget.addItem(item)
            
        layout = QVBoxLayout()
        
        layout.addWidget(list_widget)
        
        self.setLayout(layout)
        
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    input_window = InputWindow()
    
    input_window.show()
    
    app.exec()