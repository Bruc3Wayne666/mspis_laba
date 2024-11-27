import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from db import DB_HOST, DB_PASSWORD, DB_USER, DB_NAME, cur, DB_PORT


class MindMapWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.home_screen = None
        self.setWindowTitle("Интеллект-карта")
        self.setGeometry(100, 100, 800, 600)

        self.back_button = QPushButton("Назад на главный экран")
        self.back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(self.back_button)

        # Создаем горизонтальный layout для размещения графа и гистограммы
        self.graph_layout = QHBoxLayout()

        # Создаем канвас для графа
        self.graph_canvas = FigureCanvas(plt.Figure())
        self.graph_layout.addWidget(self.graph_canvas)

        # Создаем канвас для гистограммы
        self.histogram_canvas = FigureCanvas(plt.Figure())
        self.graph_layout.addWidget(self.histogram_canvas)

        layout.addLayout(self.graph_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.user_id = user_id

        # Отображаем интеллект-карту и гистограмму на основе user_id
        self.plot_mind_map(user_id)

        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()



    def go_back(self):
        from HomeWindow import HomeWindow

        self.cur.execute("SELECT * FROM users WHERE id=%s;", (self.user_id,))
        user = self.cur.fetchone()

        self.home_screen = HomeWindow(user)
        self.home_screen.show()
        self.close()

    def plot_mind_map(self, user_id):
        with psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}") as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT theme FROM results WHERE user_id = %s", (user_id,))
                themes = cursor.fetchall()

        G = nx.Graph()
        theme_list = [theme[0] for theme in themes]  # Извлекаем темы из кортежей

        for theme in theme_list:
            G.add_node(theme)

        for i in range(len(theme_list)):
            for j in range(i + 1, len(theme_list)):
                G.add_edge(theme_list[i], theme_list[j])  # Создаем связь между всеми узлами

        ax_graph = self.graph_canvas.figure.add_subplot(121)  # 1 строка, 2 колонки, 1-я ячейка
        ax_graph.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=ax_graph)
        ax_graph.set_title("Интеллект-карта")

        theme_counts = [1] * len(theme_list)  # Пример: количество тем
        ax_histogram = self.histogram_canvas.figure.add_subplot(122)  # 1 строка, 2 колонки, 2-я ячейка
        ax_histogram.clear()
        ax_histogram.bar(theme_list, theme_counts)
        ax_histogram.set_title("Гистограмма тем")
        ax_histogram.set_xlabel("Темы")
        ax_histogram.set_ylabel("Количество")

        self.graph_canvas.draw()
        self.histogram_canvas.draw()