from hardware.WmiQuery import Query


def MACAddress() -> str:
    mac = Query("SELECT MACAddress FROM Win32_NetworkAdapter WHERE NetEnabled = True")[0]
    return mac.MACAddress
