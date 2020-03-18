import os
import ctypes
import win32api
import win32con
import pickle
from junma.window import WindowThreadID
from junma.mylib import EXCEPT_PATH, KB_VK_MAP

user32 = ctypes.WinDLL("user32")
kernel32 = ctypes.WinDLL("kernel32")
os.add_dll_directory(os.path.join(os.getcwd(),"lib"))
junma_dll = ctypes.CDLL("junma.dll")
dll_handle = ctypes.c_ulonglong(win32api.GetModuleHandle("junma.dll"))
MAXWINDOWNUM = 10
MAXEXCEPTNUM = 30

class KBHook(object):
    def __init__(self):
        self.hook = None
        with open(EXCEPT_PATH, "rb") as f:
            self.exceptkeys = pickle.load(f)

    def write_exceptkeys(self):
        with open(EXCEPT_PATH, "wb") as f:
            pickle.dump(self.exceptkeys, f)

    def exceptkeys_Vk(self):
        for key in self.exceptkeys:
            if key in KB_VK_MAP:
                yield KB_VK_MAP[key]
            else:
                yield win32api.VkKeyScan(key)

    def start_except_key(self):
        VKs = (ctypes.c_int*MAXEXCEPTNUM)()
        for index,key in enumerate(self.exceptkeys_Vk()):
            VKs[index] = key
        junma_dll.setExceptKey(VKs, len(self.exceptkeys))

    def stop_except_key(self):
        junma_dll.clearExceptKey()

    def install_hook(self, thread_id):
        self.hook = user32.SetWindowsHookExA(win32con.WH_GETMESSAGE, junma_dll.hookproc, dll_handle, thread_id)
        junma_dll.sethook(self.hook)

    def uninstall_hook(self):
        user32.UnhookWindowsHookEx(self.hook)
        self.hook = None

    def set_others(self, manager):
        # 获取客户窗口数组
        others = manager.get_otherwindows()
        num_array = (ctypes.c_void_p*MAXWINDOWNUM)()
        count = 0
        for index,window in enumerate(others):
            if 'index' in window:
                num_array[index] = window['handle']
                count += 1
        # 设置客户窗口
        junma_dll.setOtherWindows(num_array, count)


    def start(self, manager):
        self.set_others(manager)
        # 安装钩子
        self.install_hook(manager.main_window["pid"][WindowThreadID])

    def stop(self):
        self.uninstall_hook()


if __name__ == '__main__':
    hook = KBHook()
    hook.start_except_key()
    hook.stop_except_key()
