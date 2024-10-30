from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from TestWindow import TestWindow


class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.test_window = TestWindow()
        self.setWindowTitle("Home")
        self.resize(300, 200)

        self.label = QLabel("Добро пожаловать!")
        self.test_button = QPushButton("Пройти тестирование")
        self.test_button.clicked.connect(self.start_test)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.test_button)

        self.setLayout(layout)

    def start_test(self):
        self.test_window.show()
        self.close()
        # self.hide()