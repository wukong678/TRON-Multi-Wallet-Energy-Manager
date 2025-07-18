# 🚀 TRON多钱包能量管理工具 | TRON Multi-Wallet Energy Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![TRON](https://img.shields.io/badge/blockchain-TRON-red.svg)](https://tron.network/)

[English](#english) | [中文](#中文)

---

## 中文

### 📖 项目简介

一个功能强大的TRON钱包管理工具，专注于USDT转账和能量优化。通过创新的多钱包能量管理策略，帮助用户大幅降低USDT转账手续费，实现高效的资金管理。

### ✨ 核心亮点

- 🎯 **多钱包能量管理** - 通过多个钱包协同工作，优化能量获取和使用
- 💰 **大幅降低手续费** - 最高可节省50%的USDT转账手续费
- 🔧 **智能策略执行** - 自动化的TRX分发、冻结和能量委托
- 📊 **小资金友好** - 30 TRX即可开始使用多钱包策略
- 🖥️ **图形化界面** - 简洁直观的操作界面，支持中英文切换

### 🎯 多钱包能量管理策略

#### 💡 策略原理
通过创建多个钱包协同工作，实现能量的高效获取和使用：
- **主钱包**: 存放USDT，执行转账，接收能量委托
- **能量钱包**: 冻结TRX获取能量，委托给主钱包使用
- **轮换机制**: 错峰冻结解冻，确保主钱包始终有充足能量

#### 📊 收益对比

| 策略模式 | 投入成本 | 获得能量 | 可转账次数 | 节省手续费 | 收益率 |
|---------|---------|---------|-----------|-----------|--------|
| 小资金模式 | 20 TRX | 20,000 | 0.67次 | ~10 TRX | 50% |
| 完整模式 | 120 TRX | 120,000 | 4次 | ~60 TRX | 50% |
| 直接支付 | - | - | 按需 | 15 TRX/次 | - |

## 功能特性

### 🔐 基础钱包管理
- **创建新钱包**: 随机生成安全的私钥和地址
- **导入钱包**: 通过私钥导入现有钱包
- **地址复制**: 一键复制钱包地址到剪贴板
- **安全存储**: 钱包信息自动保存到本地文件
- **私钥备份**: 安全的私钥查看和备份功能

### 💰 余额查询
- **TRX余额**: 实时查询TRX原生代币余额
- **USDT余额**: 实时查询USDT代币余额
- **能量余额**: 显示当前可用能量数量
- **一键刷新**: 快速更新最新余额信息

### 💸 转账功能
- **USDT转账**: 支持向任意地址发送USDT
- **智能手续费**: 优先使用能量，不足时自动使用TRX
- **安全确认**: 转账前显示详细信息确认
- **实时反馈**: 转账过程和结果实时显示

### ⚡ 能量管理
- **TRX冻结**: 冻结TRX获取能量资源
- **能量查询**: 实时显示当前能量余额
- **智能解冻**: 3天后可解冻取回TRX
- **多钱包协同**: 多个钱包能量汇集使用

### 🎯 多钱包系统
- **智能生成**: 自动生成多钱包管理系统
- **模式选择**: 小资金模式(30 TRX)和完整模式(200+ TRX)
- **策略执行**: 一键执行完整的能量管理策略
- **余额总览**: 统一查看所有钱包的余额和能量

### 📊 交易记录
- **历史记录**: 自动保存所有转账记录
- **详细信息**: 包含时间、金额、地址、交易哈希等
- **快速查看**: 图形化界面展示交易历史
- **一键复制**: 双击复制交易哈希

### 📝 操作日志
- **实时日志**: 所有操作都有详细日志记录
- **时间戳**: 每条日志都包含精确时间
- **状态提示**: 成功/失败状态清晰显示
- **多语言**: 支持中英文界面切换

## 安装要求

### 系统要求
- Windows 7/10/11 或 macOS 或 Linux
- Python 3.7 或更高版本

### 依赖库
```bash
pip install tronpy
```

## 快速开始

### 🚀 基础使用

#### 方法一：直接运行
```bash
python usdt_manager.py
```

#### 方法二：使用启动器（Windows）
```bash
# 双击运行
启动工具.bat
```

### 💰 多钱包能量管理使用指南

#### 第一步：准备工作
1. 创建或导入主钱包
2. 向主钱包充值TRX（小资金模式需要30+ TRX）
3. 确保网络连接正常

#### 第二步：生成多钱包系统
1. 在界面下方找到"多钱包能量管理"区域
2. 选择模式：
   - **小资金模式**: 适合30 TRX的用户
   - **完整模式**: 适合200+ TRX的用户
3. 点击"生成钱包系统"按钮
4. 确认生成多钱包系统

#### 第三步：执行能量策略
1. 点击"执行策略"按钮
2. 确认策略执行
3. 等待自动完成：
   - TRX分发到能量钱包
   - 冻结TRX获取能量
   - 能量汇集到主钱包

#### 第四步：享受低手续费转账
1. 主钱包获得充足能量
2. USDT转账几乎免费
3. 点击"钱包余额"查看详细信息

### 📊 策略效果示例

```
小资金模式 (30 TRX):
├── 主钱包: 保留 10 TRX (应急)
├── 能量钱包1: 冻结 10 TRX → 10,000 能量
├── 能量钱包2: 冻结 10 TRX → 10,000 能量
└── 总计: 20,000 能量 → 可免费转账 0.67 次
```

## 界面说明

### 钱包信息区域
- 显示当前钱包地址
- 显示TRX和USDT余额
- 提供创建、导入、刷新、复制等操作按钮

### 操作区域
- **收款地址**: 输入要转账的目标地址
- **转账金额**: 输入要转账的USDT数量
- **发送按钮**: 执行转账操作

### 日志区域
- 显示所有操作的详细日志
- 包含时间戳和状态信息
- 支持清空日志功能

### 底部功能
- **查看交易记录**: 打开交易历史窗口
- **清空日志**: 清除当前显示的日志
- **退出**: 关闭应用程序

## 文件说明

### 自动生成的文件
- `wallet_config.json`: 钱包配置文件（包含地址和私钥）
- `transaction_history.json`: 交易记录文件
- `usdt_abi.json`: USDT合约ABI文件

### 重要提醒
⚠️ **安全警告**:
- `wallet_config.json` 文件包含您的私钥，请妥善保管
- 不要将此文件分享给任何人
- 建议定期备份此文件到安全位置
- 如果文件丢失，您将无法访问钱包中的资金

## 使用流程

### 首次使用
1. 运行程序
2. 点击"创建新钱包"或"导入钱包"
3. 如果创建新钱包，请务必备份显示的私钥
4. 点击"刷新余额"查看当前余额

### 接收USDT
1. 点击"复制地址"获取您的钱包地址
2. 将此地址提供给转账方
3. 转账完成后点击"刷新余额"查看到账情况

### 发送USDT
1. 在"收款地址"框中输入目标地址
2. 在"转账金额"框中输入要发送的USDT数量
3. 点击"发送USDT"按钮
4. 在确认对话框中核实信息后确认
5. 等待交易完成，查看日志中的交易哈希

### 查看记录
1. 点击"查看交易记录"按钮
2. 在弹出窗口中查看所有历史交易
3. 双击任意记录可复制交易哈希

## 🔧 故障排除

### 常见问题

**Q: 程序无法启动**
A: 请检查是否已安装Python和tronpy库

**Q: 网络连接失败**
A: 请检查网络连接，确保可以访问TRON网络

**Q: 多钱包策略执行失败**
A: 请检查：
- 主钱包TRX余额是否充足
- 网络连接是否稳定
- 是否已正确生成多钱包系统

**Q: 转账失败**
A: 请检查：
- 钱包TRX余额或能量是否足够
- 收款地址是否正确
- 转账金额是否超过USDT余额

**Q: 能量显示为0**
A: 
- 新钱包需要先有TRX转入才能激活
- 冻结TRX后需要等待几分钟生效
- 点击"刷新余额"更新能量信息

**Q: 冻结TRX失败**
A: 
- 确保钱包已激活（有TRX余额）
- 检查冻结数量是否大于等于1 TRX
- 确保有足够TRX支付冻结手续费

### 💡 最佳实践

1. **首次使用**: 建议先用小额资金测试功能
2. **备份重要**: 务必备份私钥到安全位置
3. **网络稳定**: 确保网络连接稳定再执行策略
4. **分批操作**: 大额资金建议分批处理
5. **定期检查**: 定期查看钱包余额和能量状态

### 🆘 技术支持
如遇到其他问题，请查看日志区域的错误信息，这将帮助诊断问题。

## 📄 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 贡献
欢迎提交 Issue 和 Pull Request！

## ⭐ 支持项目
如果这个项目对你有帮助，请给它一个星标 ⭐

---

## English

### 📖 Project Description

A powerful TRON wallet management tool focused on USDT transfers and energy optimization. Through innovative multi-wallet energy management strategies, it helps users significantly reduce USDT transfer fees and achieve efficient fund management.

### ✨ Key Features

- 🎯 **Multi-Wallet Energy Management** - Coordinate multiple wallets to optimize energy acquisition and usage
- 💰 **Significant Fee Reduction** - Save up to 50% on USDT transfer fees
- 🔧 **Smart Strategy Execution** - Automated TRX distribution, freezing, and energy delegation
- 📊 **Small Budget Friendly** - Start with just 30 TRX for multi-wallet strategy
- 🖥️ **Graphical Interface** - Clean and intuitive UI with Chinese/English support

### 🎯 Multi-Wallet Energy Management Strategy

#### 💡 Strategy Principle
Create multiple wallets working together for efficient energy acquisition and usage:
- **Main Wallet**: Store USDT, execute transfers, receive energy delegation
- **Energy Wallets**: Freeze TRX to gain energy, delegate to main wallet
- **Rotation Mechanism**: Staggered freeze/unfreeze to ensure main wallet always has sufficient energy

#### 📊 Benefit Comparison

| Strategy Mode | Investment | Energy Gained | Free Transfers | Fee Saved | ROI |
|--------------|------------|---------------|----------------|-----------|-----|
| Small Budget | 20 TRX | 20,000 | 0.67 times | ~10 TRX | 50% |
| Full Mode | 120 TRX | 120,000 | 4 times | ~60 TRX | 50% |
| Direct Payment | - | - | As needed | 15 TRX/time | - |

## Features

### 🔐 Basic Wallet Management
- **Create New Wallet**: Generate secure private keys and addresses
- **Import Wallet**: Import existing wallets via private key
- **Address Copy**: One-click copy wallet address to clipboard
- **Secure Storage**: Automatic local storage of wallet information
- **Private Key Backup**: Secure private key viewing and backup

### 💰 Balance Query
- **TRX Balance**: Real-time TRX native token balance query
- **USDT Balance**: Real-time USDT token balance query
- **Energy Balance**: Display current available energy amount
- **One-Click Refresh**: Quick update of latest balance information

### 💸 Transfer Functions
- **USDT Transfer**: Send USDT to any address
- **Smart Fees**: Prioritize energy usage, auto-fallback to TRX
- **Security Confirmation**: Display detailed information before transfer
- **Real-time Feedback**: Live transfer process and result display

### ⚡ Energy Management
- **TRX Freezing**: Freeze TRX to obtain energy resources
- **Energy Query**: Real-time display of current energy balance
- **Smart Unfreezing**: Unfreeze TRX after 3-day period
- **Multi-Wallet Coordination**: Aggregate energy from multiple wallets

### 🎯 Multi-Wallet System
- **Smart Generation**: Auto-generate multi-wallet management system
- **Mode Selection**: Small budget mode (30 TRX) and full mode (200+ TRX)
- **Strategy Execution**: One-click execution of complete energy management strategy
- **Balance Overview**: Unified view of all wallet balances and energy

### 📊 Transaction Records
- **History Records**: Auto-save all transfer records
- **Detailed Information**: Include time, amount, address, transaction hash
- **Quick View**: Graphical interface for transaction history
- **One-Click Copy**: Double-click to copy transaction hash

### 📝 Operation Logs
- **Real-time Logs**: Detailed logging of all operations
- **Timestamps**: Each log entry includes precise time
- **Status Indicators**: Clear success/failure status display
- **Multi-language**: Support Chinese/English interface switching

## Installation Requirements

### System Requirements
- Windows 7/10/11 or macOS or Linux
- Python 3.7 or higher

### Dependencies
```bash
pip install tronpy
```

## Quick Start

### 🚀 Basic Usage

#### Method 1: Direct Run
```bash
python usdt_manager.py
```

#### Method 2: Use Launcher (Windows)
```bash
# Double-click to run
启动工具.bat
```

### 💰 Multi-Wallet Energy Management Guide

#### Step 1: Preparation
1. Create or import main wallet
2. Fund main wallet with TRX (30+ TRX for small budget mode)
3. Ensure stable network connection

#### Step 2: Generate Multi-Wallet System
1. Find "Multi-Wallet Energy Management" section at bottom of interface
2. Select mode:
   - **Small Budget Mode**: For users with 30 TRX
   - **Full Mode**: For users with 200+ TRX
3. Click "Generate Wallet System" button
4. Confirm multi-wallet system generation

#### Step 3: Execute Energy Strategy
1. Click "Execute Strategy" button
2. Confirm strategy execution
3. Wait for automatic completion:
   - TRX distribution to energy wallets
   - Freeze TRX to gain energy
   - Energy aggregation to main wallet

#### Step 4: Enjoy Low-Fee Transfers
1. Main wallet gains sufficient energy
2. USDT transfers become nearly free
3. Click "Wallet Balances" to view details

### 📊 Strategy Effect Example

```
Small Budget Mode (30 TRX):
├── Main Wallet: Keep 10 TRX (emergency)
├── Energy Wallet 1: Freeze 10 TRX → 10,000 energy
├── Energy Wallet 2: Freeze 10 TRX → 10,000 energy
└── Total: 20,000 energy → 0.67 free transfers
```

## 🔧 Troubleshooting

### Common Issues

**Q: Program won't start**
A: Check if Python and tronpy library are installed

**Q: Network connection failed**
A: Check network connection and TRON network accessibility

**Q: Multi-wallet strategy execution failed**
A: Check:
- Main wallet has sufficient TRX balance
- Network connection is stable
- Multi-wallet system is properly generated

**Q: Transfer failed**
A: Check:
- Wallet has sufficient TRX balance or energy
- Recipient address is correct
- Transfer amount doesn't exceed USDT balance

**Q: Energy shows 0**
A: 
- New wallets need TRX input for activation
- Wait a few minutes after freezing TRX
- Click "Refresh Balance" to update energy info

**Q: TRX freezing failed**
A: 
- Ensure wallet is activated (has TRX balance)
- Check freeze amount is ≥ 1 TRX
- Ensure sufficient TRX for freezing fees

### 💡 Best Practices

1. **First Use**: Test with small amounts first
2. **Backup Important**: Always backup private keys securely
3. **Stable Network**: Ensure stable connection before executing strategies
4. **Batch Operations**: Process large amounts in batches
5. **Regular Checks**: Regularly monitor wallet balances and energy status

### 🆘 Technical Support
For other issues, check the error messages in the log area for diagnosis.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 Contributing
Issues and Pull Requests are welcome!

## ⭐ Support the Project
If this project helps you, please give it a star ⭐

## 📞 Contact
- GitHub Issues: For bug reports and feature requests
- Email: [Your Email] (Optional)

## 🔄 Version History
- v2.0: Added multi-wallet energy management system
- v1.0: Basic USDT wallet management functions

---

**⚠️ Disclaimer**: This tool is for educational and personal use only. Users are responsible for the security of their private keys and funds. Always test with small amounts first.