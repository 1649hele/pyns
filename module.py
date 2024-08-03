import os as __os
system = to_cmd = __os.system


class InstallError(Exception):
    def __init__(self, name):
        self.name = "can't install %s" % name
        super(InstallError, self).__init__(self.name)
    
    __module__ = "builtins"


class UninstallError(Exception):
    def __init__(self, name):
        self.name = "can't Unistall %s" % name
        super(UninstallError, self).__init__(self.name)
    
    __module__ = "builtins"


def install(name, file=None):
    text = "pip install %s -i https://pypi.pyton.org/simple"
    if file:
        text = file + r"\python.exe -m " + text
    if system(text % name):
        raise InstallError(name) from None


def upgrade(name, file=None):
    text = "pip install --upgrade %s -i https://pypi.python.org/simple" % name
    if file:
        text = file + r"\python.exe -m " + text
    system(text)


def unistall(name, file=None, show=True):
    text = "pip unistall %s" % (name if show else name + " -y")
    if file:
        text = file + r"\python.exe -m " + text
    if __os.system(text):
        raise UninstallError(name)
