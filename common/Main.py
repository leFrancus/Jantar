from PySide6.QtWidgets import QApplication, QWidget
from pathlib import Path
import time
import sys
import os

_MainPath = Path(__file__)
_SearchEnginesDatabase = str(_MainPath.parent / 'data/SearchEngines.sqlite')


class JManager:
    def __init__(self):
        try:
            self.PATH = Path(__file__).parent
        except Exception:
            print('Unable to load: error during PATH integration')

    def IgniteEngine(self):
        try:
            Ok = True

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

    def RestoreAppData(self):
        try:
            self.APPDATA = os.path.join(os.getenv('APPDATA'), 'Jantar')
            self.USERS_FOLDER = os.makedirs(os.path.join(self.APPDATA, 'Users'), exist_ok=True)
        except Exception:
            print('Unable to restore app data')

    def StartBrowser(self, SenderWidget: QWidget, WebProfileId: int):
        SenderWidget.close()
        self.Window = Browser.Object(WebProfileId, self)
        self.Window.showMaximized()

if __name__ == '__main__':
    AppManager = JManager()
    AppManager.RestoreAppData()
    if AppManager.IgniteEngine():

        from bunch.modules import Browser
        from bunch.modules import ProfileSelector

        Application = QApplication(sys.argv)
        
        Window = ProfileSelector.Object(AppManager)
        Window.show()
        sys.exit(Application.exec())
    else:
        print('The attempt to load Jantar is failed\nQuitting...')
        sys.exit(0)
