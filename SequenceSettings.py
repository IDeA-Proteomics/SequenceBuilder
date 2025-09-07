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
            self.saveToFile("settings.json")
        return
    
    def saveToFile(self, file_path="settings.json"):
        with open(file_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        return
    
    def loadFromFile(self, file_path="settings.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.__dict__.update(data)
        return
    
