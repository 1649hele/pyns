import requests as _r


SELF = 68719476736
ERRORCODE = 137438953472
ERRORMSG = 274877906944
URL = 549755813888
AUTO = "auto"
CHINESE  = "zh"
ENGLISH  = "en"
JAPANESE = "jp"
KORAN    = "kor"
_appid = 20231107001872744
_appkey = "ihFzd1LWeKYvNgtyYTvi"


def _cantreturn(x, url, json, text):
    if not isinstance(x, (int, float)):
        return x
    else:
        from pyns.fm import isint
        if x % 2 == 1 or x > 1168231104512 or x < 1 or not isint(x):
            return x
        temp = []
        for i in (SELF, ERRORCODE, ERRORMSG, URL):
            if x & i == i:
                if i == SELF:
                    temp.append(text)
                elif i == ERRORCODE:
                    temp.append(json["error_code"])
                elif i == ERRORMSG:
                    temp.append(json["error_msg"])
                else:
                    temp.append(url)
        if len(temp) == 1:
            return temp[0]
        else:
            return temp


def md5(s, encoding='utf-8'):
    from hashlib import md5
    return md5(s.encode(encoding)).hexdigest()


def toPinyin(text, *args, **kwargs):
    import pypinyin
    return pypinyin.lazy_pinyin(text, *args, **kwargs)

    
def idlang(text, cantreturn=ERRORMSG, appid=None, appkey=None):
    from pyns.iter import split
    import string
    import random
    import re
    __appid = appid
    __appkey = appkey
    chardict = {}
    for _char in re.split(
        r"[。？！\s]\s*",
        text,
    ):
        bezh = True
        lenchar = 0
        for char in _char:
            if char not in string.digits + string.punctuation + "。，？：；‘’“”、《》！·… ":
                lenchar += 1
                if not (13312 < ord(char) < 40959):
                    bezh = False
        if bezh:
            chardict["zh"] = lenchar
            continue
        _char = "".join(_char)
        if _char == "":
            continue
        url = "https://fanyi-api.baidu.com/api/trans/vip/language"
        salt = random.randint(32768, 65536)
        for appid, appkey in (
                (20231110001876133, "_n76IPCbijgFF3os4yfQ"),
                (_appid, _appkey),
        ) if not (__appid or __appkey) else ((appid, appkey),):
            sign = md5(str(appid) + _char + str(salt) + appkey)
            payload = {
                "salt": salt,
                "appid": appid,
                "q": _char,
                "sign": sign,
            }
            r = _r.get(url, payload)
            result = r.json()
            if result["error_code"] == 0:
                for lang in result["data"].values():
                    if lang in chardict:
                        chardict[lang] += lenchar
                    else:
                        chardict[lang] = lenchar
                break
            elif appid == __appid or (appid == _appid and __appid is None):
                return _cantreturn(cantreturn, url, result, text)
    if len(chardict) == 0:
        return None
    return max(chardict.items(), key=lambda a: a[1])[0]


def translate(
    text,
    _from="auto",
    _to=ENGLISH,
    domain=None,
    cantreturn=ERRORMSG,
    action=False,
    autolang=True,
    appid=None,
    appkey=None,
):
    if _from == _to:
        return text
    if appid is None and appkey is None:
        appid = _appid
        appkey = _appkey
    text = "+".join(text.split(" "))
    if "\n" in text:
        turn = []
        for stn in text.split("\n"):
            turn.append(
                translate(
                    stn.strip(),
                    _from,
                    _to,
                    domain,
                    cantreturn,
                    action,
                    autolang,
                    appid,
                    appkey,
                )[0],
            )
        return "\n".join(turn)
    import random
    salt = random.randint(32768, 65536)
    sign = str(appid)
    sign += text
    sign += str(salt)
    if domain is not None:
        sign += domain
    sign += appkey
    sign = md5(sign)
    if domain:
        url = "https://api.fanyi.baidu.com/api/trans/vip/fieldtranslate"
    else:
        url = "https://api.fanyi.baidu.com/api/trans/vip/translate"
    payload = {
        "appid": appid,
        "q"    : text,
        "from" : _from,
        "to"   : _to,
        "salt" : salt,
        "sign" : sign,
        "action": int(action),
    }
    if domain is not None:
        payload["domain"] = domain
        del payload["action"]
    r = _r.get(url, payload)
    result = r.json()
    if "error_code" not in result or result["error_code"] in (52000, "52000", 0, "0"):
        temp = list(map(lambda n: n["dst"], result["trans_result"]))
        if not autolang:
            return temp
        if text in temp:
            if _to == ENGLISH:
                import locale
                g = locale.getlocale()[0].lower()
                if g.startswith("chinese"):
                    _to = CHINESE
                else:
                    _to = g[:2]
                    if _to == "ko":
                        _to += "r"
            else:
                _to = ENGLISH
            return translate(
                text,
                _from,
                _to,
                domain,
                cantreturn,
                action,
                autolang,
                appid,
                appkey,
            )
        return temp
    else:
        return _cantreturn(cantreturn, url, result, text)


try:
    from file import translateFile
except ImportError:
    from .file import translateFile


if __name__ == '__main__':
    import random
    text = "Hello 123456 ,"
    print(idlang(text))
    print(translate("desktop", AUTO, ENGLISH, "it"))
    print(translate("leaves", AUTO, CHINESE))
