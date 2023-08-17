import winreg
from typing import Any


def GetRobloxStudioCookie() -> str | None:
    try:
        registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Roblox\\RobloxStudioBrowser\\roblox.com")
        value, regtype = winreg.QueryValueEx(registry, ".ROBLOSECURITY")
        return value
    except FileNotFoundError:
        return None
