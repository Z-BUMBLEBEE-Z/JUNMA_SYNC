import sys
import PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("系统托盘测试")
        self.setWindowIcon(QIcon("lib/icon.png"))
        self.setGeometry(300,400,500,500)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.box = QCheckBox("你猜猜")
        layout.addWidget(self.box)

        # 托盘菜单
        self.tray_menu = QMenu()
        self.sync_action = QAction("同步窗口")
        # self.sync_action.setIcon(QIcon("lib/start.png"))
        self.exceptkeys_action = QAction("键盘排除")
        self.quit_action = QAction("退出窗口")
        self.tray_menu.addAction(self.sync_action)
        self.tray_menu.addAction(self.exceptkeys_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)

        # 系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("lib/icon.png"))
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()


        self.btn = QPushButton("显示/隐藏托盘", self)
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.btn_clicked)
        self.tray.activated.connect(self.tray_activated)
        self.sync_action.triggered.connect(self.sync_action_triggered)
        self.box.toggled.connect(self.box_toggled)

    def sync_action_triggered(self):
        self.box.toggle()

    def box_toggled(self):
        print("box toggle")

    def btn_clicked(self):
        print(self.tray.isSystemTrayAvailable())
        print(self.tray.supportsMessages())
        self.tray.showMessage("通知","按钮被点开了")
        self.sync_action.setIcon(QIcon())
        self.box.toggle()

    def tray_activated(self, reason):
        # reason
        # 双击：2  右键：1
        if reason == 2 or reason == 3:
            self.show()
        if reason == 4:
            self.close()

    def changeEvent(self, event:PyQt5.QtCore.QEvent):
        if event.type() == event.WindowStateChange:
            if self.windowState() == Qt.WindowMinimized:
                self.tray.show()
                self.hide()
                event.ignore()

    def closeEvent(self, event:QCloseEvent):
        box = QMessageBox.information(self, "1","1",QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        print(QMessageBox.Yes)
        print(box)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    exit(app.exec_())