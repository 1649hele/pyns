import requests as _r, deepl as _deepl


Chinese = "ZH"
English = "EN"


def Key(key):
    return _deepl.Translator(key)


def __getattr__(name):
    try:
        nw = lambda s, to_lang, key: getattr(Key(key), name)(s, target_lang=to_lang)
    except:
        pass
    nw.__name__ = name
    return nw
