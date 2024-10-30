import hashlib

import psycopg2
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog

from HomeWindow import HomeWindow
from db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.home_window = HomeWindow()

        self.setWindowTitle("Вход/Регистрация")

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def login(self):
        username = self.username_input.text()
        password = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        self.cur.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
        user = self.cur.fetchone()

        if user:
            QMessageBox.information(self, "Успех", "Вы успешно вошли в систему.")
            self.home_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    def register(self):
        username = self.username_input.text()
        password = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        self.cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        self.conn.commit()

        QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались.")

        self.home_window.show()
        self.close()

    def closeEvent(self, event):
        self.cur.close()
        self.conn.close()