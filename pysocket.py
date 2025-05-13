"""
请不要在端口中输入敏感信息，谨防被盗！
"""

from playwright.sync_api import sync_playwright as _sync_playwright
import hashlib as _hashlib
import atexit as _atexit
import io as _io
import sys as _sys


_playwright = _sync_playwright()
_playwright.start()
_playwright = _playwright._playwright
_browser = _playwright.chromium.launch(headless=False)
INPUT_TYPE = "textarea"


def _get_page(page):
    nw = _browser.new_page()
    nw.goto(page, wait_until="networkidle")
    nw.wait_for_selector(INPUT_TYPE, timeout=10000)
    return nw


class UserError(Exception):
    def __init__(self):
        super(UserError, self).__init__("Invalid username or password")


def _true_username_and_password(page, username, password):
    tmp = _get_page(page).locator(INPUT_TYPE).input_value()
    return tmp in [_hash_user(username, password), ""]


def set_user(page, new_username="", new_password="", username="", password=""):
    if _true_username_and_password(page, username, password):
        tmp = _get_page(page)
        tmp.fill(INPUT_TYPE, "")
        tmp.type(INPUT_TYPE, _hash_user(username, password))
    else:
        raise UserError()


class Note:
    def __init__(self, page, username, password):
        if not _true_username_and_password(page, username, password):
            raise UserError()
        self._page = _get_page(page)
        self.buffer = _io.StringIO(self._page.locator(INPUT_TYPE).input_value())
        self.page = page
        

    def flush(self):
        seek_index = self.buffer.tell()
        self.buffer.seek(0)
        text = self.buffer.read()
        self.buffer.seek(seek_index)
        self._page.fill(INPUT_TYPE, "")
        self._page.type(INPUT_TYPE, text)
    
    def close(self):
        self.flush()
        self.buffer.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def __getattr__(self, item):
        return getattr(self.buffer, item)


URL_STRING = "pyms-pysocket"


def _hash_user(username, password):
    string = "username:%s\npassword:%s" % (username, password)
    md5 = _hashlib.md5(string.encode("utf-8"))
    return md5.hexdigest()


def _hash_page(page):
    string = URL_STRING + page
    md5 = _hashlib.md5(string.encode("utf-8"))
    return md5.hexdigest()


def _exit():
    try:
        _browser.close()
    except Exception as e:
        print(f"Error closing browser: {e}", file=_sys.stderr)
    try:
        _playwright.stop()
    except Exception as e:
        print(f"Error stopping Playwright: {e}", file=_sys.stderr)



_atexit.register(_exit)

if __name__ == "__main__":
    set_user("tmp", "hele", "123456")
    result = Note("tmp", "hele", "123456")
    result.write("这是一个用play_wright编写的程序，在tmp中写入这行文字")
    