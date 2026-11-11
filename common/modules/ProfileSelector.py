from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QScrollArea, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from pathlib import Path
import sqlite3 as sql
import Main
import os

_WIDGET = None
_LocalUsersDatabase = 'data/LocalUsers.sqlite'


class Object(QWidget):
    def __init__(self, AppManager):
        super().__init__()

        self.AppManager = AppManager
        self.WebProfilesList = []

        self.CurrentWebProfileIndex = 0
        self.UnifiedStyleSheet = "background: #1f1f1f; font-family: 'Inter'; border: none; padding-left: 4px; padding-right: 4px; color: #f4f4f4;"
        self.setStyleSheet(self.UnifiedStyleSheet)
        
        self.Icon = str(Path(__file__).resolve().parent.parent / 'images' / 'Icon.ico')
        self.Icon = QIcon(self.Icon)

        self.setWindowTitle(' ')
        self.setWindowIcon(self.Icon)
        self.setMinimumSize(1000, 600)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Title = QLabel()
        self.Title.setText('Choose a local profile')
        self.Title.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 24px; font-weight: bold;')
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.Title)

        self.ScrollArea = QScrollArea()
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setStyleSheet(self.UnifiedStyleSheet)
        self.layout().addWidget(self.ScrollArea)

        self.SelectArea = QWidget()
        self.SelectArea.setLayout(QHBoxLayout())
        self.SelectArea.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.ScrollArea.setWidget(self.SelectArea)

        with sql.connect(Main._MainPath.parent / _LocalUsersDatabase) as Database:
            Cursor = Database.cursor()
            Request = "SELECT * FROM localUsers"
            self.LocalProfilesData = Cursor.execute(Request).fetchall()
        self.LoadUsers()

    def LoadUsers(self):
        # GENERATING USERS WIDGETS
        for LocalProfileData in self.LocalProfilesData:
            try:
                Id, Name, UserFolder = LocalProfileData
                self.__setattr__(f'JoinProfile_{Id}', QWidget())
                JoinProfile = self.__getattribute__(f'JoinProfile_{Id}')
                JoinProfile.setFixedWidth(180)
                JoinProfile.setLayout(QVBoxLayout())
                self.SelectArea.layout().addWidget(JoinProfile)

                ProfileIcon = QPixmap(os.path.join(UserFolder, 'Icon.jpg'))
                ProfileIcon = ProfileIcon.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                ProfileIconDisplay = QLabel()
                ProfileIconDisplay.setStyleSheet('margin-bottom: 4px;')
                ProfileIconDisplay.setPixmap(ProfileIcon)
                ProfileIconDisplay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                JoinProfile.layout().addWidget(ProfileIconDisplay)

                JoinProfileButton = QToolButton()
                JoinProfileButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                JoinProfileButton.setText(Name)
                JoinProfileButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 14px; font-weight: bold;')
                JoinProfileButton.setCursor(Qt.CursorShape.PointingHandCursor)
                JoinProfile.layout().addWidget(JoinProfileButton)

                self.WebProfilesList.append(Id)
            except Exception:
                pass
        # END

        # JOIN PRIVATE
        self.JoinPrivate = QWidget()
        self.JoinPrivate.setFixedWidth(180)
        self.JoinPrivate.setLayout(QVBoxLayout())
        self.SelectArea.layout().addWidget(self.JoinPrivate)
                
        ProfileIcon = QPixmap(str(Main._MainPath.parent / 'bunch/images/PrivateUser.png'))
        ProfileIcon = ProfileIcon.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        ProfileIconDisplay = QLabel()
        ProfileIconDisplay.setStyleSheet('margin-bottom: 4px;')
        ProfileIconDisplay.setPixmap(ProfileIcon)
        ProfileIconDisplay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.JoinPrivate.layout().addWidget(ProfileIconDisplay)
        
        self.JoinPrivateButton = QToolButton()
        self.JoinPrivateButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.JoinPrivateButton.setText('Private Mode')
        self.JoinPrivateButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 14px; font-weight: bold;')
        self.JoinPrivateButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.JoinPrivateButton.clicked.connect(lambda: self.AppManager.StartBrowser(True, self, -1))
        self.JoinPrivate.layout().addWidget(self.JoinPrivateButton)
        # END

        # CREATE NEW LOCAL USER
        self.CreateNewLocalUserWidget = QWidget()
        self.CreateNewLocalUserWidget.setFixedWidth(180)
        self.CreateNewLocalUserWidget.setLayout(QVBoxLayout())
        self.SelectArea.layout().addWidget(self.CreateNewLocalUserWidget)

        ProfileIcon = QPixmap(str(Main._MainPath.parent / 'bunch/images/UnknownUser.png'))
        ProfileIcon = ProfileIcon.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        ProfileIconDisplay = QLabel()
        ProfileIconDisplay.setStyleSheet('margin-bottom: 4px;')
        ProfileIconDisplay.setPixmap(ProfileIcon)
        ProfileIconDisplay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.CreateNewLocalUserWidget.layout().addWidget(ProfileIconDisplay)

        self.CreateNewLocalUserButton = QToolButton()
        self.CreateNewLocalUserButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.CreateNewLocalUserButton.setText('Create a new user')
        self.CreateNewLocalUserButton.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 14px; font-weight: bold;')
        self.CreateNewLocalUserButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.CreateNewLocalUserWidget.layout().addWidget(self.CreateNewLocalUserButton)
        # END


def ShowObject():
    global _WIDGET

    _WIDGET = Object()
    _WIDGET.show()
