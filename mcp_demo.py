"""
LangChain MCP Adapters + Playwright MCP 浏览器操作演示
展示如何使用 MCP 协议进行智能网页操作
"""

import sys
import asyncio
from utils.llm_wrapper import create_llm
from utils.mcp_browser_tools import create_mcp_browser_agent, MCPPlaywrightAgent


async def demo_mcp_basic_operations():
    """演示 MCP 基础浏览器操作"""
    print("🔧 MCP Playwright 基础操作演示")
    print("-" * 40)
    
    try:
        # 创建基础 MCP 代理（无需 LLM）
        agent = MCPPlaywrightAgent()
        
        # 测试基础操作
        operations = [
            ("导航到百度", "playwright_navigate", {"url": "https://www.baidu.com"}),
            ("获取页面文本", "playwright_get_visible_text", {"random_string": "dummy"}),
            ("截图", "playwright_screenshot", {"name": "baidu_homepage", "savePng": True}),
        ]
        
        for desc, tool_name, params in operations:
            print(f"\n🔄 执行: {desc}")
            try:
                result = await agent.call_tool(tool_name, **params)
                print(result)
            except Exception as e:
                print(f"❌ 操作失败: {e}")
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ MCP 基础操作演示失败: {e}")
        print("💡 请确保已安装: npm install -g @executeautomation/playwright-mcp-server")


async def demo_mcp_smart_operations():
    """演示 MCP 智能浏览器操作"""
    print("🤖 MCP 智能浏览器操作演示")
    print("-" * 40)
    
    try:
        # 创建智能 MCP 代理（需要 LLM）
        llm = create_llm()
        agent = create_mcp_browser_agent(llm)
        
        # 测试智能任务
        smart_tasks = [
            "访问 LangChain 官网，再截图保存"
        ]
        
        for i, task in enumerate(smart_tasks, 1):
            print(f"\n🎯 智能任务 {i}: {task}")
            print("=" * 50)
            
            try:
                result = await agent.execute_smart_task(task)
                print(result)
            except Exception as e:
                print(f"❌ 智能任务执行失败: {e}")
            
            print("\n" + "="*50 + "\n")
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ MCP 智能操作演示失败: {e}")


async def interactive_mcp_mode():
    """交互式 MCP 浏览器模式"""
    print("\n" + "=" * 60)
    print("🤖 交互式 MCP AI 浏览器助手")
    print("基于 Model Context Protocol (MCP) 的智能浏览器操作")
    print("支持的任务类型:")
    print("  • 智能任务: '访问百度并搜索人工智能'")
    print("输入 'quit' 或 'exit' 退出\n")

    try:
        # 创建智能 MCP 代理
        llm = create_llm()
        smart_agent = create_mcp_browser_agent(llm)
        basic_agent = MCPPlaywrightAgent()
        
        while True:
            try:
                user_input = input("👤 请输入命令或描述任务: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break

                if not user_input:
                    continue
                
                print("🤖 MCP AI 正在处理...")
                print("=" * 50)

                result = await smart_agent.execute_smart_task(user_input)
                
                print(result)
                print("=" * 50)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                print()
        
        await smart_agent.close()
        await basic_agent.close()
        
    except Exception as e:
        print(f"❌ 交互模式失败: {e}")


async def main():
    """主函数"""
    print("🚀 LangChain MCP Adapters + Playwright MCP 演示")
    print("=" * 60)
    
    try:
        print("\n📋 选择演示模式:")
        print("1. MCP 基础操作演示")
        print("2. MCP 智能任务演示") 
        print("3. 交互式 MCP 模式")
        
        choice = input("请选择模式 (1-3): ").strip()
        
        if choice == "1":
            await demo_mcp_basic_operations()
        elif choice == "2":
            await demo_mcp_smart_operations()
        elif choice == "3":
            await interactive_mcp_mode()
        else:
            print("❌ 无效选择")
            return
    
    except Exception as e:
        print(f"❌ Demo 运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 