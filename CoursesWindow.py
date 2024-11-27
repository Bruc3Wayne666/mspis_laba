import webbrowser

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox, QPushButton, QListView, QLabel, QVBoxLayout, QWidget


class CoursesWindow(QWidget):
    def __init__(self, home_window):
        super().__init__()
        self.home_window = home_window
        self.setWindowTitle("Курсы")
        self.resize(600, 400)

        self.setStyleSheet("""
            background-color: #121212; /* Темный фон */
            color: #ffffff; /* Белый текст */
        """)

        self.layout = QVBoxLayout()

        self.label = QLabel("Список доступных курсов:")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        self.layout.addWidget(self.label)

        self.courses_view = QListView()
        self.model = QStandardItemModel()
        self.courses_view.setModel(self.model)
        self.populate_courses()
        self.layout.addWidget(self.courses_view)

        self.courses_view.clicked.connect(self.open_link)

        self.back_button = QPushButton("Назад")
        self.back_button.setStyleSheet("background-color: #1E1E1E; color: #ffffff;")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def populate_courses(self):
        courses = {
            "Курс по Авто": {
                "Раздел 1: Основы": {
                    "video": "https://youtu.be/EnYL0BQUSU8?si=cB4KT6Gad0jD76YX",
                    "article": "https://zeekr-avto.ru/blog/zeekr-mix-innovacionnyj-elektricheskij-krossven-gotov-k-vyhodu-na-rynok",
                },
                "Раздел 2: Углубленное изучение": {
                    "video": "https://youtu.be/awGckl8pXQw?si=nv1oe5nviYT6jIyC",
                    "article": "https://www.autonews.ru/news/6177c0e89a79470b5d5211b8",
                },
            },
            "Курс по ИИ": {
                "Раздел 1: Основы ИИ": {
                    "video": "https://www.youtube.com/watch?v=tDyDWVqBw5s&t=40s&pp=ygUR0LjQuCDQvtGB0L3QvtCy0Ys%3D",
                    "article": "https://www.cnews.ru/book/%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82_-_%D0%98%D0%98_-_Artificial_intelligence_-_AI_-_Artificial_General_Intelligence_-_AGI",
                },
                "Раздел 2: Модели и алгоритмы": {
                    "video": "https://www.youtube.com/watch?v=9V7RbQ4XQmI&list=PL4_hYwCyhAvYJ1r22vWqp_sDwJMNf64MN",
                    "article": "https://lanbook.com/catalog/informatika/kompyuternaya-grafika-modeli-i-algoritmy/",
                },
            },
        }

        for course, sections in courses.items():
            course_item = QStandardItem(course)
            course_item.setEditable(False)
            self.model.appendRow(course_item)

            for section, links in sections.items():
                section_item = QStandardItem(f"  {section}")
                section_item.setEditable(False)
                self.model.appendRow(section_item)

                video_item = QStandardItem(f"    Видео лекция: {self.shorten_link(links['video'])}")
                video_item.setData({'type': 'video', 'link': links['video']})
                video_item.setEditable(False)
                video_item.setForeground(Qt.cyan)
                self.model.appendRow(video_item)

                article_item = QStandardItem(f"    Статья: {self.shorten_link(links['article'])}")
                article_item.setData({'type': 'article', 'link': links['article']})
                article_item.setEditable(False)
                article_item.setForeground(Qt.yellow)
                self.model.appendRow(article_item)

    def shorten_link(self, url):
        return url.split('/')[-1]

    def open_link(self, index: QModelIndex):
        if not index.isValid():
            return

        link_data = self.model.itemFromIndex(index).data()
        if link_data:
            link_type = link_data['type']
            link = link_data['link']
            if link_type in ['video', 'article']:
                webbrowser.open(link)
        else:
            QMessageBox.warning(self, "Ошибка", "Нет доступной ссылки.")

    def go_back(self):
        self.home_window.show()
        self.close()
