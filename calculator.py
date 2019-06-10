import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui


class Calculator(QtWidgets.QDialog):
    new_input = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("calculator.ui", self)
        self.show()
        self.init_buttons()

    # connect keyboard- and button-input with listener
    def init_buttons(self):
        self.ui.new_input.connect(self.handle_input)
        for button in self.numbers.children():
            button.clicked.connect(self.button_clicked(button.text()))

    def logger(func):
        def logging(*args):
            print('Button pressed: '+args[1])
            func(*args)
        return logging

    @logger
    def handle_input(self, input_text):
        text = self.input.toPlainText()

        if input_text == "REMOVE":
            text = text[:-1]
        elif input_text == "=":
            try:
                text = str(eval(text))
            except SyntaxError:
                text = "Syntax Error"
        elif input_text == "CLEAR":
            text = ""
        else:
            text += input_text

        self.input.setText(text)

    def keyPressEvent(self, event):
        # validate if input is not in alphabet
        if not event.text().isalpha():
            self.ui.new_input.emit(event.text())

    #  inform listener with value of clicked button
    def button_clicked(self, button_text):
        def clicked():
            self.ui.new_input.emit(button_text)
        return clicked


def main():
    app = QtWidgets.QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()