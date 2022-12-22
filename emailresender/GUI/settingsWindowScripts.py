try:
    from ..mail.mail import Imap, Smtp
    from ..mail.exchange import MSE
except ImportError:
    from mail.mail import Imap, Smtp
    from mail.exchange import MSE
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

def start_at_startfunc(sWindow):
    if sWindow.checkBox.isChecked():
        sWindow.start_at_start.emit(True)
    else: sWindow.start_at_start.emit(False)

def minimize_to_trayfunc(sWindow):
    if sWindow.checkBox_2.isChecked():
        sWindow.minimize_to_tray.emit(True)
    else: sWindow.minimize_to_tray.emit(False)


class Try_connect(QObject):

    def imap_and_smtp_connect(self, sWindow):
        self.imap_connect(sWindow, False)
        self.smtp_connect(sWindow, False)

    def imap_connect(self, sWindow, settings=True):
        server = sWindow.lineEdit.text()
        port = sWindow.lineEdit_port.text()
        login = sWindow.lineEdit_2.text()
        password = sWindow.lineEdit_3.text()
        if server and port and login and password:
            imap = Imap(server, port, login, password, sWindow.add_to_log)
            succes = imap.try_connect()
            if succes: sWindow.pushButton.setText("Подключено")
            else: sWindow.pushButton.setText("Ошибка")
            if settings:
                sWindow.save_imap_settings.emit([server, port, login, password])

    def smtp_connect(self, sWindow, settings=True):
        server = sWindow.lineEdit_5.text()
        port = sWindow.lineEdit_5port.text()
        login = sWindow.lineEdit_4.text()
        password = sWindow.lineEdit_6.text()
        if server and port and login and password:
            smtp = Smtp(server, port, login, password, sWindow.add_to_log)
            succes = smtp.try_connect()
            if succes: sWindow.pushButton_2.setText("Подключено")
            else: sWindow.pushButton_2.setText("Ошибка")
            if settings:
                sWindow.save_smtp_settings.emit([server, port, login, password])

    def mse_connect(self, sWindow, settings=True):
        addres = sWindow.leAddr.text()
        login = sWindow.leLogin.text()
        password = sWindow.lePass.text()
        server = sWindow.leServer.text()

        if login and password and addres:
            mse = MSE(addres, login, password, server, sWindow.add_to_log)
            succes = mse.try_connect()
            if succes: sWindow.pbMSConnect.setText("Подключено")
            else: sWindow.pbMSConnect.setText("Ошибка")
            if settings:
                sWindow.save_mse_settings.emit([addres, login, password, server])

def imap_change(sWindow):
    sWindow.pushButton.setText("Подключиться")
def smtp_change(sWindow):
    sWindow.pushButton_2.setText("Подключиться")
def mse_change(sWindow):
    sWindow.pbMSConnect.setText("Подключиться")

def chooseTypeConnect(sWindow, type):
    if type == "IMAP/SMTP": 
        sWindow.imapTab.setEnabled(True)
        sWindow.MSTab.setEnabled(False)
        sWindow.tabWidget.setCurrentIndex(0)

    else: 
        sWindow.imapTab.setEnabled(False)
        sWindow.MSTab.setEnabled(True)
        sWindow.tabWidget.setCurrentIndex(1)
    sWindow.typeConnect.emit(type)
    
        
