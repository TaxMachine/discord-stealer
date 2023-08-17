import requests
import json
from utils.paths import json_to_obj
from typing import Dict


class RobloxUser:
    def __init__(self):
        self.UserId = None
        self.Name = None
        self.DisplayName = None
        self.UserEmail = None
        self.IsEmailVerified = None
        self.AgeBracket = None
        self.UserAbove13 = None


class Roblox:
    def __init__(self, cookie: str):
        self.cookie = cookie

    def makeRequest(self, url):
        r = requests.get(url, cookies={
            ".ROBLOSECURITY": self.cookie
        }, headers={
            "Accept-Encoding": "identity"
        })
        return r

    def GetAccount(self) -> RobloxUser:
        payload = self.makeRequest("https://roblox.com/my/account/json")
        return json_to_obj(payload.json(), RobloxUser)

    def GetBalance(self, userid: int) -> int:
        payload = self.makeRequest("https://economy.roblox.com/v1/users/" + str(userid) + "/currency")
        return payload.json()["robux"]

    def GetSkin(self, userid: int) -> str:
        image = self.makeRequest("https://thumbnails.roblox.com/v1/users/avatar?userIds=" + str(userid) + "&isCircular=false&format=Png&size=420x420")
        return image.json()["data"][0]["imageUrl"]
