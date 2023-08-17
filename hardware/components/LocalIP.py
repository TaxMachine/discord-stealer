from socket import gethostbyname, gethostname


def LocalIP() -> str:
    return gethostbyname(gethostname())
