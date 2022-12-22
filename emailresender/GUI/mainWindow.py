from PyQt6 import QtCore, QtGui, QtWidgets
try:
    from .mainWindowScripts import *
    from .styles import *
    from .settingsWindow import SettingsWindow
    from .aboutWindow import aboutWindow
    from .customUI import MyButton
    from ..mail.mail import MailResender
    from ..mail.exchange import MailResenderMSE
    from ..services.res_patch import resource_path
except ImportError:
    from GUI.mainWindowScripts import *
    from GUI.styles import *
    from GUI.settingsWindow import SettingsWindow
    from GUI.aboutWindow import aboutWindow
    from GUI.customUI import MyButton
    from mail.mail import MailResender
    from mail.exchange import MailResenderMSE
    from services.res_patch import resource_path


class MainWindow(QtWidgets.QMainWindow):

    mailthread = QtCore.QThread()
    def __init__(self, config, work_dir, work_dir_for_res):
        super().__init__()
        self.w = 1000
        self.h = 700
        self.r = 0
        self.config = config
        self.work_dir = work_dir
        self.work_dir_for_res = work_dir_for_res

        #will storage some data
        self.log_lines = 0
        self.log_text = ""
        self.counters = {}
        for addr in config["inputAdrs"]:
            self.counters[addr] = 0


        self.mail()
        #Create mainWindow
        self.setupUi()
        self.showMainWindow()


        #start at startup
        if self.config["startAtStart"]:
            self.pbStart.click()
        
        #MINIMIZE TO TRAY
        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon(resource_path('res/icon_passive.png', self.work_dir_for_res)))
        show_action = QtGui.QAction("Развернуть", self)
        quit_action = QtGui.QAction("Выход", self)
        hide_action = QtGui.QAction("Свернуть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.trayIcon.setContextMenu(tray_menu)
        self.trayIcon.show()
    def closeEvent(self, event):
        if self.config["minimizeToTray"]:
            event.ignore()
            self.hide()
            self.trayIcon.showMessage(
                "Email Resender",
                "Приложение еще работает",
                QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                1000
            )
    def mail(self):
        #mail class
        if self.config["connectType"] == "IMAP/SMTP":
            self.mail_resender = MailResender()
        if self.config["connectType"] == "MS Exchange":
            self.mail_resender = MailResenderMSE()
        #connect signals from mail class
        self.mail_resender.add_to_log.connect(lambda signal: add_to_log(self, signal))
        self.mail_resender.status_signal.connect(lambda signal: status_change(self, signal))
        self.mail_resender.new_mail.connect(lambda signal: new_mail(self, signal))

        #prepare thread
        # self.mailthread = QtCore.QThread()
        self.mail_resender.moveToThread(self.mailthread)
        self.mailthread.started.connect(self.mail_resender.start_work)


        #send config to mail
        self.mail_resender.update_config(self.config)

        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(self.w, self.h)
        rp = resource_path("res/bg.png", self.work_dir_for_res)
        self.setStyleSheet("MainWindow{background-image: url("+rp+");\
                        background-position: right bottom;\
                        background-repeat: no-repeat;}")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(Styles.mainBG)
        


        self.grid = QtWidgets.QGridLayout()
        self.grid.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setSpacing(10)
        self.grid.setObjectName("grid")
        self.centralwidget.setLayout(self.grid)

        #ROW 0
        self.pbAddDtr = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbAddDtr.sizePolicy().hasHeightForWidth())
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_DialogOkButton")
        self.pbAddDtr.setIcon(self.style().standardIcon(pixmapi))
        self.pbAddDtr.setSizePolicy(sizePolicy)
        self.pbAddDtr.setMinimumSize(QtCore.QSize(0, 30))
        self.pbAddDtr.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pbAddDtr.setFont(font)
        self.pbAddDtr.setAutoFillBackground(False)
        self.pbAddDtr.setStyleSheet(Styles.labelText)
        self.pbAddDtr.setEnabled(False)
        self.pbAddDtr.setText("")
        self.pbAddDtr.setShortcut("")
        self.pbAddDtr.setCheckable(False)
        self.pbAddDtr.setAutoDefault(False)
        self.pbAddDtr.setDefault(False)
        self.pbAddDtr.setFlat(False)
        self.pbAddDtr.setObjectName("pbAddDtr")
        self.pbAddDtr.clicked.connect(lambda: pbAddDtrfunc(self))
        self.grid.addWidget(self.pbAddDtr, self.r, 3, 1, 1)

        self.leInputAddrs = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leInputAddrs.sizePolicy().hasHeightForWidth())
        self.leInputAddrs.setSizePolicy(sizePolicy)
        self.leInputAddrs.setMinimumSize(QtCore.QSize(0, 30))
        self.leInputAddrs.setMaximumSize(QtCore.QSize(10000, 30))
        self.leInputAddrs.setSizeIncrement(QtCore.QSize(0, 0))
        self.leInputAddrs.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.leInputAddrs.setFont(font)
        self.leInputAddrs.setAcceptDrops(True)
        self.leInputAddrs.setToolTip('Введите адрес с которого будут приходить письма')
        self.leInputAddrs.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.leInputAddrs.setStyleSheet(Styles.labelText)
        self.leInputAddrs.setText("")
        self.leInputAddrs.setMaxLength(30)
        self.leInputAddrs.setFrame(False)
        self.leInputAddrs.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.leInputAddrs.setCursorPosition(0)
        self.leInputAddrs.setDragEnabled(False)
        self.leInputAddrs.setReadOnly(False)
        self.leInputAddrs.setPlaceholderText("mail@example.ru")
        self.leInputAddrs.setClearButtonEnabled(True)
        reg_ex = QtCore.QRegularExpression("[0-9A-Za-z\-_.]+@[0-9A-Za-z\-_.]+\.[0-9A-Za-z\-_.]+")
        input_validator = QtGui.QRegularExpressionValidator(reg_ex, self.leInputAddrs)
        self.leInputAddrs.setValidator(input_validator)
        self.leInputAddrs.textEdited.connect(lambda: checkleInputAddrs(self.leInputAddrs, self.pbAddDtr))
        self.leInputAddrs.returnPressed.connect(self.pbAddDtr.click)
        self.leInputAddrs.setObjectName("leInputAddrs")
        self.grid.addWidget(self.leInputAddrs, self.r, 2, 1, 1)

        self.lbInputAddrs = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbInputAddrs.setFont(font)
        self.lbInputAddrs.setStyleSheet(Styles.lbInputBG)
        self.lbInputAddrs.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.lbInputAddrs.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.lbInputAddrs.setLineWidth(0)
        self.lbInputAddrs.setMidLineWidth(0)
        self.lbInputAddrs.setText("Список входящих адресов:")
        self.lbInputAddrs.setObjectName("lbInputAddrs")
        self.grid.addWidget(self.lbInputAddrs, self.r, 0, 1, 1)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem4, self.r, 4, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem2, self.r, 1, 1, 1)
        self.r += 1
    
        #DINAMIC ROW 1
        if len(self.config["inputAdrs"]) > 0:
            for addr, active_subject in self.config["inputAdrs"].items():
                self.lcdNumber_2 = QtWidgets.QLCDNumber()
                self.lcdNumber_2.setStyleSheet(Styles.lcdNumber)
                self.lcdNumber_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
                self.lcdNumber_2.setLineWidth(1)
                self.lcdNumber_2.setSmallDecimalPoint(False)
                self.lcdNumber_2.setDigitCount(3)
                self.lcdNumber_2.setMode(QtWidgets.QLCDNumber.Mode.Dec)
                self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
                self.lcdNumber_2.setProperty("intValue", self.counters[addr])
                self.lcdNumber_2.setObjectName("lcdNumber_"+addr)
                self.lcdNumber_2.setToolTip("<html><head/><body><p><span style=\" color:#000000;\">Количество полученных писем с адреса "+addr+"</span></p></body></html>")
                self.grid.addWidget(self.lcdNumber_2, self.r, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
            
                self.cbDtrAddr = QtWidgets.QCheckBox()
                self.cbDtrAddr.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.cbDtrAddr.setFont(font)
                self.cbDtrAddr.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
                self.cbDtrAddr.setAutoFillBackground(False)
                # if active_subject[0]:
                self.cbDtrAddr.setStyleSheet(Styles.cbStyle)
                # else: 
                #     self.cbDtrAddr.setStyleSheet(Styles.cbUnCheckedBG)
                self.cbDtrAddr.setText(addr)
                self.cbDtrAddr.setChecked(active_subject[0])
                self.cbDtrAddr.setObjectName("cbDtrAddr_"+addr)
                self.cbDtrAddr.stateChanged.connect(lambda: cbDtrAddrfunc(self))
                self.grid.addWidget(self.cbDtrAddr, self.r, 2, 1, 1)

                self.pbDellDtr = QtWidgets.QPushButton()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pbDellDtr.sizePolicy().hasHeightForWidth())
                pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_DialogCancelButton")
                self.pbDellDtr.setIcon(self.style().standardIcon(pixmapi))
                self.pbDellDtr.setSizePolicy(sizePolicy)
                self.pbDellDtr.setMinimumSize(QtCore.QSize(0, 30))
                self.pbDellDtr.setMaximumSize(QtCore.QSize(50, 50))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.pbDellDtr.setFont(font)
                self.pbDellDtr.setAutoFillBackground(False)
                self.pbDellDtr.setStyleSheet(Styles.labelText)
                self.pbDellDtr.setText("")
                self.pbDellDtr.setShortcut("")
                self.pbDellDtr.setCheckable(False)
                self.pbDellDtr.setAutoDefault(False)
                self.pbDellDtr.setDefault(False)
                self.pbDellDtr.setFlat(False)
                self.pbDellDtr.setObjectName("pbDellDtr_"+addr)
                self.pbDellDtr.clicked.connect(lambda: pbDellDtrfunc(self))
                self.grid.addWidget(self.pbDellDtr, self.r, 3, 1, 1)

                self.leSubject = QtWidgets.QLineEdit()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.leSubject.sizePolicy().hasHeightForWidth())
                self.leSubject.setSizePolicy(sizePolicy)
                self.leSubject.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.leSubject.setFont(font)
                self.leSubject.setAcceptDrops(True)
                self.leSubject.setToolTip("<html><head/><body><p><span style=\" color:#000000;\">Введите строку содержащуюся в теме сообщения от "+addr+". Или оставьте пустым. Регистр не учитывается, возможны две опечатки</span></p></body></html>")
                self.leSubject.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
                self.leSubject.setStyleSheet(Styles.labelText)
                self.leSubject.setText(active_subject[1])
                self.leSubject.setMaxLength(30)
                self.leSubject.setFrame(False)
                self.leSubject.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                self.leSubject.setCursorPosition(0)
                self.leSubject.setDragEnabled(False)
                self.leSubject.setReadOnly(False)
                self.leSubject.setClearButtonEnabled(True)
                self.leSubject.editingFinished.connect(lambda: checkleSubject(self))
                self.leSubject.setObjectName("leSubject_"+addr)
                self.grid.addWidget(self.leSubject, self.r, 4, 1, 2)
                

                self.r += 1



        #ROW SAVE ATTACHMENT 0

        self.pbAddOutputAddr = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbAddOutputAddr.sizePolicy().hasHeightForWidth())
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_FileDialogNewFolder")
        self.pbAddOutputAddr.setIcon(self.style().standardIcon(pixmapi))
        self.pbAddOutputAddr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pbAddOutputAddr.setFont(font)
        self.pbAddOutputAddr.setAutoFillBackground(False)
        self.pbAddOutputAddr.setStyleSheet(Styles.labelText)
        self.pbAddOutputAddr.setText("")
        self.pbAddOutputAddr.setShortcut("")
        self.pbAddOutputAddr.setCheckable(False)
        self.pbAddOutputAddr.setAutoDefault(False)
        self.pbAddOutputAddr.setDefault(False)
        self.pbAddOutputAddr.setFlat(False)
        self.pbAddOutputAddr.setObjectName("pbAddOutputAddr")
        self.pbAddOutputAddr.clicked.connect(lambda: choseFolderDialog(self))
        self.grid.addWidget(self.pbAddOutputAddr, self.r, 5, 1, 1)

        self.leSaveAttch = QtWidgets.QLineEdit()
        self.leSaveAttch.setMinimumSize(QtCore.QSize(0, 30))
        self.leSaveAttch.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.leSaveAttch.setFont(font)
        self.leSaveAttch.setStyleSheet(Styles.labelText)
        if self.config["attachmentFolder"]: text = self.config["attachmentFolder"]
        else: text = self.work_dir
        self.leSaveAttch.setText(text)
        self.leSaveAttch.setFrame(False)
        self.leSaveAttch.setObjectName("leSaveAttch")
        self.leSaveAttch.editingFinished.connect(lambda :choseFolderDialog(self, True))
        self.grid.addWidget(self.leSaveAttch, self.r, 2, 1, 3)

        self.saveAttachCB = QtWidgets.QCheckBox()
        self.saveAttachCB.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.saveAttachCB.setFont(font)
        self.saveAttachCB.setToolTipDuration(1)
        self.saveAttachCB.setWhatsThis("")
        self.saveAttachCB.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.saveAttachCB.setAutoFillBackground(False)
        self.saveAttachCB.setStyleSheet(Styles.cbStyle)
        self.saveAttachCB.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.saveAttachCB.setText("Сохранять вложения")
        self.saveAttachCB.setObjectName("saveAttachCB")
        self.saveAttachCB.stateChanged.connect(lambda: saveAttachCBfunc(self))
        if self.config["saveAttachment"]: self.saveAttachCB.setChecked(True)
        else: self.saveAttachCB.setChecked(False)
        self.grid.addWidget(self.saveAttachCB, self.r, 0, 1, 1)



        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem1, self.r, 1, 1, 1)  

        self.r += 1


        #ROW OUTPUT
        self.lbOutputAddr = QtWidgets.QLabel()
        self.lbOutputAddr.setMinimumSize(QtCore.QSize(0, 30))
        self.lbOutputAddr.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbOutputAddr.setFont(font)
        self.lbOutputAddr.setStyleSheet(Styles.lbInputBG)
        self.lbOutputAddr.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.lbOutputAddr.setLineWidth(1)
        self.lbOutputAddr.setText("Список рассылки:")
        self.lbOutputAddr.setObjectName("lbOutputAddr")
        self.grid.addWidget(self.lbOutputAddr, self.r, 0, 1, 1)

        self.lcdNumber_3 = QtWidgets.QLCDNumber()
        self.lcdNumber_3.setStyleSheet(Styles.lcdNumber)
        self.lcdNumber_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.lcdNumber_3.setLineWidth(1)
        self.lcdNumber_3.setSmallDecimalPoint(False)
        self.lcdNumber_3.setDigitCount(3)
        self.lcdNumber_3.setMode(QtWidgets.QLCDNumber.Mode.Dec)
        self.lcdNumber_3.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.lcdNumber_3.setProperty("intValue", 0)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.grid.addWidget(self.lcdNumber_3, self.r, 1, 1, 1)

        self.teOutputAddrs = QtWidgets.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.teOutputAddrs.setFont(font)
        self.teOutputAddrs.setToolTip('Список адресов для рассылки с любым разделителем')
        # self.teOutputAddrs.setAccessibleName("")
        # self.teOutputAddrs.setAccessibleDescription("")
        self.teOutputAddrs.setStyleSheet(Styles.labelText)
        self.teOutputAddrs.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.teOutputAddrs.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.teOutputAddrs.setLineWidth(1)
        self.teOutputAddrs.setObjectName("teOutputAddrs")
        self.teOutputAddrs.textChanged.connect(lambda: teOutputAddrsfunc(self))
        self.teOutputAddrs.setText("; ".join(self.config["outputAdrs"]))   
        self.grid.addWidget(self.teOutputAddrs, self.r, 2, 3, 4)

        self.r += 1

        #ROW OUTPUT 2 AND ROW BUTTON START
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.grid.addItem(spacerItem3, self.r, 1, 1, 1)
        
        self.pbStart = MyButton()
        self.pbStart.setEnabled(True)
        self.pbStart.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont("Helvetica", 14)
        font.setBold(True)
        font.setWeight(75)
        self.pbStart.setFont(font)
        self.pbStart.setStyleSheet(Styles.pbStartBG)
        self.pbStart.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        if self.mail_resender.run: self.pbStart.setText("Стоп")
        else: self.pbStart.setText("Начать работу")
        self.pbStart.setObjectName("pbStart")
        self.pbStart.clicked.connect(lambda :start_clicked(self))

        self.grid.addWidget(self.pbStart, self.r, 0, 2, 1)

        self.r += 1

        #ROW 5
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem, self.r, 1, 1, 1)

        self.r += 1

        #ROW LOG
        self.pteLog = QtWidgets.QPlainTextEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pteLog.sizePolicy().hasHeightForWidth())
        self.pteLog.setSizePolicy(sizePolicy)
        self.pteLog.setToolTip("")
        self.pteLog.setToolTipDuration(3)
        self.pteLog.setStyleSheet(Styles.labelText)
        self.pteLog.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.pteLog.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.pteLog.setLineWidth(1)
        self.pteLog.setReadOnly(True)
        self.pteLog.setObjectName("pteLog")
        self.pteLog.setPlainText(self.log_text)
        self.grid.addWidget(self.pteLog, self.r, 0, 1, 6)


        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 901, 26))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setTitle("Меню")
        self.menu.setObjectName("menu")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Остановлен")
        self.setStatusBar(self.statusbar)

        self.settings = QtGui.QAction(self)
        self.settings.setText("Настройки")
        self.settings.setObjectName("settings")

        self.about = QtGui.QAction(self)
        self.about.setText("О программе")
        self.about.setObjectName("about")

        self.menu.addAction(self.settings)
        self.menu.addSeparator()
        self.menu.addAction(self.about)
        self.menubar.addAction(self.menu.menuAction())
        #menu funcs
        self.settings.triggered.connect(self.settings_show)
        self.about.triggered.connect(self.about_show)

    def settings_show(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.move(self.geometry().center() - self.settings_window.geometry().center())
        self.settings_window.show()
        #connect signals
        self.settings_window.start_at_start.connect(lambda signal: start_at_start(self, signal))
        self.settings_window.minimize_to_tray.connect(lambda signal: minimize_to_tray(self, signal))
        self.settings_window.add_to_log.connect(lambda signal: add_to_log(self, signal))
        self.settings_window.save_imap_settings.connect(lambda signal: save_imap_settings(self, signal))
        self.settings_window.save_smtp_settings.connect(lambda signal: save_smtp_settings(self, signal))
        self.settings_window.save_mse_settings.connect(lambda signal: save_mse_settings(self, signal))
        self.settings_window.refreshInterval.connect(lambda signal: refreshIntervalChange(self, signal))
        self.settings_window.typeConnect.connect(lambda signal: TypeConnectChange(self, signal))
        

    def about_show(self):
        self.about_window = aboutWindow(self)
        self.about_window.move(self.geometry().center() - self.about_window.geometry().center())
        self.about_window.show()
        
    def showMainWindow(self):
        self.setGeometry(200, 200, self.w, self.h)
        self.setWindowTitle("Email Resender")
        self.setWindowIcon(QtGui.QIcon(resource_path('res/icon_passive.png', self.work_dir_for_res)))
        self.show()

    def updateMainWindow(self):
        self.show()

if __name__ == "__main__":
    pass
