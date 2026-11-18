from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QSizePolicy, QLineEdit, QComboBox, QFrame, QCheckBox, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from pathlib import Path
import sqlite3 as sql
import os
from . import ProfileMini

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
        self.WidgetStyle = self.UnifiedStyleSheet + " background: #fff; 2px solid #efefef;"


def ShowObject(WebProfileId: int):
    global _WIDGET

    _WIDGET = Object(WebProfileId)
    _WIDGET.show()

