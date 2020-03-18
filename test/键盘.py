from PyQt5.QtWidgets import QApplication, QWidget,QLabel,QPushButton, QListWidget, QMessageBox
import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("窗口测试")
        self.resize(300,500)
        self.mylist = QListWidget(self)
        self.mylist.addItems(["good", "1"])
        self.mylist.doubleClicked.connect(self.mylist_doubleclicked)


    def mylist_doubleclicked(self):
        QMessageBox.about(self, "hello", "kugou")

if __name__=='__main__':
    app=QApplication(sys.argv)  #创建应用
    ui = UI()
    ui.show()
    sys.exit(app.exec_())