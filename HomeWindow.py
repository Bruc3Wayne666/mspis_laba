from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from CoursesWindow import CoursesWindow
from MindMapWindow import MindMapWindow
from TestWindow import TestWindow
from db import cur


class HomeWindow(QWidget):
    def __init__(self, user):
        super().__init__()

        self.courses_window = None
        self.mind_map_window = None
        self.user_id = user[0]
        self.username = user[1]

        self.test_window = None
        self.setWindowTitle("Home")
        self.resize(300, 200)

        self.label = QLabel("Добро пожаловать!")
        # self.test_button = QPushButton("Пройти тестирование")
        # self.test_button.clicked.connect(self.start_test)

        self.courses_button = QPushButton("Курсы")
        self.mind_map_button = QPushButton("Перейти к интеллект-карте")
        self.theme1_button = QPushButton("Тест по теме Авто")
        self.theme2_button = QPushButton("Тест по теме ИИ")
        self.theme3_button = QPushButton("Тест по теме МСПИС")

        self.theme1_button.clicked.connect(lambda: self.start_test("cars"))
        self.theme2_button.clicked.connect(lambda: self.start_test("AI"))
        self.theme3_button.clicked.connect(lambda: self.start_test("mspis"))
        self.mind_map_button.clicked.connect(self.open_mind_map)
        self.courses_button.clicked.connect(self.open_courses)

        self.label = QLabel(f"Добро пожаловать, {self.username} (ID: {self.user_id})!")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # layout.addWidget(self.test_button)
        layout.addWidget(self.mind_map_button)
        layout.addWidget(self.theme1_button)
        layout.addWidget(self.theme2_button)
        layout.addWidget(self.theme3_button)
        layout.addWidget(self.courses_button)

        self.setLayout(layout)


    def start_test(self, theme):
        self.test_window = TestWindow(theme, user_id=self.user_id)
        self.test_window.show()
        self.close()
        # self.hide()

    def open_mind_map(self):
        self.mind_map_window = MindMapWindow(self.user_id)
        self.mind_map_window.show()
        self.close()

    def open_courses(self):
        self.courses_window = CoursesWindow(self)
        self.courses_window.show()
        self.close()
