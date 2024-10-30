import random

import psycopg2
from PyQt5.QtCore import QTimer, QObject

# PORT = 5000
# DB_NAME = 'mspis'
# DB_USER = 'postgres'
# DB_PASSWORD = 'password'
# DB_HOST = 'localhost'
# DB_PORT = 5432
# SECRET = 'secret_word'
#
# # Установите соединение с базой данных
# conn = psycopg2.connect(
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )
#
# cur = conn.cursor()

# Создайте таблицы
from LoginDialog import LoginDialog
from db import cur, conn

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(100) NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
  id SERIAL PRIMARY KEY,
  aspect VARCHAR(20) NOT NULL CHECK (aspect IN ('integrity', 'completeness', 'ability')),
  difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 3),
  question TEXT NOT NULL,
  answer CHAR(1) NOT NULL CHECK (answer IN ('A', 'B', 'C', 'D')),
  options TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS test_results (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  test_time INTEGER NOT NULL,
  score INTEGER NOT NULL
);
""")

# Сохраните изменения и закройте соединение
conn.commit()
cur.close()
conn.close()

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication, QWidget, \
    QRadioButton, QButtonGroup
import hashlib
import psycopg2
import sys
from QuestionManager import QuestionManager


# class Question:
#     def __init__(self, question, answer, options, difficulty):
#         self.question = question
#         self.answer = answer
#         self.options = options
#         self.difficulty = difficulty
#
#
# class QuestionManager(QObject):
#     def __init__(self, conn):
#         super().__init__()
#         self.conn = conn
#         self.cur = conn.cursor()
#
#     def get_question_count(self, aspects, difficulty):
#         difficulty = str(difficulty)
#         aspect = random.choice(aspects)
#
#         self.cur.execute(
#             "SELECT COUNT(*) FROM questions WHERE aspect=%s AND difficulty=%s",
#             (aspect, difficulty),
#         )
#         return self.cur.fetchone()[0]
#
#     def get_all_questions(self):
#         self.cur.execute("SELECT * FROM questions ORDER BY RANDOM()")
#         c = self.cur.fetchall()
#         # print(c)
#         # # print([row for row in c])
#         # for row in c:
#         #     print(*row, sep='|')
#         # return [Question(*row) for row in self.cur.fetchall()]
#         # print([row[3] for row in c])
#         return [Question(row[3], row[5], row[4], row[2]) for row in c]
#
#     def insert_test_results(self, username, test_time, score):
#         self.cur.execute(
#             "INSERT INTO test_results (username, test_time, score) VALUES (%s, %s, %s)",
#             (username, test_time, score),
#         )
#         self.conn.commit()
#
#     # def get_random_question(self, aspects, difficulty):
#     #     difficulty = str(difficulty)
#     #     aspect = random.choice(aspects)
#     #
#     #     self.cur.execute(
#     #         "SELECT question, answer, options FROM questions WHERE aspect=%s AND difficulty=%s ORDER BY RANDOM() LIMIT 1",
#     #         (aspect, difficulty),
#     #     )
#     #     question, answer, options = self.cur.fetchone()
#     #     # return Question(question, answer, options.split('|'))
#     #     return Question(question, answer, options.split(','))
#
#     def get_random_question(self, aspects, difficulty):
#         difficulty = str(difficulty)
#         aspect = random.choice(aspects)
#
#         self.cur.execute(
#             "SELECT question, answer, options FROM questions WHERE aspect=%s AND difficulty=%s ORDER BY RANDOM() LIMIT 1",
#             (aspect, difficulty),
#         )
#         result = self.cur.fetchone()
#
#         if result is None:
#             return None
#
#         question, answer, options = result
#         return Question(question, int(answer) - 1, options.split(','))
#
#
# class TestWindow(QWidget):
#     def __init__(self):
#         super().__init__()
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
#         self.question_manager = QuestionManager(conn)
#
#     def start_timer(self):
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_time)
#         self.timer.start(1000)  # Update time every second
#
#     def fetch_all_questions(self):
#         self.available_questions = self.question_manager.get_all_questions()
#         random.shuffle(self.available_questions)
#         print('fetch 1')
#         print(self.available_questions)
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
#         # Insert test results into the database
#         self.question_manager.insert_test_results(self.username, self.time_left, self.correct_answers)
#
#         # Return to the home screen
#         # self.close()
#         # self.home_window = HomeWindow()
#         self.home_window.show(username=self.username)
#
#
# class HomeWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.test_window = TestWindow()
#         self.setWindowTitle("Home")
#         self.resize(300, 200)
#
#         self.label = QLabel("Добро пожаловать!")
#         self.test_button = QPushButton("Пройти тестирование")
#         self.test_button.clicked.connect(self.start_test)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.test_button)
#
#         self.setLayout(layout)
#
#     def start_test(self):
#         self.test_window.show()
#         self.close()
#         # self.hide()
#
#
# class LoginDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#
#         self.home_window = HomeWindow()
#
#         self.setWindowTitle("Вход/Регистрация")
#
#         self.username_label = QLabel("Имя пользователя:")
#         self.username_input = QLineEdit()
#
#         self.password_label = QLabel("Пароль:")
#         self.password_input = QLineEdit()
#         self.password_input.setEchoMode(QLineEdit.Password)
#
#         self.login_button = QPushButton("Войти")
#         self.login_button.clicked.connect(self.login)
#
#         self.register_button = QPushButton("Зарегистрироваться")
#         self.register_button.clicked.connect(self.register)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.username_label)
#         layout.addWidget(self.username_input)
#         layout.addWidget(self.password_label)
#         layout.addWidget(self.password_input)
#         layout.addWidget(self.login_button)
#         layout.addWidget(self.register_button)
#
#         self.setLayout(layout)
#
#         self.conn = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         self.cur = self.conn.cursor()
#
#     def login(self):
#         username = self.username_input.text()
#         password = hashlib.sha256(self.password_input.text().encode()).hexdigest()
#
#         self.cur.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
#         user = self.cur.fetchone()
#
#         if user:
#             QMessageBox.information(self, "Успех", "Вы успешно вошли в систему.")
#             self.home_window.show()
#             self.close()
#         else:
#             QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")
#
#     def register(self):
#         username = self.username_input.text()
#         password = hashlib.sha256(self.password_input.text().encode()).hexdigest()
#
#         self.cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
#         self.conn.commit()
#
#         QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались.")
#
#         self.home_window.show()
#         self.close()
#
#     def closeEvent(self, event):
#         self.cur.close()
#         self.conn.close()
#
#
# class TestWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Test")
#         self.resize(300, 200)
#
#         self.score = 0
#         self.time_left = 600  # 10 minutes in seconds
#
#         self.question_label = QLabel("")
#         self.answer_input = QLineEdit()
#         self.submit_button = QPushButton("Submit")
#         self.submit_button.clicked.connect(self.check_answer)
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_time)
#         self.timer.start(1000)  # Update time every second
#
#         self.connect_to_db()
#
#         self.load_question()
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.question_label)
#         layout.addWidget(self.answer_input)
#         layout.addWidget(self.submit_button)
#
#         self.setLayout(layout)
#
#     def connect_to_db(self):
#         self.conn = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         self.cur = self.conn.cursor()
#
#     def load_question(self):
#         aspects = ['integrity', 'completeness', 'ability']
#         difficulty = random.choice([1, 2, 3])
#         aspect = random.choice(aspects)
#
#         difficulty = str(difficulty)
#         aspect = str(aspect)
#
#         self.cur.execute(
#             "SELECT question, answer FROM questions WHERE aspect=%s AND difficulty=%s ORDER BY RANDOM() LIMIT 1",
#             (aspect, difficulty),
#         )
#         question, answer = self.cur.fetchone()
#
#         self.question_label.setText(question)
#         self.answer = answer
#
#     def check_answer(self):
#         user_answer = self.answer_input.text().strip().lower()
#
#         if user_answer == self.answer.lower():
#             self.score += 1
#             QMessageBox.information(self, "Correct!", "You got it right!")
#         else:
#             QMessageBox.warning(self, "Incorrect", f"Wrong answer! The correct answer is: {self.answer}")
#
#         self.answer_input.clear()
#         self.load_question()
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
#         QMessageBox.information(
#             self,
#             "Test Completed",
#             f"Your score: {self.score}\nTotal questions: {self.score}",
#         )
#         self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = LoginDialog()
    window.show()

    sys.exit(app.exec_())
