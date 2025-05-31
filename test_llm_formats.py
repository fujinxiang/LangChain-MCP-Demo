#!/usr/bin/env python3
"""
测试 LLM 调用格式问题
"""

import sys
import os
import asyncio

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_llm_formats():
    """测试不同的 LLM 调用格式"""
    print("🧪 测试 LLM 调用格式...")
    
    try:
        from utils.llm_wrapper import create_llm
        print("✅ LLM 模块导入成功")
        
        llm = create_llm()
        print("✅ LLM 创建成功")
        
        # 测试不同的调用格式
        test_prompt = "你好，请简单回复'测试成功'"
        
        print("\n📝 测试格式1: 直接字符串")
        try:
            response1 = llm.invoke(test_prompt)
            print(f"✅ 格式1成功: {response1[:50]}...")
        except Exception as e:
            print(f"❌ 格式1失败: {e}")
        
        print("\n📝 测试格式2: 字典格式 (旧版本)")
        try:
            response2 = llm.invoke({"question": test_prompt})
            print(f"✅ 格式2成功: {response2[:50]}...")
        except Exception as e:
            print(f"❌ 格式2失败: {e}")
        
        # 测试浏览器代理
        print("\n🌐 测试浏览器代理...")
        from utils.browser_tools import create_browser_agent
        
        agent = create_browser_agent(llm, headless=True)
        
        # 简单任务测试
        task = "访问 https://example.com"
        print(f"任务: {task}")
        
        result = await agent.execute_task(task)
        print("✅ 浏览器代理测试成功")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_llm_formats())
