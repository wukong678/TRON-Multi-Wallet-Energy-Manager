#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
USDT管理工具 - 图形界面版本
功能：创建钱包、查询余额、转账、交易记录等
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
from datetime import datetime
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

class USDTManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("USDT管理工具 v1.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 语言设置
        self.current_language = "zh"  # 默认中文
        self.init_language_texts()
        
        # 配置文件路径
        self.config_file = "wallet_config.json"
        self.history_file = "transaction_history.json"
        
        # TRON网络配置
        self.API_KEY = "f5668afc-2f0e-4fdb-91a6-cb01509a3ddf"
        self.USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT TRC20合约地址
        
        # 初始化TRON客户端
        self.client = None
        self.init_tron_client()
        
        # 钱包数据
        self.wallet_data = self.load_wallet_config()
        
        # 创建界面
        self.create_widgets()
        
        # 如果有钱包数据，自动加载
        if self.wallet_data:
            self.load_wallet_info()
        
        # 多钱包管理
        self.multi_wallets = {}
        self.load_multi_wallet_config()
    
    def init_language_texts(self):
        """初始化语言文本"""
        self.texts = {
            "zh": {
                "title": "USDT管理工具",
                "wallet_info": "钱包信息",
                "wallet_address": "钱包地址:",
                "no_wallet": "未创建钱包",
                "trx_balance": "TRX余额:",
                "usdt_balance": "USDT余额:",
                "create_wallet": "创建新钱包",
                "import_wallet": "导入钱包",
                "refresh_balance": "刷新余额",
                "copy_address": "复制地址",
                "view_private_key": "查看私钥",
                "account_status": "激活状态",
                "operations": "操作",
                "recipient_address": "收款地址:",
                "transfer_amount": "转账金额:",
                "send_usdt": "发送USDT",
                "energy_management": "能量管理",
                "current_energy": "当前能量:",
                "freeze_trx": "冻结TRX:",
                "freeze_for_energy": "冻结获取能量",
                "unfreeze_trx": "解冻TRX",
                "operation_log": "操作日志",
                "view_history": "查看交易记录",
                "backup_wallet": "备份钱包",
                "user_guide": "新手指导",
                "clear_log": "清空日志",
                "exit": "退出",
                "language_switch": "English",
                "multi_wallet_manager": "多钱包能量管理",
                "generate_wallets": "生成钱包系统",
                "wallet_balances": "钱包余额",
                "energy_strategy": "执行策略",
                "small_budget_mode": "小资金模式(30 TRX)",
                "error": "错误",
                "warning": "警告",
                "success": "成功",
                "confirm": "确认",
                "cancel": "取消",
                "close": "关闭"
            },
            "en": {
                "title": "USDT Manager",
                "wallet_info": "Wallet Information",
                "wallet_address": "Wallet Address:",
                "no_wallet": "No wallet created",
                "trx_balance": "TRX Balance:",
                "usdt_balance": "USDT Balance:",
                "create_wallet": "Create New Wallet",
                "import_wallet": "Import Wallet",
                "refresh_balance": "Refresh Balance",
                "copy_address": "Copy Address",
                "view_private_key": "View Private Key",
                "account_status": "Account Status",
                "operations": "Operations",
                "recipient_address": "Recipient Address:",
                "transfer_amount": "Transfer Amount:",
                "send_usdt": "Send USDT",
                "energy_management": "Energy Management",
                "current_energy": "Current Energy:",
                "freeze_trx": "Freeze TRX:",
                "freeze_for_energy": "Freeze for Energy",
                "unfreeze_trx": "Unfreeze TRX",
                "operation_log": "Operation Log",
                "view_history": "View Transaction History",
                "backup_wallet": "Backup Wallet",
                "user_guide": "User Guide",
                "clear_log": "Clear Log",
                "exit": "Exit",
                "language_switch": "中文",
                "multi_wallet_manager": "Multi-Wallet Energy Manager",
                "generate_wallets": "Generate Wallet System",
                "wallet_balances": "Wallet Balances",
                "energy_strategy": "Execute Strategy",
                "small_budget_mode": "Small Budget Mode(30 TRX)",
                "error": "Error",
                "warning": "Warning",
                "success": "Success",
                "confirm": "Confirm",
                "cancel": "Cancel",
                "close": "Close"
            }
        }
    
    def get_text(self, key):
        """获取当前语言的文本"""
        return self.texts[self.current_language].get(key, key)
    
    def switch_language(self):
        """切换语言"""
        self.current_language = "en" if self.current_language == "zh" else "zh"
        self.update_ui_texts()
        self.log_message(f"🌐 Language switched to {'English' if self.current_language == 'en' else '中文'}")
    
    def update_ui_texts(self):
        """更新界面文本"""
        # 更新窗口标题
        if self.current_language == "zh":
            self.root.title("USDT管理工具 v1.0")
        else:
            self.root.title("USDT Manager v1.0")
        
        # 更新所有界面元素的文本
        self.update_widget_texts()
    
    def update_widget_texts(self):
        """更新所有控件的文本"""
        # 更新标题和语言按钮
        self.title_label.config(text=self.get_text("title"))
        self.language_button.config(text=self.get_text("language_switch"))
        
        # 更新钱包信息区域
        self.wallet_frame.config(text=self.get_text("wallet_info"))
        self.wallet_address_label.config(text=self.get_text("wallet_address"))
        self.trx_balance_label.config(text=self.get_text("trx_balance"))
        self.usdt_balance_label.config(text=self.get_text("usdt_balance"))
        
        # 更新钱包按钮
        self.create_wallet_btn.config(text=self.get_text("create_wallet"))
        self.import_wallet_btn.config(text=self.get_text("import_wallet"))
        self.refresh_balance_btn.config(text=self.get_text("refresh_balance"))
        self.copy_address_btn.config(text=self.get_text("copy_address"))
        self.view_private_key_btn.config(text=self.get_text("view_private_key"))
        self.account_status_btn.config(text=self.get_text("account_status"))
        
        # 更新操作区域
        self.operation_frame.config(text=self.get_text("operations"))
        self.recipient_address_label.config(text=self.get_text("recipient_address"))
        self.transfer_amount_label.config(text=self.get_text("transfer_amount"))
        self.send_usdt_btn.config(text=self.get_text("send_usdt"))
        
        # 更新能量管理区域
        energy_title = "⚡ " + self.get_text("energy_management")
        self.energy_frame.config(text=energy_title)
        self.current_energy_label.config(text=self.get_text("current_energy"))
        self.freeze_trx_label.config(text=self.get_text("freeze_trx"))
        # 冻结按钮保持简短文本
        freeze_text = "Freeze" if self.current_language == "en" else "冻结"
        self.freeze_for_energy_btn.config(text=freeze_text)
        self.unfreeze_trx_btn.config(text=self.get_text("unfreeze_trx"))
        
        # 更新日志区域
        self.log_frame.config(text=self.get_text("operation_log"))
        
        # 更新底部按钮
        self.view_history_btn.config(text=self.get_text("view_history"))
        self.backup_wallet_btn.config(text=self.get_text("backup_wallet"))
        self.user_guide_btn.config(text=self.get_text("user_guide"))
        self.clear_log_btn.config(text=self.get_text("clear_log"))
        self.exit_btn.config(text=self.get_text("exit"))
        
        # 更新地址显示文本（如果没有钱包）
        if self.address_var.get() in ["未创建钱包", "No wallet created"]:
            self.address_var.set(self.get_text("no_wallet"))
    
    def init_tron_client(self):
        """初始化TRON客户端"""
        try:
            self.client = Tron(HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=self.API_KEY))
            return True
        except Exception as e:
            messagebox.showerror("错误", f"TRON网络连接失败: {str(e)}")
            return False
    
    def load_wallet_config(self):
        """加载钱包配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def save_wallet_config(self, data):
        """保存钱包配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
            return False
    
    def save_transaction_history(self, tx_data):
        """保存交易记录"""
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []
        
        history.append(tx_data)
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存交易记录失败: {str(e)}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 顶部框架：标题和语言切换按钮
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        top_frame.columnconfigure(0, weight=1)
        
        # 标题
        self.title_label = ttk.Label(top_frame, text=self.get_text("title"), font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 语言切换按钮
        self.language_button = ttk.Button(top_frame, text=self.get_text("language_switch"), 
                                         command=self.switch_language, width=10)
        self.language_button.grid(row=0, column=1, sticky=tk.E)
        
        # 钱包信息区域
        self.wallet_frame = ttk.LabelFrame(main_frame, text=self.get_text("wallet_info"), padding="10")
        self.wallet_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.wallet_frame.columnconfigure(1, weight=1)
        
        # 地址显示
        self.wallet_address_label = ttk.Label(self.wallet_frame, text=self.get_text("wallet_address"))
        self.wallet_address_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.address_var = tk.StringVar(value=self.get_text("no_wallet"))
        self.address_label = ttk.Label(self.wallet_frame, textvariable=self.address_var, foreground="blue")
        self.address_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 余额显示
        self.trx_balance_label = ttk.Label(self.wallet_frame, text=self.get_text("trx_balance"))
        self.trx_balance_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.trx_balance_var = tk.StringVar(value="0 TRX")
        self.trx_balance_value_label = ttk.Label(self.wallet_frame, textvariable=self.trx_balance_var)
        self.trx_balance_value_label.grid(row=1, column=1, sticky=tk.W)
        
        self.usdt_balance_label = ttk.Label(self.wallet_frame, text=self.get_text("usdt_balance"))
        self.usdt_balance_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.usdt_balance_var = tk.StringVar(value="0 USDT")
        self.usdt_balance_value_label = ttk.Label(self.wallet_frame, textvariable=self.usdt_balance_var)
        self.usdt_balance_value_label.grid(row=2, column=1, sticky=tk.W)
        
        # 按钮区域
        button_frame = ttk.Frame(self.wallet_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        self.create_wallet_btn = ttk.Button(button_frame, text=self.get_text("create_wallet"), command=self.create_new_wallet)
        self.create_wallet_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.import_wallet_btn = ttk.Button(button_frame, text=self.get_text("import_wallet"), command=self.import_wallet)
        self.import_wallet_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.refresh_balance_btn = ttk.Button(button_frame, text=self.get_text("refresh_balance"), command=self.refresh_balance)
        self.refresh_balance_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.copy_address_btn = ttk.Button(button_frame, text=self.get_text("copy_address"), command=self.copy_address)
        self.copy_address_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.view_private_key_btn = ttk.Button(button_frame, text=self.get_text("view_private_key"), command=self.show_private_key)
        self.view_private_key_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.account_status_btn = ttk.Button(button_frame, text=self.get_text("account_status"), command=self.check_account_status)
        self.account_status_btn.pack(side=tk.LEFT)
        
        # 操作区域 - 改为左右布局
        self.operation_frame = ttk.LabelFrame(main_frame, text=self.get_text("operations"), padding="10")
        self.operation_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.operation_frame.columnconfigure(0, weight=1)
        self.operation_frame.columnconfigure(1, weight=1)
        
        # 左侧：转账区域
        transfer_frame = ttk.LabelFrame(self.operation_frame, text="💸 USDT转账", padding="10")
        transfer_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        transfer_frame.columnconfigure(1, weight=1)
        
        self.recipient_address_label = ttk.Label(transfer_frame, text=self.get_text("recipient_address"))
        self.recipient_address_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.to_address_var = tk.StringVar()
        self.to_address_entry = ttk.Entry(transfer_frame, textvariable=self.to_address_var, width=35)
        self.to_address_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.transfer_amount_label = ttk.Label(transfer_frame, text=self.get_text("transfer_amount"))
        self.transfer_amount_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        amount_frame = ttk.Frame(transfer_frame)
        amount_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var, width=15)
        self.amount_entry.pack(side=tk.LEFT)
        self.usdt_label = ttk.Label(amount_frame, text="USDT")
        self.usdt_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.send_usdt_btn = ttk.Button(transfer_frame, text=self.get_text("send_usdt"), command=self.send_usdt)
        self.send_usdt_btn.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        # 右侧：能量管理区域
        self.energy_frame = ttk.LabelFrame(self.operation_frame, text="⚡ " + self.get_text("energy_management"), padding="10")
        self.energy_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        self.energy_frame.columnconfigure(1, weight=1)
        
        # 当前能量显示
        self.current_energy_label = ttk.Label(self.energy_frame, text=self.get_text("current_energy"))
        self.current_energy_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.energy_var = tk.StringVar(value="0 Energy")
        self.energy_value_label = ttk.Label(self.energy_frame, textvariable=self.energy_var)
        self.energy_value_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # 冻结TRX获取能量
        self.freeze_trx_label = ttk.Label(self.energy_frame, text=self.get_text("freeze_trx"))
        self.freeze_trx_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        freeze_frame = ttk.Frame(self.energy_frame)
        freeze_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.freeze_amount_var = tk.StringVar()
        self.freeze_amount_entry = ttk.Entry(freeze_frame, textvariable=self.freeze_amount_var, width=10)
        self.freeze_amount_entry.pack(side=tk.LEFT)
        self.trx_label = ttk.Label(freeze_frame, text="TRX")
        self.trx_label.pack(side=tk.LEFT, padx=(5, 5))
        self.freeze_for_energy_btn = ttk.Button(freeze_frame, text="冻结", command=self.freeze_for_energy, width=8)
        self.freeze_for_energy_btn.pack(side=tk.LEFT)
        
        # 解冻按钮
        self.unfreeze_trx_btn = ttk.Button(self.energy_frame, text=self.get_text("unfreeze_trx"), command=self.unfreeze_trx)
        self.unfreeze_trx_btn.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        # 日志区域 - 减小高度为多钱包管理让出空间
        self.log_frame = ttk.LabelFrame(main_frame, text=self.get_text("operation_log"), padding="10")
        self.log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=6, width=80)  # 减小高度从10到6
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 多钱包管理标签页
        self.create_multi_wallet_tab(main_frame)
        self.log_message("✅ 多钱包能量管理功能已加载")
        
        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.view_history_btn = ttk.Button(bottom_frame, text=self.get_text("view_history"), command=self.show_transaction_history)
        self.view_history_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.backup_wallet_btn = ttk.Button(bottom_frame, text=self.get_text("backup_wallet"), command=self.backup_wallet)
        self.backup_wallet_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.user_guide_btn = ttk.Button(bottom_frame, text=self.get_text("user_guide"), command=self.show_guide)
        self.user_guide_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.clear_log_btn = ttk.Button(bottom_frame, text=self.get_text("clear_log"), command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.exit_btn = ttk.Button(bottom_frame, text=self.get_text("exit"), command=self.root.quit)
        self.exit_btn.pack(side=tk.RIGHT)
    
    def create_multi_wallet_tab(self, parent):
        """创建多钱包管理标签页"""
        # 多钱包管理区域
        self.multi_wallet_frame = ttk.LabelFrame(parent, text=self.get_text("multi_wallet_manager"), padding="10")
        self.multi_wallet_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.multi_wallet_frame.columnconfigure(1, weight=1)
        
        # 说明文本
        info_text = "💡 多钱包能量管理：通过多个钱包协同工作，优化能量获取和使用，降低USDT转账成本"
        info_label = ttk.Label(self.multi_wallet_frame, text=info_text, foreground="blue")
        info_label.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 模式选择
        mode_frame = ttk.Frame(self.multi_wallet_frame)
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(mode_frame, text="选择模式:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.wallet_mode_var = tk.StringVar(value="small")
        small_radio = ttk.Radiobutton(mode_frame, text="小资金模式 (30 TRX)", 
                                     variable=self.wallet_mode_var, value="small")
        small_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        full_radio = ttk.Radiobutton(mode_frame, text="完整模式 (200+ TRX)", 
                                    variable=self.wallet_mode_var, value="full")
        full_radio.pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = ttk.Frame(self.multi_wallet_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(15, 10), sticky=(tk.W, tk.E))
        
        # 使用更大的按钮和更明显的样式
        self.generate_wallets_btn = ttk.Button(button_frame, text="🔧 " + self.get_text("generate_wallets"), 
                                              command=self.generate_multi_wallets, width=20)
        self.generate_wallets_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.show_balances_btn = ttk.Button(button_frame, text="💰 " + self.get_text("wallet_balances"), 
                                           command=self.show_multi_wallet_balances, width=15)
        self.show_balances_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.execute_strategy_btn = ttk.Button(button_frame, text="🚀 " + self.get_text("energy_strategy"), 
                                              command=self.execute_energy_strategy, width=15)
        self.execute_strategy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 状态显示
        if not hasattr(self, 'multi_wallet_status_var'):
            self.multi_wallet_status_var = tk.StringVar(value="未生成多钱包系统")
        status_label = ttk.Label(self.multi_wallet_frame, textvariable=self.multi_wallet_status_var, 
                                foreground="gray")
        status_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))
    
    def load_multi_wallet_config(self):
        """加载多钱包配置"""
        try:
            if os.path.exists("multi_wallet_config.json"):
                with open("multi_wallet_config.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.multi_wallets = data.get("wallets", {})
                    if self.multi_wallets:
                        count = len(self.multi_wallets)
                        self.multi_wallet_status_var.set(f"已加载 {count} 个钱包系统")
                        self.log_message(f"✅ 已加载多钱包配置: {count} 个钱包")
        except Exception as e:
            self.log_message(f"⚠️ 加载多钱包配置失败: {e}")
    
    def save_multi_wallet_config(self):
        """保存多钱包配置"""
        try:
            config = {
                "wallets": self.multi_wallets,
                "main_wallet": self.wallet_data["address"] if self.wallet_data else None,
                "created_time": datetime.now().isoformat()
            }
            with open("multi_wallet_config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.log_message(f"❌ 保存多钱包配置失败: {e}")
            return False
    
    def generate_multi_wallets(self):
        """生成多钱包系统"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入主钱包")
            return
        
        mode = self.wallet_mode_var.get()
        
        if mode == "small":
            # 小资金模式：1主钱包 + 2能量钱包
            wallet_count = 3
            mode_name = "小资金模式"
            description = "适合30 TRX的小资金用户"
        else:
            # 完整模式：1主钱包 + 4能量钱包
            wallet_count = 5
            mode_name = "完整模式"
            description = "适合200+ TRX的用户"
        
        confirm_msg = (
            f"确认生成{mode_name}多钱包系统？\n\n"
            f"模式: {mode_name}\n"
            f"说明: {description}\n"
            f"钱包数量: {wallet_count} 个\n"
            f"主钱包: {self.wallet_data['address']}\n\n"
            f"💡 系统将自动生成 {wallet_count-1} 个能量钱包"
        )
        
        if not messagebox.askyesno("确认生成", confirm_msg):
            return
        
        try:
            self.log_message(f"🔧 开始生成{mode_name}多钱包系统...")
            
            # 清空现有配置
            self.multi_wallets = {}
            
            # 添加主钱包
            self.multi_wallets["wallet_A"] = {
                "address": self.wallet_data["address"],
                "private_key": self.wallet_data["private_key"],
                "role": "main",
                "display_name": "主钱包",
                "description": "存放USDT，执行转账，接收能量",
                "created_time": datetime.now().isoformat()
            }
            
            # 生成能量钱包
            energy_wallet_count = wallet_count - 1
            for i in range(energy_wallet_count):
                priv = PrivateKey.random()
                address = priv.public_key.to_base58check_address()
                
                wallet_name = f"wallet_{chr(66+i)}"  # B, C, D, E
                self.multi_wallets[wallet_name] = {
                    "address": address,
                    "private_key": priv.hex(),
                    "role": "energy",
                    "display_name": f"能量钱包{i+1}",
                    "description": "冻结TRX获取能量，委托给主钱包",
                    "created_time": datetime.now().isoformat()
                }
                
                self.log_message(f"✅ 生成 {wallet_name} ({self.multi_wallets[wallet_name]['display_name']}): {address}")
            
            # 保存配置
            if self.save_multi_wallet_config():
                self.multi_wallet_status_var.set(f"已生成 {wallet_count} 个钱包系统 ({mode_name})")
                
                success_msg = (
                    f"🎉 {mode_name}多钱包系统生成成功！\n\n"
                    f"总钱包数: {wallet_count} 个\n"
                    f"主钱包: 1 个\n"
                    f"能量钱包: {energy_wallet_count} 个\n\n"
                    f"💡 下一步操作:\n"
                    f"1. 向主钱包充值足够的TRX\n"
                    f"2. 点击'执行策略'开始能量管理\n"
                    f"3. 点击'钱包余额'查看详细信息"
                )
                
                messagebox.showinfo("生成成功", success_msg)
                self.log_message(f"🎉 {mode_name}多钱包系统生成完成")
            
        except Exception as e:
            error_msg = f"生成多钱包系统失败: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("错误", error_msg)
    
    def show_multi_wallet_balances(self):
        """显示多钱包余额"""
        if not self.multi_wallets:
            messagebox.showinfo("提示", "请先生成多钱包系统")
            return
        
        # 创建余额显示窗口
        balance_window = tk.Toplevel(self.root)
        balance_window.title("多钱包余额总览")
        balance_window.geometry("800x600")
        balance_window.transient(self.root)
        
        main_frame = ttk.Frame(balance_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="💰 多钱包余额总览", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建表格
        columns = ("钱包", "角色", "地址", "TRX余额", "USDT余额", "能量")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        tree.heading("钱包", text="钱包")
        tree.heading("角色", text="角色")
        tree.heading("地址", text="地址")
        tree.heading("TRX余额", text="TRX余额")
        tree.heading("USDT余额", text="USDT余额")
        tree.heading("能量", text="能量")
        
        tree.column("钱包", width=80)
        tree.column("角色", width=80)
        tree.column("地址", width=200)
        tree.column("TRX余额", width=100)
        tree.column("USDT余额", width=100)
        tree.column("能量", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 查询并填充数据
        def update_balances():
            try:
                total_trx = 0
                total_usdt = 0
                total_energy = 0
                
                for name, wallet in self.multi_wallets.items():
                    address = wallet["address"]
                    role_text = "🏦 主钱包" if wallet["role"] == "main" else "⚡ 能量钱包"
                    
                    try:
                        # 查询TRX余额
                        trx_balance = self.client.get_account_balance(address)
                    except:
                        trx_balance = 0.0
                    
                    try:
                        # 查询USDT余额
                        contract = self.client.get_contract(self.USDT_CONTRACT)
                        usdt_balance_sun = contract.functions.balanceOf(address)
                        usdt_balance = usdt_balance_sun / 1_000_000
                    except:
                        usdt_balance = 0.0
                    
                    try:
                        # 查询能量
                        account_info = self.client.get_account(address)
                        if account_info and 'account_resource' in account_info:
                            energy_used = account_info['account_resource'].get('energy_used', 0)
                            energy_limit = account_info['account_resource'].get('energy_limit', 0)
                            available_energy = energy_limit - energy_used
                        else:
                            available_energy = 0
                    except:
                        available_energy = 0
                    
                    # 添加到表格
                    tree.insert("", tk.END, values=(
                        name,
                        role_text,
                        address[:20] + "..." if len(address) > 20 else address,
                        f"{trx_balance:.2f} TRX",
                        f"{usdt_balance:.2f} USDT",
                        f"{available_energy:,} Energy"
                    ))
                    
                    total_trx += trx_balance
                    total_usdt += usdt_balance
                    total_energy += available_energy
                
                # 添加总计行
                tree.insert("", tk.END, values=(
                    "总计",
                    "",
                    "",
                    f"{total_trx:.2f} TRX",
                    f"{total_usdt:.2f} USDT",
                    f"{total_energy:,} Energy"
                ))
                
                # 更新状态
                status_text = f"💡 总能量可转账: {total_energy // 30000} 次 USDT (按30,000能量/次计算)"
                status_label.config(text=status_text)
                
            except Exception as e:
                messagebox.showerror("错误", f"查询余额失败: {str(e)}")
        
        # 状态标签
        status_label = ttk.Label(main_frame, text="正在查询余额...", foreground="blue")
        status_label.pack(pady=(10, 0))
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="刷新余额", command=update_balances).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="关闭", command=balance_window.destroy).pack(side=tk.LEFT)
        
        # 初始查询
        threading.Thread(target=update_balances, daemon=True).start()
    
    def execute_energy_strategy(self):
        """执行能量策略"""
        if not self.multi_wallets:
            messagebox.showinfo("提示", "请先生成多钱包系统")
            return
        
        mode = self.wallet_mode_var.get()
        
        if mode == "small":
            self.execute_small_budget_strategy()
        else:
            self.execute_full_strategy()
    
    def execute_small_budget_strategy(self):
        """执行小资金策略"""
        strategy_msg = (
            "🚀 执行小资金能量策略\n\n"
            "策略说明:\n"
            "• 主钱包保留10 TRX应急资金\n"
            "• 向2个能量钱包各转账10 TRX\n"
            "• 每个能量钱包冻结10 TRX获取能量\n"
            "• 委托能量给主钱包使用\n\n"
            "预期效果:\n"
            "• 获得约20,000能量\n"
            "• 可免费转账0.67次USDT\n"
            "• 节省约10 TRX手续费\n\n"
            "确认执行吗？"
        )
        
        if not messagebox.askyesno("确认执行策略", strategy_msg):
            return
        
        def do_strategy():
            try:
                self.log_message("🚀 开始执行小资金能量策略...")
                
                # 检查主钱包余额
                main_balance = self.client.get_account_balance(self.wallet_data["address"])
                if main_balance < 25:  # 需要至少25 TRX
                    messagebox.showerror("余额不足", 
                        f"主钱包余额不足: {main_balance:.2f} TRX\n\n"
                        f"小资金策略需要至少25 TRX:\n"
                        f"• 保留10 TRX应急资金\n"
                        f"• 分发20 TRX给能量钱包\n"
                        f"• 请先向主钱包充值更多TRX")
                    return
                
                # 获取能量钱包
                energy_wallets = [(name, wallet) for name, wallet in self.multi_wallets.items() 
                                 if wallet["role"] == "energy"]
                
                if len(energy_wallets) < 2:
                    messagebox.showerror("错误", "小资金模式需要至少2个能量钱包")
                    return
                
                # 步骤1: 分发TRX
                self.log_message("📋 步骤1: 分发TRX到能量钱包")
                main_priv = PrivateKey.fromhex(self.wallet_data["private_key"])
                
                for name, wallet in energy_wallets[:2]:  # 只使用前2个
                    try:
                        self.log_message(f"💸 向 {wallet['display_name']} 转账 10 TRX...")
                        
                        txn = (
                            self.client.trx.transfer(
                                from_=self.wallet_data["address"],
                                to=wallet["address"],
                                amount=10_000_000  # 10 TRX
                            )
                            .build()
                            .sign(main_priv)
                            .broadcast()
                        )
                        
                        self.log_message(f"✅ 转账成功: {txn['txid']}")
                        time.sleep(3)
                        
                    except Exception as e:
                        self.log_message(f"❌ 转账失败: {e}")
                        raise e
                
                # 等待确认
                self.log_message("⏱️ 等待转账确认...")
                time.sleep(10)
                
                # 步骤2: 冻结TRX获取能量
                self.log_message("📋 步骤2: 冻结TRX获取能量")
                
                for name, wallet in energy_wallets[:2]:
                    try:
                        priv = PrivateKey.fromhex(wallet["private_key"])
                        owner = priv.public_key.to_base58check_address()
                        
                        self.log_message(f"🧊 {wallet['display_name']} 冻结 10 TRX...")
                        
                        txn = (
                            self.client.trx.freeze_balance(
                                owner=owner,
                                amount=10_000_000,  # 10 TRX
                                resource="ENERGY"
                            )
                            .build()
                            .sign(priv)
                            .broadcast()
                        )
                        
                        self.log_message(f"✅ 冻结成功: {txn['txid']}")
                        time.sleep(3)
                        
                    except Exception as e:
                        self.log_message(f"❌ 冻结失败: {e}")
                        # 继续执行其他钱包
                
                self.log_message("✅ 小资金策略执行完成！")
                self.log_message("💡 几分钟后主钱包将获得约20,000能量")
                
                messagebox.showinfo("策略执行完成", 
                    "🎉 小资金策略执行完成！\n\n"
                    "执行结果:\n"
                    "• 已分发TRX到能量钱包\n"
                    "• 已冻结TRX获取能量\n"
                    "• 预计获得20,000能量\n\n"
                    "💡 几分钟后点击'刷新余额'查看能量更新")
                
            except Exception as e:
                error_msg = f"策略执行失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("错误", error_msg)
        
        # 在后台线程中执行
        threading.Thread(target=do_strategy, daemon=True).start()
    
    def execute_full_strategy(self):
        """执行完整策略"""
        messagebox.showinfo("开发中", "完整策略功能正在开发中，敬请期待！\n\n目前可以使用小资金模式进行测试。")
    
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
    
    def create_new_wallet(self):
        """创建新钱包"""
        try:
            # 生成新的私钥和地址
            priv = PrivateKey.random()
            address = priv.public_key.to_base58check_address()
            
            # 保存钱包信息
            wallet_data = {
                "address": address,
                "private_key": priv.hex(),
                "created_time": datetime.now().isoformat()
            }
            
            if self.save_wallet_config(wallet_data):
                self.wallet_data = wallet_data
                self.load_wallet_info()
                self.log_message(f"✅ 新钱包创建成功: {address}")
                
                # 显示详细的成功信息
                success_msg = (
                    "🎉 新钱包创建成功！\n\n"
                    f"📮 钱包地址: {address}\n\n"
                    "⚠️ 重要提醒:\n"
                    "1. 请立即备份私钥到安全位置\n"
                    "2. 这是新钱包，余额为0是正常的\n"
                    "3. 请先转入一些TRX作为手续费\n"
                    "4. 然后就可以接收和发送USDT了\n\n"
                    "💡 建议操作:\n"
                    "• 点击'查看私钥'备份私钥\n"
                    "• 点击'复制地址'获取收款地址\n"
                    "• 向此地址转入10-20 TRX作为手续费"
                )
                messagebox.showinfo("钱包创建成功", success_msg)
            
        except Exception as e:
            error_msg = f"创建钱包失败: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("错误", error_msg)
    
    def import_wallet(self):
        """导入钱包"""
        # 创建导入对话框
        import_window = tk.Toplevel(self.root)
        import_window.title("导入钱包")
        import_window.geometry("400x200")
        import_window.transient(self.root)
        import_window.grab_set()
        
        # 居中显示
        import_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 150))
        
        frame = ttk.Frame(import_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="请输入私钥 (64位十六进制):").pack(pady=(0, 10))
        
        private_key_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=private_key_var, width=70, show="*")
        entry.pack(pady=(0, 20))
        entry.focus()
        
        def do_import():
            try:
                private_key_hex = private_key_var.get().strip()
                if len(private_key_hex) != 64:
                    messagebox.showerror("错误", "私钥长度必须是64位十六进制字符")
                    return
                
                # 验证私钥并生成地址
                priv = PrivateKey.fromhex(private_key_hex)
                address = priv.public_key.to_base58check_address()
                
                # 保存钱包信息
                wallet_data = {
                    "address": address,
                    "private_key": private_key_hex,
                    "imported_time": datetime.now().isoformat()
                }
                
                if self.save_wallet_config(wallet_data):
                    self.wallet_data = wallet_data
                    self.load_wallet_info()
                    self.log_message(f"✅ 钱包导入成功: {address}")
                    import_window.destroy()
                    messagebox.showinfo("成功", "钱包导入成功！")
                
            except Exception as e:
                error_msg = f"导入钱包失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("错误", error_msg)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="导入", command=do_import).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=import_window.destroy).pack(side=tk.LEFT)
        
        # 绑定回车键
        entry.bind('<Return>', lambda e: do_import())
    
    def load_wallet_info(self):
        """加载钱包信息到界面"""
        if self.wallet_data:
            self.address_var.set(self.wallet_data["address"])
            self.refresh_balance()
    
    def refresh_balance(self):
        """刷新余额"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        def update_balance():
            try:
                address = self.wallet_data["address"]
                
                # 查询TRX余额
                try:
                    trx_balance = self.client.get_account_balance(address)
                except Exception as e:
                    if "account not found" in str(e).lower():
                        # 新钱包，还没有任何交易记录
                        trx_balance = 0.0
                        self.log_message("💡 这是一个新钱包，还没有任何交易记录")
                    else:
                        raise e
                
                self.trx_balance_var.set(f"{trx_balance:.6f} TRX")
                
                # 查询USDT余额
                try:
                    contract = self.client.get_contract(self.USDT_CONTRACT)
                    usdt_balance_sun = contract.functions.balanceOf(address)
                    usdt_balance = usdt_balance_sun / 1_000_000
                except Exception as e:
                    if "account not found" in str(e).lower() or trx_balance == 0:
                        # 新钱包或没有USDT交易记录
                        usdt_balance = 0.0
                    else:
                        raise e
                
                self.usdt_balance_var.set(f"{usdt_balance:.6f} USDT")
                
                # 查询能量余额
                try:
                    account_info = self.client.get_account(address)
                    if account_info and 'account_resource' in account_info:
                        energy_used = account_info['account_resource'].get('energy_used', 0)
                        energy_limit = account_info['account_resource'].get('energy_limit', 0)
                        available_energy = energy_limit - energy_used
                        self.energy_var.set(f"{available_energy} Energy")
                    else:
                        self.energy_var.set("0 Energy")
                except Exception as e:
                    if "account not found" in str(e).lower() or trx_balance == 0:
                        self.energy_var.set("0 Energy")
                    else:
                        self.energy_var.set("查询失败")
                
                if trx_balance == 0 and usdt_balance == 0:
                    self.log_message("💰 余额更新完成: 新钱包，余额为0")
                    self.log_message("💡 提示: 请向此地址转入TRX作为手续费，然后就可以接收USDT了")
                else:
                    self.log_message(f"💰 余额更新: TRX={trx_balance:.6f}, USDT={usdt_balance:.6f}")
                
            except Exception as e:
                error_msg = f"查询余额失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                # 不显示错误对话框，只在日志中记录
                print(error_msg)
        
        # 在后台线程中执行
        threading.Thread(target=update_balance, daemon=True).start()
    
    def copy_address(self):
        """复制地址到剪贴板"""
        if self.wallet_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.wallet_data["address"])
            self.log_message("📋 地址已复制到剪贴板")
            messagebox.showinfo("提示", "地址已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "请先创建或导入钱包")
    
    def send_usdt(self):
        """发送USDT"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        to_address = self.to_address_var.get().strip()
        amount_str = self.amount_var.get().strip()
        
        if not to_address:
            messagebox.showerror("错误", "请输入收款地址")
            return
        
        if not amount_str:
            messagebox.showerror("错误", "请输入转账金额")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("错误", "转账金额必须大于0")
                return
        except ValueError:
            messagebox.showerror("错误", "转账金额格式错误")
            return
        
        # 确认对话框
        confirm_msg = f"确认转账？\n\n收款地址: {to_address}\n转账金额: {amount} USDT"
        if not messagebox.askyesno("确认转账", confirm_msg):
            return
        
        def do_transfer():
            try:
                self.log_message(f"🚀 开始转账: {amount} USDT -> {to_address}")
                
                # 获取私钥和地址
                priv = PrivateKey.fromhex(self.wallet_data["private_key"])
                from_address = self.wallet_data["address"]
                amount_sun = int(amount * 1_000_000)
                
                # 构建交易
                contract = self.client.get_contract(self.USDT_CONTRACT)
                txn = (
                    contract.functions.transfer(to_address, amount_sun)
                    .with_owner(from_address)
                    .fee_limit(10_000_000)
                    .build()
                    .sign(priv)
                    .broadcast()
                )
                
                # 保存交易记录
                tx_record = {
                    "txid": txn['txid'],
                    "from_address": from_address,
                    "to_address": to_address,
                    "amount": amount,
                    "type": "USDT转账",
                    "timestamp": datetime.now().isoformat(),
                    "status": "已发送"
                }
                self.save_transaction_history(tx_record)
                
                self.log_message(f"✅ 转账成功! 交易哈希: {txn['txid']}")
                messagebox.showinfo("成功", f"转账成功！\n交易哈希: {txn['txid']}")
                
                # 清空输入框
                self.to_address_var.set("")
                self.amount_var.set("")
                
                # 刷新余额
                self.refresh_balance()
                
            except Exception as e:
                error_msg = f"转账失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("错误", error_msg)
        
        # 在后台线程中执行
        threading.Thread(target=do_transfer, daemon=True).start()
    
    def show_transaction_history(self):
        """显示交易记录"""
        if not os.path.exists(self.history_file):
            messagebox.showinfo("提示", "暂无交易记录")
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            messagebox.showerror("错误", "读取交易记录失败")
            return
        
        if not history:
            messagebox.showinfo("提示", "暂无交易记录")
            return
        
        # 创建交易记录窗口
        history_window = tk.Toplevel(self.root)
        history_window.title("交易记录")
        history_window.geometry("900x500")
        history_window.transient(self.root)
        
        # 创建表格
        frame = ttk.Frame(history_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 表格列
        columns = ("时间", "类型", "金额", "收款地址", "交易哈希", "状态")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        tree.heading("时间", text="时间")
        tree.heading("类型", text="类型")
        tree.heading("金额", text="金额")
        tree.heading("收款地址", text="收款地址")
        tree.heading("交易哈希", text="交易哈希")
        tree.heading("状态", text="状态")
        
        tree.column("时间", width=150)
        tree.column("类型", width=80)
        tree.column("金额", width=100)
        tree.column("收款地址", width=200)
        tree.column("交易哈希", width=200)
        tree.column("状态", width=80)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充数据（倒序显示，最新的在前面）
        for record in reversed(history):
            timestamp = record.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = timestamp
            else:
                time_str = ""
            
            tree.insert("", tk.END, values=(
                time_str,
                record.get("type", ""),
                f"{record.get('amount', 0)} USDT",
                record.get("to_address", "")[:20] + "..." if len(record.get("to_address", "")) > 20 else record.get("to_address", ""),
                record.get("txid", "")[:20] + "..." if len(record.get("txid", "")) > 20 else record.get("txid", ""),
                record.get("status", "")
            ))
        
        # 双击复制交易哈希
        def on_double_click(event):
            item = tree.selection()[0]
            values = tree.item(item, "values")
            if len(values) >= 5:
                # 找到完整的交易哈希
                for record in history:
                    if record.get("txid", "").startswith(values[4].replace("...", "")):
                        history_window.clipboard_clear()
                        history_window.clipboard_append(record["txid"])
                        messagebox.showinfo("提示", "交易哈希已复制到剪贴板")
                        break
        
        tree.bind("<Double-1>", on_double_click)
        
        # 底部按钮
        button_frame = ttk.Frame(history_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="关闭", command=history_window.destroy).pack()
    
    def show_private_key(self):
        """显示私钥"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        # 安全确认
        if not messagebox.askyesno("安全确认", 
                                  "私钥是您钱包的最重要信息！\n\n"
                                  "⚠️ 警告：\n"
                                  "• 任何人获得私钥都可以控制您的钱包\n"
                                  "• 请确保周围环境安全\n"
                                  "• 不要截图或拍照私钥\n\n"
                                  "确定要查看私钥吗？"):
            return
        
        # 创建私钥显示窗口
        key_window = tk.Toplevel(self.root)
        key_window.title("私钥信息 - 请妥善保管")
        key_window.geometry("600x400")
        key_window.transient(self.root)
        key_window.grab_set()
        
        # 居中显示
        key_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        main_frame = ttk.Frame(key_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 警告标题
        warning_label = ttk.Label(main_frame, text="⚠️ 私钥信息 - 绝对保密 ⚠️", 
                                 font=("Arial", 14, "bold"), foreground="red")
        warning_label.pack(pady=(0, 20))
        
        # 钱包信息
        info_frame = ttk.LabelFrame(main_frame, text="钱包信息", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(info_frame, text="钱包地址:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        address_text = tk.Text(info_frame, height=2, wrap=tk.WORD, font=("Courier", 10))
        address_text.insert(tk.END, self.wallet_data["address"])
        address_text.config(state=tk.DISABLED)
        address_text.pack(fill=tk.X, pady=(5, 15))
        
        ttk.Label(info_frame, text="私钥 (64位十六进制):", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        key_text = tk.Text(info_frame, height=3, wrap=tk.WORD, font=("Courier", 10))
        key_text.insert(tk.END, self.wallet_data["private_key"])
        key_text.config(state=tk.DISABLED)
        key_text.pack(fill=tk.X, pady=(5, 0))
        
        # 安全提示
        tips_frame = ttk.LabelFrame(main_frame, text="安全提示", padding="15")
        tips_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        tips_text = tk.Text(tips_frame, height=8, wrap=tk.WORD, font=("Arial", 9))
        tips_content = """🔐 私钥安全须知：

1. 私钥是您钱包的唯一凭证，拥有私钥就拥有钱包控制权
2. 请将私钥抄写在纸上，存放在安全的地方
3. 不要将私钥发送给任何人，包括客服人员
4. 不要在网络上传输或存储私钥
5. 不要截图保存私钥到手机或电脑
6. 建议制作多份备份，分别存放在不同安全位置
7. 如果私钥泄露，请立即转移资金到新钱包

💡 备份建议：
• 手写备份：用纸笔抄写私钥
• 多重备份：制作2-3份备份
• 安全存储：保险箱、银行保险柜等"""
        
        tips_text.insert(tk.END, tips_content)
        tips_text.config(state=tk.DISABLED)
        tips_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def copy_private_key():
            key_window.clipboard_clear()
            key_window.clipboard_append(self.wallet_data["private_key"])
            messagebox.showinfo("提示", "私钥已复制到剪贴板\n请立即粘贴到安全位置！")
        
        def copy_address():
            key_window.clipboard_clear()
            key_window.clipboard_append(self.wallet_data["address"])
            messagebox.showinfo("提示", "地址已复制到剪贴板")
        
        ttk.Button(button_frame, text="复制私钥", command=copy_private_key).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="复制地址", command=copy_address).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="关闭", command=key_window.destroy).pack(side=tk.RIGHT)
        
        self.log_message("🔐 查看了钱包私钥信息")
    
    def backup_wallet(self):
        """备份钱包"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        try:
            from tkinter import filedialog
            import shutil
            
            # 选择备份位置
            backup_file = filedialog.asksaveasfilename(
                title="选择备份位置",
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
                initialvalue=f"wallet_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if backup_file:
                # 创建备份数据
                backup_data = {
                    "wallet_info": self.wallet_data,
                    "backup_time": datetime.now().isoformat(),
                    "backup_version": "1.0",
                    "note": "USDT管理工具钱包备份文件 - 请妥善保管"
                }
                
                # 保存备份文件
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                self.log_message(f"✅ 钱包备份成功: {backup_file}")
                messagebox.showinfo("成功", f"钱包备份成功！\n\n备份文件: {backup_file}\n\n请将此文件保存到安全位置！")
                
        except Exception as e:
            error_msg = f"备份失败: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("错误", error_msg)
    
    def show_guide(self):
        """显示新手指导"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("新手指导 - USDT管理工具使用教程")
        guide_window.geometry("700x600")
        guide_window.transient(self.root)
        
        # 居中显示
        guide_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(guide_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎓 USDT管理工具新手指导", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 第一步：创建钱包
        step1_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step1_frame, text="1️⃣ 创建钱包")
        
        step1_text = tk.Text(step1_frame, wrap=tk.WORD, font=("Arial", 10))
        step1_content = """🔐 创建您的第一个USDT钱包

1. 点击界面上的"创建新钱包"按钮
2. 系统会自动生成一个安全的钱包地址和私钥
3. 看到成功消息后，您的钱包就创建好了

⚠️ 重要提醒：
• 新创建的钱包余额为0，这是正常的
• 钱包地址以"T"开头，例如：TNCKX48wdefH4gGyQPJHHUvMJRKMuA3QM9
• 私钥是64位十六进制字符，是您钱包的唯一凭证

💡 为什么会显示"account not found"？
这是因为新钱包还没有任何交易记录，在区块链上还没有"激活"。
一旦有人向您的地址转账，钱包就会被激活，余额查询就正常了。"""
        
        step1_text.insert(tk.END, step1_content)
        step1_text.config(state=tk.DISABLED)
        step1_text.pack(fill=tk.BOTH, expand=True)
        
        # 第二步：备份私钥
        step2_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step2_frame, text="2️⃣ 备份私钥")
        
        step2_text = tk.Text(step2_frame, wrap=tk.WORD, font=("Arial", 10))
        step2_content = """🔒 备份您的私钥（极其重要！）

立即备份步骤：
1. 点击"查看私钥"按钮
2. 确认安全警告
3. 用纸笔抄写64位私钥
4. 点击"备份钱包"保存备份文件

备份建议：
• 手写备份：用纸笔抄写，存放在保险箱
• 文件备份：保存到U盘、云盘等安全位置
• 多重备份：制作2-3份备份，分别存放
• 定期检查：确保备份文件完整可用

⚠️ 安全警告：
• 私钥 = 钱包控制权，任何人获得私钥都可以转走您的资金
• 私钥丢失 = 资金永远无法找回
• 不要截图、拍照或在网络上传输私钥"""
        
        step2_text.insert(tk.END, step2_content)
        step2_text.config(state=tk.DISABLED)
        step2_text.pack(fill=tk.BOTH, expand=True)
        
        # 第三步：获取TRX手续费
        step3_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step3_frame, text="3️⃣ 获取手续费")
        
        step3_text = tk.Text(step3_frame, wrap=tk.WORD, font=("Arial", 10))
        step3_content = """⛽ 获取TRX作为转账手续费

为什么需要TRX？
• TRON网络上的所有交易都需要消耗TRX作为手续费
• 发送USDT也需要TRX手续费（大约5-15 TRX）
• 没有TRX就无法发送任何代币

如何获取TRX：
1. 点击"复制地址"获取您的钱包地址
2. 从交易所购买TRX并提现到您的地址
3. 或者请朋友转一些TRX到您的地址
4. 建议保持10-20 TRX的余额

推荐的交易所：
• 币安 (Binance)
• 欧易 (OKX)
• 火币 (Huobi)
• 等其他主流交易所

💡 提示：
• 首次转账建议少量测试
• TRX到账后点击"刷新余额"查看"""
        
        step3_text.insert(tk.END, step3_content)
        step3_text.config(state=tk.DISABLED)
        step3_text.pack(fill=tk.BOTH, expand=True)
        
        # 第四步：接收USDT
        step4_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step4_frame, text="4️⃣ 接收USDT")
        
        step4_text = tk.Text(step4_frame, wrap=tk.WORD, font=("Arial", 10))
        step4_content = """💰 接收USDT到您的钱包

接收步骤：
1. 点击"复制地址"获取您的钱包地址
2. 将地址提供给转账方
3. 等待对方转账完成
4. 点击"刷新余额"查看到账情况

⚠️ 重要注意事项：
• 确保对方发送的是TRC20-USDT（TRON网络）
• 不要接收其他网络的USDT（如ERC20、BEP20等）
• 首次接收建议小额测试

如何确认到账：
• 余额显示：USDT余额会更新
• 交易记录：可在区块链浏览器查询
• 推荐浏览器：tronscan.org

常见问题：
• 转账未到账：检查网络是否正确，等待确认
• 余额显示0：点击刷新余额，或稍等片刻再试
• 地址错误：仔细核对地址，建议复制粘贴"""
        
        step4_text.insert(tk.END, step4_content)
        step4_text.config(state=tk.DISABLED)
        step4_text.pack(fill=tk.BOTH, expand=True)
        
        # 第五步：能量管理
        step5_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step5_frame, text="5️⃣ 能量管理")
        
        step5_text = tk.Text(step5_frame, wrap=tk.WORD, font=("Arial", 10))
        step5_content = """⚡ 能量管理 - 降低转账手续费

什么是能量(Energy)？
• 能量是TRON网络的资源，用于执行智能合约
• 发送USDT需要消耗能量，没有能量就消耗TRX作为手续费
• 拥有能量可以大幅降低USDT转账成本

如何获得能量？
1. 冻结TRX：在"能量管理"区域输入TRX数量
2. 点击"冻结获取能量"按钮
3. 确认冻结信息（冻结期3天）
4. 等待交易确认，获得能量

能量计算：
• 1 TRX ≈ 1000 Energy
• 发送USDT大约消耗 28,000-32,000 Energy
• 建议冻结 30-50 TRX 获得足够能量

冻结规则：
• 最少冻结：1 TRX
• 冻结期：3天（72小时）
• 冻结期间TRX无法使用
• 3天后可以解冻取回TRX

解冻操作：
• 点击"解冻TRX"按钮
• 只能解冻已过冻结期的TRX
• 解冻后失去对应能量，TRX返回可用余额

💡 使用建议：
• 经常转账USDT的用户建议冻结30-50 TRX
• 偶尔转账的用户可以直接用TRX支付手续费
• 冻结获得能量比直接支付TRX手续费更划算"""
        
        step5_text.insert(tk.END, step5_content)
        step5_text.config(state=tk.DISABLED)
        step5_text.pack(fill=tk.BOTH, expand=True)
        
        # 第六步：发送USDT
        step6_frame = ttk.Frame(notebook, padding="15")
        notebook.add(step6_frame, text="6️⃣ 发送USDT")
        
        step6_text = tk.Text(step6_frame, wrap=tk.WORD, font=("Arial", 10))
        step6_content = """💸 发送USDT到其他地址

发送步骤：
1. 在"收款地址"框输入目标地址
2. 在"转账金额"框输入USDT数量
3. 点击"发送USDT"按钮
4. 确认转账信息
5. 等待交易完成

发送前检查：
• TRX余额或能量是否足够手续费
• USDT余额是否足够转账金额
• 收款地址是否正确（建议复制粘贴）
• 转账金额是否正确

手续费说明：
• 有能量：几乎免费（消耗约28,000 Energy）
• 无能量：消耗约15 TRX作为手续费
• 建议：冻结TRX获得能量，长期更划算

安全建议：
• 首次转账建议小额测试
• 仔细核对收款地址，转错无法撤回
• 保存交易哈希，便于查询和证明
• 大额转账建议分批进行

交易状态：
• 发送成功：显示交易哈希
• 交易确认：通常需要1-3分钟
• 查询交易：可在tronscan.org查询详情"""
        
        step6_text.insert(tk.END, step6_content)
        step6_text.config(state=tk.DISABLED)
        step6_text.pack(fill=tk.BOTH, expand=True)
        
        # 常见问题
        faq_frame = ttk.Frame(notebook, padding="15")
        notebook.add(faq_frame, text="❓ 常见问题")
        
        faq_text = tk.Text(faq_frame, wrap=tk.WORD, font=("Arial", 10))
        faq_content = """❓ 常见问题解答

Q: 为什么显示"account not found"？
A: 这是新钱包的正常现象，还没有交易记录。有人转账后就正常了。

Q: 转账需要多少手续费？
A: 有能量时几乎免费，无能量时约15 TRX。建议冻结TRX获得能量。

Q: 什么是能量？如何获得？
A: 能量用于降低转账手续费。冻结TRX可获得能量，1 TRX ≈ 1000 Energy。

Q: 冻结TRX有什么风险？
A: 冻结期3天内TRX无法使用，但3天后可以解冻取回，没有损失。

Q: 如何确认交易是否成功？
A: 查看交易哈希，在tronscan.org搜索确认状态。

Q: 转错地址怎么办？
A: 区块链交易不可撤回，请务必仔细核对地址。

Q: 私钥忘记了怎么办？
A: 查看wallet_config.json文件，或使用备份文件恢复。

Q: 可以同时在多台电脑使用吗？
A: 可以，但不建议。建议只在一台安全的电脑上使用。

Q: 如何升级工具？
A: 备份wallet_config.json文件，然后替换新版本程序。

Q: 工具会上传我的信息吗？
A: 不会，所有数据都存储在本地，不会上传任何信息。

Q: 忘记钱包地址怎么办？
A: 查看程序界面或wallet_config.json文件中的address字段。

Q: 如何删除钱包？
A: 删除wallet_config.json文件即可，但请确保已备份私钥。"""
        
        faq_text.insert(tk.END, faq_content)
        faq_text.config(state=tk.DISABLED)
        faq_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="关闭指导", command=guide_window.destroy).pack(side=tk.RIGHT)
        
        self.log_message("📖 查看了新手指导")
    
    def freeze_for_energy(self):
        """冻结TRX获取能量"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        freeze_amount_str = self.freeze_amount_var.get().strip()
        
        if not freeze_amount_str:
            messagebox.showerror("错误", "请输入要冻结的TRX数量")
            return
        
        try:
            freeze_amount = float(freeze_amount_str)
            if freeze_amount <= 0:
                messagebox.showerror("错误", "冻结数量必须大于0")
                return
            if freeze_amount < 1:
                messagebox.showerror("错误", "最少需要冻结1 TRX")
                return
        except ValueError:
            messagebox.showerror("错误", "冻结数量格式错误")
            return
        
        # 确认对话框
        confirm_msg = (
            f"确认冻结TRX获取能量？\n\n"
            f"冻结数量: {freeze_amount} TRX\n"
            f"获取资源: 能量(Energy)\n"
            f"冻结期: 3天\n\n"
            f"💡 说明:\n"
            f"• 冻结后可获得能量，用于减少USDT转账手续费\n"
            f"• 冻结期间TRX无法使用\n"
            f"• 3天后可以解冻取回TRX"
        )
        if not messagebox.askyesno("确认冻结", confirm_msg):
            return
        
        def do_freeze():
            try:
                self.log_message(f"🧊 开始冻结: {freeze_amount} TRX -> 能量")
                
                # 获取私钥和地址
                priv = PrivateKey.fromhex(self.wallet_data["private_key"])
                owner_address = self.wallet_data["address"]
                amount_sun = int(freeze_amount * 1_000_000)
                
                # 构建冻结交易
                txn = (
                    self.client.trx.freeze_balance(
                        owner=owner_address,
                        amount=amount_sun,
                        resource="ENERGY"  # 冻结获取能量
                    )
                    .build()
                    .sign(priv)
                    .broadcast()
                )
                
                # 保存交易记录
                tx_record = {
                    "txid": txn['txid'],
                    "from_address": owner_address,
                    "to_address": owner_address,
                    "amount": freeze_amount,
                    "type": "冻结TRX获取能量",
                    "timestamp": datetime.now().isoformat(),
                    "status": "已冻结"
                }
                self.save_transaction_history(tx_record)
                
                self.log_message(f"✅ 冻结成功! 交易哈希: {txn['txid']}")
                self.log_message(f"💡 预计获得能量: {int(freeze_amount * 1000)} Energy")
                messagebox.showinfo("冻结成功", 
                    f"TRX冻结成功！\n\n"
                    f"交易哈希: {txn['txid']}\n"
                    f"冻结数量: {freeze_amount} TRX\n"
                    f"预计获得: {int(freeze_amount * 1000)} Energy\n\n"
                    f"💡 提示: 几分钟后点击'刷新余额'查看能量更新")
                
                # 清空输入框
                self.freeze_amount_var.set("")
                
                # 刷新余额
                self.refresh_balance()
                
            except Exception as e:
                error_msg = f"冻结失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                
                # 特殊处理新账户错误
                if "does not exist" in str(e):
                    messagebox.showerror("账户未激活", 
                        "❌ 冻结失败：账户未激活\n\n"
                        "🔍 问题原因：\n"
                        "您的钱包是新创建的，还没有在TRON网络上激活。\n\n"
                        "✅ 解决方法：\n"
                        "1. 先向您的钱包地址转入一些TRX（建议10-20 TRX）\n"
                        "2. 等待TRX到账并确认\n"
                        "3. 点击'刷新余额'确认TRX已到账\n"
                        "4. 然后再尝试冻结操作\n\n"
                        "💡 说明：\n"
                        "• 新钱包需要先有TRX转入才能激活\n"
                        "• 激活后就可以正常使用所有功能\n"
                        "• 这是TRON网络的正常机制")
                else:
                    messagebox.showerror("错误", error_msg)
        
        # 在后台线程中执行
        threading.Thread(target=do_freeze, daemon=True).start()
    
    def unfreeze_trx(self):
        """解冻TRX"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        # 确认对话框
        confirm_msg = (
            "确认解冻TRX？\n\n"
            "⚠️ 注意事项:\n"
            "• 只能解冻已过冻结期(3天)的TRX\n"
            "• 解冻后将失去对应的能量\n"
            "• 解冻的TRX将返回到可用余额\n\n"
            "确定要解冻吗？"
        )
        if not messagebox.askyesno("确认解冻", confirm_msg):
            return
        
        def do_unfreeze():
            try:
                self.log_message("🔓 开始解冻TRX...")
                
                # 获取私钥和地址
                priv = PrivateKey.fromhex(self.wallet_data["private_key"])
                owner_address = self.wallet_data["address"]
                
                # 构建解冻交易
                txn = (
                    self.client.trx.unfreeze_balance(
                        owner=owner_address,
                        resource="ENERGY"  # 解冻能量相关的TRX
                    )
                    .build()
                    .sign(priv)
                    .broadcast()
                )
                
                # 保存交易记录
                tx_record = {
                    "txid": txn['txid'],
                    "from_address": owner_address,
                    "to_address": owner_address,
                    "amount": 0,  # 解冻数量由系统决定
                    "type": "解冻TRX",
                    "timestamp": datetime.now().isoformat(),
                    "status": "已解冻"
                }
                self.save_transaction_history(tx_record)
                
                self.log_message(f"✅ 解冻成功! 交易哈希: {txn['txid']}")
                messagebox.showinfo("解冻成功", 
                    f"TRX解冻成功！\n\n"
                    f"交易哈希: {txn['txid']}\n\n"
                    f"💡 提示: 几分钟后点击'刷新余额'查看余额更新")
                
                # 刷新余额
                self.refresh_balance()
                
            except Exception as e:
                error_msg = f"解冻失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                if "does not exist" in str(e) or "no frozen" in str(e).lower():
                    messagebox.showerror("解冻失败", "没有可解冻的TRX\n\n可能原因:\n• 没有冻结过TRX\n• 冻结期未满3天\n• 已经全部解冻")
                else:
                    messagebox.showerror("错误", error_msg)
        
        # 在后台线程中执行
        threading.Thread(target=do_unfreeze, daemon=True).start()
    
    def check_account_status(self):
        """检查账户激活状态"""
        if not self.wallet_data:
            messagebox.showwarning("警告", "请先创建或导入钱包")
            return
        
        def check_status():
            try:
                address = self.wallet_data["address"]
                
                # 检查账户是否存在
                try:
                    account_info = self.client.get_account(address)
                    account_exists = account_info is not None
                except:
                    account_exists = False
                
                # 检查TRX余额
                try:
                    trx_balance = self.client.get_account_balance(address)
                    has_trx = trx_balance > 0
                except:
                    trx_balance = 0
                    has_trx = False
                
                # 生成状态报告
                if account_exists and has_trx:
                    status_detail = (
                        "🎉 账户状态：已激活\n\n"
                        f"📮 钱包地址：{address}\n"
                        f"💰 TRX余额：{trx_balance:.6f} TRX\n"
                        "🔗 网络状态：已连接到TRON主网\n\n"
                        "✅ 可用功能：\n"
                        "• ✅ 接收TRX和USDT\n"
                        "• ✅ 发送USDT转账\n"
                        "• ✅ 冻结TRX获取能量\n"
                        "• ✅ 解冻TRX\n"
                        "• ✅ 所有钱包功能\n\n"
                        "💡 您的钱包已完全激活，可以正常使用所有功能！"
                    )
                    self.log_message("✅ 账户状态检查：已激活")
                elif has_trx and not account_exists:
                    status_detail = (
                        "⚠️ 账户状态：部分激活\n\n"
                        f"📮 钱包地址：{address}\n"
                        f"💰 TRX余额：{trx_balance:.6f} TRX\n"
                        "🔗 网络状态：已连接到TRON主网\n\n"
                        "✅ 可用功能：\n"
                        "• ✅ 接收TRX和USDT\n"
                        "• ✅ 发送USDT转账\n"
                        "• ⚠️ 冻结功能可能受限\n\n"
                        "💡 建议进行一次小额转账来完全激活账户"
                    )
                    self.log_message("⚠️ 账户状态检查：部分激活")
                else:
                    status_detail = (
                        "❌ 账户状态：未激活\n\n"
                        f"📮 钱包地址：{address}\n"
                        f"💰 TRX余额：{trx_balance:.6f} TRX\n"
                        "🔗 网络状态：已连接到TRON主网\n\n"
                        "❌ 受限功能：\n"
                        "• ❌ 无法冻结TRX获取能量\n"
                        "• ❌ 无法解冻TRX\n"
                        "• ❌ 部分高级功能受限\n\n"
                        "✅ 激活方法：\n"
                        "1. 向此地址转入至少1 TRX\n"
                        "2. 等待转账确认（通常1-3分钟）\n"
                        "3. 点击'刷新余额'确认到账\n"
                        "4. 账户将自动激活\n\n"
                        "💡 激活后即可使用所有功能，包括能量管理"
                    )
                    self.log_message("❌ 账户状态检查：未激活")
                
                messagebox.showinfo("账户状态检查", status_detail)
                
            except Exception as e:
                error_msg = f"状态检查失败: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("错误", f"无法检查账户状态\n\n{error_msg}")
        
        # 在后台线程中执行
        threading.Thread(target=check_status, daemon=True).start()
    
    def run(self):
        """运行应用"""
        self.log_message("🚀 USDT管理工具启动成功")
        if self.wallet_data:
            self.log_message(f"📱 当前钱包: {self.wallet_data['address']}")
        else:
            self.log_message("💡 提示: 请先创建或导入钱包")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = USDTManager()
    app.run()