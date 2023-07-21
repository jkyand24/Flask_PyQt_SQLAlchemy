import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow,\
    QVBoxLayout, QWidget, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QStackedWidget, QListWidget
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

#

os.makedirs("db", exist_ok=True)

now = datetime.datetime.now().strftime('%H_%M_%S')

engine = create_engine(f'sqlite:///db/db_{now}.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()

# 사용자 정보

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
# register page: username 입력, password 입력, register(user 등록), login 이동

class RegisterPage(QWidget): 
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        
        #
        
        self.username_label = QLabel("Username: ")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Password: ")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        
        #
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)
        
        self.setLayout(self.layout)
        
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
            
        if username and password:
            user = User(username, password)
            
            session.add(user)
            
            session.commit()
            
            QMessageBox.information(self, "Success", "Registration Success")
            
            self.main_window.show_login_page()
            
        else:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
                
# login page: username 입력, password 입력, login(admin 이동), register 이동

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        
        #
        
        self.username_label = QLabel("Username: ")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Password: ")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        
        #
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        
        self.setLayout(self.layout)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = session.query(User).filter_by(username=username, password=password).first()
        
        if user:
            QMessageBox.information(self, "Success", "Login Success")
            
            self.main_window.show_admin_page()
        
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            
    def register(self):
        self.main_window.show_register_page()
        
# admin page: user list 보기, logout(login 이동)

class AdminPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        
        #
        
        self.show_user_list_button = QPushButton("Show User List")
        self.show_user_list_button.clicked.connect(self.show_user_list)
        
        self.user_list = QListWidget()
        
        self.logout_button =QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        
        #
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.show_user_list_button)
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(self.logout_button)
        
        self.setLayout(self.layout)
        
    def show_user_list(self):
        self.user_list.clear()
        
        users = session.query(User).all()
        
        for user in users:
            self.user_list.addItem(user.username)
            
    def logout(self):
        self.main_window.show_login_page()
        
# main page

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main")
        
        # stacked_widget에 login_page, register_page, admin_page를 담음
            # 각 page는 별도의 class로서 정의됨
                # 특정 page로 이동하는 기능은 main_window의 함수를 가져다 씀
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.register_page = RegisterPage(self)
        self.login_page = LoginPage(self)
        self.admin_page = AdminPage(self)
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.admin_page)
        
        # 맨 처음, login page에서 시작
        
        self.show_login_page()
        
    # login / register / admin 이동 함수 
    
    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)
        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        
    def show_register_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.register_page.username_input.clear()
        self.register_page.password_input.clear()
        
    def show_admin_page(self):
        self.stacked_widget.setCurrentIndex(2)
    
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    Base.metadata.create_all(engine)
    
    window = MainWindow()
    
    window.show()
    
    app.exec()