import json
import os


class AppSettings():

    def __init__(self):
        if os.path.exists("settings.json"):
            self.loadFromFile("settings.json")
        else:
            self.default_tray = 'G'
            self.default_instrument = "Exploris1"
            self.default_save_folder = "/home/david/IDeA_Scripts/TestData/"
            self.default_vertical = False
            self.saveToFile("settings.json")
        return
    
    def saveToFile(self, file_path="settings.json"):
        with open(file_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        return
    
    def loadFromFile(self, file_path="settings.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            missing = False
            if 'default_tray' not in data:
                data['default_tray'] = 'G'
                missing = True
            if 'default_instrument' not in data:
                data['default_instrument'] = "Exploris1"
                missing = True
            if 'default_save_folder' not in data:
                data['default_save_folder'] = ""
                missing = True
            if 'default_vertical' not in data:
                data['default_vertical'] = False
                missing = True
            self.__dict__.update(data)
            if missing:
                self.saveToFile(file_path)
        return
    
