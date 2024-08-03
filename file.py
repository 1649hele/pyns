import os as _os

from pyns.iter import flatten as _flatten


userfile = _os.path.expanduser("~")


def keywords(file):
    from pyns.url import translate, ENGLISH
    if "\\" in file or "/" in file:
        return _os.path.abspath(file)
    t = translate(file, _to=ENGLISH, autolang=False)[0]
    if _os.path.exists(_os.path.join(userfile, t)):
        return _os.path.join(userfile, t)
    elif _os.path.exists(_os.path.join(userfile, t.title())):
        return _os.path.join(userfile, t.title())
    elif _os.path.exists(_os.path.join(userfile, "." + t)):
        return _os.path.join(userfile, "." + t)
    elif _os.path.exists(_os.path.join(userfile, "." + t.title())):
        return _os.path.join(userfile, "." + t.title())
    return _os.path.abspath(file)


def seek(filename, *seekdirs, eq=False, findone=False):
    seekdirs = map(lambda n: keywords(n), _flatten(seekdirs))
    if not findone:
        findlist = []
    for seekdir in seekdirs:
        if (eq and filename == seekdir) or (filename in seekdir and not eq):
            if findone:
                return seekdir
            else:
                findlist.append(seekdir)
        try:
            dir = list(map(lambda d: _os.path.join(seekdir, d), _os.listdir(seekdir)))
        except (PermissionError, NotADirectoryError):
            continue
        newfind = seek(filename, *dir, eq=eq, findone=findone)
        if findone and newfind is not None:
            return newfind
        elif not findone:
            findlist.extend(newfind)
    if findone:
        return None
    else:
        return findlist


class NotSupportedError(Exception):
    pass


def _htmltopdf(content, file):
    from weasyprint import HTML
    from io import BytesIO
    pdf_bytes = BytesIO()
    HTML(string=content).write_pdf(target=pdf_bytes)
    with open(file, "wb") as f:
        f.write(pdf_bytes.getvalue())


def cff(od_file, new_file, *args, **kwargs):
    if not (
        (new_file.endswith(".pdf") or new_file.endswith(".docx")) and
        (od_file.startswith("https://") or od_file.endswith(".pdf") or od_file.endswith(".docx"))
    ):
        raise NotSupportedError(
            "Can only achieve PDF and Word to Word conversion and webpage to Word or PDF conversion")
    if od_file.startswith("https://"):
        import requests
        response = requests.get(od_file)
        content = response.text
        if new_file.endswith(".pdf"):
            _htmltopdf(content, new_file)
        else:
            _htmltoword(content, new_file)
        return
    from pdf2docx import Converter
    cv = Converter(od_file)
    cv.convert(new_file, *args, **kwargs)
    cv.close()


def translateFile(filename):
    if filename.endswith(".pdf"):
        filename = filename.rstrip(".pdf")
        cff(filename, filename + ".docx")
        filename += "docx"
    if not filename.endswith(".docx"):
        raise


if __name__ == '__main__':
    cff("https://wenku.baidu.com/view/a02d6a6c1eb91a37f1115c6a.html?fr=income1-doc-search&_wkts_=1714617378522&wkQuery=j&needWelcomeRecommand=1", "j.pdf")
