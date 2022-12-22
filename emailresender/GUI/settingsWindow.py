from PyQt6 import QtCore, QtGui, QtWidgets
try:
    from .settingsWindowScripts import *
except ImportError:
    from GUI.settingsWindowScripts import * 

class SettingsWindow(QtWidgets.QWidget):
    #try connect methods
    tc = Try_connect()
    #SIGNALS
    start_at_start = QtCore.pyqtSignal(bool)
    minimize_to_tray = QtCore.pyqtSignal(bool)
    save_imap_settings = QtCore.pyqtSignal(list)
    save_smtp_settings = QtCore.pyqtSignal(list)
    save_mse_settings = QtCore.pyqtSignal(list)
    add_to_log = QtCore.pyqtSignal(str)
    refreshInterval = QtCore.pyqtSignal(int)
    typeConnect = QtCore.pyqtSignal(str)

    thread = QtCore.QThread()
    def __init__(self, mainWindow):
        super().__init__()
        self.w = mainWindow.w
        self.h = mainWindow.h
        if mainWindow.w > 900: self.w = 900
        if mainWindow.h > 500: self.h = 500

        self.setupUi(mainWindow)
        #check connections (try connect)
        # self.thread = QtCore.QThread()
        self.tc.moveToThread(self.thread)
        self.thread.started.connect(lambda : self.tc.imap_and_smtp_connect(self))
        self.thread.start()


    def setupUi(self, mainWindow):
        self.setObjectName("Settings")
        self.setWindowTitle("Настройки")
        self.resize(self.w, self.h)
        self.setStyleSheet("background-color: rgb(200, 200, 200);")

        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.lbSettings = QtWidgets.QLabel()
        self.lbSettings.setText("Настройки")
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
        self.lbSettings.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbSettings.setObjectName("lbSettings")
        self.gridLayout_2.addWidget(self.lbSettings, 0, 0, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(20, 0, 20, 10)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        #Общие
        self.label = QtWidgets.QLabel()
        self.label.setText("Общие")
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        #Start at startup
        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setText("Старт при запуске приложения")
        self.checkBox.setMinimumSize(QtCore.QSize(0, 40))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(lambda: start_at_startfunc(self))
        if mainWindow.config["startAtStart"]: self.checkBox.setChecked(True)
        else: self.checkBox.setChecked(False)
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox()
        self.checkBox_2.setText("Сворачивать в трей")
        self.checkBox_2.setMinimumSize(QtCore.QSize(0, 40))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(lambda: minimize_to_trayfunc(self))
        if mainWindow.config["minimizeToTray"]: self.checkBox_2.setChecked(True)
        else: self.checkBox_2.setChecked(False)
        self.gridLayout.addWidget(self.checkBox_2, 2, 0, 1, 1)

        #type of connection
        self.lbType = QtWidgets.QLabel()
        self.lbType.setText("Тип подключения:")
        self.lbType.setObjectName("lbType")
        self.lbType.setMinimumSize(QtCore.QSize(0, 20))
        self.gridLayout.addWidget(self.lbType, 3, 0, 1, 1)

        self.cbTypeConnect = QtWidgets.QComboBox()
        self.cbTypeConnect.setObjectName("cbTypeConnect")
        self.cbTypeConnect.addItem("IMAP/SMTP")
        self.cbTypeConnect.addItem("MS Exchange")
        self.cbTypeConnect.setCurrentText(mainWindow.config["connectType"])
        self.cbTypeConnect.currentTextChanged.connect(lambda type:chooseTypeConnect(self, type))
        self.gridLayout.addWidget(self.cbTypeConnect, 4, 0, 1, 1)

        #Search interval
        self.label_8 = QtWidgets.QLabel()
        self.label_8.setText("Интервал проверки писем (мин):")
        self.label_8.setMinimumSize(QtCore.QSize(0, 20))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimumSize(QtCore.QSize(100, 20))
        self.spinBox.setMaximumSize(QtCore.QSize(100, 30))
        self.spinBox.setValue(mainWindow.config["refreshInterval"])
        self.spinBox.valueChanged.connect(lambda value, :self.refreshInterval.emit(value))
        self.gridLayout.addWidget(self.spinBox, 6, 0, 1, 1)

        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 10, 1)

        #MAIL
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setDocumentMode(True)
        
        #IMAP
        self.imapTab = QtWidgets.QWidget()
        self.imapTab.setObjectName("imapTab")
            

        self.gridImapTab = QtWidgets.QGridLayout(self.imapTab)
        self.gridImapTab.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridImapTab.setHorizontalSpacing(20)
        self.gridImapTab.setVerticalSpacing(0)
        self.gridImapTab.setObjectName("gridImapTab")
        
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setText("Сервер входящей почты IMAP:")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.gridImapTab.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setStyleSheet("background-color: rgba(255, 85, 0, 180);")
        self.lineEdit.setInputMask("")
        self.lineEdit.setPlaceholderText("imap.example.ru")
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 20))
        try: self.lineEdit.setText(mainWindow.config["imap"][0])
        except IndexError: self.lineEdit.setText("")
        self.lineEdit.setFrame(False)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textEdited.connect(lambda: imap_change(self))
        imap_change
        self.gridImapTab.addWidget(self.lineEdit, 0, 1, 1, 2)

        self.lineEdit_port = QtWidgets.QLineEdit()
        self.lineEdit_port.setStyleSheet("background-color: rgba(255, 85, 0, 180);")
        self.lineEdit_port.setInputMask("")
        self.lineEdit_port.setMinimumSize(QtCore.QSize(0, 20))
        try: self.lineEdit_port.setText(mainWindow.config["imap"][1])
        except IndexError: self.lineEdit_port.setText("993")
        self.lineEdit_port.setFrame(False)
        self.lineEdit_port.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_port.setObjectName("lineEdit")
        self.lineEdit_port.setMaximumWidth(50)
        reg_ex = QtCore.QRegularExpression("[0-9]+")
        input_validator = QtGui.QRegularExpressionValidator(reg_ex, self.lineEdit_port)
        self.lineEdit_port.setValidator(input_validator)
        self.lineEdit_port.textEdited.connect(lambda: imap_change(self))
        self.gridImapTab.addWidget(self.lineEdit_port, 0, 3, 1, 1)

        self.label_4 = QtWidgets.QLabel()
        self.label_4.setToolTip("")
        self.label_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setText("Логин:")
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridImapTab.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setStyleSheet("background-color: rgba(255, 85, 0, 180);")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setPlaceholderText("user@example.ru")
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 20))
        try: self.lineEdit_2.setText(mainWindow.config["imap"][2])
        except IndexError: self.lineEdit_2.setText("")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.textEdited.connect(lambda: imap_change(self))
        self.gridImapTab.addWidget(self.lineEdit_2, 1, 1, 1, 2)

        self.label_5 = QtWidgets.QLabel()
        self.label_5.setText("Пароль:")
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridImapTab.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_3 = QtWidgets.QLineEdit()
        self.lineEdit_3.setStyleSheet("background-color: rgba(255, 85, 0, 180);")
        try: self.lineEdit_3.setText(mainWindow.config["imap"][3])
        except IndexError: self.lineEdit_3.setText("")
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.textEdited.connect(lambda: imap_change(self))
        self.gridImapTab.addWidget(self.lineEdit_3, 2, 1, 1, 2)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setText("Подключиться")
        self.pushButton.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda :self.tc.imap_connect(self))
        self.gridImapTab.addWidget(self.pushButton, 2, 3, 1, 2)


        #SMTP
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridImapTab.addWidget(self.line_2, 5, 0, 1, 5)

        self.label_6 = QtWidgets.QLabel()
        self.label_6.setText("Сервер исходящей почты SMTP:")
        self.label_6.setMinimumSize(QtCore.QSize(0, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridImapTab.addWidget(self.label_6, 6, 0, 1, 1)

        self.lineEdit_5 = QtWidgets.QLineEdit()
        self.lineEdit_5.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.lineEdit_5.setInputMask("")
        self.lineEdit_5.setPlaceholderText("smtp.example.ru")
        try: self.lineEdit_5.setText(mainWindow.config["smtp"][0])
        except IndexError: self.lineEdit_5.setText("")
        self.lineEdit_5.setFrame(False)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.textEdited.connect(lambda: smtp_change(self))
        self.gridImapTab.addWidget(self.lineEdit_5, 6, 1, 1, 2)

        self.lineEdit_5port = QtWidgets.QLineEdit()
        self.lineEdit_5port.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.lineEdit_5port.setInputMask("")
        self.lineEdit_5port.setMinimumSize(QtCore.QSize(0, 20))
        try: self.lineEdit_5port.setText(mainWindow.config["smtp"][1])
        except IndexError: self.lineEdit_5port.setText("465")
        self.lineEdit_5port.setFrame(False)
        self.lineEdit_5port.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_5port.setObjectName("lineEdit_5")
        self.lineEdit_5port.setMaximumWidth(50)
        reg_ex = QtCore.QRegularExpression("[0-9]+")
        input_validator = QtGui.QRegularExpressionValidator(reg_ex, self.lineEdit_port)
        self.lineEdit_5port.setValidator(input_validator)
        self.lineEdit_5port.textEdited.connect(lambda: smtp_change(self))
        self.gridImapTab.addWidget(self.lineEdit_5port, 6, 3, 1, 1)

        self.label_7 = QtWidgets.QLabel()
        self.label_7.setText("Логин:")
        self.label_7.setMinimumSize(QtCore.QSize(0, 20))
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridImapTab.addWidget(self.label_7, 7, 0, 1, 1)

        self.lineEdit_4 = QtWidgets.QLineEdit()
        self.lineEdit_4.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.lineEdit_4.setInputMask("")
        self.lineEdit_4.setPlaceholderText("user@example.ru")
        try: self.lineEdit_4.setText(mainWindow.config["smtp"][2])
        except IndexError: self.lineEdit_4.setText("")
        self.lineEdit_4.setFrame(False)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.textEdited.connect(lambda: smtp_change(self))
        self.gridImapTab.addWidget(self.lineEdit_4, 7, 1, 1, 2)

        self.label_9 = QtWidgets.QLabel()
        self.label_9.setText("Пароль:")
        self.label_9.setMinimumSize(QtCore.QSize(0, 20))
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridImapTab.addWidget(self.label_9, 8, 0, 1, 1)

        self.lineEdit_6 = QtWidgets.QLineEdit()
        self.lineEdit_6.setStyleSheet("background-color: rgb(85, 170, 127);")
        try: self.lineEdit_6.setText(mainWindow.config["smtp"][3])
        except IndexError: self.lineEdit_6.setText("")
        self.lineEdit_6.setFrame(False)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.textEdited.connect(lambda: smtp_change(self))
        self.gridImapTab.addWidget(self.lineEdit_6, 8, 1, 1, 2)


        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setText("Подключиться")
        self.pushButton_2.setStyleSheet("background-color: rgb(95, 191, 142);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda :self.tc.smtp_connect(self))
        self.gridImapTab.addWidget(self.pushButton_2, 8, 3, 1, 2)


        #connect imap tab to tab
        self.tabWidget.addTab(self.imapTab, "IMAP/SMTP")



        #MS EXCHANGE
        self.MSTab = QtWidgets.QWidget()
        self.MSTab.setObjectName("MSTab")
        self.tabWidget.addTab(self.MSTab, "MS Exchange")
        if self.cbTypeConnect.currentText() != "MS Exchange": 
            self.MSTab.setEnabled(False)
        else:
            self.imapTab.setEnabled(False)
            self.tabWidget.setCurrentIndex(1)

        self.gridMSTab = QtWidgets.QGridLayout(self.MSTab)
        self.gridMSTab.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridMSTab.setHorizontalSpacing(20)
        self.gridMSTab.setVerticalSpacing(20)
        self.gridMSTab.setObjectName("gridMSTab")
       
        self.lbMSAddr = QtWidgets.QLabel()
        self.lbMSAddr.setText("Адрес ящика:")
        self.lbMSAddr.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbMSAddr.setObjectName("label_3")
        self.lbMSAddr.setMinimumSize(QtCore.QSize(0, 20))
        self.gridMSTab.addWidget(self.lbMSAddr, 0, 0, 1, 1)

        self.leAddr = QtWidgets.QLineEdit()
        self.leAddr.setStyleSheet("background-color: rgb(95, 191, 142);")
        self.leAddr.setInputMask("")
        self.leAddr.setPlaceholderText("user@example.ru")
        self.leAddr.setMinimumSize(QtCore.QSize(0, 20))
        try: self.leAddr.setText(mainWindow.config["mse"][0])
        except IndexError: self.leAddr.setText("")
        self.leAddr.setFrame(False)
        self.leAddr.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.leAddr.setObjectName("leAddr")
        self.leAddr.textEdited.connect(lambda: mse_change(self))
        self.gridMSTab.addWidget(self.leAddr, 0, 1, 1, 2)

        self.lbLogin = QtWidgets.QLabel()
        self.lbLogin.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.lbLogin.setAutoFillBackground(False)
        self.lbLogin.setText("Логин:")
        self.lbLogin.setMinimumSize(QtCore.QSize(0, 20))
        self.lbLogin.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.lbLogin.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbLogin.setObjectName("lbLogin")
        self.gridMSTab.addWidget(self.lbLogin, 1, 0, 1, 1)

        self.leLogin = QtWidgets.QLineEdit()
        self.leLogin.setStyleSheet("background-color: rgb(95, 191, 142);")
        self.leLogin.setMinimumSize(QtCore.QSize(0, 20))
        self.leLogin.setPlaceholderText("user@example.ru или DOMAIN/User")
        try: self.leLogin.setText(mainWindow.config["mse"][1])
        except IndexError: self.leLogin.setText("")
        self.leLogin.setFrame(False)
        self.leLogin.setObjectName("leLogin")
        self.leLogin.textEdited.connect(lambda: mse_change(self))
        self.gridMSTab.addWidget(self.leLogin, 1, 1, 1, 2)

        self.lbPass = QtWidgets.QLabel()
        self.lbPass.setText("Пароль:")
        self.lbPass.setMinimumSize(QtCore.QSize(0, 20))
        self.lbPass.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbPass.setObjectName("lbPass")
        self.gridMSTab.addWidget(self.lbPass, 2, 0, 1, 1)

        self.lePass = QtWidgets.QLineEdit()
        self.lePass.setStyleSheet("background-color: rgb(95, 191, 142);")
        try: self.lePass.setText(mainWindow.config["mse"][2])
        except IndexError: self.lePass.setText("")
        self.lePass.setFrame(False)
        self.lePass.setMinimumSize(QtCore.QSize(0, 20))
        self.lePass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lePass.setObjectName("lePass")
        self.lePass.textEdited.connect(lambda: mse_change(self))
        self.gridMSTab.addWidget(self.lePass, 2, 1, 1, 2)

        self.lbServer = QtWidgets.QLabel()
        self.lbServer.setText("Сервер:")
        self.lbServer.setMinimumSize(QtCore.QSize(0, 20))
        self.lbServer.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbServer.setObjectName("lbServer")
        self.gridMSTab.addWidget(self.lbServer, 3, 0, 1, 1)

        self.leServer = QtWidgets.QLineEdit()
        self.leServer.setStyleSheet("background-color: rgb(95, 191, 142);")
        self.leServer.setPlaceholderText("https://computer.domain.contoso.com/EWS/Exchange.asmx")
        try: self.leServer.setText(mainWindow.config["mse"][3])
        except IndexError: self.leServer.setText("")
        self.leServer.setFrame(False)
        self.leServer.setMinimumSize(QtCore.QSize(0, 20))
        self.leServer.setObjectName("leServer")
        self.leServer.setToolTip("<html><head/><body><p><span style=\" color:#000000;\">Адрес EWS endpoint. Если оставить пустым программа попытается сама обнаружить, по адресу ящика</span></p></body></html>")
        self.lePass.textEdited.connect(lambda: mse_change(self))
        self.gridMSTab.addWidget(self.leServer, 3, 1, 1, 3)

        self.pbMSConnect = QtWidgets.QPushButton()
        self.pbMSConnect.setText("Подключиться")
        self.pbMSConnect.setStyleSheet("background-color: rgb(95, 191, 142);")
        self.pbMSConnect.setObjectName("pbMSConnect")
        self.pbMSConnect.clicked.connect(lambda :self.tc.mse_connect(self))
        self.gridMSTab.addWidget(self.pbMSConnect, 4, 2, 1, 2)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridMSTab.addItem(spacerItem, 5, 0, 1, 1)

        #connect tab to grid
        self.gridLayout.addWidget(self.tabWidget, 0, 2, 10, 4)

        #connect grid to maingrid2
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.setLayout(self.gridLayout_2)

        self.resize(self.w, self.h)

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SettingsWindow()
    sys.exit(app.exec_())