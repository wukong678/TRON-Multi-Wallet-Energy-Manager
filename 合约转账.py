from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from tronpy.contract import Contract
import json

# ===== 用户配置 =====
hex_private_key = "8b88e95da37759a2ea21937eb5d2482b41b677b844177e3cf797a8ce3c4a6ad9"
to_address = "TMQPpk2BZD7fnhPnZUq7P9JzZhiGhFz4XX"
amount_usdt = 10 

# ===== 系统设置 =====
USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"
API_KEY = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"
client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=API_KEY))
priv = PrivateKey(bytes.fromhex(hex_private_key))
from_address = priv.public_key.to_base58check_address()
amount_sun = int(amount_usdt * 1_000_000)

# ===== 载入 ABI 并构建合约 =====
with open("usdt_abi.json", "r") as f:
    abi = json.load(f)

from tronpy.contract import Contract
usdt_contract = Contract(client=client, abi=abi)
usdt_contract._contract_address = USDT_CONTRACT

# ===== 构造并发起交易 =====
print("🔍 查询余额中...")
print("💰 TRX 余额:", client.get_account_balance(from_address))
usdt_balance = usdt_contract.functions.balanceOf(from_address)
print(f"💰 USDT 余额: {usdt_balance / 1_000_000:.6f} USDT")

try:
    print("🔐 FROM:", from_address)
    print("🎯 TO:", to_address)
    txn = (
        usdt_contract.functions.transfer(to_address, amount_sun)
        .with_owner(from_address)
        .fee_limit(5_000_000)
        .build()
        .sign(priv)
        .broadcast()
    )
    print("✅ 转账成功，交易哈希:", txn['txid'])
except Exception as e:
    import traceback
    print("❌ 转账失败:", e)
    traceback.print_exc()