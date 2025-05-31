#!/usr/bin/env python3
"""
简单的 LLM 调用测试
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔧 导入模块...")
    from utils.llm_wrapper import create_llm
    print("✅ 模块导入成功")
    
    print("🤖 创建 LLM...")
    llm = create_llm()
    print("✅ LLM 创建成功")
    
    print("📝 测试简单调用...")
    test_prompt = "你好，请回答'测试成功'"
    
    response = llm.invoke(test_prompt)
    print(f"✅ LLM 调用成功: {response}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
