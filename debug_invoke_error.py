#!/usr/bin/env python3
"""
调试 LLM invoke 错误
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_llm_invoke():
    """测试 LLM invoke 方法"""
    print("🔧 测试 LLM invoke 方法...")
    
    try:
        from utils.llm_wrapper import SiliconFlowLLM
        
        # 创建 LLM 实例
        llm = SiliconFlowLLM()
        print(f"✅ LLM 创建成功，类型: {type(llm)}")
        print(f"✅ LLM 类型标识: {llm._llm_type}")
        
        # 检查 invoke 方法
        print(f"✅ 是否有 invoke 方法: {hasattr(llm, 'invoke')}")
        
        # 测试不同类型的输入
        test_prompt = "你好，请简单回复"
        
        print("\n📝 测试1: 直接字符串调用")
        try:
            response = llm.invoke(test_prompt)
            print(f"✅ 字符串调用成功: {response[:50]}...")
        except Exception as e:
            print(f"❌ 字符串调用失败: {e}")
            print(f"错误类型: {type(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n📝 测试2: 字典格式调用")
        try:
            response = llm.invoke({"prompt": test_prompt})
            print(f"✅ 字典调用成功: {response[:50]}...")
        except Exception as e:
            print(f"❌ 字典调用失败: {e}")
            print(f"错误类型: {type(e)}")
        
        print("\n📝 测试3: 列表格式调用")
        try:
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=test_prompt)]
            response = llm.invoke(messages)
            print(f"✅ 消息列表调用成功: {response[:50]}...")
        except Exception as e:
            print(f"❌ 消息列表调用失败: {e}")
            print(f"错误类型: {type(e)}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def inspect_llm_structure():
    """检查 LLM 类的结构"""
    print("\n🔍 检查 LLM 类结构...")
    
    try:
        from utils.llm_wrapper import SiliconFlowLLM
        from langchain.llms.base import LLM
        
        llm = SiliconFlowLLM()
        
        print(f"✅ SiliconFlowLLM 基类: {SiliconFlowLLM.__bases__}")
        print(f"✅ LLM 基类: {LLM.__bases__}")
        
        # 检查关键方法
        key_methods = ['invoke', '_call', '_stream', '_llm_type']
        for method in key_methods:
            has_method = hasattr(llm, method)
            print(f"✅ {method}: {'存在' if has_method else '不存在'}")
            
        # 检查 invoke 方法的来源
        if hasattr(llm, 'invoke'):
            print(f"✅ invoke 方法来源: {llm.invoke.__qualname__}")
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == "__main__":
    print("🚀 LLM invoke 错误调试")
    print("=" * 50)
    
    inspect_llm_structure()
    test_llm_invoke()
