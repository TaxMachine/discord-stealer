import base64, json

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


class ChromiumCrypt:
    def __init__(self):
        self.key = None

    def GetMasterKey(self, keyfile):
        f = open(keyfile, "r")
        content = json.loads(f.read())
        rawkey = content["os_crypt"]["encrypted_key"]
        self.key = CryptUnprotectData(base64.b64decode(rawkey)[5:], None, None, None, 0)[1]

    def decrypt(self, blob) -> str:
        iv = blob[3:15]
        ciphertext = blob[15:]
        aes = AES.new(self.key, AES.MODE_GCM, iv)
        decrypted = aes.decrypt(ciphertext)[:-16].decode()
        return decrypted
