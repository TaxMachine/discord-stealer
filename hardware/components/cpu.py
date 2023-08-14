from hardware.WmiQuery import Query


def CPU() -> str:
    return Query("SELECT Name FROM Win32_Processor")[0].Name