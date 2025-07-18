from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

# TronGrid 的 API Key
API_KEY = 'f5668afc-2f0e-4fdb-91a6-cb01509a3ddf'

# 初始化 Tron 客户端（带 API Key）
client = Tron(provider=HTTPProvider(api_key=API_KEY), network='mainnet')

# 以下内容和原来一样
private_key = PrivateKey.fromhex('8b88e95da37759a2ea21937eb5d2482b41b677b844177e3cf797a8ce3c4a6ad9')
from_address = private_key.public_key.to_base58check_address()
to_address = 'TMQPpk2BZD7fnhPnZUq7P9JzZhiGhFz4XX'
contract_address = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
contract = client.get_contract(contract_address)
amount = 10 * 1_000_000

txn = (
    contract.functions.transfer(to_address, amount)
    .with_owner(from_address)
    .fee_limit(10_000_000)
    .build()
    .sign(private_key)
)

result = txn.broadcast()
print(f'Transaction ID: {result['txid']}')