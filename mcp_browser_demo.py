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
            ("导航到百度", "navigate_to", {"url": "https://www.baidu.com"}),
            ("获取页面文本", "get_page_text", {}),
            ("截图", "take_screenshot", {"name": "baidu_homepage", "savePng": True}),
        ]
        
        for desc, method, params in operations:
            print(f"\n🔄 执行: {desc}")
            try:
                method_func = getattr(agent, method)
                result = await method_func(**params)
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
            "访问希沃官网，然后滚动到页面底部，再点击链接 '开得联官网'，打开新页面后再截图保存"
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


async def demo_mcp_advanced_features():
    """演示 MCP 高级功能"""
    print("⚡ MCP Playwright 高级功能演示")
    print("-" * 40)
    
    try:
        agent = MCPPlaywrightAgent()
        
        # 高级功能测试
        advanced_tests = [
            {
                "name": "JavaScript 执行",
                "method": "execute_javascript",
                "params": {"script": "document.title"}
            },
            {
                "name": "控制台日志获取",
                "method": "get_console_logs",
                "params": {"log_type": "all", "limit": 10}
            },
            {
                "name": "按键操作",
                "method": "press_key",
                "params": {"key": "F12"}
            }
        ]
        
        # 首先导航到一个页面
        print("🌐 导航到测试页面...")
        await agent.navigate_to("https://httpbin.org/html")
        
        for test in advanced_tests:
            print(f"\n🔧 测试: {test['name']}")
            try:
                method_func = getattr(agent, test['method'])
                result = await method_func(**test['params'])
                print(result)
            except Exception as e:
                print(f"❌ 测试失败: {e}")
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ MCP 高级功能演示失败: {e}")


async def demo_mcp_codegen():
    """演示 MCP 代码生成功能"""
    print("📝 MCP Playwright 代码生成演示")
    print("-" * 40)
    
    try:
        agent = MCPPlaywrightAgent()
        
        # 开始代码生成会话
        output_path = "/d%3A/Code/FuJinxiang/LangChainDemo"  # 使用项目根目录
        print("🚀 开始代码生成会话...")
        result = await agent.start_codegen_session(output_path, "MCPDemo")
        print(result)
        
        # 执行一些操作（这些操作会被记录）
        operations = [
            ("navigate_to", {"url": "https://www.baidu.com"}),
            ("fill_input", {"selector": "#kw", "value": "Playwright"}),
            ("click_element", {"selector": "#su"}),
            ("take_screenshot", {"name": "search_result"}),
        ]
        
        print("\n📋 执行操作（将被记录为测试代码）:")
        for method, params in operations:
            print(f"  🔄 {method}: {params}")
            try:
                method_func = getattr(agent, method)
                await method_func(**params)
                await asyncio.sleep(1)  # 等待页面响应
            except Exception as e:
                print(f"    ❌ 操作失败: {e}")
        
        # 结束代码生成会话
        print("\n📄 生成测试代码...")
        result = await agent.end_codegen_session()
        print(result)
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ MCP 代码生成演示失败: {e}")


