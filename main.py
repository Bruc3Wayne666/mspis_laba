from LoginDialog import LoginDialog
from db import cur, conn
from PyQt5.QtWidgets import QApplication
import sys

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

cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    user_id INT,
    score INT,
    theme VARCHAR(50),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

conn.commit()
cur.close()
conn.close()

if __name__ == "__main__":
    app = QApplication([])
    window = LoginDialog()
    window.show()

    sys.exit(app.exec_())
