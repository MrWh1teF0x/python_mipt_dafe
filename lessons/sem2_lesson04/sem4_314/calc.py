from PyQt6 import QtWidgets
from calc_ui import Ui_Form


class Window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.cur = 0
        self.next = 0

        self.numbers = [
            self.ui.pushButton_0,
            self.ui.pushButton_1,
            self.ui.pushButton_2,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
            self.ui.pushButton_5,
            self.ui.pushButton_6,
            self.ui.pushButton_7,
            self.ui.pushButton_8,
            self.ui.pushButton_9,
        ]

        for i in range(10):
            self.connect_button(self.numbers[i], i)

        self.ui.pushButton_plus.connect.clicked(self.summ)

    def summ(self):
        self.cur = self.next
        self.next = 0

        text = self.ui.lineEdit.displayText()
        if text[-1] not in self.ops:
            text += "+"
            self.ui.lineEdit.setText(text)

    def connect_button(self, button, number):
        button.clicked.connect(lambda: self.change_number(number))

    def change_number(self, number):
        text = self.ui.lineEdit.displayText()

        last_num = self.next

        self.next *= 10
        self.next += number

        new_text = text + str(self.next)[-1]

        if self.next != last_num:
            if text == 0:
                self.ui.lineEdit.setText(str(self.next)[-1])
            else:
                self.ui.lineEdit.setText(new_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()

    app.exec()
