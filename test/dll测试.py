import ctypes
import os
import win32con
import win32api


os.add_dll_directory(os.path.join(os.getcwd(), "lib"))

user32 = ctypes.WinDLL("user32")
kernel32 = ctypes.WinDLL("kernel32")
my_dll = ctypes.cdll.LoadLibrary("lib/junma.dll")
dll_handle = win32api.GetModuleHandle("lib/junma.dll")

dll_handle = ctypes.c_ulonglong(dll_handle)
hook = user32.SetWindowsHookExW(win32con.WH_KEYBOARD, my_dll.hookporc, dll_handle, 20124)
my_dll.sethook(hook)
print(win32api.GetLastError())
print(my_dll.gethook())