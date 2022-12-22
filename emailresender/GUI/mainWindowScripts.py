import re, time
from PyQt6 import QtCore, QtWidgets, QtGui
try:
    from .styles import *
    from ..services.config import Config
    from ..services.res_patch import resource_path
except ImportError:
    from GUI.styles import *
    from services.config import Config
    from services.res_patch import resource_path



def saveAttachCBfunc(window):
    if window.saveAttachCB.isChecked():
        # window.saveAttachCB.setStyleSheet(Styles.cbCheckedBG)
        window.leSaveAttch.setEnabled(True)
        window.config["attachmentFolder"] = window.leSaveAttch.text()
        window.config["saveAttachment"] = True
    else: 
        # window.saveAttachCB.setStyleSheet(Styles.cbUnCheckedBG)
        window.leSaveAttch.setEnabled(False)
        window.config["saveAttachment"] = False
    Config.save(window.config, window.work_dir)
    window.mail_resender.update_config(window.config)

def cbDtrAddrfunc(window):
    source = window.sender()
    cb = window.findChild(QtWidgets.QCheckBox, source.objectName())
    if cb.isChecked():
        # cb.setStyleSheet(Styles.cbCheckedBG)
        window.config["inputAdrs"][source.objectName()[10:]][0] = True
    else: 
        # cb.setStyleSheet(Styles.cbUnCheckedBG)
        window.config["inputAdrs"][source.objectName()[10:]][0] = False
    Config.save(window.config, window.work_dir)
    window.mail_resender.update_config(window.config)

def pbAddDtrfunc(window):
    new_addr = window.leInputAddrs.text()
    window.config["inputAdrs"][new_addr] = [True, ""]
    window.counters[new_addr] = 0
    window.setupUi()
    window.updateMainWindow()
    Config.save(window.config, window.work_dir)
    window.mail_resender.update_config(window.config)

def pbDellDtrfunc(window):
    source = window.sender()
    pb = window.findChild(QtWidgets.QCheckBox, source.objectName())
    window.config["inputAdrs"].pop(source.objectName()[10:])
    window.setupUi()
    window.updateMainWindow()
    Config.save(window.config, window.work_dir)
    window.mail_resender.update_config(window.config)

def checkleInputAddrs(leInputAddrs:QtWidgets.QLineEdit, pbAddDtr:QtWidgets.QPushButton):
    if re.search(r"[0-9A-Za-z-_\.]+@[0-9A-Za-z-_]+\.[A-Za-z-_]+", leInputAddrs.text()):
        pbAddDtr.setEnabled(True)
        pbAddDtr.setStyleSheet(Styles.pbBGactive)
    else:
        pbAddDtr.setEnabled(False)
        pbAddDtr.setStyleSheet(Styles.labelText)

def checkleSubject(window):
    source = window.sender()
    le = window.findChild(QtWidgets.QLineEdit, source.objectName())
    window.config["inputAdrs"][source.objectName()[10:]][1] = le.text()
    Config.save(window.config, window.work_dir)
    window.mail_resender.update_config(window.config)

def choseFolderDialog(window, manual=False):
    if manual: fname = window.leSaveAttch.text()
    else: fname = QtWidgets.QFileDialog.getExistingDirectory(window)
    if fname:
        window.leSaveAttch.setText(fname)
        window.config["attachmentFolder"] = fname
        Config.save(window.config, window.work_dir)
        window.mail_resender.update_config(window.config)

def teOutputAddrsfunc(window):
    outputs = re.findall(r"[0-9A-Za-z-_\.]+@[0-9A-Za-z-_]+\.[A-Za-z-_]+", window.teOutputAddrs.toPlainText())
    window.lcdNumber_3.setProperty("intValue", len(outputs))
    if outputs != window.config["outputAdrs"]:
        window.config["outputAdrs"] = outputs
        Config.save(window.config, window.work_dir)
        window.mail_resender.update_config(window.config)
    

#Signals from settings
def start_at_start(window, signal):
    window.config["startAtStart"] = signal
    Config.save(window.config, window.work_dir)

def minimize_to_tray(window, signal):
    window.config["minimizeToTray"] = signal
    Config.save(window.config, window.work_dir)

def add_to_log(window, signal):
    log = window.pteLog.toPlainText()
    log += signal + "\n"
    window.log_lines += 1

    if window.log_lines > 100+1:
        logList = log.split("\n")
        logList = logList[len(logList)-100-1:]
        log = "\n".join(logList)
        window.log_lines = len(logList)
    window.pteLog.setPlainText(log)
    window.log_text = log

def save_imap_settings(window, signal):
    window.config["imap"] = signal
    window.mail_resender.update_config(window.config)
    Config.save(window.config, window.work_dir)
def save_smtp_settings(window, signal):
    window.config["smtp"] = signal
    window.mail_resender.update_config(window.config)
    Config.save(window.config, window.work_dir)
def save_mse_settings(window, signal):
    window.config["mse"] = signal
    window.mail_resender.update_config(window.config)
    Config.save(window.config, window.work_dir)

def refreshIntervalChange(window, signal):
    window.config["refreshInterval"] = signal
    window.mail_resender.update_config(window.config)
    Config.save(window.config, window.work_dir)
    
def start_clicked(window):
    source = window.sender()
    change_color_start(source)
    if not window.mail_resender.run:
        window.mailthread.start()
    else:
        window.pbStart.setEnabled(False)
        window.mail_resender.run = False
        window.mailthread.exit()

def status_change(window, status):
    window.statusbar.showMessage(status)
    if status == "Остановлен":
        window.setWindowIcon(QtGui.QIcon(resource_path('res/icon_passive.png', window.work_dir_for_res)))
        window.trayIcon.setIcon(QtGui.QIcon(resource_path('res/icon_passive.png', window.work_dir_for_res)))
        window.pbStart.setEnabled(True)
        if  window.pbStart.text() != "Начать работу": window.pbStart.setText("Начать работу")
    else:
        window.setWindowIcon(QtGui.QIcon(resource_path('res/icon_active.png', window.work_dir_for_res)))
        window.trayIcon.setIcon(QtGui.QIcon(resource_path('res/icon_active.png', window.work_dir_for_res)))
        if  window.pbStart.text() != "Стоп": window.pbStart.setText("Стоп")

def new_mail(window, addr):
    lcd = window.findChild(QtWidgets.QLCDNumber, "lcdNumber_"+addr)
    window.counters[addr] += 1
    lcd.setProperty("intValue", window.counters[addr])

def TypeConnectChange(window, signal):
    window.config["connectType"] = signal
    window.mail_resender.run = False
    window.mailthread.exit()
    while window.mailthread.isRunning():
        time.sleep(0.1)
        pass
    window.mailthread = QtCore.QThread()
    window.mail()
    Config.save(window.config, window.work_dir)

    
def change_color_start(button):
    def updateColor(color, button, text):
        if button.text() != text:
            button.setText(text)
        palette.setColor(role, color)
        button.setPalette(palette)
    palette = button.palette()
    role = button.foregroundRole()
    anim = QtCore.QVariantAnimation(button)
    anim.setDuration(1200)
    anim.setStartValue(QtGui.QColor(255, 170, 0))
    anim.setEndValue(QtGui.QColor(0, 0, 0))
    if button.text() == 'Начать работу':
        new_text = 'Стоп'
    else: new_text = 'Начать работу'
    anim.valueChanged.connect(lambda color: updateColor(color, button, new_text))
    anim.start()