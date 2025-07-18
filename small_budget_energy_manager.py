#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小资金能量管理器 - 专为30 TRX设计
适合资金有限但想优化能量使用的用户
"""

import json
import time
import datetime
from typing import Dict, List, Optional
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

class SmallBudgetEnergyManager:
    def __init__(self, api_key: str = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"):
        """初始化小资金能量管理器"""
        self.client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=api_key))
        self.wallets = {}
        self.main_wallet = None
        self.config_file = "small_budget_config.json"
        self.load_config()
    
    def generate_small_wallet_system(self) -> Dict[str, Dict]:
        """生成适合小资金的3钱包系统"""
        print("🔧 正在生成小资金钱包系统 (3个钱包)...")
        
        wallets = {}
        wallet_configs = [
            ("wallet_A", "main", "主钱包", 10, "存放USDT和应急资金"),
            ("wallet_B", "energy", "能量钱包1", 10, "冻结TRX获取能量"),
            ("wallet_C", "energy", "能量钱包2", 10, "冻结TRX获取能量")
        ]
        
        for name, role, display_name, recommended_trx, description in wallet_configs:
            priv = PrivateKey.random()
            address = priv.public_key.to_base58check_address()
            
            wallets[name] = {
                "address": address,
                "private_key": priv.hex(),
                "role": role,
                "display_name": display_name,
                "recommended_trx": recommended_trx,
                "description": description,
                "created_time": datetime.datetime.now().isoformat(),
                "frozen_trx": 0,
                "energy_balance": 0
            }
            
            role_icon = "🏦" if role == "main" else "⚡"
            print(f"✅ {role_icon} {name} ({display_name}): {address}")
            print(f"   建议TRX: {recommended_trx} | {description}")
        
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
                print(f"✅ 已加载小资金钱包配置")
        except FileNotFoundError:
            print("⚠️ 配置文件不存在，将创建新的钱包系统")
            self.wallets = {}
            self.main_wallet = None
    
    def save_config(self):
        """保存钱包配置"""
        config = {
            "wallets": self.wallets,
            "main_wallet": self.main_wallet,
            "budget_type": "small_30trx",
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"💾 配置已保存到 {self.config_file}")
    
    def get_wallet_balances(self) -> Dict:
        """查询所有钱包余额"""
        balances = {}
        
        for name, wallet in self.wallets.items():
            try:
                address = wallet["address"]
                
                # 查询TRX余额
                trx_balance = self.client.get_account_balance(address)
                
                # 查询账户资源信息
                account_info = self.client.get_account(address)
                
                # 获取能量和冻结信息
                energy_balance = 0
                frozen_trx = 0
                
                if account_info:
                    if 'frozen' in account_info:
                        for frozen in account_info['frozen']:
                            if frozen.get('frozen_balance', 0) > 0:
                                frozen_trx += frozen['frozen_balance'] / 1_000_000
                    
                    if 'account_resource' in account_info:
                        energy_balance = account_info['account_resource'].get('energy_limit', 0)
                
                balances[name] = {
                    "address": address,
                    "trx_balance": trx_balance,
                    "frozen_trx": frozen_trx,
                    "energy_balance": energy_balance,
                    "role": wallet["role"],
                    "display_name": wallet["display_name"]
                }
                
            except Exception as e:
                print(f"❌ 查询 {name} 余额失败: {e}")
                balances[name] = {"error": str(e)}
        
        return balances
    
    def transfer_trx_to_energy_wallets(self, amount_per_wallet: float = 10.0):
        """从主钱包向能量钱包转账"""
        if not self.main_wallet:
            print("❌ 未设置主钱包")
            return False
        
        # 获取主钱包信息
        main_wallet_info = self.wallets["wallet_A"]
        energy_wallets = [(name, wallet) for name, wallet in self.wallets.items() 
                         if wallet["role"] == "energy"]
        
        total_needed = amount_per_wallet * len(energy_wallets)
        
        # 检查主钱包余额
        balances = self.get_wallet_balances()
        main_balance = balances["wallet_A"]["trx_balance"]
        
        if main_balance < total_needed + 5:  # 保留5 TRX作为应急
            print(f"❌ 主钱包余额不足: {main_balance:.2f} < {total_needed + 5:.2f}")
            print(f"💡 建议: 向主钱包 {self.main_wallet} 充值更多TRX")
            return False
        
        print(f"💸 开始从主钱包分发TRX...")
        print(f"每个能量钱包将获得: {amount_per_wallet} TRX")
        
        # 执行转账
        priv = PrivateKey.fromhex(main_wallet_info["private_key"])
        success_count = 0
        
        for name, wallet in energy_wallets:
            try:
                print(f"💸 向 {wallet['display_name']} 转账 {amount_per_wallet} TRX...")
                
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
                success_count += 1
                time.sleep(3)  # 避免网络拥堵
                
            except Exception as e:
                print(f"❌ 向 {name} 转账失败: {e}")
        
        print(f"📊 转账完成: {success_count}/{len(energy_wallets)} 成功")
        return success_count == len(energy_wallets)
    
    def freeze_all_energy_wallets(self, amount_per_wallet: float = 10.0):
        """冻结所有能量钱包的TRX"""
        energy_wallets = [(name, wallet) for name, wallet in self.wallets.items() 
                         if wallet["role"] == "energy"]
        
        print(f"🧊 开始冻结所有能量钱包的TRX...")
        success_count = 0
        
        for name, wallet in energy_wallets:
            try:
                priv = PrivateKey.fromhex(wallet["private_key"])
                owner = priv.public_key.to_base58check_address()
                amount_sun = int(amount_per_wallet * 1_000_000)
                
                print(f"🧊 {wallet['display_name']} 冻结 {amount_per_wallet} TRX...")
                
                txn = (
                    self.client.trx.freeze_balance(
                        owner=owner,
                        amount=amount_sun,
                        resource="ENERGY"
                    )
                    .build()
                    .sign(priv)
                    .broadcast()
                )
                
                # 更新钱包信息
                self.wallets[name]["frozen_trx"] += amount_per_wallet
                
                print(f"✅ {wallet['display_name']} 冻结成功，交易哈希: {txn['txid']}")
                success_count += 1
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ {wallet['display_name']} 冻结失败: {e}")
        
        self.save_config()
        print(f"📊 冻结完成: {success_count}/{len(energy_wallets)} 成功")
        return success_count == len(energy_wallets)
    
    def delegate_all_energy_to_main(self):
        """将所有能量委托给主钱包"""
        energy_wallets = [(name, wallet) for name, wallet in self.wallets.items() 
                         if wallet["role"] == "energy"]
        
        print(f"🔄 开始委托所有能量给主钱包...")
        success_count = 0
        
        for name, wallet in energy_wallets:
            try:
                priv = PrivateKey.fromhex(wallet["private_key"])
                owner = priv.public_key.to_base58check_address()
                
                print(f"🔄 {wallet['display_name']} 委托能量给主钱包...")
                
                # 获取当前能量余额
                balances = self.get_wallet_balances()
                energy_amount = balances[name]["energy_balance"]
                
                if energy_amount <= 0:
                    print(f"⚠️ {wallet['display_name']} 没有可委托的能量")
                    continue
                
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
                
                print(f"✅ {wallet['display_name']} 委托成功，交易哈希: {txn['txid']}")
                success_count += 1
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ {wallet['display_name']} 委托失败: {e}")
        
        print(f"📊 委托完成: {success_count}/{len(energy_wallets)} 成功")
        return success_count > 0
    
    def execute_small_budget_strategy(self):
        """执行小资金策略"""
        print("\n" + "="*60)
        print("🚀 执行30 TRX小资金能量策略")
        print("="*60)
        
        # 步骤1: 分发TRX
        print("\n📋 步骤1: 分发TRX到能量钱包")
        if not self.transfer_trx_to_energy_wallets(10.0):
            print("❌ TRX分发失败，请检查主钱包余额")
            return False
        
        print("⏱️ 等待5秒后继续...")
        time.sleep(5)
        
        # 步骤2: 冻结TRX获取能量
        print("\n📋 步骤2: 冻结TRX获取能量")
        if not self.freeze_all_energy_wallets(10.0):
            print("❌ TRX冻结失败")
            return False
        
        print("⏱️ 等待5秒后继续...")
        time.sleep(5)
        
        # 步骤3: 委托能量给主钱包
        print("\n📋 步骤3: 委托能量给主钱包")
        if not self.delegate_all_energy_to_main():
            print("❌ 能量委托失败")
            return False
        
        print("\n✅ 小资金策略执行完成！")
        print("💡 现在主钱包应该有约20,000能量可用")
        return True
    
    def show_strategy_summary(self):
        """显示策略总结"""
        print("\n" + "="*60)
        print("📊 30 TRX 小资金策略总结")
        print("="*60)
        
        balances = self.get_wallet_balances()
        
        total_trx = 0
        total_energy = 0
        
        for name, balance in balances.items():
            if "error" in balance:
                continue
            
            icon = "🏦" if balance["role"] == "main" else "⚡"
            print(f"\n{icon} {balance['display_name']} ({name}):")
            print(f"  📮 地址: {balance['address']}")
            print(f"  💰 TRX余额: {balance['trx_balance']:.2f} TRX")
            print(f"  🧊 冻结TRX: {balance['frozen_trx']:.2f} TRX")
            print(f"  ⚡ 能量余额: {balance['energy_balance']:,} Energy")
            
            total_trx += balance['trx_balance'] + balance['frozen_trx']
            total_energy += balance['energy_balance']
        
        print(f"\n📈 总计:")
        print(f"  💰 总TRX: {total_trx:.2f} TRX")
        print(f"  ⚡ 总能量: {total_energy:,} Energy")
        
        if total_energy > 0:
            free_transfers = total_energy // 30000
            saved_trx = free_transfers * 15
            print(f"  🎯 可免费转账: {free_transfers} 次")
            print(f"  💰 节省手续费: {saved_trx} TRX")
            print(f"  📊 投资回报: {(saved_trx/20)*100:.1f}% (基于20 TRX投入)")
        
        print("="*60)

def main():
    """主函数"""
    manager = SmallBudgetEnergyManager()
    
    while True:
        print("\n" + "="*50)
        print("💰 30 TRX 小资金能量管理器")
        print("="*50)
        print("1. 生成小资金钱包系统 (3个钱包)")
        print("2. 查看钱包余额")
        print("3. 分发TRX到能量钱包")
        print("4. 执行完整策略 (分发→冻结→委托)")
        print("5. 策略效果总结")
        print("6. 导出钱包信息")
        print("0. 退出")
        print("-"*50)
        
        choice = input("请选择操作 (0-6): ").strip()
        
        if choice == "1":
            manager.generate_small_wallet_system()
            print("\n💡 下一步: 向主钱包充值30 TRX，然后执行完整策略")
            
        elif choice == "2":
            manager.show_strategy_summary()
            
        elif choice == "3":
            manager.transfer_trx_to_energy_wallets(10.0)
            
        elif choice == "4":
            manager.execute_small_budget_strategy()
            
        elif choice == "5":
            manager.show_strategy_summary()
            
        elif choice == "6":
            print("\n📋 钱包信息:")
            for name, wallet in manager.wallets.items():
                icon = "🏦" if wallet["role"] == "main" else "⚡"
                print(f"\n{icon} {wallet['display_name']} ({name}):")
                print(f"  地址: {wallet['address']}")
                print(f"  私钥: {wallet['private_key']}")
                print(f"  建议TRX: {wallet['recommended_trx']}")
            
        elif choice == "0":
            print("👋 再见!")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()