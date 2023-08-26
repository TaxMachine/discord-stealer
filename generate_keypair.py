from Crypto.PublicKey import ECC


keypair = ECC.generate(curve="P-521")

publickey = keypair.public_key().export_key(format="PEM")
privatekey = keypair.export_key(format="PEM")

print(publickey)
print(privatekey)

config = open("./config.py", "r+")
configcontent = config.read()
newconfig = configcontent.replace("%ECC_PUBLIC_KEY%", publickey)
newconfig = newconfig.replace("%ECC_PRIVATE_KEY%", privatekey)
config.seek(0)
config.write(newconfig)
config.truncate()
config.close()
