from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QSizePolicy, QLineEdit, QComboBox, QFrame, QCheckBox, QMessageBox, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from pathlib import Path
import sqlite3 as sql
import os
from . import ProfileMini
import shutil

_WIDGET = None
_LocalUsersDatabase = Path(__file__).resolve().parent.parent.parent / 'data/LocalUsers-Safe.sqlite'  # Temp -Safe file


class Object(QWidget):
    def __init__(self, WebProfileId: int):
        super().__init__()
        self.CurrentWebProfileId = WebProfileId

        self.UnifiedStyleSheet = "font-family: 'Inter'; color: #0a0a0a;"
        self.ProgressStyleSheet = """QProgressBar {
                background: #f4f4f4;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: #ffd940;
                border-radius: 2px;
            }"""

        self.InputStyleSheet = """
            font-size: 12px;
            background-color: #ffffff;
            border: 2px solid #efefef;
            border-radius: 8px;
            padding: 2px 2px;
            color: #0a0a0a;
            outline: none;
        """
        self.setFont('Inter')

        if self.CurrentWebProfileId == -1:
            self.ProfileIcon = str(Path(__file__).resolve().parent.parent / 'images' / 'PrivateUser.png')
            self.ProfileIcon = QPixmap(self.ProfileIcon)
        else:
            with sql.connect(_LocalUsersDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT userFolder FROM localUsers WHERE id = ?"
                PathToIcon = Cursor.execute(Request, (self.CurrentWebProfileId,)).fetchone()[0]
                PathToIcon = os.path.join(PathToIcon, 'Icon.png')
                self.ProfileIcon = QPixmap(PathToIcon)
            Database.close()

        self.setWindowTitle(' ')
        self.setWindowIcon(self.ProfileIcon)
        self.setFixedWidth(600)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.setLayout(QVBoxLayout())

        # self.layout().setContentsMargins(20, 20, 20, 20)
        # self.layout().setSpacing(10)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        TitleCommon = QLabel()
        TitleCommon.setText('Settings')
        TitleCommon.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 22px; font-weight: bold;')
        TitleCommon.setWordWrap(True)
        self.layout().addWidget(TitleCommon)

        TopLine = QFrame()
        TopLine.setFrameShape(QFrame.Shape.HLine)
        TopLine.setFrameShadow(QFrame.Shadow.Sunken)
        TopLine.setStyleSheet("background-color: #efefef;")
        self.layout().addWidget(TopLine)

        Title_1 = QLabel()
        Title_1.setText('• Personal')
        Title_1.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 16px; font-weight: bold;')
        Title_1.setWordWrap(True)
        self.layout().addWidget(Title_1)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('Homepage')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px; font-family: "Inter"')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.HomepageEdit = QLineEdit()
        self.HomepageEdit.setStyleSheet(self.InputStyleSheet)
        self.HomepageEdit.setPlaceholderText('None')
        Setting.layout().addWidget(self.HomepageEdit)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('Search engine by default')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px;')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.SearchEngineBox = QComboBox()
        self.SearchEngineBox.addItem('Google')
        self.SearchEngineBox.addItem('DuckDuckGo')
        self.SearchEngineBox.addItem('Bing')
        Setting.layout().addWidget(self.SearchEngineBox)

        Line = QFrame()
        Line.setFrameShape(QFrame.Shape.HLine)
        Line.setFrameShadow(QFrame.Shadow.Sunken)
        Line.setStyleSheet("background-color: #efefef;")
        self.layout().addWidget(Line)

        Title_2 = QLabel()
        Title_2.setText('• Safety')
        Title_2.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 16px; font-weight: bold;')
        Title_2.setWordWrap(True)
        self.layout().addWidget(Title_2)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('HTTPS-sites only')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px;')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.HttpsOnlyCheck = QCheckBox()
        Setting.layout().addWidget(self.HttpsOnlyCheck)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('Necessary Cookies only')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px;')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.NecessaryCookiesCheck = QCheckBox()
        Setting.layout().addWidget(self.NecessaryCookiesCheck)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('Block external requests')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px;')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.BlockExternalRequestsCheck = QCheckBox()
        Setting.layout().addWidget(self.BlockExternalRequestsCheck)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        SetTitle = QLabel()
        SetTitle.setText('Request policy')
        SetTitle.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px;')
        SetTitle.setWordWrap(True)
        Setting.layout().addWidget(SetTitle)
        Setting.layout().addStretch()
        self.RequestPolicy = QComboBox()
        self.RequestPolicy.addItem('Soft')
        self.RequestPolicy.addItem('Strict')
        self.RequestPolicy.addItem('None')
        Setting.layout().addWidget(self.RequestPolicy)

        Setting = QWidget()
        Setting.setLayout(QHBoxLayout())
        Setting.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(Setting)
        self.DeleteProfileButton = QToolButton()
        self.DeleteProfileButton.setText('Delete local profile')
        self.DeleteProfileButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 12px; background-color: #f40000; border-color: #d90000; color: #f4f4f4;')
        self.DeleteProfileButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.DeleteProfileButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.DeleteProfileButton.clicked.connect(self.DeleteProfile)
        Setting.layout().addWidget(self.DeleteProfileButton)

        self.layout().addStretch()

        BottomLine = QFrame()
        BottomLine.setFrameShape(QFrame.Shape.HLine)
        BottomLine.setFrameShadow(QFrame.Shadow.Sunken)
        BottomLine.setStyleSheet("background-color: #efefef;")
        self.layout().addWidget(BottomLine)

        self.Buttons = QWidget()
        self.Buttons.setLayout(QHBoxLayout())
        self.layout().addWidget(self.Buttons)

        self.CloseButton = QToolButton()
        self.CloseButton.setStyleSheet('background: transparent; border: none; font-family: "Inter";')
        self.CloseButton.setText('↩ Back')
        self.CloseButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.CloseButton.clicked.connect(self.Close)
        self.Buttons.layout().addWidget(self.CloseButton)

        self.Buttons.layout().addStretch()

        Notice = QLabel()
        Notice.setText('All changes will be applied after restart.')
        Notice.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 9px; color: #777;')
        Notice.setWordWrap(True)
        self.Buttons.layout().addWidget(Notice)

        self.Buttons.layout().addStretch()

        self.CommitButton = QToolButton()
        self.CommitButton.setStyleSheet('background-color: #d9d9d9; font-family: "Inter"; color: #777;')
        self.CommitButton.setText('Commit')
        self.CommitButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.CommitButton.clicked.connect(self.Commit)
        self.Buttons.layout().addWidget(self.CommitButton)

        self.LoadSettings()
        self.HasChanges = False

        self.HomepageEdit.textEdited.connect(self.SetSomethingChanged)
        self.SearchEngineBox.currentIndexChanged.connect(self.SetSomethingChanged)
        self.HttpsOnlyCheck.toggled.connect(self.SetSomethingChanged)
        self.NecessaryCookiesCheck.toggled.connect(self.SetSomethingChanged)
        self.BlockExternalRequestsCheck.toggled.connect(self.SetSomethingChanged)
        self.RequestPolicy.currentIndexChanged.connect(self.SetSomethingChanged)

    def SetSomethingChanged(self):
        self.CommitButton.setStyleSheet('background-color: #00d900; font-family: "Inter"; color: #f4f4f4;')
        self.HasChanges = True

    def Commit(self):
        self.CommitButton.setStyleSheet('background-color: #d9d9d9; font-family: "Inter"; color: #777;')
        self.UpdateSettings()
        self.HasChanges = False

    def LoadSettings(self):
        with sql.connect(_LocalUsersDatabase) as Database:
            Cursor = Database.cursor()
            Request = "SELECT userFolder FROM localUsers WHERE id = ?"
            UserPath = Cursor.execute(Request, (self.CurrentWebProfileId,)).fetchone()[0]
        Database.close()
        UserPath += '\\Data.db'

        with sql.connect(UserPath) as Database:
            Cursor = Database.cursor()
            Request = "SELECT value FROM userSettings"  # Homepage, SearchEngineByDefault, CacheFolder, PersistentFolder
            UserSettings = Cursor.execute(Request).fetchall()

            Request = "SELECT value FROM safetySettings"  # HttpsOnly, NecessaryCookiesOnly, CertificatePolicy, BlockExternalRequests
            SafetySettings = Cursor.execute(Request).fetchall()
        Database.close()
        self.HomepageEdit.setText(UserSettings[0][0])
        self.SearchEngineBox.setCurrentIndex(int(UserSettings[1][0]) - 1)
            
        self.HttpsOnlyCheck.setChecked(bool(SafetySettings[0][0]))
        self.NecessaryCookiesCheck.setChecked(bool(SafetySettings[1][0]))
        self.RequestPolicy.setCurrentIndex(int(SafetySettings[2][0]) - 1)
        self.BlockExternalRequestsCheck.setChecked(bool(SafetySettings[3][0]))

    def UpdateSettings(self):
        with sql.connect(_LocalUsersDatabase) as Database:
            Cursor = Database.cursor()
            Request = "SELECT userFolder FROM localUsers WHERE id = ?"
            UserPath = Cursor.execute(Request, (self.CurrentWebProfileId,)).fetchone()[0]
        Database.close()

        UserPath = os.path.join(UserPath, 'Data.db')
        
        with sql.connect(UserPath) as Database:
            Cursor = Database.cursor()

            Cursor.execute("UPDATE userSettings SET value = ? WHERE name = ?", (QUrl(self.HomepageEdit.text()).toString(), "Homepage"))
            Cursor.execute("UPDATE userSettings SET value = ? WHERE name = ?", (str(self.SearchEngineBox.currentIndex() + 1), "SearchEngineByDefault"))

            Cursor.execute("UPDATE safetySettings SET value = ? WHERE name = ?", (str(int(self.HttpsOnlyCheck.isChecked())), "HttpsOnly"))
            Cursor.execute("UPDATE safetySettings SET value = ? WHERE name = ?", (str(int(self.NecessaryCookiesCheck.isChecked())), "NecessaryCookiesOnly"))
            Cursor.execute("UPDATE safetySettings SET value = ? WHERE name = ?", (str(self.RequestPolicy.currentIndex() + 1), "CertificatePolicy"))
            Cursor.execute("UPDATE safetySettings SET value = ? WHERE name = ?", (str(int(self.BlockExternalRequestsCheck.isChecked())), "BlockExternalRequests"))
        Database.close()

    def closeEvent(self, event):
        Ok = self.Close(IsCrossClicked=True)
        if Ok:
            event.accept()
        else:
            event.ignore()

    def Close(self, IsCrossClicked=False):
        if not IsCrossClicked:
            self.close()
        else:
            if self.HasChanges:
                Decision = QMessageBox.warning(self, 'Hey!', 'You have unsaved settings! Would you really like to close this window without saving?',
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
                if Decision == QMessageBox.StandardButton.Yes:
                    ProfileMini.ShowObject(self.CurrentWebProfileId)
                    return True
                else:
                    return False
            else:
                ProfileMini.ShowObject(self.CurrentWebProfileId)
                return True

    def DeleteProfile(self):
        Ok = QMessageBox.warning(self, 'Hey!', 'You are going to delete the local profile! That means you won\'t be available to your services without rejoining.\nAre you sure you want to delete your profile?',
            QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if Ok == QMessageBox.StandardButton.Yes:
            with sql.connect(_LocalUsersDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT userFolder FROM localUsers WHERE id = ?"
                Folder = Cursor.execute(Request, (self.CurrentWebProfileId,)).fetchone()[0]

            try:
                for Root, _, Files in os.walk(Folder):
                    for File in Files:
                        os.remove(os.path.join(Root, File))
                os.rmdir(Folder)
            except Exception:
                QMessageBox.critical(self, 'Oh!', 'Unable to delete the profile', QMessageBox.StandardButton.Ok)
            else:
                Request = "DELETE FROM localUsers WHERE id = ?"
                Cursor.execute(Request, (self.CurrentWebProfileId,))
            Database.close()
            print('Deleted local profile')


def ShowObject(WebProfileId: int):
    global _WIDGET

    _WIDGET = Object(WebProfileId)
    _WIDGET.show()

