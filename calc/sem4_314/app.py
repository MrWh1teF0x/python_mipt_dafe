from PyQt6 import QtWidgets
import sys


class FirstApp(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hello World")

        self.button = QtWidgets.QPushButton("Send")

        self.label = QtWidgets.QLabel("fcsDfsf")
        self.lineEdit = QtWidgets.QLineEdit()

        self.my_layout = QtWidgets.QVBoxLayout()
        self.my_layout.addWidget(self.lineEdit)
        self.my_layout.addWidget(self.label)
        self.my_layout.addWidget(self.button)

        self.button.clicked.connect(self.button_func)

        self.wid = QtWidgets.QWidget()
        self.wid.setLayout(self.my_layout)
        self.setCentralWidget(self.wid)

    def button_func(self) -> None:
        text = self.lineEdit.text()
        self.label.setText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FirstApp()
    window.show()

    app.exec()
