import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui


class Calculator(QtWidgets.QDialog):
    new_input = QtCore.pyqtSignal(str)
    timer_logger = QtCore.pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("calculator.ui", self)
        self.show()
        self.init_buttons()
        self.timer = QtCore.QTime()

    # connect keyboard- and button-input with listener
    def init_buttons(self):
        self.ui.new_input.connect(self.handle_input)
        self.ui.timer_logger.connect(self.logging_timer)
        for button in self.numbers.children():
            button.pressed.connect(self.button_clicked(button.text()))
            button.released.connect(self.button_released(button.text()))

    def logging_timer(self, ev, button):
        if ev:
            self.start_measurement()
            print('Button pressed,'+button)

        else:
            self.stop_measurement()
            print('Button released,'+button+","+ str(self.stop_measurement()))

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

    def start_measurement(self):
        self.timer.start()

    def stop_measurement(self):
        return self.timer.elapsed()

    def keyReleaseEvent(self, event):
        self.ui.timer_logger.emit(False, event.text())

    def keyPressEvent(self, event):
        self.ui.timer_logger.emit(True, event.text())
        # validate if input is not in alphabet
        if not event.text().isalpha():
            self.ui.new_input.emit(event.text())

    #  inform listener with value of clicked button
    def button_clicked(self, button_text):
        def clicked():
            self.ui.timer_logger.emit(True, button_text)
            self.ui.new_input.emit(button_text)
        return clicked

    def button_released(self, button_text):
        def released():
            self.ui.timer_logger.emit(False, button_text)
        return released

def main():
    app = QtWidgets.QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()