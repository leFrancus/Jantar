from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel, QSizePolicy, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path
import sqlite3 as sql
import os
from . import ProfileSettings

_WIDGET = None
_LocalUsersDatabase = Path(__file__).resolve().parent.parent.parent / 'data/LocalUsers.db'


class Object(QWidget):
    def __init__(self, WebProfileId: int, AppManager):
        super().__init__()

        self.CurrentWebProfileId = WebProfileId
        self.AppManager = AppManager
        self.UnifiedStyleSheet = "background: #f4f4f4; font-family: 'Inter'; border: none; padding-left: 4px; padding-right: 4px; color: #0a0a0a;"
        self.ProgressStyleSheet = """QProgressBar {
                background: #f4f4f4;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: #ffd940;
                border-radius: 2px;
            }"""
        self.setStyleSheet(self.UnifiedStyleSheet)

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
        self.setFixedWidth(200)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.setLayout(QVBoxLayout())
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.UsernameLabel = QLabel()
        if self.CurrentWebProfileId == -1:
            Name = 'You are in private mode'
        else:
            with sql.connect(_LocalUsersDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT name FROM localUsers WHERE id = ?"
                Name = Cursor.execute(Request, (self.CurrentWebProfileId,)).fetchone()[0]
            Database.close()
        self.UsernameLabel.setText(Name)
        self.UsernameLabel.setStyleSheet(self.UnifiedStyleSheet + ' font-size: 22px; font-weight: bold;')
        self.UsernameLabel.setWordWrap(True)
        self.layout().addWidget(self.UsernameLabel)

        Line = QFrame()
        Line.setFrameShape(QFrame.Shape.HLine)
        Line.setFrameShadow(QFrame.Shadow.Sunken)
        Line.setStyleSheet("background-color: #efefef;")
        self.layout().addWidget(Line)

        if self.CurrentWebProfileId != -1:
            self.PreferencesButton = QToolButton()
            self.PreferencesButton.setStyleSheet(self.UnifiedStyleSheet)
            self.PreferencesButton.setText('⚙️ Preferences')
            self.PreferencesButton.setCursor(Qt.CursorShape.PointingHandCursor)
            self.PreferencesButton.clicked.connect(self.OpenSettings)
            self.layout().addWidget(self.PreferencesButton)

        Line = QFrame()
        Line.setFrameShape(QFrame.Shape.HLine)
        Line.setFrameShadow(QFrame.Shadow.Sunken)
        Line.setStyleSheet("background-color: #efefef;")
        self.layout().addWidget(Line)

        self.CloseButton = QToolButton()
        self.CloseButton.setStyleSheet(self.UnifiedStyleSheet)
        self.CloseButton.setText('↩ Back')
        self.CloseButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.CloseButton.clicked.connect(self.close)
        self.layout().addWidget(self.CloseButton)

    def OpenSettings(self):
        ProfileSettings.ShowObject(self.CurrentWebProfileId, self.AppManager)
        self.close()


def ShowObject(WebProfileId: int, AppManager):
    global _WIDGET

    _WIDGET = Object(WebProfileId, AppManager)
    _WIDGET.show()
