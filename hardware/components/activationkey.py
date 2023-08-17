from hardware.WmiQuery import Query


def ActivationKey() -> str:
    key = Query("SELECT OA3xOriginalProductKey FROM SoftwareLicensingService")[0].OA3xOriginalProductKey
    if key == "":
        return "No Key"
    else:
        return key