async def interactive_mcp_mode():
    """交互式 MCP 浏览器模式"""
    print("\n" + "=" * 60)
    print("🤖 交互式 MCP AI 浏览器助手")
    print("基于 Model Context Protocol (MCP) 的智能浏览器操作")
    print("支持的任务类型:")
    print("  • 智能任务: '访问百度并搜索人工智能'")
    print("  • 基础操作: 'navigate:https://www.baidu.com'")
    print("  • 截图: 'screenshot:page_name'")
    print("  • 获取文本: 'text'")
    print("  • JavaScript: 'js:document.title'")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'tools' 查看可用工具\n")
    
    try:
        # 创建智能 MCP 代理
        llm = create_llm()
        smart_agent = create_mcp_browser_agent(llm)
        basic_agent = MCPPlaywrightAgent()
        
        # 显示可用工具
        print("🔧 获取可用工具...")
        tools = await basic_agent.get_available_tools()
        print(f"✅ MCP 工具包含 {len(tools)} 个工具")
        
        while True:
            try:
                user_input = input("👤 请输入命令或描述任务: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break
                
                if user_input.lower() == 'tools':
                    print("🛠️ 可用工具:")
                    for tool in tools:
                        print(f"  • {tool}")
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 MCP AI 正在处理...")
                print("=" * 50)
                
                # 解析命令类型
                if user_input.startswith('navigate:'):
                    url = user_input[9:].strip()
                    result = await basic_agent.navigate_to(url)
                elif user_input.startswith('screenshot:'):
                    name = user_input[11:].strip() or "screenshot"
                    result = await basic_agent.take_screenshot(name, savePng=True)
                elif user_input.startswith('js:'):
                    script = user_input[3:].strip()
                    result = await basic_agent.execute_javascript(script)
                elif user_input.lower() == 'text':
                    result = await basic_agent.get_page_text()
                elif user_input.lower() == 'html':
                    result = await basic_agent.get_page_html()
                elif user_input.lower() == 'back':
                    result = await basic_agent.go_back()
                elif user_input.lower() == 'forward':
                    result = await basic_agent.go_forward()
                else:
                    # 智能任务处理
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


def show_mcp_info():
    """显示 MCP 相关信息"""
    print("🚀 LangChain MCP Adapters + Playwright MCP")
    print("=" * 60)
    
    print("📋 MCP (Model Context Protocol) 优势:")
    advantages = [
        "🔗 标准化的工具调用协议",
        "⚡ 更高效的工具执行性能",
        "🛠️ 丰富的 Playwright 操作支持",
        "🤖 与 LangChain 无缝集成",
        "📊 更好的错误处理和日志",
        "🔄 支持实时代码生成"
    ]
    
    for advantage in advantages:
        print(f"  {advantage}")
    
    print(f"\n🛠️ 支持的 Playwright 操作:")
    operations = [
        "navigate_to - 页面导航",
        "click_element - 元素点击", 
        "fill_input - 输入填写",
        "take_screenshot - 页面截图",
        "execute_javascript - JS 执行",
        "get_page_text/html - 内容提取",
        "hover_element - 元素悬停",
        "drag_and_drop - 拖拽操作",
        "press_key - 键盘操作",
        "save_as_pdf - PDF 保存",
        "get_console_logs - 控制台日志",
        "start/end_codegen_session - 代码生成"
    ]
    
    for operation in operations:
        print(f"  • {operation}")
    
    print(f"\n⚙️ 环境要求:")
    requirements = [
        "pip install langchain-mcp-adapters",
        "npm install -g @executeautomation/playwright-mcp-server",
        "playwright install  # 安装浏览器"
    ]
    
    for req in requirements:
        print(f"  📦 {req}")


async def main():
    """主函数"""
    print("🚀 LangChain MCP Adapters + Playwright MCP 演示")
    print("=" * 60)
    
    # 显示 MCP 信息
    show_mcp_info()
    
    try:
        print("\n🔧 检查 MCP 环境...")
        
        # 简单的环境检查
        # try:
        #     from langchain_mcp_adapters import MultiServerMCPClient
        #     print("✅ langchain-mcp-adapters 已安装")
        # except ImportError:
        #     print("❌ 请安装: pip install langchain-mcp-adapters")
        #     return
        
        print("\n📋 选择演示模式:")
        print("1. MCP 基础操作演示")
        print("2. MCP 智能任务演示") 
        print("3. MCP 高级功能演示")
        print("4. MCP 代码生成演示")
        print("5. 交互式 MCP 模式")
        print("0. 运行所有演示")
        
        choice = input("请选择模式 (0-5): ").strip()
        
        if choice == "1":
            await demo_mcp_basic_operations()
        elif choice == "2":
            await demo_mcp_smart_operations()
        elif choice == "3":
            await demo_mcp_advanced_features()
        elif choice == "4":
            await demo_mcp_codegen()
        elif choice == "5":
            await interactive_mcp_mode()
        elif choice == "0":
            print("\n🎬 运行所有演示...")
            await demo_mcp_basic_operations()
            print("\n" + "="*60 + "\n")
            await demo_mcp_smart_operations()
            print("\n" + "="*60 + "\n")
            await demo_mcp_advanced_features()
            print("\n" + "="*60 + "\n")
            await demo_mcp_codegen()
        else:
            print("❌ 无效选择")
            return
    
    except Exception as e:
        print(f"❌ Demo 运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 