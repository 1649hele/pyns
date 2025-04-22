"""
请不要在端口中输入敏感信息，谨防被盗！
"""

from playwright.sync_api import sync_playwright
import hashlib as _hashlib
import io as _io
from random import randint as _randint


class UserError(Exception):
    def __init__(self):
        super(UserError, self).__init__("Username or password was wrong")


def _true_username_and_password(page, username, password):
    page = _hash_page(page)
    data = {
        "page": page,
    }
    tmp = _requests.get(API + "/read", data=data).json()
    return tmp in [_hash_user(username, password), ""]


def set_user(page, new_username="", new_password="", username="", password=""):
    if _true_username_and_password(page, username, password):
        data = {
            "page": _hash_page(page),
            "text": _hash_user(new_username, new_password),
        }
    else:
        raise UserError()


class Note:
    def __init__(self, page, username, password):
        if not _true_username_and_password(page, username, password):
            raise UserError()
        self._playwright = sync_playwright()
        self._playwright.__enter__()
        self._browser = self._playwright.chromium.launch(headless=False)
        self._page = self._browser.new_page()
        self._page.goto(page, wait_until="networkidle")
        _type = "textarea"
        self._page.wait_for_selector(_type, timeout=10000)
        self.buffer = _io.StringIO(self._page.locator(_type).input_value())
        self.page = page
        

    def flush(self):
        self.buffer.seek(0)
        data = {
            "page": self.page,
            "text": self.buffer.read(),
        }
        self.buffer.seek(0)
        _requests.post(API + "/write", data=data)
    
    def close(self):
        self.flush()
        self.buffer.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def __getattr__(self, item):
        raise getattr(self.buffer, item)


URL_STRING = "pyms-pysocket"
PASSWORD = _randint(-2147483648, 2147483647)
API = "https://notems.dreamqjlight.us.kg/"


def _hash_user(username, password):
    string = "username:%s\npassword:%s" % (username, password)
    md5 = _hashlib.md5(string.endcode("utf-8"))
    return md5.hexdigest()


def _hash_page(page):
    string = URL_STRING + str(PASSWORD) + page
    md5 = _hashlib.md5(string.encode("utf-8"))
    return md5.hexdigest()


if __name__ == "__main__":
    set_user("hele", "hele", "123456")
    result = Note("hele", "hele", "123456")
    result
    