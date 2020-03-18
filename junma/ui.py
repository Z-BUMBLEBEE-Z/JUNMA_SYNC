import sys
from junma.window import WindowManager
from junma.keybd_hook import KBHook
from junma.mylib import VERSION, ICON, KB_VK_MAP, KB_INFO, VK_SCAN_AVAIABLE, ARRANGE_1_4, ARRANGE_2_3, ARRANGE_4_1, \
    UNSELECTED,YES_ICON
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget,
                             QApplication,
                             QListWidget,
                             QListWidgetItem,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QRadioButton,
                             QButtonGroup,
                             QMessageBox,
                             QLabel,
                             QCheckBox,
                             QFrame,
                             QInputDialog,
                             QSystemTrayIcon,
                             QAction,
                             QMenu)


class UI(QWidget):
    def __init__(self, app):
        super().__init__()
        self.handlemanager = WindowManager()
        self.hookmanager = KBHook()
        self.initUI()
        self.initFunc()
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)

    def initUI(self):
        self.setGeometry(300, 300, 370, 220)
        self.setWindowIcon(QIcon(ICON))
        self.setWindowTitle(f"骏马同步器 v.{VERSION}")
        self.mainwindow_layout = QVBoxLayout()
        self.setLayout(self.mainwindow_layout)
        self.YES_ICON = QIcon(YES_ICON)

        # 窗口监听选择
        self.window_select_layout = QHBoxLayout()
        self.window_btn_layout = QVBoxLayout()
        self.window_handles_list = QListWidget()
        self.window_select_btn = QPushButton("监听")
        self.window_unselect_btn = QPushButton("取消监听")
        self.window_flush_btn = QPushButton("刷新窗口")
        self.window_sort_btn = QPushButton("自动排序")
        self.window_unselect_btn.setEnabled(False)

        UI.addWidgets(self.window_btn_layout, (self.window_select_btn, self.window_unselect_btn, self.window_flush_btn, self.window_sort_btn))
        self.window_select_layout.addWidget(self.window_handles_list)
        self.window_select_layout.addLayout(self.window_btn_layout)
        self.mainwindow_layout.addLayout(self.window_select_layout)

        # 分割线条
        self.add_split_hline()

        # 按键屏蔽
        self.exceptkey_layout = QHBoxLayout()
        self.exceptkey_btn_layout = QVBoxLayout()
        self.exceptkey_list = QListWidget()
        self.exceptkey_list.addItems(self.hookmanager.exceptkeys)
        self.exceptkey_add_btn = QPushButton("添加按键")
        self.exceptkey_move_btn = QPushButton("删除按键")
        self.exceptkey_clear_btn = QPushButton("清空按键")
        self.exceptkey_checkbox = QCheckBox("排除按键")
        UI.addWidgets(self.exceptkey_btn_layout,
                      (self.exceptkey_add_btn, self.exceptkey_move_btn, self.exceptkey_clear_btn,
                       self.exceptkey_checkbox))
        self.exceptkey_layout.addWidget(self.exceptkey_list)
        self.exceptkey_layout.addLayout(self.exceptkey_btn_layout)
        self.mainwindow_layout.addLayout(self.exceptkey_layout)

        # 分割线条
        self.add_split_hline()

        # 窗口布局
        self.arrange_layout = QHBoxLayout()
        self.arrange_grp = QButtonGroup()
        self.arrange_1_4 = QRadioButton("1:4布局")
        self.arrange_2_3 = QRadioButton("2:3布局")
        self.arrange_4_1 = QRadioButton("4:1布局")
        self.arrange_grp.addButton(self.arrange_1_4, id=ARRANGE_1_4)
        self.arrange_grp.addButton(self.arrange_2_3, id=ARRANGE_2_3)
        self.arrange_grp.addButton(self.arrange_4_1, id=ARRANGE_4_1)
        self.arrange_btn = QPushButton("排列窗口")

        # 必须先设置主控窗口才可以进行窗口排列，在后期可以采用设置每个进程的位置来完善
        self.arrange_layout.addWidget(self.arrange_1_4)
        self.arrange_layout.addWidget(self.arrange_2_3)
        self.arrange_layout.addWidget(self.arrange_4_1)
        self.arrange_layout.addWidget(self.arrange_btn)
        self.mainwindow_layout.addLayout(self.arrange_layout)

        # 分割线条
        self.add_split_hline()

        # 功能按钮
        self.func_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始同步")
        self.stop_btn = QPushButton("暂停同步")
        self.func_layout.addWidget(self.start_btn)
        self.func_layout.addWidget(self.stop_btn)
        self.mainwindow_layout.addLayout(self.func_layout)

        # 同步器状态
        self.status_layout = QHBoxLayout()
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status_layout.addWidget(self.status)
        self.mainwindow_layout.addLayout(self.status_layout)


        # 托盘菜单
        self.tray_menu = QMenu()
        self.sync_action = QAction("同步窗口")
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


    def initFunc(self):
        # 窗口监听选择
        self.window_select_btn.clicked.connect(self.window_select_btn_clicked)
        self.window_unselect_btn.clicked.connect(self.window_unselect_btn_clicked)
        self.window_flush_btn.clicked.connect(self.window_flush_btn_clicked)

        # 按键屏蔽
        self.exceptkey_add_btn.clicked.connect(self.exceptkey_add_btn_clicked)
        self.exceptkey_move_btn.clicked.connect(self.exceptkey_move_btn_clicked)
        self.exceptkey_clear_btn.clicked.connect(self.exceptkey_clear_btn_clicked)
        self.exceptkey_checkbox.toggled.connect(self.exceptkey_checkbox_toggled)
        # 窗口布局
        self.window_handles_list.doubleClicked.connect(self.window_handles_list_doubleClicked)
        self.arrange_btn.clicked.connect(self.arrange_btn_clicked)
        self.window_sort_btn.clicked.connect(self.window_sort_btn_clicked)
        # 功能按钮
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.stop_btn.clicked.connect(self.stop_btn_clicked)
        # 系统托盘
        self.sync_action.triggered.connect(self.sync_action_triggered)
        self.exceptkeys_action.triggered.connect(self.exceptkey_checkbox.toggle)
        self.quit_action.triggered.connect(self.close)
        self.tray.activated.connect(self.tray_activated)

    # 窗口选择
    def window_select_btn_clicked(self):
        if self.hookmanager.hook:
            QMessageBox.about(self, "监听窗口失败", "请先退出同步再监听窗口")
        item = self.window_handles_list.currentItem()  # type:QListWidgetItem
        if item == None:
            QMessageBox.about(self, "未选取窗口", "请选择要监听的窗口！")
            return
        select_row = self.window_handles_list.currentIndex().row()
        self.handlemanager.set_mainwindow(self.handlemanager.windows_handles[select_row])
        self.handlemanager.main_window['selected'] = '监听端'
        self.window_unselect_btn.setEnabled(True)
        self.window_select_btn.setEnabled(False)
        self.window_flush_btn.setEnabled(False)
        self.flush_window_list()

    def window_unselect_btn_clicked(self):
        del self.handlemanager.main_window["selected"]
        self.handlemanager.main_window = None
        self.window_select_btn.setEnabled(True)
        self.window_flush_btn.setEnabled(True)
        self.window_unselect_btn.setEnabled(False)
        self.flush_window_list()

    def flush_window_list(self):
        windows = []
        self.window_handles_list.clear()
        for window in self.handlemanager.windows_handles:
            windows.append(f"{window['title']} - {window['pid'][-1]} - {window.get('selected', '客户端')} - 窗口位置："
                           f"{window.get('index', '未配置')}")
        self.window_handles_list.addItems(windows)
        # if self.handlemanager.main_window:
        #     self.hookmanager.set_others(self.handlemanagers)

    def window_flush_btn_clicked(self):
        '''刷新窗口
        1. 清理List表格
        2. 从window实例中获取窗口
            2_1. window实例刷新窗口
        3. 显示窗口
        '''
        self.handlemanager.flush_window()
        self.handlemanager.findWindows()
        self.flush_window_list()

    # 按键屏蔽
    def exceptkey_checkbox_toggled(self):
        if self.exceptkey_checkbox.isChecked():
            self.hookmanager.start_except_key()
            self.exceptkeys_action.setIcon(self.YES_ICON)
        else:
            self.hookmanager.stop_except_key()
            self.exceptkeys_action.setIcon(QIcon())

    def exceptkey_add_btn_clicked(self):
        keys, ok = QInputDialog.getText(self, "添加排除键", "请输入需要排除的键：（只支持单字符小写，如果需要增加多个值，请用空格分开）\n"
                                                       "直接输入数字屏蔽的为上方数字键，并非屏蔽小写键盘，如需屏蔽小写键盘，请在字符前加x，如1，则输入x1\n"
                                                       f"{KB_INFO}")
        if ok:
            keys = keys.split()
            for key in keys:  # type: str
                if key in VK_SCAN_AVAIABLE or key in KB_VK_MAP.keys():
                    continue
                else:
                    QMessageBox.about(self, "输入错误！", "输入字符有问题，请看输出提示")
                    return
        self.hookmanager.exceptkeys.extend(set(keys) - set(self.hookmanager.exceptkeys))
        # 判断目前的排除键状态
        self.flush_exceptkey_list()

    def exceptkey_move_btn_clicked(self):
        index = self.exceptkey_list.currentIndex().row()
        if index == UNSELECTED:
            QMessageBox.about(self, "未选择需要删除的键", "请选中相应项后再执行该操作！")
        else:
            del self.hookmanager.exceptkeys[index]
        self.flush_exceptkey_list()

    def exceptkey_clear_btn_clicked(self):
        self.hookmanager.exceptkeys.clear()
        self.flush_exceptkey_list()

    def flush_exceptkey_list(self):
        self.exceptkey_checkbox_toggled()
        self.exceptkey_list.clear()
        self.exceptkey_list.addItems(self.hookmanager.exceptkeys)
        self.hookmanager.write_exceptkeys()

    # 排列窗口
    def window_handles_list_doubleClicked(self):
        handle_index = self.window_handles_list.currentIndex().row()
        if 'index' in self.handlemanager.windows_handles[handle_index].keys():
            del self.handlemanager.windows_handles[handle_index]['index']
            self.flush_window_list()
        else:
            index_value, ok = QInputDialog.getInt(self, "输入位置", "请输入该窗口要放置的位置", min=1, max=5)
            if ok:
                self.handlemanager.windows_handles[handle_index]['index'] = index_value
                self.flush_window_list()

    def window_sort_btn_clicked(self):
        current_index = [window.get("index") for window in self.handlemanager.windows_handles if window.get("index")]
        indexs = list(range(1, len(self.handlemanager.windows_handles)+1))
        for index in current_index:
            try:
                indexs.remove(index)
            except ValueError:
                continue
        indexs.reverse()
        for window in self.handlemanager.windows_handles:
            if "index" not in window:
                index = indexs.pop()
                window['index'] = index
        self.flush_window_list()


    def arrange_btn_clicked(self):
        id = self.arrange_grp.checkedId()
        if id != UNSELECTED:
            self.handlemanager.set_windows_pos(id)
            for window in self.handlemanager.windows_handles:
                print(window,type(window.get('index')))

    # 窗口监听
    def start_btn_clicked(self):
        if self.handlemanager.main_window == None:
            QMessageBox.about(self, "同步失败", "未选择监听窗口或者已经加载")
            return
        if self.hookmanager.hook:
            QMessageBox.about(self, "同步失败", "同步程序已经加载，无需重新同步")
            return
        self.hookmanager.start(self.handlemanager)
        self.status.setText("已开始同步")
        self.sync_action.setIcon(self.YES_ICON)

    def stop_btn_clicked(self):
        if self.hookmanager.hook == None:
            QMessageBox.about(self, "取消同步失败", "还没开始监听就急着关？")
            return
        self.hookmanager.stop()
        self.status.setText("已暂停同步")
        self.sync_action.setIcon(QIcon())

    # 托盘
    def sync_action_triggered(self):
        if self.hookmanager.hook:
            self.stop_btn.click()
        else:
            self.start_btn.click()

    def tray_activated(self, reason):
        if reason ==3:
            self.tray.hide()
            self.show()
            self.showNormal()

    def add_split_hline(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.mainwindow_layout.addWidget(line)

    @staticmethod
    def addWidgets(layout, widgets):
        for widget in widgets:
            layout.addWidget(widget)

    def closeEvent(self, event):
        self.handlemanager.flush_window()
        if self.hookmanager != None:
            pass
        self.hookmanager.stop()
        # 对UI进行处理
        self.tray_menu.close()
        self.app.quit()


    def changeEvent(self, event):
        if event.type() == event.WindowStateChange and self.windowState() == Qt.WindowMinimized:
            self.hide()
            self.tray.show()


def init():
    app = QApplication(sys.argv)
    ui = UI(app)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    init()
