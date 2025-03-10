# import random
#
# import psycopg2
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QWidget, QLabel, QButtonGroup, QPushButton, QVBoxLayout, QRadioButton, QMessageBox
#
# from QuestionManager import QuestionManager
# from db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
#
#
# class TestWindow(QWidget):
#     def __init__(self, theme, user_id):
#         super().__init__()
#
#         self.theme = theme  # Сохраняем выбранную тему
#
#         self.user_id = user_id
#
#         self.init_ui()
#         self.init_question_manager()
#         self.fetch_all_questions()  # Fetch all questions and shuffle the list
#         self.load_question()
#
#         self.start_timer()
#
#     def init_ui(self):
#         self.setWindowTitle("Test")
#         self.resize(300, 300)
#
#         self.time_left = 600  # 10 minutes in seconds
#
#         self.correct_answers = 0
#         self.incorrect_answers = 0
#         self.total_questions = 10
#         self.score = 0
#
#         self.question_number = 0
#
#         self.question_label = QLabel("")
#         self.answer_buttons = QButtonGroup()
#         self.answer_buttons.buttonClicked.connect(self.check_answer)
#         self.submit_button = QPushButton("Next")
#         self.submit_button.setObjectName("next_button")
#         self.submit_button.clicked.connect(self.next_question)
#         self.question_counter = QLabel(f"Question {self.question_number} / 10")
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.question_label)
#         layout.addWidget(self.question_counter)
#         for i in range(4):
#             button = QRadioButton("")
#             button.setObjectName(f"answer_{i}")
#             self.answer_buttons.addButton(button)
#             layout.addWidget(button)
#         layout.addWidget(self.submit_button)
#
#         self.setLayout(layout)
#
#     def init_question_manager(self):
#         conn = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#
#         self.cur = conn.cursor()
#         self.question_manager = QuestionManager(conn)
#
#     def start_timer(self):
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_time)
#         self.timer.start(1000)  # Update time every second
#
#     # def fetch_all_questions(self):
#     #     self.available_questions = self.question_manager.get_all_questions()
#     #     random.shuffle(self.available_questions)
#     #     print('fetch 1')
#     #     print(self.available_questions)
#
#     def fetch_all_questions(self):
#         self.available_questions = self.question_manager.get_questions_by_theme(self.theme)
#         random.shuffle(self.available_questions)
#
#     def load_question(self):
#         try:
#             aspects = ['integrity', 'completeness', 'ability']
#             difficulty = random.choice([1, 2, 3])
#
#             if not self.available_questions:
#                 # QMessageBox.warning(self, "No more questions", "The test is over.")
#                 self.timer.stop()
#                 self.show_results()
#                 return
#
#             self.question = self.available_questions.pop(0)
#
#             if self.question is None:
#                 raise ValueError("No more questions left")
#
#             self.question_label.setText(self.question.question)
#
#             self.answer = self.question.answer
#
#             options = self.question.options
#
#             options = options.split(', ')
#
#             for i, button in enumerate(self.answer_buttons.buttons()):
#                 button.setText(options[i])
#                 button.setObjectName(f"answer_{i + 1}")
#
#             self.question_number += 1
#             self.question_counter.setText(f"Question {self.question_number} / 10")
#
#         except Exception as e:
#             print(f"An error occurred -> : {e}")
#             self.close()
#
#     def check_answer(self, button):
#         try:
#             selected_answer = int(button.objectName().split("_")[-1]) - 1
#             print(f"Selected answer: {selected_answer}, Correct answer: {self.answer}")
#
#             if selected_answer == self.answer:
#                 self.correct_answers += 1
#                 self.score += self.question.difficulty
#             else:
#                 self.incorrect_answers += 1
#         except Exception as e:
#             print(f"An error occurred: {e}")
#
#     def next_question(self):
#         print("Next question called")
#         if self.question_number < self.total_questions:
#             # self.answer_buttons.buttonClicked.disconnect(self.next_question)
#             self.load_question()
#             self.answer_buttons.buttonClicked.connect(self.check_answer)
#         else:
#             self.timer.stop()
#             self.show_results()
#
#     def update_time(self):
#         self.time_left -= 1
#         if self.time_left == 0:
#             self.timer.stop()
#             self.show_results()
#         else:
#             minutes, seconds = divmod(self.time_left, 60)
#             time_str = f"{minutes:02d}:{seconds:02d}"
#             self.setWindowTitle(f"Test - Time left: {time_str}")
#
#     def show_results(self):
#         message = f"Ваш результат: {self.score} .\nВы ответили на: {self.correct_answers}\n из 10 Неверные: {self.incorrect_answers}\nВремени ушло: {self.time_left} секунд"
#
#         QMessageBox.information(
#             self,
#             "Тест завершён",
#             message,
#         )
#
#         print('before save')
#         self.question_manager.insert_test_results(self.user_id, self.score, self.theme)
#
#         from HomeWindow import HomeWindow
#
#         self.cur.execute("SELECT * FROM users WHERE id=%s;", (self.user_id,))
#         user = self.cur.fetchone()
#
#         self.home_window = HomeWindow(user)
#         self.home_window.show()
#
#         self.close()
#



