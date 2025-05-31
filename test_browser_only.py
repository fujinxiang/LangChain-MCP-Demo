#!/usr/bin/env python3
"""
测试浏览器工具（不使用 LLM）
"""

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.browser_tools import PlaywrightToolkit


async def test_browser_toolkit():
    """测试浏览器工具包"""
    print("🧪 测试浏览器工具包...")
    
    try:
        # 创建浏览器工具包
        toolkit = PlaywrightToolkit(headless=True)
        
        print("🔧 初始化浏览器...")
        await toolkit.initialize()
        
        print("📋 测试基本导航...")
        result = await toolkit.navigate_to("https://httpbin.org/html")
        print(f"导航结果: {result}")
        
        print("📄 测试页面标题...")
        title = await toolkit.get_page_title()
        print(f"页面标题: {title}")
        
        print("🔗 测试当前URL...")
        url = await toolkit.get_current_url()
        print(f"当前URL: {url}")
        
        print("📝 测试文本提取...")
        text = await toolkit.extract_text()
        print(f"页面文本（前200字符）: {text[:200]}...")
        
        print("🔗 测试链接提取...")
        links = await toolkit.extract_links()
        print(f"找到 {len(links)} 个链接")
        if links:
            print(f"第一个链接: {links[0]}")
        
        # 关闭浏览器
        await toolkit.close()
        
        print("✅ 浏览器工具包测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    print("🚀 浏览器工具包测试")
    print("=" * 40)
    
    success = await test_browser_toolkit()
    
    if success:
        print("\n✅ 所有测试通过！")
        print("💡 浏览器工具包工作正常，问题可能在 LLM 调用部分")
    else:
        print("\n❌ 浏览器工具包测试失败！")


if __name__ == "__main__":
    asyncio.run(main())
