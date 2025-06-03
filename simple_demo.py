#!/usr/bin/env python3
"""
硅基流动 + MCP Playwright 简单演示

这个文件展示了如何使用项目的两个核心功能：
1. 硅基流动 LLM 对话
2. MCP Playwright 浏览器自动化
"""

import asyncio
from utils.llm_wrapper import SiliconFlowLLM
from utils.mcp_browser_tools import MCPPlaywrightAgent


def demo_siliconflow_llm():
    """演示硅基流动 LLM 功能"""
    print("🤖 硅基流动 LLM 演示")
    print("=" * 50)
    
    try:
        # 创建 LLM 实例
        llm = SiliconFlowLLM()
        
        # 简单对话
        questions = [
            "你好，请简单介绍一下硅基流动",
            "什么是 MCP 协议？",
            "Playwright 有什么优势？"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n问题 {i}: {question}")
            response = llm.invoke(question)
            print(f"回答: {response}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ LLM 演示失败: {e}")
        print("💡 请检查 .env 文件中的 SILICONFLOW_API_KEY 配置")


async def demo_mcp_playwright():
    """演示 MCP Playwright 功能"""
    print("\n🌐 MCP Playwright 演示")
    print("=" * 50)
    
    try:
        # 创建 MCP Playwright 代理
        agent = MCPPlaywrightAgent()
        
        # 基础浏览器操作
        print("1. 导航到百度首页...")
        await agent.navigate("https://www.baidu.com")
        
        print("2. 截图保存...")
        await agent.screenshot("baidu_homepage", savePng=True)
        
        print("3. 获取页面标题...")
        title = await agent.evaluate("document.title")
        print(f"   页面标题: {title}")
        
        print("4. 搜索框输入...")
        await agent.fill("#kw", "人工智能")
        
        print("5. 点击搜索按钮...")
        await agent.click("#su")
        
        # 等待页面加载
        await asyncio.sleep(2)
        
        print("6. 搜索结果页截图...")
        await agent.screenshot("search_results", savePng=True)
        
        print("7. 关闭浏览器...")
        await agent.close()
        
        print("✅ MCP Playwright 演示完成")
        
    except Exception as e:
        print(f"❌ MCP Playwright 演示失败: {e}")
        print("💡 请确保已安装 MCP Playwright 服务器:")
        print("   npm install -g @executeautomation/playwright-mcp-server")


async def main():
    """主函数"""
    print("🚀 硅基流动 + MCP Playwright 简单演示")
    print("=" * 60)
    
    # 演示硅基流动 LLM
    demo_siliconflow_llm()
    
    # 演示 MCP Playwright
    await demo_mcp_playwright()
    
    print("\n🎉 演示完成！")
    print("\n📖 更多功能请查看:")
    print("   - mcp_browser_demo.py (完整的 MCP Playwright 演示)")
    print("   - utils/llm_wrapper.py (硅基流动 LLM 包装器)")
    print("   - utils/mcp_browser_tools.py (MCP Playwright 工具)")


if __name__ == "__main__":
    asyncio.run(main()) 