import random
import psycopg2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QButtonGroup, QPushButton, QVBoxLayout, QRadioButton, QMessageBox
from QuestionManager import QuestionManager
from db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class TestWindow(QWidget):
    def __init__(self, theme, user_id):
        super().__init__()

        self.theme = theme  # Сохраняем выбранную тему
        self.user_id = user_id

        self.init_ui()
        self.init_question_manager()
        self.fetch_all_questions()  # Fetch all questions and shuffle the list
        self.load_question()

        self.start_timer()

    def init_ui(self):
        self.setWindowTitle("Test")
        self.resize(300, 300)

        self.time_left = 600  # 10 minutes in seconds

        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_questions = 10
        self.score = 0

        self.question_number = 0

        self.question_label = QLabel("")
        self.difficulty_label = QLabel("")  # Новый QLabel для отображения уровня сложности
        self.answer_buttons = QButtonGroup()
        self.answer_buttons.buttonClicked.connect(self.check_answer)
        self.submit_button = QPushButton("Next")
        self.submit_button.setObjectName("next_button")
        self.submit_button.clicked.connect(self.next_question)
        self.question_counter = QLabel(f"Question {self.question_number} / 10")

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.difficulty_label)  # Добавляем QLabel для уровня сложности
        layout.addWidget(self.question_counter)
        for i in range(4):
            button = QRadioButton("")
            button.setObjectName(f"answer_{i}")
            self.answer_buttons.addButton(button)
            layout.addWidget(button)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def init_question_manager(self):
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        self.cur = conn.cursor()
        self.question_manager = QuestionManager(conn)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update time every second

    def fetch_all_questions(self):
        self.available_questions = self.question_manager.get_questions_by_theme(self.theme)
        random.shuffle(self.available_questions)

    def load_questions_and_time(self):
        # Загружаем вопросы и устанавливаем общее время на тест
        for question in self.available_questions:
            difficulty = question.difficulty
            if difficulty == 1:
                self.total_time += 60  # 1 минута
            elif difficulty == 2:
                self.total_time += 120  # 2 минуты
            elif difficulty == 3:
                self.total_time += 180  # 3 минуты

        self.time_left = self.total_time  # Устанавливаем оставшееся время на общее время

    def load_question(self):
        try:
            if not self.available_questions:
                self.timer.stop()
                self.show_results()
                return

            self.question = self.available_questions.pop(0)

            if self.question is None:
                raise ValueError("No more questions left")

            self.question_label.setText(self.question.question)
            self.answer = self.question.answer

            options = self.question.options.split(', ')

            for i, button in enumerate(self.answer_buttons.buttons()):
                button.setText(options[i])
                button.setObjectName(f"answer_{i + 1}")

            self.question_number += 1
            self.question_counter.setText(f"Question {self.question_number} / {self.total_questions}")

            # Обновляем уровень сложности
            difficulty = self.question.difficulty
            self.difficulty_label.setText(f"Уровень сложности: {difficulty}")

        except Exception as e:
            print(f"An error occurred -> : {e}")
            self.close()

    def set_time_for_question(self, difficulty):
        # Устанавливаем время в зависимости от сложности
        if difficulty == 1:
            self.time_left = 60  # 1 минута
        elif difficulty == 2:
            self.time_left = 120  # 2 минуты
        elif difficulty == 3:
            self.time_left = 180  # 3 минуты
        else:
            self.time_left = 60

    def check_answer(self, button):
        try:
            selected_answer = int(button.objectName().split("_")[-1]) - 1
            print(f"Selected answer: {selected_answer}, Correct answer: {self.answer}")

            if selected_answer == self.answer:
                self.correct_answers += 1
                self.score += self.question.difficulty
            else:
                self.incorrect_answers += 1
        except Exception as e:
            print(f"An error occurred: {e}")

    def next_question(self):
        print("Next question called")
        if self.question_number < self.total_questions:
            self.load_question()
        else:
            self.timer.stop()
            self.show_results()

    def update_time(self):
        self.time_left -= 1
        if self.time_left == 0:
            self.timer.stop()
            self.show_results()
        else:
            minutes, seconds = divmod(self.time_left, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.setWindowTitle(f"Test - Time left: {time_str}")

    def show_results(self):
        message = f"Ваш результат: {self.score} .\nВы ответили на: {self.correct_answers}\n из 10 Неверные: {self.incorrect_answers}\nВремени ушло: {self.time_left} секунд"

        QMessageBox.information(
            self,
            "Тест завершён",
            message,
        )

        print('before save')
        self.question_manager.insert_test_results(self.user_id, self.score, self.theme)

        from HomeWindow import HomeWindow

        self.cur.execute("SELECT * FROM users WHERE id=%s;", (self.user_id,))
        user = self.cur.fetchone()

        self.home_window = HomeWindow(user)
        self.home_window.show()

        self.close()
