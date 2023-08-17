import socket

from hardware.components.processes import Processes

from ctypes import *
from typing import List
from sys import exit


DBGPROCS: List[str] = [
    "procmon", "tcpview", "processhacker",
    "httpdebugger", "wireshark", "fiddler",
    "regedit", "taskmgr", "vboxservice",
    "df5serv", "procexp", "ida64", "ollydbg",
    "pestudio", "vmwareuser", "vgauthservice",
    "vmacthlp", "x96dbg", "vmsrvc", "x32dbg",
    "vmusrvc", "prl_cc", "prl_tools",
    "xenservice", "qemu-ga", "joeboxcontrol",
    "ksdumperclient", "ksdumper", "joeboxserver",
    "gdb", "autoruns", "cacheset",
    "dbgview", "adinsight", "adexplorer",
    "accessenum", "bginfo", "cpustres",
    "diskmon", "diskview", "desktops",
    "loadord", "notmyfault", "procexp",
    "rammap", "hxd", "rdcman", "shareenum",
    "shellrunas", "vmmap", "winobj",
    "zoomit", "whois"
]


def TestConnectivity() -> bool:
    try:
        socket.gethostbyname("www.google.com")
        return True
    except socket.gaierror:
        return False


def DetectDebugger() -> bool:
    if windll.kernel32.isDebuggerPresent():
        return True
    for proc in DBGPROCS:
        for p in Processes():
            return proc in p.name().lower()


def DebuggerCheck():
    while True:
        if DetectDebugger():
            exit(0)
