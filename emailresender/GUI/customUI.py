from PyQt6 import QtWidgets, QtGui, QtCore

class MyButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent)

        self.effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect.setOffset(3, 3)
        self.effect.setBlurRadius(50)
        self.effect.setColor(QtGui.QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)

    def change_color(self, enter):
        if enter: 
            c1 = QtGui.QColor(0, 0, 0, 100)
            c2 = QtGui.QColor(31, 113, 255, 255)
        else:
            c1 = QtGui.QColor(31, 113, 255, 255)
            c2 = QtGui.QColor(0, 0, 0, 100)
        def updateColor(color):
            self.effect.setColor(QtGui.QColor(color))

        anim = QtCore.QVariantAnimation(self)
        anim.setDuration(500)
        anim.setStartValue(c1)
        anim.setEndValue(c2)
        anim.valueChanged.connect(lambda color: updateColor(color))
        anim.start()

    def enterEvent(self, QEvent):
        self.change_color(True)
        pass


    def leaveEvent(self, QEvent):
        self.change_color(False)
        pass