from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

# 初始化 Tron 主网客户端（请替换为你自己的 API Key）
API_KEY = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"
client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=API_KEY))

# 私钥和地址（请替换为你的私钥）
priv = PrivateKey.fromhex("8b88e95da37759a2ea21937eb5d2482b41b677b844177e3cf797a8ce3c4a6ad9")
from_addr = priv.public_key.to_base58check_address()

# 接收地址（请替换为目标地址）
to_addr = "TKXJsXPK8XsyXwNjVfXdyAcqfgsVdP2aBj"

# 转账金额（单位 TRX）
amount = 0.9
amount_sun = int(amount * 1_000_000)

try:
    print("🔐 FROM:", from_addr)
    print("🎯 TO:", to_addr)

    txn = (
        client.trx.transfer(from_addr, to_addr, amount_sun)
        .memo("测试转账")
        .fee_limit(10_000_000)
        .build()
        .sign(priv)
        .broadcast()
    )

    print("✅ 广播成功，交易哈希:", txn["txid"])

except Exception as e:
    print("❌ 转账失败:", e)
    traceback.print_exc()