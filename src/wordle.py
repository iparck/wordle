from PyQt5 import QtWidgets
from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
import sys, json, random

class Wordle(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.enter_button.clicked.connect(self.get_guess)
        self.ui.input_box.returnPressed.connect(self.get_guess)

        self.answer = ""
        self.current_row = 0
        self.grid_labels = []
        
        for row in range(6):
            row_labels = []
            for col in range(5):
                label = QLabel("")
                label.setFixedSize(60, 60)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(""" 
                    background-color: white;
                    border: 2px solid #d3d6da;
                    font-size: 28px;
                    font-weight: bold;
                    color: black;
                """)

                self.ui.guesses_layout.addWidget(label, row, col)
                row_labels.append(label)
            self.grid_labels.append(row_labels)
            

        self.change_answer()

    def get_guess(self):
        guess = self.ui.input_box.text().strip().lower()
        if len(guess) == 5:
            self.check_guess(guess)
            self.ui.input_box.clear()
        else:
            self.ui.statusbar.showMessage("Please enter a 5-letter word", 2000)

    def check_guess(self, guess):
        if self.current_row >= 6:
            return

        answer_copy = list(self.answer)
        for i, letter in enumerate(guess):
            color = "black"
            
            if letter == self.answer[i]:
                color = "green"
                answer_copy[i] = None
            elif letter in answer_copy:
                color = "yellow"
                answer_copy[answer_copy.index(letter)] = None

            label = self.grid_labels[self.current_row][i]
            label.setText(letter.upper())
            colors = {
                "green": "#6aaa64",
                "yellow": "#c9b458",
                "black": "#787c7e"
            }
            label.setStyleSheet(f"""
                background-color: {colors[color]};
                border: 2px solid {colors[color]};
                color: white;
                font-size: 28px;
                font-weight: bold;
            """)

        self.current_row += 1

        if guess == self.answer:
            self.ui.statusbar.showMessage(f"You got it! The word was {self.answer.upper()}", 3000)
            QTimer.singleShot(1500, self.reset_game)
        elif self.current_row >= 6:
            self.ui.statusbar.showMessage(f"Game over! The word was {self.answer.upper()}", 3000)
            QTimer.singleShot(1500, self.reset_game)

    def reset_game(self):
        for row in self.grid_labels:
            for label in row:
                label.setText("")
                label.setStyleSheet("""
                    background-color: white;
                    border: 2px solid #d3d6da;
                    font-size: 28px;
                    font-weight: bold;
                    color: black;
                """)
        self.current_row = 0
        self.change_answer()
        self.ui.statusbar.showMessage("New game started!", 2000)

    def change_answer(self):
        with open('words.json', 'r') as file:
            words = json.load(file)
        self.answer = random.choice(words)
        print(f"DEBUG: New answer is {self.answer}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Wordle()
    window.show()
    sys.exit(app.exec_())