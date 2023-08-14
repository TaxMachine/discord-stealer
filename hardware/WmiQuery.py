import wmi


def Query(query):
    w = wmi.WMI()
    return w.query(query)


def Security(query):
    w = wmi.WMI(moniker="winmgmts:{impersonationLevel=impersonate}!\\\\.\\root\\securitycenter2")
    return w.query(query)
