from hardware.WmiQuery import Query


class MotherBoard:
    def __init__(self, manufacturer: str, model: str, serial: int):
        self.Manufacturer: str = manufacturer
        self.Model: str = model
        self.Serial: int = serial


def MOTHERBOARD() -> MotherBoard:
    mboard = Query("SELECT Manufacturer, Product, SerialNumber FROM Win32_BaseBoard WHERE Status = 'OK'")[0]
    return MotherBoard(mboard.Manufacturer, mboard.Product, mboard.SerialNumber)
