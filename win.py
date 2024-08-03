try:
    from func import Count
except ModuleNotFoundError:
    from .func import Count


_tray_show_num = Count(1)

import ctypes
from ctypes import wintypes

from PIL import Image


SHGFI_ICON = 0x000000100
SHGFI_SMALLICON = 0x000000001
SHGFI_USEFILEATTRIBUTES = 0x000000010


class SHFILEINFO(ctypes.Structure):
    _fields_ = [
        ("hIcon", wintypes.HANDLE),
        ("iIcon", ctypes.c_int),
        ("dwAttributes", ctypes.c_uint),
        ("szDisplayName", ctypes.c_wchar * 260),
        ("szTypeName", ctypes.c_wchar * 80)
    ]


SHGetFileInfo = ctypes.windll.shell32.SHGetFileInfoW
SHGetFileInfo.argtypes = [wintypes.LPCWSTR, wintypes.DWORD,
                          ctypes.POINTER(SHFILEINFO), ctypes.c_uint,
                          wintypes.UINT]
SHGetFileInfo.restype = wintypes.DWORD


def get_file_icon(file_path):
    file_info = SHFILEINFO()
    SHGetFileInfo(
        file_path, 0, ctypes.byref(file_info),
        ctypes.sizeof(file_info),
        SHGFI_ICON | SHGFI_SMALLICON | SHGFI_USEFILEATTRIBUTES
    )
    icon_handle = file_info.hIcon
    return icon_handle


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]


def get_file_icon(file_path):
    file_info = SHFILEINFO()
    SHGetFileInfo(
        file_path, 0, ctypes.byref(file_info),
        ctypes.sizeof(file_info),
        SHGFI_ICON | SHGFI_SMALLICON | SHGFI_USEFILEATTRIBUTES
    )
    icon_handle = file_info.hIcon
    return icon_handle


def icon_to_image(icon_handle):
    hdc = ctypes.windll.user32.GetDC(0)
    hdc_desktop = ctypes.windll.user32.GetDC(0)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_desktop)
    
    bm_info = BITMAPINFOHEADER()
    bm_info.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bm_info.biWidth = 32
    bm_info.biHeight = 32
    bm_info.biPlanes = 1
    bm_info.biBitCount = 32
    bm_info.biCompression = 0
    
    bmp = ctypes.windll.gdi32.CreateDIBSection(
        hdc_mem, ctypes.byref(bm_info), 0, 0, 0, 0
    )
    old_bmp = ctypes.windll.gdi32.SelectObject(hdc_mem, bmp)
    
    ctypes.windll.user32.DrawIconEx(
        hdc_mem, 0, 0, icon_handle, 32, 32, 0, 0, 0x0003
    )
    
    buffer = ctypes.create_string_buffer(32 * 32 * 4)
    ctypes.windll.gdi32.GetDIBits(
        hdc_mem, bmp, 0, 32, buffer, ctypes.byref(bm_info), 0
    )
    
    image = Image.frombytes('RGBA', (32, 32), buffer, 'raw', 'BGRA', 0, -1)
    ctypes.windll.gdi32.SelectObject(hdc_mem, old_bmp)
    ctypes.windll.gdi32.DeleteObject(bmp)
    ctypes.windll.gdi32.DeleteDC(hdc_mem)
    
    return image


from pystray import Icon, Menu, MenuItem


def create_tray_icon(icon_image):
    icon = Icon("File Icon")
    icon_bytes = icon_image
    icon.icon = icon_bytes
    menu = Menu(MenuItem("Exit", icon.stop), MenuItem("Stop", exit))
    icon.menu = menu
    import threading
    
    threading.Thread(target=icon.run).start()


file_path = r"F:\Python\Windows\pypassword.py"
icon_handle = get_file_icon(file_path)
print(icon_handle)
image = icon_to_image(icon_handle)
image.resize((200, 200))
image.save("./temp.png")
create_tray_icon(image)


def tray_show(
        image,
        stop=lambda: False,
        icon=lambda: None,
        menu=lambda: None,
        title="",
        *items,
):
    count = str(next(_tray_show_num))
    from pystray import Icon, Menu
    
    _icon = Icon()
    icon_bytes = icon_image
    _icon.icon = icon_bytes
    menu = Menu(*items)
    _icon.menu = menu
    _icon.title = title
    import threading
    threading.Thread(target=_icon.run, daemon=True, name="run icon " + count).start()
    
    def diplay():
        while True:
            if stop():
                _icon.stop()
                return
            get = icon()
            if get:
                _icon.icon = get
            get = menu()
            if get:
                _icon.menu = menu
    
    threading.Thread(target=diplay, daemon=True, name="display icon " + count).start()
    
