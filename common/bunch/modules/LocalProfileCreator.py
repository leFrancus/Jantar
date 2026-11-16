from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolButton, QLabel, QLineEdit, QSizePolicy, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from pathlib import Path
import sqlite3 as sql
import Main
import os
from . import ProfileSelector
import argon2

_WIDGET = None
_LocalUsersDatabase = Path(__file__).resolve().parent.parent.parent / 'data/LocalUsers-Safe.sqlite'  # Temp -Safe file


class Object(QWidget):
    def __init__(self, AppManager):
        super().__init__()

        self.AppManager = AppManager
        self.WebProfilesList = []

        self.CurrentWebProfileIndex = 0
        self.UnifiedStyleSheet = "background: #f4f4f4; font-family: 'Inter'; border: none; padding-left: 4px; padding-right: 4px; color: #0a0a0a;"
        self.setStyleSheet(self.UnifiedStyleSheet)
        
        self.Icon = str(Path(__file__).resolve().parent.parent / 'images' / 'Icon.ico')
        self.Icon = QIcon(self.Icon)

        self.setWindowTitle(' ')
        self.setWindowIcon(self.Icon)
        self.setMinimumSize(500, 456)
        self.setMaximumSize(500, 456)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.BackButton = QToolButton()
        self.BackButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.BackButton.setText('↩ Back')
        self.BackButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 14px; font-weight: bold;')
        self.BackButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.BackButton.clicked.connect(self.Return)
        self.layout().addWidget(self.BackButton)

        self.Title = QLabel()
        self.Title.setText('New local profile')
        self.Title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.Title.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 24px; font-weight: bold; margin-bottom: 32px;')
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.Title)

        self.CreateNewLocalUserWidget = QWidget()
        self.CreateNewLocalUserWidget.setLayout(QVBoxLayout())
        self.layout().addWidget(self.CreateNewLocalUserWidget)
        
        self.ProfileIcon = QPixmap(str(Main._MainPath.parent / 'bunch/images/UnknownUser.png'))
        self.ProfileIcon = self.ProfileIcon.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ProfileIconDisplay = QLabel()
        self.ProfileIconDisplay.setStyleSheet('margin-bottom: 32px;')
        self.ProfileIconDisplay.setPixmap(self.ProfileIcon)
        self.ProfileIconDisplay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.CreateNewLocalUserWidget.layout().addWidget(self.ProfileIconDisplay)

        self.EditStyle = self.UnifiedStyleSheet + ' border-style: solid; border-color: #efefef; background-color: #fff; border-width: 2px; border-radius: 8px;'

        self.ProfileIconButton = QToolButton()
        self.ProfileIconButton.setStyleSheet(self.EditStyle)
        self.ProfileIconButton.setText('Select an icon (square images only)')
        self.ProfileIconButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.ProfileIconButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ProfileIconButton.clicked.connect(self.SelectIcon)
        self.CreateNewLocalUserWidget.layout().addWidget(self.ProfileIconButton)

        self.ProfileNameEdit = QLineEdit()
        self.ProfileNameEdit.setStyleSheet(self.EditStyle)
        self.ProfileNameEdit.setPlaceholderText('Username*')
        self.CreateNewLocalUserWidget.layout().addWidget(self.ProfileNameEdit)

        self.ProfilePasswordEdit = QLineEdit()
        self.ProfilePasswordEdit.setPlaceholderText('Password (set blank if you want no-password entry)')
        self.ProfilePasswordEdit.setStyleSheet(self.EditStyle)
        self.ProfilePasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.CreateNewLocalUserWidget.layout().addWidget(self.ProfilePasswordEdit)

        self.ProfilePasswordConfirm = QLineEdit()
        self.ProfilePasswordConfirm.setPlaceholderText('Confirm password (if any)')
        self.ProfilePasswordConfirm.setStyleSheet(self.EditStyle)
        self.ProfilePasswordConfirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.CreateNewLocalUserWidget.layout().addWidget(self.ProfilePasswordConfirm)

        Remark = QLabel()
        Remark.setText('* - necessary')
        Remark.setStyleSheet('color: #777;')
        self.CreateNewLocalUserWidget.layout().addWidget(Remark)
        
        self.CreateNewLocalUserButton = QToolButton()
        self.CreateNewLocalUserButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.CreateNewLocalUserButton.setText('Create')
        self.CreateNewLocalUserButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 14px; font-weight: bold;')
        self.CreateNewLocalUserButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.CreateNewLocalUserButton.clicked.connect(self.CreateNewLocalUser)
        self.CreateNewLocalUserWidget.layout().addWidget(self.CreateNewLocalUserButton)

    def Return(self):
        ProfileSelector.ShowObject(self.AppManager)
        self.close()

    def SelectIcon(self):
        ImagePath = QFileDialog.getOpenFileName(self, 'Choose an image', '', 'JPEG (*.jpeg, *.jpg);;PNG (*.png)')[0]
        self.ProfileIcon = QPixmap(ImagePath)
        Ratio = self.ProfileIcon.width() / self.ProfileIcon.height()
        if not (0.96 <= Ratio <= 1.04):
            QMessageBox.warning(self, 'Hey!', 'Only square images can be an icon!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return None
        self.ProfileIcon = self.ProfileIcon.scaled(128, 128, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ProfileIconDisplay.setPixmap(self.ProfileIcon)

    def CreateNewLocalUser(self):
        ASCII = ''.join(chr(k) for k in range(128))
        Name = self.ProfileNameEdit.text()
        Password = self.ProfilePasswordEdit.text()
        for Char in Password:
            if Char not in ASCII:
                QMessageBox.warning(self, 'Hey!', 'Only letters A-z, digits 0-9 and ASCII-symbols are accepted in password', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                return None

        if len(Password) < 6 and len(Password) != 0:
            QMessageBox.warning(self, 'Hey!', 'The length of the password should be more than or equals 6', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return None

        if self.ProfilePasswordConfirm.text() != Password:
            QMessageBox.warning(self, 'Hey!', 'Password and its confirmation are inequal', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return None

        with sql.connect(_LocalUsersDatabase) as Database:
            Cursor = Database.cursor()
            Request = "SELECT id FROM localUsers WHERE name = ?"
            CheckList = Cursor.execute(Request, (Name,)).fetchone()

            if CheckList is not None:
                QMessageBox.warning(self, 'Hey!', 'User with that name exists already', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                return None

            UserPath = os.path.join(os.getenv('APPDATA'), 'Jantar', 'Users')

            Request = "INSERT INTO localUsers (name, userFolder) VALUES (?, ?)"
            Cursor.execute(Request, (Name, UserPath))

            Request = "SELECT MAX(id) FROM localUsers"
            Id = Cursor.execute(Request).fetchone()[0]

            UserPath = os.path.join(os.getenv('APPDATA'), 'Jantar', 'Users', str(Id))

            Request = "UPDATE localUsers SET userFolder = ? WHERE id = ?"
            Cursor.execute(Request, (UserPath, Id))

            if len(Password) == 0:
                pass
            else:
                Hasher = argon2.PasswordHasher()
                Password = Hasher.hash(Password)
                Request = "UPDATE localUsers SET password = ? WHERE id = ?"
                Cursor.execute(Request, (Password, Id))
        Database.close()

        CachePath = os.path.join(UserPath, 'Cache')
        os.makedirs(CachePath, exist_ok=True)
        PersistentPath = os.path.join(UserPath, 'Persistent')
        os.makedirs(PersistentPath, exist_ok=True)

        Img = self.ProfileIcon.toImage()
        ImgPath = os.path.join(UserPath, 'Icon.png')
        Img = Img.save(ImgPath, 'PNG', 64)

        with sql.connect(os.path.join(UserPath, 'Data.db')) as Database:
            Cursor = Database.cursor()

            RequestCreate = """CREATE TABLE IF NOT EXISTS safetySettings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value TEXT)"""
            Request = "INSERT INTO safetySettings (name, value) VALUES (?, ?)"
            Cursor.execute(RequestCreate)
            Cursor.execute(Request, ('HttpsOnly', 1))
            Cursor.execute(Request, ('NecessaryCookiesOnly', 1))
            Cursor.execute(Request, ('CertificatePolicy', 1))
            Cursor.execute(Request, ('BlockExternalRequests', 1))

            RequestCreate = RequestCreate.replace('safetySettings', 'userSettings')
            Request = "INSERT INTO userSettings (name, value) VALUES (?, ?)"
            Cursor.execute(RequestCreate)
            Cursor.execute(Request, ('Homepage', ''))
            Cursor.execute(Request, ('SearchEngineByDefault', 1))
            Cursor.execute(Request, ('CacheFolder', CachePath))
            Cursor.execute(Request, ('PersistentFolder', PersistentPath))

            RequestCreate = """CREATE TABLE IF NOT EXISTS downloadsReg (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT,
                size TEXT,
                datetime TEXT)"""
            Cursor.execute(RequestCreate)
        Database.close()

        print('New local profile has been created')
        self.AppManager.StartBrowser(self, Id)


def ShowObject(AppManager):
    global _WIDGET

    _WIDGET = Object(AppManager)
    _WIDGET.show()
