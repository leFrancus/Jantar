from PySide6.QtWidgets import QApplication
from pathlib import Path
import time
import sys
import os

_SearchEnginesDatabase = 'data/SearchEngines.sqlite'


class JManager:
    def __init__(self):
        self.ControlHex = '0x19'
        self.FactHex = '0x'
        try:
            self.PATH = Path(__file__).resolve().parent
        except Exception:
            print('Unable to load: error during PATH integration')

    def IgniteEngine(self):
        try:

            from bunch.modules import ProfileSelector, Browser, ProfileMini  # Imports working check

            DatabaseLength = str(hex(_SearchEnginesDatabase.__len__()))[2:]
            self.FactHex += DatabaseLength

            Ok = self.CompareHex()

            if Ok:
                time.sleep(2)
                return True
            else:
                return False
        except ImportError:
            print('Unable to load: error during importing modules')
            return False
        except Exception:
            print('Unable to load: error during ignition')
            return False

    def CompareHex(self):
        try:
            int(self.ControlHex, 16)
            int(self.FactHex, 16)
            if self.FactHex != self.ControlHex:
                raise ValueError
        except ValueError:
            print('Files are broken or edited incorrectly (ControlHex != FactHex)')
            return False
        except Exception:
            print('Unable to compare: error during hex-comparation')
            return False
        else:
            print('Successful hex-comparation')
            return True

    def RestoreAppData(self):
        try:
            self.APPDATA = os.path.join(os.environ['APPDATA'], 'Jantar')
            self.USERS_FOLDER = os.makedirs(os.path.join(self.APPDATA, 'Users'), exist_ok=True)
        except Exception:
            print('Unable to restore app data')

if __name__ == '__main__':
    AppManager = JManager()
    AppManager.RestoreAppData()
    if AppManager.IgniteEngine():

        from bunch.modules import Browser
        from bunch.modules import ProfileSelector

        Application = QApplication(sys.argv)
        
        Window = ProfileSelector.Object()
        Window.show()
        sys.exit(Application.exec())
    else:
        print('The attempt to load Jantar is failed\nQuitting...')
        sys.exit(0)
