from typing import List

def keywords(file: str) -> str:...
def seek(
        filename: str,
        *seekdirs: str,
        eq: bool = False,
        findone: bool = False,
) -> str | List[str]:...