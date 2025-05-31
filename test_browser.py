#!/usr/bin/env python3
"""
测试浏览器工具是否正常工作
"""

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.llm_wrapper import create_llm
from utils.browser_tools import create_browser_agent


async def test_browser_agent():
    """测试浏览器代理"""
    print("🧪 测试浏览器代理...")
    
    try:
        # 创建 LLM 和浏览器代理
        llm = create_llm()
        agent = create_browser_agent(llm, headless=True)
        
        # 测试任务
        test_task = "访问 https://example.com 并提取页面标题"
        
        print(f"📋 测试任务: {test_task}")
        print("🤖 AI 正在分析任务...")
        
        # 执行任务分析
        result = await agent.execute_task(test_task)
        print("✅ 任务分析成功！")
        print(result)
        
        # 关闭代理
        await agent.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def main():
    """主函数"""
    print("🚀 浏览器工具测试")
    print("=" * 40)
    
    success = await test_browser_agent()
    
    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 测试失败！")


if __name__ == "__main__":
    asyncio.run(main())
