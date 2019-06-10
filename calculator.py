import sys
from datetime import datetime
from PyQt5 import uic, QtWidgets, QtCore, QtGui


class Calculator(QtWidgets.QDialog):
    new_input = QtCore.pyqtSignal(str)
    timer_logger = QtCore.pyqtSignal(bool, str, str)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.ui = uic.loadUi("calculator.ui", self)
        self.show()
        self.init_buttons()
        self.timer = QtCore.QTime()
        self.mouse_timer = QtCore.QTime()
        self.moving = False

    # connect keyboard- and button-input with listener
    def init_buttons(self):
        self.ui.new_input.connect(self.handle_input)
        self.ui.timer_logger.connect(self.click_timer)
        for button in self.numbers.children():
            button.pressed.connect(self.button_clicked(button.text()))
            button.released.connect(self.button_released(button.text()))

    def click_timer(self, ev, device, button):
        if ev:
            self.start_measurement()

        else:
            self.stop_measurement()
            self.logger(["Button clicked", device, str(self.stop_measurement()), repr(button).replace("'","")])

    def logger(self, data):
        text = ""
        for items in data:
            text += str(items)+","
        text += str(datetime.now())
        print(text)

    def handle_input(self, input_text):
        text = self.input.toPlainText()

        if input_text == "DEL":
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

    def start_mouse_measurement(self):
        if not self.moving:
            self.mouse_timer.start()
            self.moving = True
            self.logger(["Mouse started moving", "m", 0, ""])

    def stop_mouse_measurement(self, text):
        if self.moving:
            self.logger(["Mouse moved", "m", str(self.mouse_timer.elapsed()), text])
            self.moving = False

    def keyReleaseEvent(self, event):
        self.ui.timer_logger.emit(False, "k", event.text())

    def keyPressEvent(self, event):
        self.ui.timer_logger.emit(True, "k", event.text())
        # validate if input is not in alphabet
        if not event.text().isalpha():
            self.ui.new_input.emit(event.text())

    #  inform listener with value of clicked button
    def button_clicked(self, button_text):
        def clicked():
            self.ui.timer_logger.emit(True, "m", button_text)
            self.ui.new_input.emit(button_text)
            self.stop_mouse_measurement(button_text)
        return clicked

    def button_released(self, button_text):
        def released():
            self.ui.timer_logger.emit(False, "m", button_text)
        return released
    
    def mouseMoveEvent(self, event):
        self.start_mouse_measurement()


def main():
    app = QtWidgets.QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()