from PyQt6 import QtCore, QtGui, QtWidgets

class aboutWindow(QtWidgets.QWidget):

    def __init__(self, mainWindow):
        super().__init__()
        self.w = mainWindow.w
        self.h = mainWindow.h
        if mainWindow.w > 900: self.w = 900
        if mainWindow.h > 500: self.h = 500

        self.setupUi()


    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(893, 520)


        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.lbSettings = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbSettings.sizePolicy().hasHeightForWidth())
        self.lbSettings.setSizePolicy(sizePolicy)
        self.lbSettings.setMinimumSize(QtCore.QSize(0, 90))
        self.lbSettings.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.lbSettings.setFont(font)
        self.lbSettings.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0149254 rgba(152, 152, 152, 255), stop:1 rgba(75, 75, 75, 255));")
        self.lbSettings.setText("О программе")
        self.lbSettings.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbSettings.setObjectName("lbSettings")
        self.gridLayout_2.addWidget(self.lbSettings, 0, 0, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(20, 0, 20, 10)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.label_2 = QtWidgets.QLabel()
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setText("Автор: bds89")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QtWidgets.QLabel()
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText("Описание:")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel()
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setText('Сайт: <a href="https://github.com/bds89/">github.com/bds89</a>')
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)

        self.label = QtWidgets.QLabel()
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setText("Версия программы: 0.3")
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        font = QtGui.QFont()
        font.setPointSize(8)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setPlainText("- Программа получает письма с указанных ящиков, с указанной темой сообщения и рассылает их по списку рассылки.\n"
"\n"
"- Фильтр тем сообщений допускает несколько ошибок (например \"Отчт\" и \"отчет\" - одно и тоже.\n"
"\n"
"- Адреса для списков рассылки, необходимо разделять любым разделителем, кроме символов [0-9A-Za-z-_.@], можно использовать пробелы.\n"
"\n"
"- Вложения можно сохранять в указанную папку, по умолчанию - папка запуска программы.\n"
"\n"
"- Программа проверяет вашу почту подключаясь через IMAP/MS Exchange с заданным интервалом. Если на указанный ящик приходит письмо, подходящее под критерии(адрес, тема сообщения) рассылки - программа его отправит. Если в момент запуска в ящике уже есть письма, подходящие под критерии рассылки - отправка не произойдет. Если вы измените критерии и в ящике уже будут письма подходящие под них, программа отправит их по списку рассылки.\n"
"\n"
"- Для отправки используется SMTP/MS Exchange.\n"
"\n"
"- Можно использовать разные ящики для получения и отправки писем.\n"
"\n"
"- Для подключения к MS Exchange требуется адрес почтового ящика(myuser@example.com), логин(MYWINDOMAIN\\myuser или myuser@example.com), пароль. Программа попытается сама обнаружить точку подключения EWS(EWS endpoint_url) и хранить в кэшэ до закрытия, если вы знаете URL-адрес EWS добавьте его в поле сервер(https://<mail-server>/ews/exchange.asmx).\n")
        self.plainTextEdit.setTabStopDistance(20)
        self.plainTextEdit.setCursorWidth(1)
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 5, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.setLayout(self.gridLayout_2)
        self.setWindowTitle("О программе")
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = aboutWindow()
    sys.exit(app.exec())