import requests


def GetServer() -> str:
    r = requests.get("https://api.gofile.io/getServer")
    r = r.json()
    if not r["status"] == "ok":
        raise ConnectionError("Gofile raised an exception")
    return r["data"]["server"]


def UploadFile(path: str):
    try:
        r = requests.post(f"https://{GetServer()}.gofile.io/uploadFile", files={"file": path})
        r = r.json()
        if not r["status"] == "ok":
            raise FileNotFoundError("Couldn't upload " + path)
        return r["data"]["downloadPage"]
    except ConnectionError:
        raise
