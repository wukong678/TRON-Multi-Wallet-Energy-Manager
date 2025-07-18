from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

API_KEY = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"
client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=API_KEY))

priv = PrivateKey.fromhex("8b88e95da37759a2ea21937eb5d2482b41b677b844177e3cf797a8ce3c4a6ad9")
owner = priv.public_key.to_base58check_address()

amount_trx = 5  # 单位是 TRX
amount_sun = amount_trx * 1_000_000  # 转换为 SUN

try:
    txn = (
        client.trx.freeze_balance(
            owner=owner,
            amount=amount_sun,
            resource="BANDWIDTH"
        )
        .build()
        .sign(priv)
        .broadcast()
    )
    print("✅ 冻结成功，交易哈希:", txn["txid"])
except Exception as e:
    print("❌ 冻结失败:", e)
    traceback.print_exc()