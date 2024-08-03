from typing import Any, List, Union, overload

from pypinyin import lazy_pinyin


toPinyin = lazy_pinyin

SELF     : int
ERRORCODE: int
ERRORMSG : int
URL      : int
AUTO    : str
CHINESE : str
ENGLISH : str
JAPANESE: str
KORAN   : str

@overload
def idlang(
    text: str,
    cantreturn: int | Any = ERRORMSG,
) -> str | int | List[str | int]:...
@overload
def idlang(
    text: str,
    cantreturn: int | Any,
    appid: int,
    appkey: str,
) -> str | int | List[str | int]:...
@overload
def idlang(
    text: str,
    cantreturn: int | Any = ERRORMSG,
    *,
    appid: int,
    appkey: int,
) -> str:...

@overload
def translate(
    text: str,
    _from: str = AUTO,
    _to: str = ENGLISH,
    domain: str | None = None,
    cantreturn: int | Any = ERRORMSG,
    action: bool = False,
    autolang: bool = True,
) -> List[str]:...
@overload
def translate(
    text: str,
    _from: str,
    _to: str,
    domain: str | None,
    cantreturn: Union[SELF, RAISE, ERRORCODE] | Any,
    action: bool,
    autolang: bool,
    appid: int,
    appkey: str,
) -> List[str]:...
@overload
def translate(
    text: str,
    _from: str = ...,
    _to: str = ENGLISH,
    domain: str | None = None,
    cantreturn: Union[SELF, RAISE, ERRORCODE] | Any = ERRORCODE,
    action: bool = False,
    autolang: bool = True,
    *,
    appid: str,
    appkey: str,
) -> List[str]:...