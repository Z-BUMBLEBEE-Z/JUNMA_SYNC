import win32gui
import win32api
import win32con
import win32process
import pywintypes
import ctypes
import junma.mylib
from junma.mylib import ARRANGE_1_4, ARRANGE_2_3, ARRANGE_4_1, get_rect_by_mode

WindowProcessId = 1
WindowThreadID = 0
CLASSNAME = "GxWindowClass"
WINDOWNAME = "魔兽世界"
WORK_AREA = junma.mylib.get_workarea()
# MAIN_WINDOW_AREA = junma.mylib.split(WORK_AREA, 4)[0]
# MAIN_WINDOW_AREA.right = MAIN_WINDOW_AREA.right * 3
# OTHER_WINDOWS_AREA = junma.mylib.split(WORK_AREA, 4)[-1]


class WindowManager(object):

    def __init__(self):
        self.main_window = None
        self.windows_handles = []

    def show_windows_list(self):
        for index, window in enumerate(self.windows_handles, 1):
            print(f"no:{index}, window:{window}")


    def findWindows(self):
        '''查找游戏窗口'''
        while True:
            handle = win32gui.FindWindow(CLASSNAME, WINDOWNAME)
            if handle:
                title = win32gui.GetWindowText(handle)
                pid = win32process.GetWindowThreadProcessId(handle)
                self.windows_handles.append({'title':title, 'handle':handle, 'pid':pid})
                win32gui.SetWindowText(handle, f"{title} - pid:{pid[-1]}")
            else:
                break

    def flush_window(self):
        '''
        刷新窗口并将窗口队列中的所有窗口取消
        如果需要对窗口操作，需要重新调用findWindows()
        :return:
        '''
        self.main_window = None
        for window in self.windows_handles:
            try:
                win32gui.SetWindowText(window['handle'], window['title'])
            except pywintypes.error as e:
                continue
        self.windows_handles.clear()

    def set_mainwindow(self, handle=None):
        """设置主窗口"""
        if not handle:
            self.show_windows_list()
            no = int(input("请输入主控窗口序号："))
            handle = self.windows_handles[no-1]
        self.main_window = handle

    def get_otherwindows(self):
        try:
            if self.main_window == None:
                raise RuntimeError("未设置主控窗口")
            return [window for window in self.windows_handles if window!=self.main_window]
        except RuntimeError as e:
            raise e


    @staticmethod
    def set_window_pos(handle, rect):
        '''静态函数，设置游戏窗口调用函数'''
        win32gui.SetWindowPos(handle, win32con.HWND_TOP, rect.left, rect.top, rect.right-rect.left, rect.bottom-rect.top, win32con.SWP_SHOWWINDOW)

    # def set_windows_rect(self, num):
    #     '''
    #     设置窗口大小，主窗口默认占桌面左半部分，num为分割右半部分的数量
    #     先设置主窗口再执行此方法，否则抛出RuntimeError异常
    #     '''
    #     try:
    #         if self.main_window == None:
    #             raise RuntimeError("未设置主控窗口！")
    #         self.main_window["rect"] = MAIN_WINDOW_AREA
    #         other_windows = self.get_otherwindows()
    #         for rect, window in zip(junma.mylib.vsplit(rect=OTHER_WINDOWS_AREA, num=num), other_windows):
    #             window['rect'] = rect
    #     except RuntimeError as e:
    #         raise e

    # def set_windows_pos(self):
    #     '''更新游戏窗口位置'''
    #     for window in self.windows_handles:
    #         if 'rect' in window:
    #             WindowManager.set_window_pos(window['handle'], window['rect'])

    def set_windows_pos(self, mode):
        rect_list = get_rect_by_mode(mode)
        for window in self.windows_handles:
            if window.get('index'):
                WindowManager.set_window_pos(window['handle'], rect_list[window['index']-1])
                # print(window.get['index'])
