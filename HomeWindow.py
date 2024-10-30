from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from TestWindow import TestWindow


class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.test_window = None
        self.setWindowTitle("Home")
        self.resize(300, 200)

        self.label = QLabel("Добро пожаловать!")
        self.test_button = QPushButton("Пройти тестирование")
        self.test_button.clicked.connect(self.start_test)

        self.theme1_button = QPushButton("Тест по теме Авто")
        self.theme2_button = QPushButton("Тест по теме ИИ")

        self.theme1_button.clicked.connect(lambda: self.start_test("cars"))
        self.theme2_button.clicked.connect(lambda: self.start_test("AI"))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.test_button)
        layout.addWidget(self.theme1_button)
        layout.addWidget(self.theme2_button)

        self.setLayout(layout)

    def start_test(self, theme):
        self.test_window = TestWindow(theme)
        self.test_window.show()
        self.close()
        # self.hide()