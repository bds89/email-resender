import imaplib
import email
import os, re
import smtplib, ssl, datetime, time, locale
from PyQt6 import QtCore
try:
    from ..services.my_exception import BreakLoop
except ImportError:
    from services.my_exception import BreakLoop

class Imap():
    def __init__(self, server, port, login, password, add_to_log) -> None:
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.add_to_log = add_to_log
        
        
    def try_connect(self) -> bool:
        try:
            imap = imaplib.IMAP4_SSL(self.server, int(self.port))
            imap.login(self.login, self.password)
            status, f_list = imap.list()
            if status == "OK":
                status, select_data = imap.select('INBOX', readonly=True)
                if status == "OK":
                    return True
            else: 
                self.add_to_log.emit(f"{datetime.datetime.now()}: Подключение установлено, но запрос списка папок не успешен")
                return False 
            imap.logout()
        except Exception as e:
            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка подключения ({e})")
            return False 


class Smtp():
    def __init__(self, server, port, login, password, add_to_log) -> None:
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.add_to_log = add_to_log
        

    def try_connect(self) -> bool:
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                server.login(self.login, self.password)
            return True
        except Exception as e:
            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка подключения ({e})")
            return False

class MailResender(QtCore.QObject):
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
            self.i_server = config["imap"][0]
            self.i_port = config["imap"][1]
            self.i_login = config["imap"][2]
            self.i_password = config["imap"][3]


            if config["saveAttachment"]:
                self.attachmentFolder = config["attachmentFolder"]
            else: self.attachmentFolder = ""
            self.inputAdrs = config["inputAdrs"]
            self.outputAdrs = config["outputAdrs"]

            self.s_server = config["smtp"][0]
            self.s_port = config["smtp"][1]
            self.s_login = config["smtp"][2]
            self.s_password = config["smtp"][3]

            self.refreshInterval = config["refreshInterval"]
        except Exception as e:
            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при передаче настроек в рабочий поток. Исключение: {e}")

    def sleep_refresh_interval(self, lastLoop):
        while(datetime.datetime.now()-lastLoop < datetime.timedelta(minutes=int(self.refreshInterval), seconds=5)):
            time.sleep(0.5)
            if not self.run:
                raise BreakLoop()

    def start_work(self):
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        self.run = True
        #construct search criteria
        criteria = ""
        if len(self.inputAdrs) > 1:
            criteria = 'OR'
        for addr in self.inputAdrs.items():
            if addr[1]:
                criteria += " FROM " + addr[0]
        criteria += " SINCE "+(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")   #01-Dec-2022
        print(criteria.strip())
        

        while (self.run):
            try:
                lastLoop = datetime.datetime.now()
                self.status_signal.emit("Работает")
                #clear very old messages from self.old_emails
                for id, date in self.old_emails:
                    if email.utils.parsedate_to_datetime(date).replace(tzinfo=None) < (datetime.datetime.now() - datetime.timedelta(days=2)).replace(tzinfo=None):
                        self.old_emails.remove(id, date)
                try:
                    #IMAP connect
                    imap = imaplib.IMAP4_SSL(self.i_server, int(self.i_port))
                    imap.login(self.i_login, self.i_password)

                    #Select inbox mailbox
                    status, select_data = imap.select("INBOX", readonly=True)

                    #get messages
                    if status != "OK": 
                        self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при выборе ящика входящих писем. row_data: {select_data}")
                        self.sleep_refresh_interval(lastLoop)
                        continue
                    status, search_data = imap.search(None, criteria.strip())  # get all emails
                    if status != "OK": 
                        self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при выборе критериев поиска писем. Возможно сервер не поддерживает критерий FROM. row_data: {search_data}")
                        #try without FROM
                        criteria = "SINCE "+(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")   #01-Dec-2022
                        status, search_data = imap.search(None, criteria.strip())  # get all emails
                        if status != "OK": 
                            self.sleep_refresh_interval(lastLoop)
                            continue
                    for msg_id in search_data[0].split():
                        status, msg_data = imap.fetch(msg_id, '(RFC822)')
                        if status != "OK": 
                            self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при получении частей письма. row_data: {msg_data}")
                            continue
                        msg_raw = msg_data[0][1]
                        msg = email.message_from_bytes(msg_raw)
                        

                        #get message date
                        message_date = msg["Date"]

                        #get FROM message
                        fromm = ""
                        if msg["From"]:
                            bytes_msg = email.header.decode_header(msg["From"])
                            for bs in bytes_msg:
                                if type(bs[0]) == bytes:
                                    if bs[1] == None:
                                        frm = re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", bs[0].decode())
                                        if frm:
                                            fromm = frm[0]
                                    else:
                                        frm = re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", bs[0].decode(bs[1]))
                                        if frm:
                                            fromm = frm[0]
                                else: 
                                    frm = re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", bs[0])
                                    if frm:
                                        fromm = frm[0]
                        if not fromm: 
                            continue
                        if not fromm in self.inputAdrs: 
                            self.sleep_refresh_interval(lastLoop)
                            continue

                        #get message ID
                        if "Message-ID" in msg and msg["Message-ID"]:
                            bytes_msg = email.header.decode_header(msg["Message-ID"])        
                            if type(bytes_msg[0][0]) == bytes:
                                message_id = bytes_msg[0][0].decode(bytes_msg[0][1])
                            else: message_id = bytes_msg[0][0]
                        else: message_id = message_date
                        #check if old
                        if (message_id, message_date) in self.old_emails:
                            continue

                        #Get subject
                        if self.inputAdrs[fromm][1] and "Subject" in msg and msg["Subject"]:
                            bytes_msg = email.header.decode_header(msg["Subject"])        
                            if type(bytes_msg[0][0]) == bytes:
                                sbj = bytes_msg[0][0].decode(bytes_msg[0][1])
                            else: sbj = bytes_msg[0][0]
                            if not self.compare_string(self.inputAdrs[fromm][1], sbj):
                                continue
                        else: 
                            if self.inputAdrs[fromm][1] and (not "Subject" in msg or not msg["Subject"]):
                                continue

                        self.old_emails.add((message_id, message_date))
                        if self.flag_init:
                            continue

                        self.add_to_log.emit(f"{datetime.datetime.now()}: Получено новое письмо от: {fromm}")
                        self.new_mail.emit(fromm)
                        #Get attachment
                        
                        n = 1
                        if msg.is_multipart():
                            for part in msg.walk():
                                ctype = part.get_content_type()
                                cdispo = str(part.get('Content-Disposition'))
                                fileName = part.get_filename()
                                if bool(fileName):
                                    fname = "Attachment_"+str(n)
                                    n+=1
                                    bytes_filename = email.header.decode_header(fileName)
                                    if type(bytes_filename[0][0]) == bytes:
                                        fname = bytes_filename[0][0].decode(bytes_filename[0][1])
                                    else:
                                        fname = bytes_filename[0][0]

                                    #Save attachment
                                    if self.attachmentFolder:
                                        att = part.get_payload(decode=True)
                                        filePath = os.path.join(self.attachmentFolder, fname)
                                        with open(filePath, 'wb') as file:
                                            file.write(att)

                                # skip any text/plain (txt) attachments
                                if ctype == 'text/plain' and 'attachment' not in cdispo:
                                    continue
                        #connect smtp
                        if self.outputAdrs:
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(self.s_server, self.s_port, context=context) as smtp:
                                smtp.login(self.s_login, self.s_password)
                                msg.__delitem__('From')
                                msg.__delitem__('To')
                                msg.__setitem__('From', self.s_login)
                                msg.__setitem__('To', ";".join(self.outputAdrs))
                                smtp.send_message(msg)
                                self.add_to_log.emit(f"{datetime.datetime.now()}: Письмо от {fromm} отправлено по списку рассылки")

                except Exception as e:
                    if e.__class__.__name__ != BreakLoop().__class__.__name__:
                        self.add_to_log.emit(f"{datetime.datetime.now()}: Ошибка при работе, исключение: {e.__class__.__name__, e, e.args}")
                
                if self.flag_init:
                    self.flag_init = False
                #sleep refreshInterval
                if "imap" in locals() and imap:
                    imap.logout()
                self.sleep_refresh_interval(lastLoop)
            except BreakLoop: 
                self.status_signal.emit("Остановлен")
                break