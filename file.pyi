from typing import List

def change_display_file(file: str, display: bool) -> None:...
def keywords(file: str) -> str:...
def seek(
        filename: str,
        *seekdirs: str,
        eq: bool = False,
        findone: bool = False,
) -> str | List[str]:...