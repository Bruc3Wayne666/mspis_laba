import random

from PyQt5.QtCore import QObject

from Question import Question


class QuestionManager(QObject):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.cur = conn.cursor()

    def get_question_count(self, aspects, difficulty):
        difficulty = str(difficulty)
        aspect = random.choice(aspects)

        self.cur.execute(
            "SELECT COUNT(*) FROM questions WHERE aspect=%s AND difficulty=%s",
            (aspect, difficulty),
        )
        return self.cur.fetchone()[0]

    def get_all_questions(self):
        self.cur.execute("SELECT * FROM questions ORDER BY RANDOM()")
        c = self.cur.fetchall()
        # print(c)
        # # print([row for row in c])
        # for row in c:
        #     print(*row, sep='|')
        # return [Question(*row) for row in self.cur.fetchall()]
        # print([row[3] for row in c])
        return [Question(row[3], row[5], row[4], row[2]) for row in c]

    def insert_test_results(self, username, test_time, score):
        self.cur.execute(
            "INSERT INTO test_results (username, test_time, score) VALUES (%s, %s, %s)",
            (username, test_time, score),
        )
        self.conn.commit()

    # def get_random_question(self, aspects, difficulty):
    #     difficulty = str(difficulty)
    #     aspect = random.choice(aspects)
    #
    #     self.cur.execute(
    #         "SELECT question, answer, options FROM questions WHERE aspect=%s AND difficulty=%s ORDER BY RANDOM() LIMIT 1",
    #         (aspect, difficulty),
    #     )
    #     question, answer, options = self.cur.fetchone()
    #     # return Question(question, answer, options.split('|'))
    #     return Question(question, answer, options.split(','))

    def get_random_question(self, aspects, difficulty):
        difficulty = str(difficulty)
        aspect = random.choice(aspects)

        self.cur.execute(
            "SELECT question, answer, options FROM questions WHERE aspect=%s AND difficulty=%s ORDER BY RANDOM() LIMIT 1",
            (aspect, difficulty),
        )
        result = self.cur.fetchone()

        if result is None:
            return None

        question, answer, options = result
        return Question(question, int(answer) - 1, options.split(','))

    def get_questions_by_theme(self, theme):
        self.cur.execute(
            "SELECT * FROM questions WHERE theme=%s ORDER BY RANDOM()",
            (theme,)
        )
        return [Question(row[3], row[5], row[4], row[2]) for row in self.cur.fetchall()]
