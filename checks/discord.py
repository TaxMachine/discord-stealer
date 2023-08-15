import requests
import json
from base64 import b64encode


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
}))


def json_to_obj(data: json, class_type):
    obj = class_type()
    for k, v in data.items():
        if isinstance(v, (list, dict)):
            v = json_to_obj(v, list if isinstance(v, list) else dict)
        setattr(obj, k, v)
    return obj


class DiscordUser:
    def __init__(self):
        self.id = ""
        self.username: ""
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


class Discord:
    def __init__(self, token: str):
        self.token = token

    def makeRequest(self, url):
        r = requests.get(url, headers={
            "Authorization": self.token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-super-properties": PROPERTIES.decode()
        })
        return r

    def GetUser(self):
        payload = self.makeRequest("https://discord.com/api/v9/users/@me")
        if payload.status_code == 401:
            raise ValueError(payload.json()["message"])
        return json_to_obj(payload.json(), DiscordUser)
