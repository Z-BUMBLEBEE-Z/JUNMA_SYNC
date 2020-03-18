import ctypes
import win32con
import string

VERSION = 3.0
ICON = "lib/icon.png"
YES_ICON = "lib/yes.png"
EXCEPT_PATH = "lib/exceptkey"
user32 = ctypes.WinDLL("user32")
ARRANGE_1_4 = 1
ARRANGE_2_3 = 2
ARRANGE_4_1 = 3
UNSELECTED = -1
__all__ = ['ARRANGE_1_4','ARRANGE_2_3','ARRANGE_4_1','get_rect_by_mode']

VK_SCAN_AVAIABLE = tuple('`1234567890-=' 'abcdefghijklmnopqrstuvwxyz' r"[]\;',./")

KB_VK_MAP = {
    'num': win32con.VK_NUMLOCK,
    'home': win32con.VK_HOME,
    'end': win32con.VK_END,
    'pageup': win32con.VK_PRIOR,
    'pagedown': win32con.VK_NEXT,
    'backspace': win32con.VK_BACK,
    'enter': win32con.VK_RETURN,
    'space': win32con.VK_SPACE,
    'esc': win32con.VK_ESCAPE,
    'tab': win32con.VK_TAB,
    'delete': win32con.VK_DELETE,
    'capslock': win32con.VK_CAPITAL,
    'alt': win32con.VK_MENU,
    'lctrl': win32con.VK_LCONTROL,
    'rctrl': win32con.VK_RCONTROL,
    'lwin': win32con.VK_LWIN,
    'rwin': win32con.VK_RWIN,
    'lshift': win32con.VK_LSHIFT,
    'rshift': win32con.VK_RSHIFT,
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'x/': win32con.VK_DIVIDE,
    'x*': win32con.VK_MULTIPLY,
    'x-': win32con.VK_SUBTRACT,
    'x+': win32con.VK_ADD,
    'x.': win32con.VK_DECIMAL
}

KB_INFO = "按键映射名如下：\n" \
          f"正常86键键盘区：{''.join(VK_SCAN_AVAIABLE)} \n" \
          "功能键：space、home、end、pageup、pagedown、enter、backspace、lwin、rwin\n" \
          "方向键：up、down、left、right\n" \
          "控制键：lshift、rshift、lctrl、rctrl、alt、num、capslock、delete\n" \
          "数字键盘：x0-x9  x/  x*  x-  x+  x。\n"

# 增加小写数字
for rect in range(10):
    KB_VK_MAP['x' + str(rect)] = win32con.VK_NUMPAD0 + rect


class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]


def rect_dict(rect: RECT) -> dict:
    return {'left': rect.left,
            'top': rect.top,
            'right': rect.right,
            'bottom': rect.bottom}


def get_workarea():
    rect = RECT(0, 0, 0, 0)
    user32.SystemParametersInfoA(win32con.SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    return rect


WORKAREA = get_workarea()


def vsplit(rect, num):
    assert num > 0 and isinstance(num, int), f"Num is a unsigned int ({type(num)} given)"
    result = []
    increment = int((rect.bottom - rect.top) / num)
    top = rect.top
    for i in range(num):
        bottom = top + increment
        result.append(RECT(rect.left, top, rect.right, bottom))
        top = bottom
    return result


def split(rect, num):
    assert num > 0 and isinstance(num, int), f"Num is a unsigned int ({type(num)} given)"
    result = []
    increment = int((rect.right - rect.left) / num)
    left = rect.left
    for i in range(num):
        right = left + increment
        result.append(RECT(left, rect.top, right, rect.bottom))
        left = right
    return result


# def windows_proportion(proportion):
#     rect = get_workarea()
#     if proportion == "1_1":
#         return [{}]

def get_rect_by_mode(mode):
    rects = []
    if mode == ARRANGE_1_4:
        # 1号窗口位置
        temp = split(WORKAREA, 4)
        num_1 = temp[0]
        num_1.right = num_1.right * 3
        num_2345 = vsplit(temp[-1], 4)
        rects.append(num_1)
        rects.extend(num_2345)

    elif mode == ARRANGE_2_3:
        temp = vsplit(WORKAREA, 3)
        num_12 = temp[0]
        num_12.bottom = num_12.bottom * 2
        num_12 = split(num_12, 2)
        num_345 = split(temp[-1], 3)
        rects.extend(num_12)
        rects.extend(num_345)

    elif mode == ARRANGE_4_1:
        h_decrement = int(WORKAREA.right / 8)
        v_decrement = int(WORKAREA.bottom / 8)
        num_1 = RECT(WORKAREA.left + h_decrement,
                     WORKAREA.top + v_decrement,
                     WORKAREA.right - h_decrement,
                     WORKAREA.bottom - v_decrement)
        rects.append(num_1)
        for i, row in enumerate(vsplit(WORKAREA, 3)):
            for j, cow in enumerate(split(row, 3)):
                if (i == 0 or i == 2) and (j == 0 or j == 2):
                    rects.append(cow)
    return rects

def show_rect(rect):
    print(f"left:{rect.left} top:{rect.top} right:{rect.right} bottom:{rect.bottom}")
#
# if __name__ == '__main__':
#     # show_rect(WORKAREA)
#     # for rect in get_rect_by_mode(ARRANGE_2_3):
#     #     show_rect(rect)