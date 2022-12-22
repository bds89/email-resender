import sys, inspect, os, yaml

class Config():
  
    def check_config(config):
        if not "inputAdrs" in config:
            config.update({"inputAdrs":{}})
        if not "attachmentFolder" in config:
            config.update({"attachmentFolder":""})
        if not "saveAttachment" in config:
            config.update({"saveAttachment":False})
        if not "outputAdrs" in config:
            config.update({"outputAdrs":[]})
        if not "minimizeToTray" in config:
            config.update({"minimizeToTray":False})
        if not "startAtStart" in config:
            config.update({"startAtStart":False})
        if not "imap" in config:
            config.update({"imap":["", "993", "", ""]})
        if not "smtp" in config:
            config.update({"smtp":["", "465", "", ""]})
        if not "mse" in config:
            config.update({"mse":["", "", "", ""]})
        if not "folder" in config:
            config.update({"folder":"Все"})
        if not "refreshInterval" in config:
            config.update({"refreshInterval":5})  
        if not "connectType" in config:
            config.update({"connectType":"IMAP/SMTP"})        
            

            
            
            
        return config

    def load(work_dir):
        CONFIG_PATCH = os.path.join(work_dir, "config.yaml")
        if not os.path.exists(CONFIG_PATCH):
            with open(CONFIG_PATCH, mode='w', encoding='utf-8') as f:
                CONFIG = {}
                CONFIG = Config.check_config(CONFIG)
        else:
            with open(CONFIG_PATCH, encoding='utf-8') as f:
                CONFIG = yaml.load(f.read(), Loader=yaml.FullLoader)
                if not CONFIG: CONFIG = {}
                CONFIG = Config.check_config(CONFIG)
        return CONFIG
    
    def save(config, work_dir):
        CONFIG_PATCH = os.path.join(work_dir, "config.yaml")
        with open(CONFIG_PATCH, "w", encoding='utf-8') as f:
            f.write(yaml.dump(config, sort_keys=True, allow_unicode=True))
