import win32gui
import win32con
import win32api
import win32ui
import ctypes

user32 = ctypes.WinDLL("user32.dll")

#获取句柄
# 参数1：IPCLASSNAME
# 参数2：窗口NAME
# 返回：32位窗口句柄
notepad = win32gui.FindWindow('Notepad', 'ok.txt - 记事本')

# 窗口显示
# 参数1：句柄
# 参数2：3最大化，2最小化，1正常窗口
win32gui.ShowWindow(notepad,1)

# 获取屏幕分辨率
# 参数win32con.SM_CXSCREEN :x轴
# 参数win32con.SM_CYSCREEN :Y轴
# screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
# screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
# print((screen_x,screen_y))

# 获取可用屏幕大小
# SystemParametersInfo
# 参数：
# h = ctypes.windll.LoadLibrary(r"C:\Users\VULCAN\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\WinSDK\Lib\User32.Lib")
# print(h.SystemParametersInfo(win32con.SPI_GETWORKAREA))
class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]
rect = RECT(0,0,0,0)
user32.SystemParametersInfoA(win32con.SPI_GETWORKAREA,0, ctypes.byref(rect), 0)
print(rect.left)
print(rect.top)
print(rect.right)
print(rect.bottom)


# 窗口移动
#
# BOOL SetWindowPos(
#   HWND hWnd,             // handle to window
#   HWND hWndInsertAfter,  // placement-order handle
#   int X,                 // horizontal position
#   int Y,                 // vertical position
#   int cx,                // width
#   int cy,                // height
#   UINT uFlags            // window-positioning flags
# );
print(win32gui.SetWindowPos(notepad, win32con.HWND_NOTOPMOST, rect.left, rect.top, int(rect.right/2), rect.bottom, win32con.SWP_NOREDRAW))

win32api.SendMessage(notepad, )

# print(f"{notepad:X}")