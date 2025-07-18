#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多钱包能量管理系统
通过5个钱包的协同操作来优化能量获取和使用
"""

import json
import time
import datetime
from typing import Dict, List, Optional
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

class MultiWalletEnergyManager:
    def __init__(self, api_key: str = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"):
        """初始化多钱包能量管理器"""
        self.client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=api_key))
        self.wallets = {}  # 存储所有钱包信息
        self.main_wallet = None  # 主钱包地址
        self.config_file = "multi_wallet_config.json"
        self.load_config()
    
    def generate_wallets(self, count: int = 5) -> Dict[str, Dict]:
        """生成指定数量的钱包"""
        print(f"🔧 正在生成 {count} 个钱包...")
        
        wallets = {}
        for i in range(count):
            # 生成随机私钥
            priv = PrivateKey.random()
            address = priv.public_key.to_base58check_address()
            
            wallet_info = {
                "address": address,
                "private_key": priv.hex(),
                "role": "main" if i == 0 else "energy_provider",
                "created_time": datetime.datetime.now().isoformat(),
                "frozen_trx": 0,
                "energy_balance": 0,
                "last_freeze_time": None,
                "last_unfreeze_time": None
            }
            
            wallet_name = f"wallet_{chr(65+i)}"  # A, B, C, D, E
            wallets[wallet_name] = wallet_info
            
            print(f"✅ {wallet_name} ({'主钱包' if i == 0 else '能量钱包'}): {address}")
        
        # 设置主钱包
        self.main_wallet = wallets["wallet_A"]["address"]
        self.wallets = wallets
        self.save_config()
        
        return wallets
    
    def load_config(self):
        """加载钱包配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.wallets = data.get("wallets", {})
                self.main_wallet = data.get("main_wallet", None)
                print(f"✅ 已加载 {len(self.wallets)} 个钱包配置")
        except FileNotFoundError:
            print("⚠️ 配置文件不存在，将创建新的钱包")
            self.wallets = {}
            self.main_wallet = None
    
    def save_config(self):
        """保存钱包配置"""
        config = {
            "wallets": self.wallets,
            "main_wallet": self.main_wallet,
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"💾 配置已保存到 {self.config_file}")
    
    def get_wallet_balances(self, wallet_name: str = None) -> Dict:
        """查询钱包余额"""
        if wallet_name:
            wallets_to_check = {wallet_name: self.wallets[wallet_name]}
        else:
            wallets_to_check = self.wallets
        
        balances = {}
        for name, wallet in wallets_to_check.items():
            try:
                address = wallet["address"]
                
                # 查询TRX余额
                trx_balance = self.client.get_account_balance(address)
                
                # 查询账户资源信息
                account_info = self.client.get_account(address)
                
                # 获取能量信息
                energy_balance = 0
                frozen_trx = 0
                
                if account_info:
                    # 获取冻结的TRX数量和能量
                    if 'frozen' in account_info:
                        for frozen in account_info['frozen']:
                            if frozen.get('frozen_balance', 0) > 0:
                                frozen_trx += frozen['frozen_balance'] / 1_000_000
                    
                    # 获取能量余额
                    if 'account_resource' in account_info:
                        energy_balance = account_info['account_resource'].get('energy_limit', 0)
                
                balances[name] = {
                    "address": address,
                    "trx_balance": trx_balance,
                    "frozen_trx": frozen_trx,
                    "energy_balance": energy_balance,
                    "role": wallet["role"]
                }
                
            except Exception as e:
                print(f"❌ 查询 {name} 余额失败: {e}")
                balances[name] = {"error": str(e)}
        
        return balances
    
    def freeze_trx_for_energy(self, wallet_name: str, amount_trx: float) -> bool:
        """在指定钱包中冻结TRX获取能量"""
        try:
            wallet = self.wallets[wallet_name]
            priv = PrivateKey.fromhex(wallet["private_key"])
            owner = priv.public_key.to_base58check_address()
            amount_sun = int(amount_trx * 1_000_000)
            
            print(f"🧊 {wallet_name} 正在冻结 {amount_trx} TRX 获取能量...")
            
            # 执行冻结操作
            txn = (
                self.client.trx.freeze_balance(
                    owner=owner,
                    amount=amount_sun,
                    resource="ENERGY"  # 冻结获取能量
                )
                .build()
                .sign(priv)
                .broadcast()
            )
            
            # 更新钱包信息
            self.wallets[wallet_name]["frozen_trx"] += amount_trx
            self.wallets[wallet_name]["last_freeze_time"] = datetime.datetime.now().isoformat()
            self.save_config()
            
            print(f"✅ {wallet_name} 冻结成功，交易哈希: {txn['txid']}")
            return True
            
        except Exception as e:
            print(f"❌ {wallet_name} 冻结失败: {e}")
            traceback.print_exc()
            return False
    
    def delegate_energy_to_main(self, wallet_name: str, energy_amount: int = None) -> bool:
        """将能量委托给主钱包"""
        try:
            if not self.main_wallet:
                print("❌ 未设置主钱包")
                return False
            
            wallet = self.wallets[wallet_name]
            priv = PrivateKey.fromhex(wallet["private_key"])
            owner = priv.public_key.to_base58check_address()
            
            # 如果未指定能量数量，委托所有可用能量
            if energy_amount is None:
                balances = self.get_wallet_balances(wallet_name)
                energy_amount = balances[wallet_name]["energy_balance"]
            
            if energy_amount <= 0:
                print(f"⚠️ {wallet_name} 没有可委托的能量")
                return False
            
            print(f"🔄 {wallet_name} 正在委托 {energy_amount} 能量给主钱包...")
            
            # 执行能量委托
            txn = (
                self.client.trx.delegate_resource(
                    owner=owner,
                    receiver=self.main_wallet,
                    balance=energy_amount,
                    resource="ENERGY"
                )
                .build()
                .sign(priv)
                .broadcast()
            )
            
            print(f"✅ {wallet_name} 能量委托成功，交易哈希: {txn['txid']}")
            return True
            
        except Exception as e:
            print(f"❌ {wallet_name} 能量委托失败: {e}")
            traceback.print_exc()
            return False
    
    def unfreeze_trx(self, wallet_name: str) -> bool:
        """解冻TRX（3天后可用）"""
        try:
            wallet = self.wallets[wallet_name]
            priv = PrivateKey.fromhex(wallet["private_key"])
            owner = priv.public_key.to_base58check_address()
            
            print(f"🔓 {wallet_name} 正在解冻TRX...")
            
            # 执行解冻操作
            txn = (
                self.client.trx.unfreeze_balance(
                    owner=owner,
                    resource="ENERGY"
                )
                .build()
                .sign(priv)
                .broadcast()
            )
            
            # 更新钱包信息
            self.wallets[wallet_name]["frozen_trx"] = 0
            self.wallets[wallet_name]["last_unfreeze_time"] = datetime.datetime.now().isoformat()
            self.save_config()
            
            print(f"✅ {wallet_name} 解冻成功，交易哈希: {txn['txid']}")
            return True
            
        except Exception as e:
            print(f"❌ {wallet_name} 解冻失败: {e}")
            traceback.print_exc()
            return False
    
    def execute_rotation_strategy(self, freeze_amount_per_wallet: float = 30.0):
        """执行轮换策略"""
        print("🔄 开始执行多钱包轮换策略...")
        
        energy_wallets = [name for name, wallet in self.wallets.items() 
                         if wallet["role"] == "energy_provider"]
        
        for i, wallet_name in enumerate(energy_wallets):
            print(f"\n--- 处理 {wallet_name} (第{i+1}个能量钱包) ---")
            
            # 检查余额
            balances = self.get_wallet_balances(wallet_name)
            wallet_balance = balances[wallet_name]
            
            if wallet_balance["trx_balance"] < freeze_amount_per_wallet:
                print(f"⚠️ {wallet_name} TRX余额不足 ({wallet_balance['trx_balance']} < {freeze_amount_per_wallet})")
                continue
            
            # 冻结TRX获取能量
            if self.freeze_trx_for_energy(wallet_name, freeze_amount_per_wallet):
                print(f"⏱️ 等待3秒后委托能量...")
                time.sleep(3)
                
                # 委托能量给主钱包
                self.delegate_energy_to_main(wallet_name)
            
            # 间隔时间避免网络拥堵
            if i < len(energy_wallets) - 1:
                print(f"⏱️ 等待5秒后处理下一个钱包...")
                time.sleep(5)
    
    def show_all_balances(self):
        """显示所有钱包余额"""
        print("\n" + "="*80)
        print("📊 多钱包余额总览")
        print("="*80)
        
        balances = self.get_wallet_balances()
        
        total_trx = 0
        total_energy = 0
        
        for name, balance in balances.items():
            if "error" in balance:
                print(f"❌ {name}: 查询失败 - {balance['error']}")
                continue
            
            role_text = "🏦 主钱包" if balance["role"] == "main" else "⚡ 能量钱包"
            print(f"\n{role_text} {name}:")
            print(f"  📮 地址: {balance['address']}")
            print(f"  💰 TRX余额: {balance['trx_balance']:.6f} TRX")
            print(f"  🧊 冻结TRX: {balance['frozen_trx']:.6f} TRX")
            print(f"  ⚡ 能量余额: {balance['energy_balance']:,} Energy")
            
            total_trx += balance['trx_balance'] + balance['frozen_trx']
            total_energy += balance['energy_balance']
        
        print(f"\n📈 总计:")
        print(f"  💰 总TRX: {total_trx:.6f} TRX")
        print(f"  ⚡ 总能量: {total_energy:,} Energy")
        print(f"  💡 可转账次数: {total_energy // 30000} 次 (按30,000能量/次计算)")
        print("="*80)
    
    def transfer_trx_to_wallets(self, amount_per_wallet: float = 50.0):
        """从主钱包向其他钱包转账TRX"""
        if not self.main_wallet:
            print("❌ 未设置主钱包")
            return
        
        main_wallet_info = None
        for wallet in self.wallets.values():
            if wallet["address"] == self.main_wallet:
                main_wallet_info = wallet
                break
        
        if not main_wallet_info:
            print("❌ 找不到主钱包信息")
            return
        
        # 获取能量钱包列表
        energy_wallets = [(name, wallet) for name, wallet in self.wallets.items() 
                         if wallet["role"] == "energy_provider"]
        
        total_needed = amount_per_wallet * len(energy_wallets)
        
        # 检查主钱包余额
        main_balance = self.get_wallet_balances("wallet_A")["wallet_A"]["trx_balance"]
        
        if main_balance < total_needed + 10:  # 保留10 TRX作为手续费
            print(f"❌ 主钱包TRX余额不足: {main_balance} < {total_needed + 10}")
            return
        
        print(f"💸 开始从主钱包向 {len(energy_wallets)} 个能量钱包转账...")
        
        # 执行转账
        priv = PrivateKey.fromhex(main_wallet_info["private_key"])
        
        for name, wallet in energy_wallets:
            try:
                print(f"💸 向 {name} 转账 {amount_per_wallet} TRX...")
                
                txn = (
                    self.client.trx.transfer(
                        from_=self.main_wallet,
                        to=wallet["address"],
                        amount=int(amount_per_wallet * 1_000_000)
                    )
                    .build()
                    .sign(priv)
                    .broadcast()
                )
                
                print(f"✅ 转账成功，交易哈希: {txn['txid']}")
                time.sleep(3)  # 避免网络拥堵
                
            except Exception as e:
                print(f"❌ 向 {name} 转账失败: {e}")

