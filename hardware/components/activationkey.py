from hardware.WmiQuery import Query


def ActivationKey() -> str:
    return Query("SELECT OA3xOriginalProductKey FROM SoftwareLicensingService")[0].OA3xOriginalProductKey
