import os
import vdf
from os.path import join
from typing import List, Dict
from utils.paths import json_to_obj


class SteamAccount:
    def __init__(self):
        self.AccountId = None
        self.AccountName = None
        self.PersonalName = None
        self.RememberPassword = None
        self.WantsOfflineModeWarning = None
        self.SkipOfflineModeWarning = None
        self.AllowAutoLogin = None
        self.MostRecent = None
        self.Timestamp = None


class SteamRemoteClient:
    def __init__(self):
        self.DeviceId = None
        self.hostname = None
        self.LastUpdated = None
        self.lastresult = None
        self.ippublic = None


class SteamConnectCache:
    def __init__(self):
        self.DeviceID = None
        self.ConnectHash = None
        self.JWT = None


def GetSteamAccount() -> List[SteamAccount]:
    accfile = vdf.load(open(join(os.getenv("ProgramFiles(x86)"), "Steam", "config", "loginusers.vdf")))
    accs = []
    for userid, acc in accfile["users"].items():
        obj = json_to_obj(acc, SteamAccount)
        obj.AccountId = userid
        accs.append(obj)
    return accs


def GetSteamRemoteClients() -> List[SteamRemoteClient]:
    remoteclientcache = vdf.load(open(join(os.getenv("ProgramFiles(x86)"), "Steam", "config", "remoteclients.vdf")))
    clients = []
    for deviceid, device in remoteclientcache["RemoteClientCache"].items():
        obj = json_to_obj(device, SteamRemoteClient)
        obj.DeviceId = deviceid
        clients.append(obj)
    return clients


def GetRememberedMachineJWT() -> SteamConnectCache:
    config = vdf.load(open(join(os.getenv("ProgramFiles(x86)"), "Steam", "config", "config.vdf")))
    connectcache = SteamConnectCache()
    for k, v in config["InstallConfigStore"]["Authentication"]["RememberedMachineID"].items():
        connectcache.DeviceID = k
        connectcache.JWT = v
        break
    for k, v in config["InstallConfigStore"]["Software"]["Valve"]["Steam"]["ConnectCache"].items():
        if k == connectcache.DeviceID:
            connectcache.ConnectHash = v
        break
    return connectcache
