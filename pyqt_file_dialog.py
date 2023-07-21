from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

def open_file_dialog():
    file_dialog = QFileDialog()
    
    file_dialog.setWindowTitle("File Dialog")
    
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    
    file_dialog.setViewMode(QFileDialog.Detail)
    
    if file_dialog.exec(): # 파일이 선택되면
        selected_files = file_dialog.selectedFiles()
        
        print("\nSelected Files:\n", selected_files) 
        
app = QApplication()

main_window = QMainWindow()

button = QPushButton("I'm Button", main_window)

button.clicked.connect(open_file_dialog)

main_window.show()

app.exec()