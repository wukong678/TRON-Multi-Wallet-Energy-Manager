from tronpy.keys import PrivateKey

priv = PrivateKey.random()
addr = priv.public_key.to_base58check_address()

print("📮 地址 (base58):", addr)
print("🔐 私钥 (hex):", priv.hex())