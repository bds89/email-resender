import datetime, time
from exchangelib import Account, Configuration, Credentials, DELEGATE, FileAttachment
import os, re
from PyQt6 import QtCore
try:
    from ..services.my_exception import BreakLoop
except:
    from services.my_exception import BreakLoop

class MSE():
    def __init__(self, addres, login, password, server, add_to_log, auth_type=None) -> None:
        self.addres = addres
        self.server = server
        self.login = login
        self.password = password
        self.add_to_log = add_to_log
        self.auth_type = auth_type
        
        
    def try_connect(self, return_account=False, ews_auth_type="") -> bool:
        try:
            creds = Credentials(username=self.login, password=self.password)
            if self.server:
                config = Configuration(service_endpoint=self.server, credentials=creds, auth_type=self.auth_type)
                account = Account(primary_smtp_address=self.addres,  config=config, autodiscover=False, access_type=DELEGATE)
            else:
                account = Account(self.addres, credentials=creds, autodiscover=True)
            if return_account: return account
            account.protocol.close()
            return True
        except Exception as e:
            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка подключения ({e})")
            return False

class MailResenderMSE(QtCore.QObject):
    add_to_log = QtCore.pyqtSignal(str)
    status_signal = QtCore.pyqtSignal(str)
    new_mail = QtCore.pyqtSignal(str)

    old_emails = set()
    flag_init = True
    run = False


    def compare_string(self, template:str, string:str):
        template = template.lower()
        string = string.lower()
        equals = 0
        mistakes = 0
        max_equal = 0
        for n in range(len(string)):
            for m in range(len(template)):
                if m+n < len(string):
                    if string[n+m] == template[m]: equals += 1
                    else: 
                        mistakes += 1
                        if mistakes > 1:
                            mistakes = 0
                            break
            if equals > max_equal: max_equal = equals
            equals = 0
            mistakes = 0
        if max_equal >= len(template)-2: return (True)
        else: return (False)
            
    def update_config(self, config):
        try:
            self.addr = config["mse"][0]
            self.login = config["mse"][1]
            self.password = config["mse"][2]
            self.server = config["mse"][3]


            if config["saveAttachment"]:
                self.attachmentFolder = config["attachmentFolder"]
            else: self.attachmentFolder = ""
            self.inputAdrs = config["inputAdrs"]
            self.outputAdrs = config["outputAdrs"]

            self.refreshInterval = config["refreshInterval"]
        except Exception as e:
            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при передаче настроек в рабочий поток. Исключение: {e}")

        #cache EWS
        self.ews_auth_type = None

    def sleep_refresh_interval(self, lastLoop):
        while(datetime.datetime.now()-lastLoop < datetime.timedelta(minutes=int(self.refreshInterval), seconds=5)):
            time.sleep(1)
            if not self.run: raise BreakLoop()

    def start_work(self):
        self.run = True      

        while (self.run):
            try:
                lastLoop = datetime.datetime.now()
                self.status_signal.emit("Работает")
                #clear very old messages from self.old_emails
                for id, date in self.old_emails:
                    if date.replace(tzinfo=None) < (datetime.datetime.now() - datetime.timedelta(days=2)).replace(tzinfo=None):
                        self.old_emails.remove(id, date)

                try:
                    #MSE connect
                    mse = MSE(self.addr, self.login, self.password, self.server, self.add_to_log, self.ews_auth_type)
                    a = mse.try_connect(True)
                    if not a:
                        self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при подключении к MS Exchange")
                        self.sleep_refresh_interval(lastLoop)
                        continue
                    if not self.server:
                        self.server = a.protocol.service_endpoint
                        self.ews_auth_type = a.protocol.auth_type

                    #get messages
                    items = a.inbox.filter(start__gt=datetime.datetime.now(tz=a.default_timezone) - datetime.timedelta(minutes=int(self.refreshInterval)+1))
                    for item in items:
                        fromm = item.sender.email_address
                        if fromm in self.inputAdrs:
                            
                            #get message date
                            message_date = item.datetime_received

                            #get message ID
                            message_id = item.message_id

                            if (message_id, message_date) in self.old_emails: 
                                continue

                            #Get subject
                            sbj = item.subject
                            if not self.compare_string(self.inputAdrs[fromm][1], sbj):
                                continue
                            else: 
                                if self.inputAdrs[fromm][1] and not sbj:
                                    continue

                            self.old_emails.add((message_id, message_date))
                            if self.flag_init:
                                continue

                            self.add_to_log.emit(f"{datetime.datetime.now()}: Получено новое письмо от: {fromm}")
                            self.new_mail.emit(fromm)
                            #Get attachment
                            for attachment in item.attachments:
                                if isinstance(attachment, FileAttachment):
                                    #Save attachment
                                    if self.attachmentFolder:
                                        filePath = os.path.join(self.attachmentFolder, attachment.name)
                                        with open(filePath, 'wb') as file:
                                            file.write(attachment.content)

                            #send message
                            item.forward(
                                subject='Fwd: '+sbj,
                                body='Переслано от '+fromm,
                                to_recipients=self.outputAdrs
                            )
                            self.add_to_log.emit(f"{datetime.datetime.now()}: Письмо от {fromm} отправлено по списку рассылки")

                except Exception as e:
                    if e.__class__.__name__ != BreakLoop().__class__.__name__:
                        self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при работе, исключение: {e.__class__.__name__, e, e.args}")
                
                if self.flag_init:
                    self.flag_init = False
                #sleep refreshInterval
                self.sleep_refresh_interval(lastLoop)
            except BreakLoop: 
                self.status_signal.emit("Остановлен")
                break