import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Table View")
        
        table_view = QTableView(self)
        
        self.setCentralWidget(table_view)
        
        model = QStandardItemModel(4, 3, self)
        
        model.setHorizontalHeaderLabels(['이름', '나이', '성별'])
        
        model.setItem(0, 0, QStandardItem("정기연"))
        model.setItem(0, 1, QStandardItem("250"))
        model.setItem(0, 2, QStandardItem("여성"))
        
        model.setItem(1, 0, QStandardItem("안희상"))
        model.setItem(1, 1, QStandardItem("3"))
        model.setItem(1, 2, QStandardItem("남성"))
        
        model.setItem(2, 0, QStandardItem("카리나"))
        model.setItem(2, 1, QStandardItem("20"))
        model.setItem(2, 2, QStandardItem("신"))
        
        model.setItem(3, 0, QStandardItem("신짱구"))
        model.setItem(3, 1, QStandardItem("5"))
        model.setItem(3, 2, QStandardItem("남성"))
        
        table_view.setModel(model)
        
        table_view.resizeColumnsToContents()
        
        table_view.setEditTriggers(QTableView.NoEditTriggers) # 편집 금지
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    window.show()
    
    sys.exit(app.exec())