def main():
    """主函数 - 演示多钱包能量管理"""
    manager = MultiWalletEnergyManager()
    
    while True:
        print("\n" + "="*60)
        print("🚀 多钱包能量管理系统")
        print("="*60)
        print("1. 生成5个钱包")
        print("2. 查看所有钱包余额")
        print("3. 从主钱包分发TRX到能量钱包")
        print("4. 执行轮换策略 (冻结TRX + 委托能量)")
        print("5. 手动冻结指定钱包的TRX")
        print("6. 手动委托能量到主钱包")
        print("7. 解冻指定钱包的TRX")
        print("8. 导出钱包信息")
        print("0. 退出")
        print("-"*60)
        
        choice = input("请选择操作 (0-8): ").strip()
        
        if choice == "1":
            manager.generate_wallets(5)
            print("\n💡 提示: 请向主钱包(wallet_A)充值TRX，然后使用选项3分发到其他钱包")
            
        elif choice == "2":
            manager.show_all_balances()
            
        elif choice == "3":
            amount = input("请输入每个能量钱包分发的TRX数量 (默认50): ").strip()
            amount = float(amount) if amount else 50.0
            manager.transfer_trx_to_wallets(amount)
            
        elif choice == "4":
            amount = input("请输入每个钱包冻结的TRX数量 (默认30): ").strip()
            amount = float(amount) if amount else 30.0
            manager.execute_rotation_strategy(amount)
            
        elif choice == "5":
            print("可用的能量钱包:")
            energy_wallets = [name for name, wallet in manager.wallets.items() 
                            if wallet["role"] == "energy_provider"]
            for i, name in enumerate(energy_wallets, 1):
                print(f"  {i}. {name}")
            
            wallet_choice = input("请选择钱包编号: ").strip()
            if wallet_choice.isdigit() and 1 <= int(wallet_choice) <= len(energy_wallets):
                wallet_name = energy_wallets[int(wallet_choice) - 1]
                amount = input("请输入冻结的TRX数量: ").strip()
                if amount:
                    manager.freeze_trx_for_energy(wallet_name, float(amount))
            
        elif choice == "6":
            print("可用的能量钱包:")
            energy_wallets = [name for name, wallet in manager.wallets.items() 
                            if wallet["role"] == "energy_provider"]
            for i, name in enumerate(energy_wallets, 1):
                print(f"  {i}. {name}")
            
            wallet_choice = input("请选择钱包编号: ").strip()
            if wallet_choice.isdigit() and 1 <= int(wallet_choice) <= len(energy_wallets):
                wallet_name = energy_wallets[int(wallet_choice) - 1]
                manager.delegate_energy_to_main(wallet_name)
            
        elif choice == "7":
            print("可用的能量钱包:")
            energy_wallets = [name for name, wallet in manager.wallets.items() 
                            if wallet["role"] == "energy_provider"]
            for i, name in enumerate(energy_wallets, 1):
                print(f"  {i}. {name}")
            
            wallet_choice = input("请选择钱包编号: ").strip()
            if wallet_choice.isdigit() and 1 <= int(wallet_choice) <= len(energy_wallets):
                wallet_name = energy_wallets[int(wallet_choice) - 1]
                manager.unfreeze_trx(wallet_name)
            
        elif choice == "8":
            print("\n📋 钱包信息导出:")
            for name, wallet in manager.wallets.items():
                role_text = "主钱包" if wallet["role"] == "main" else "能量钱包"
                print(f"\n{name} ({role_text}):")
                print(f"  地址: {wallet['address']}")
                print(f"  私钥: {wallet['private_key']}")
            
        elif choice == "0":
            print("👋 再见!")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()