#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试GUI是否可用
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("✅ tkinter库可用")
    
    # 创建测试窗口
    root = tk.Tk()
    root.title("GUI测试")
    root.geometry("300x150")
    
    ttk.Label(root, text="GUI测试成功！", font=("Arial", 12)).pack(pady=20)
    ttk.Button(root, text="关闭", command=root.quit).pack(pady=10)
    
    print("✅ GUI测试窗口已创建，请关闭窗口继续...")
    root.mainloop()
    print("✅ GUI测试完成")
    
except ImportError as e:
    print(f"❌ GUI库导入失败: {e}")
except Exception as e:
    print(f"❌ GUI测试失败: {e}")