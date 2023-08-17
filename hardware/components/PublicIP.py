import requests


def PublicIP() -> str:
    return requests.get("https://ipwhois.app/json/").json()["ip"]
