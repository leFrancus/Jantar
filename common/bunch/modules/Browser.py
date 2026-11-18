from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QProgressBar, QSizePolicy, QToolButton, QTabBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QEvent, QTimer, QUrl
from pathlib import Path
import sqlite3 as sql
from . import ProfileMini
import os

_LocalUsersDatabase = Path(__file__).resolve().parent.parent.parent / 'data/LocalUsers.db'
_SearchEnginesDatabase = Path(__file__).resolve().parent.parent.parent / 'data/SearchEngines.sqlite'


class Object(QWidget):
    def __init__(self, WebProfileId: int, AppManager):
        super().__init__()

        # PROFILE
        self.WebProfileId = WebProfileId
        self.AppManager = AppManager
        if self.WebProfileId != -1:
            with sql.connect(_LocalUsersDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT name, userFolder FROM localUsers WHERE id = ?"
                WebProfileName, self.WebProfilePath = Cursor.execute(Request, (self.WebProfileId,)).fetchone()
            self.WebProfile = QWebEngineProfile(WebProfileName, self)
        # END

        self.WebViewRegister = []
        self.CurrentWebViewIndex = 0
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
        
        self.setStyleSheet('background: #f4f4f4;')

        self.Icon = str(Path(__file__).resolve().parent.parent / 'images' / 'Icon.ico')
        self.Icon = QIcon(self.Icon)

        self.setWindowTitle('Jantar')
        self.setWindowIcon(self.Icon)
        self.setMinimumSize(640, 480)

        self.WindowLayout = QVBoxLayout(self)
        self.WindowLayout.setContentsMargins(0, 0, 0, 0)
        self.WindowLayout.setSpacing(0)

        self.LoadingProgressBar = QProgressBar()
        self.LoadingProgressBar.setStyleSheet(self.ProgressStyleSheet)
        self.LoadingProgressBar.setTextVisible(False)
        self.LoadingProgressBar.setFixedHeight(4)
        self.WindowLayout.addWidget(self.LoadingProgressBar)

        self.ActionBar = QFrame()
        self.ActionBar.setFixedHeight(40)
        self.ActionBar.setLayout(QHBoxLayout())
        self.ActionBar.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ActionBar.layout().setContentsMargins(1, 1, 1, 1)
        self.ActionBar.layout().setSpacing(0)
        self.WindowLayout.addWidget(self.ActionBar)

        self.ActionButtonStyle = self.UnifiedStyleSheet + ' border-style: solid none none none; border-color: #d4d4d4; border-width: 2px; font-size: 12px;'

        self.UndoButton = QToolButton()
        self.UndoButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.UndoButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.UndoButton.setStyleSheet(self.ActionButtonStyle)
        self.UndoButton.setFixedHeight(self.ActionBar.height() - 2)
        self.UndoButton.setFixedWidth(self.UndoButton.height() - 6)
        self.UndoButton.setText('↩')
        self.ActionBar.layout().addWidget(self.UndoButton)

        self.RedoButton = QToolButton()
        self.RedoButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.RedoButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.RedoButton.setStyleSheet(self.ActionButtonStyle)
        self.RedoButton.setFixedHeight(self.ActionBar.height() - 2)
        self.RedoButton.setFixedWidth(self.RedoButton.height() - 6)
        self.RedoButton.setText('↪')
        self.ActionBar.layout().addWidget(self.RedoButton)

        self.SearchButton = QToolButton()
        self.SearchButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.SearchButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.SearchButton.setStyleSheet(self.ActionButtonStyle)
        self.SearchButton.setFixedHeight(self.ActionBar.height() - 2)
        self.SearchButton.setFixedWidth(self.SearchButton.height() - 6)
        self.SearchButton.setText('⌕')
        self.ActionBar.layout().addWidget(self.SearchButton)

        self.SearchEdit = QLineEdit('')
        self.SearchEdit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        self.SearchEdit.setFixedWidth(256)
        self.SearchEditStyle = self.UnifiedStyleSheet + ' border-style: solid none none none; border-color: #d4d4d4; border-width: 2px;'
        self.SearchEdit.setStyleSheet(self.SearchEditStyle)
        self.SearchEdit.setPlaceholderText('Search...')
        self.ActionBar.layout().addWidget(self.SearchEdit)

        self.SearchEdited = False

        self.ReloadButton = QToolButton()
        self.ReloadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.LastButtonStyle = self.UnifiedStyleSheet + ' border-style: solid solid none none; border-color: #d4d4d4; border-width: 2px; font-size: 12px;'
        self.ReloadButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ReloadButton.setStyleSheet(self.LastButtonStyle)
        self.ReloadButton.setFixedHeight(self.ActionBar.height() - 2)
        self.ReloadButton.setFixedWidth(self.ReloadButton.height() - 6)
        self.ReloadButton.setText('↺')
        self.ActionBar.layout().addWidget(self.ReloadButton)

        self.LoadingRightNow = False

        self.TabWidget = QWidget()
        self.TabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.TabWidget.setStyleSheet(self.SearchEditStyle)
        self.TabWidget.setLayout(QHBoxLayout())
        self.TabWidget.layout().setContentsMargins(4, 4, 4, 4)
        self.ActionBar.layout().addWidget(self.TabWidget)

        self.TabArea = QTabBar()
        self.TabStyle = """QTabBar::tab {
            background: #fff;
            border-style: solid;
            border-color: #efefef;
            border-width: 2px;
            border-radius: 12px;
            padding: 4px 8px 4px 8px;
            margin: 0 2px 0 2px;
        }
        QTabBar::tab:selected {
            background: #fff;
            border-style: solid;
            border-color: #efefef;
            border-width: 2px;
            border-radius: 12px;
            padding: 4px 8px 4px 8px;
            margin: 0 2px 0 2px;
        }"""
        self.TabArea.setStyleSheet(self.TabStyle)
        self.TabArea.setCursor(Qt.CursorShape.PointingHandCursor)
        self.TabWidget.layout().addWidget(self.TabArea)
        self.TabArea.setIconSize(QSize(16, 16))

        self.NewTab = QToolButton()
        self.NewTab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.NewTab.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.NewTab.setStyleSheet(self.LastButtonStyle)
        self.NewTab.setFixedHeight(self.ActionBar.height() - 2)
        self.NewTab.setFixedWidth(self.NewTab.height() - 6)
        self.NewTab.setText('+')
        self.ActionBar.layout().addWidget(self.NewTab)

        self.IsCreatingHoldOn = False

        self.AccountMenuButton = QToolButton()
        self.AccountMenuButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.AccountStyle = self.UnifiedStyleSheet + ' border-style: solid none none none; border-color: #d4d4d4; border-width: 2px; padding: 0;'
        self.AccountMenuButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.AccountMenuButton.setStyleSheet(self.AccountStyle)
        self.AccountMenuButton.setFixedHeight(self.ActionBar.height() - 2)
        self.AccountMenuButton.setFixedWidth(self.AccountMenuButton.height())
        self.AccountMenuButton.clicked.connect(lambda: ProfileMini.ShowObject(self.WebProfileId, self.AppManager))
        if self.WebProfileId == -1:
            Icon = QIcon(str(Path(__file__).resolve().parent.parent / 'images/PrivateUser.png'))
        else:
            with sql.connect(_LocalUsersDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT userFolder FROM localUsers WHERE id = ?"
                self.UserPath = Cursor.execute(Request, (self.WebProfileId,)).fetchone()[0]
                PathToIcon = os.path.join(self.UserPath, 'Icon.png')
                Icon = QIcon(PathToIcon)
            Database.close()
        self.AccountMenuButton.setIconSize(QSize(self.AccountMenuButton.height(), self.AccountMenuButton.width()))
        self.AccountMenuButton.setIcon(Icon)
        self.ActionBar.layout().addWidget(self.AccountMenuButton)

        if self.WebProfileId != -1:
            self.UserDatabase = os.path.join(self.UserPath, 'Data.db')
            with sql.connect(self.UserDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT value FROM userSettings WHERE name = 'SearchEngineByDefault'"
                SearchEngineId = int(Cursor.execute(Request).fetchone()[0])
            Database.close()
            with sql.connect(_SearchEnginesDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT baseLink, requestLink FROM searchEngines WHERE id = ?"
                self.EngineLink, self.RequestLink = Cursor.execute(Request, (SearchEngineId,)).fetchone()
            Database.close()
        else:
            with sql.connect(_SearchEnginesDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT baseLink, requestLink FROM searchEngines WHERE id = ?"
                self.EngineLink, self.RequestLink = Cursor.execute(Request, (1,)).fetchone()
            Database.close()

        # CONNECTIONS
        self.UndoButton.clicked.connect(self.GoBack)
        self.RedoButton.clicked.connect(self.GoForward)
        self.ReloadButton.clicked.connect(self.Reload)
        self.SearchEdit.textEdited.connect(self.ChangeSearchEdited)
        self.SearchButton.clicked.connect(lambda: self.ExecReq(IsSelf=False))
        self.NewTab.clicked.connect(lambda: self.CreateNewTab())
        self.SearchEdit.installEventFilter(self)

        # START
        self.CreateNewTab(JustOpened=True)
        self.CheckWebMovement()

        # OTHER CONNECTIONS
        self.TabArea.currentChanged.connect(self.ChangeTab)

    def eventFilter(self, watched, event):
        if watched is self.SearchEdit and event.type() == QEvent.Type.FocusIn and not self.SearchEdited:
            self.SearchEdit.setText(self.CurrentWebUrl.toString())
            QTimer.singleShot(0, self.SearchEdit.selectAll)
            self.SearchEdit.selectAll()
        elif watched is self.SearchEdit and event.type() == QEvent.Type.FocusOut and not self.SearchEdited:
            self.SearchEdit.setText(self.CurrentWebTitle)
        return super().eventFilter(watched, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and self.SearchEdit.hasFocus():
            self.ExecReq(IsSelf=False)

    def CreateNewTab(self, Name='New tab', JustOpened=False):
        self.IsCreatingHoldOn = True
        Index = self.TabArea.count()
        self.TabArea.addTab(Name)
        self.__setattr__(f'WebInterface_{Index}', QWebEngineView())
        WebInterface = self.__getattribute__(f'WebInterface_{Index}')
        if self.WebProfileId != -1:
            Page = QWebEnginePage(self.WebProfile, WebInterface)
            WebInterface.setPage(Page)
        WebInterface.setStyleSheet('background: f4f4f4;')
        WebInterface.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        WebInterface.loadStarted.connect(self.StartWebLoad)
        WebInterface.loadProgress.connect(self.LoadingProgressBar.setValue)
        WebInterface.loadFinished.connect(lambda: self.FinishWebLoad(WebInterface))
        WebInterface.iconChanged.connect(lambda: self.TabArea.setTabIcon(Index, WebInterface.icon()))
        WebInterface.page().fullScreenRequested.connect(self._HandleFullScreen)
        self.WebViewRegister.append(WebInterface)
        self.WebViewRegister[self.CurrentWebViewIndex].hide()
        self.WindowLayout.insertWidget(1, WebInterface)
        WebInterface.show()
        self.TabArea.setCurrentIndex(Index)
        self.CurrentWebViewIndex = Index
        self.IsCreatingHoldOn = False
        self.ExecReq(IsSelf=True)
        if JustOpened and self.WebProfileId != -1:
            with sql.connect(self.UserDatabase) as Database:
                Cursor = Database.cursor()
                Request = "SELECT value FROM userSettings WHERE name = ?"
                self.Homepage = Cursor.execute(Request, ('Homepage',)).fetchone()[0]
            Database.close()
            self.ExecReq(Homepage=True)
        else:
            self.ExecReq(IsSelf=True)

    def ChangeTab(self):   
        if self.IsCreatingHoldOn:
            return None

        try:
            Index = self.CurrentWebViewIndex
            OldWebInterface = self.__getattribute__(f'WebInterface_{Index}')
            OldWebInterface.hide()

            NewWebInterface = self.__getattribute__(f'WebInterface_{self.TabArea.currentIndex()}')
            self.CurrentWebTitle = NewWebInterface.title()
            self.CurrentWebUrl = NewWebInterface.url()
            self.SearchEdit.clearFocus()
            self.SearchEdit.setText(self.CurrentWebTitle)
            NewWebInterface.show()
            self.setWindowTitle(self.CurrentWebTitle)
            self.CurrentWebViewIndex = self.TabArea.currentIndex()
            self.CheckWebMovement()
        except Exception:
            return None

    def ChangeSearchEdited(self):
        self.SearchEdited = True

    def ExecReq(self, IsSelf=False, Homepage=False):
        if IsSelf:
            Request = self.EngineLink
            self.WebViewRegister[self.CurrentWebViewIndex].load(Request)
            return None
        elif Homepage:
            Request = self.Homepage
        else:
            Request = self.SearchEdit.text().strip(' \t')
        try:
            ReqTemp = QUrl.fromUserInput(Request)
            ReqHost = ReqTemp.host()
            if not ReqTemp.isValid() or not ('.' in ReqHost or '://' in ReqHost) or ReqHost.startswith('.') or ReqHost.endswith('.'):
                raise TypeError
            else:
                Request = ReqTemp
        except Exception:
            Request = self.RequestLink + Request.replace(' ', '+')
        finally:
            self.WebViewRegister[self.CurrentWebViewIndex].load(Request)

    def StartWebLoad(self):
        self.SearchEdited = False
        self.ReloadButton.setText('⨉')
        self.LoadingRightNow = True

    def FinishWebLoad(self, Web):
        self.LoadingRightNow = False
        self.SearchEdited = False
        self.LoadingProgressBar.setValue(0)
        self.CurrentWebTitle, self.CurrentWebUrl = Web.title(), Web.url()
        self.SearchEdit.clearFocus()
        self.SearchEdit.setText(self.CurrentWebTitle)
        self.setWindowTitle(self.CurrentWebTitle)
        self.TabArea.setTabText(self.CurrentWebViewIndex, self.CurrentWebTitle)
        self.CheckWebMovement()
        self.ReloadButton.setText('↺')

    def CheckWebMovement(self):
        History = self.WebViewRegister[self.CurrentWebViewIndex].history()
        YesStyle, NoStyle = self.ActionButtonStyle + ' color: #0a0a0a;', self.ActionButtonStyle + ' color: #727272;'
        if not History.canGoBack():
            self.UndoButton.setStyleSheet(NoStyle)
            self.UndoButton.setEnabled(False)
            self.UndoButton.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.UndoButton.setStyleSheet(YesStyle)
            self.UndoButton.setEnabled(True)
            self.UndoButton.setCursor(Qt.CursorShape.PointingHandCursor)

        if not History.canGoForward():
            self.RedoButton.setStyleSheet(NoStyle)
            self.RedoButton.setEnabled(False)
            self.RedoButton.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.RedoButton.setStyleSheet(YesStyle)
            self.RedoButton.setEnabled(True)
            self.RedoButton.setCursor(Qt.CursorShape.PointingHandCursor)

    def GoBack(self):
        self.WebViewRegister[self.CurrentWebViewIndex].back()
        self.CheckWebMovement()

    def GoForward(self):
        self.WebViewRegister[self.CurrentWebViewIndex].forward()
        self.CheckWebMovement()

    def Reload(self):
        if not self.LoadingRightNow:
            self.LoadingRightNow = True
            self.WebViewRegister[self.CurrentWebViewIndex].reload()
            self.ReloadButton.setText('⨉')
        else:
            self.LoadingRightNow = False
            self.SearchEdited = False
            self.WebViewRegister[self.CurrentWebViewIndex].stop()
            self.ReloadButton.setText('↺')


    def _HandleFullScreen(self, Request):
        if Request.toggleOn():
            self.showFullScreen()
            self._ToggleActionBar()
        else:
            self.showMaximized()
            self._ToggleActionBar()
        Request.accept()

    def _ToggleActionBar(self):
        if self.ActionBar.isHidden():
            self.ActionBar.show()
        else:
            self.ActionBar.hide()
