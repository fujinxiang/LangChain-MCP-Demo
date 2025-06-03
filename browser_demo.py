"""
LangChain + 硅基流动 + Playwright 浏览器操作 Demo
演示如何使用 AI 进行智能网页操作
支持传统 Playwright 和 MCP 模式
"""

import sys
import asyncio
from utils.llm_wrapper import create_llm
from utils.browser_tools import create_browser_agent

# MCP 模式支持
try:
    from utils.mcp_browser_tools import create_mcp_browser_agent, MCPPlaywrightAgent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP 模式不可用，请安装: pip install langchain-mcp-adapters")


def select_browser_mode():
    """选择浏览器操作模式"""
    print("🚀 浏览器操作模式选择")
    print("=" * 40)
    print("1. 传统 Playwright 模式 (原生实现)")
    print("2. MCP Playwright 模式 (基于 MCP 协议)")
    
    if not MCP_AVAILABLE:
        print("⚠️ MCP 模式不可用，自动选择传统模式")
        return "traditional"
    
    while True:
        choice = input("请选择模式 (1 或 2): ").strip()
        if choice == "1":
            return "traditional"
        elif choice == "2":
            return "mcp"
        else:
            print("❌ 请输入 1 或 2")


async def demo_browser_planning():
    """演示浏览器任务规划"""
    print("🌐 浏览器任务规划演示")
    print("-" * 40)
    
    try:
        # 创建 LLM 和浏览器代理
        llm = create_llm()
        agent = create_browser_agent(llm, headless=False)
        
        # 示例任务
        tasks = [
            # "访问百度首页并搜索'人工智能'",
            # "访问GitHub，搜索LangChain项目",
            # "访问希沃首页并截图保存到本地",
        ]
        
        print("🤖 AI 浏览器助手准备就绪")
        print("选择执行模式:")
        print("1. 仅规划步骤 (planning)")
        print("2. 真正执行任务 (execute)")
        
        mode = input("请选择模式 (1 或 2): ").strip()
        execute_mode = mode == "2"
        
        print(f"\n{'🚀 执行模式' if execute_mode else '📋 规划模式'} 已启用\n")
        
        for i, task in enumerate(tasks, 1):
            print(f"📋 任务 {i}: {task}")
            
            try:
                if execute_mode:
                    result = await agent.execute_task_with_actions(task)
                else:
                    result = await agent.execute_task(task)
                print(result)
                print("\n" + "="*50 + "\n")
                
            except Exception as e:
                print(f"❌ 任务执行失败: {e}\n")
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        print("💡 请确保已安装 Playwright: pip install playwright && playwright install")


async def demo_simple_navigation():
    """演示简单的页面导航和内容提取"""
    print("🔍 简单页面操作演示")
    print("-" * 40)
    
    try:
        llm = create_llm()
        agent = create_browser_agent(llm, headless=True)
        
        # 测试网站列表
        test_sites = [
            ("https://httpbin.org/html", "测试HTML页面"),
            ("https://httpbin.org/json", "JSON API测试")
        ]
        
        for url, description in test_sites:
            print(f"\n🌐 访问: {description} ({url})")
            
            try:
                # 提取页面文本
                text_result = await agent.navigate_and_extract(url, "text")
                print("📄 页面文本:")
                print(text_result[:500] + "..." if len(text_result) > 500 else text_result)
                
                # 提取页面链接
                link_result = await agent.navigate_and_extract(url, "links")
                print("\n🔗 页面链接:")
                print(link_result[:300] + "..." if len(link_result) > 300 else link_result)
                
                print("\n" + "-"*30)
                
            except Exception as e:
                print(f"❌ 访问失败: {e}")
        
        await agent.close()
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


async def interactive_browser_mode():
    """交互式浏览器模式"""
    print("\n" + "=" * 50)
    print("🤖 交互式 AI 浏览器助手")
    
    # 选择浏览器模式
    mode = select_browser_mode()
    
    if mode == "mcp":
        print("🔗 使用 MCP (Model Context Protocol) 模式")
        print("支持的任务类型:")
        print("  • 智能任务: '访问百度并搜索人工智能'")
        print("  • 基础操作: 'navigate:https://www.baidu.com'")
        print("  • 截图: 'screenshot:page_name'")
        print("  • 获取文本: 'text'")
        print("  • JavaScript: 'js:document.title'")
    else:
        print("🏗️ 使用传统 Playwright 模式")
        print("支持的任务类型:")
        print("  • 百度搜索: '访问百度并搜索人工智能'")
        print("  • GitHub搜索: '访问GitHub，搜索LangChain项目'")
        print("  • 截图: '对当前页面截图'")
    
    print("输入 'quit' 或 'exit' 退出\n")
    
    try:
        llm = create_llm()
        
        if mode == "mcp" and MCP_AVAILABLE:
            # MCP 模式
            smart_agent = create_mcp_browser_agent(llm)
            basic_agent = MCPPlaywrightAgent()
            
            # 显示可用工具
            print("🔧 获取 MCP 可用工具...")
            tools = await basic_agent.get_available_tools()
            print(f"✅ MCP 工具包含 {len(tools)} 个工具")
            
            while True:
                try:
                    user_task = input("👤 请描述您的浏览器任务: ").strip()
                    
                    if user_task.lower() in ['quit', 'exit', '退出']:
                        print("👋 再见！")
                        break
                    
                    if user_task.lower() == 'tools':
                        print("🛠️ 可用 MCP 工具:")
                        for tool in tools:
                            print(f"  • {tool}")
                        continue
                    
                    if not user_task:
                        continue
                    
                    print("🤖 MCP AI 正在执行任务...")
                    print("=" * 50)
                    
                    # 解析命令类型
                    if user_task.startswith('navigate:'):
                        url = user_task[9:].strip()
                        result = await basic_agent.navigate_to(url)
                    elif user_task.startswith('screenshot:'):
                        name = user_task[11:].strip() or "screenshot"
                        result = await basic_agent.take_screenshot(name, savePng=True)
                    elif user_task.startswith('js:'):
                        script = user_task[3:].strip()
                        result = await basic_agent.execute_javascript(script)
                    elif user_task.lower() == 'text':
                        result = await basic_agent.get_page_text()
                    elif user_task.lower() == 'html':
                        result = await basic_agent.get_page_html()
                    elif user_task.lower() == 'back':
                        result = await basic_agent.go_back()
                    elif user_task.lower() == 'forward':
                        result = await basic_agent.go_forward()
                    else:
                        # 智能任务处理
                        result = await smart_agent.execute_smart_task(user_task)
                    
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
            
        else:
            # 传统模式
            agent = create_browser_agent(llm, headless=False)  # 改为非无头模式，便于观察
            
            while True:
                try:
                    user_task = input("👤 请描述您的浏览器任务: ").strip()
                    
                    if user_task.lower() in ['quit', 'exit', '退出']:
                        print("👋 再见！")
                        break
                    
                    if not user_task:
                        continue
                    
                    print("🤖 AI 正在执行任务...")
                    print("=" * 50)
                    
                    # 使用传统执行方法
                    result = await agent.execute_task_with_actions(user_task)
                    print(result)
                    print("=" * 50)
                    print()
                    
                except KeyboardInterrupt:
                    print("\n👋 再见！")
                    break
                except Exception as e:
                    print(f"❌ 发生错误: {e}")
                    print()
            
            await agent.close()
        
    except Exception as e:
        print(f"❌ 交互模式失败: {e}")


def show_browser_tools_info():
    """显示浏览器工具信息"""
    print("🛠️ Playwright 浏览器工具包")
    print("=" * 50)
    
    print("📋 传统模式工具:")
    tools_info = [
        ("navigate_browser", "导航到指定URL"),
        ("click", "点击页面元素"),
        ("extract_text", "提取页面文本内容"),
        ("extract_hyperlinks", "提取页面中的所有链接"),
        ("get_elements", "获取指定选择器的页面元素"),
        ("current_page", "获取当前页面信息")
    ]
    
    for tool_name, description in tools_info:
        print(f"  • {tool_name}: {description}")
    
    if MCP_AVAILABLE:
        print("\n📋 MCP 模式新增工具:")
        mcp_tools = [
            ("execute_javascript", "执行 JavaScript 代码"),
            ("get_console_logs", "获取控制台日志"),
            ("press_key", "键盘按键操作"),
            ("drag_and_drop", "拖拽操作"),
            ("save_as_pdf", "保存页面为 PDF"),
            ("start/end_codegen_session", "代码生成会话"),
            ("hover_element", "元素悬停"),
            ("go_back/forward", "浏览器前进后退")
        ]
        
        for tool_name, description in mcp_tools:
            print(f"  • {tool_name}: {description}")
        
        print("\n🔗 MCP 模式优势:")
        advantages = [
            "⚡ 更高效的工具执行性能",
            "🛠️ 更丰富的 Playwright 操作支持",
            "📊 更好的错误处理和日志",
            "🔄 支持实时代码生成",
            "🤖 标准化的工具调用协议"
        ]
        
        for advantage in advantages:
            print(f"  {advantage}")
    
    print("\n💡 使用场景:")
    scenarios = [
        "🔍 网页内容抓取和分析",
        "🤖 自动化表单填写",
        "📊 数据采集和监控",
        "🧪 网站功能测试",
        "📰 新闻和信息收集",
        "🛒 价格比较和监控"
    ]
    
    for scenario in scenarios:
        print(f"  {scenario}")
    
    print("\n⚠️ 注意事项:")
    print("  • 请遵守网站的robots.txt和使用条款")
    print("  • 避免对网站造成过大负载")
    print("  • 尊重网站的访问频率限制")
    
    if MCP_AVAILABLE:
        print("\n⚙️ MCP 环境要求:")
        print("  📦 pip install langchain-mcp-adapters")
        print("  📦 npm install -g @executeautomation/playwright-mcp-server")

async def main():
    """主函数"""
    print("🚀 LangChain + 硅基流动 + Playwright 浏览器操作 Demo")
    print("=" * 60)
    
    # 显示工具信息
    show_browser_tools_info()
    
    try:
        # 检查 Playwright 是否可用
        print("\n🔧 检查 Playwright 环境...")
        
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                await browser.close()
            print("✅ Playwright 环境正常")
        except Exception as e:
            print(f"❌ Playwright 环境检查失败: {e}")
            print("💡 请运行: pip install playwright && playwright install")
            return
        
        # 运行演示
        print("\n📋 开始演示...")
        
        # 任务规划演示
        # await demo_browser_planning()
        
        # 简单导航演示
        # await demo_simple_navigation()
        
        # 交互模式
        await interactive_browser_mode()
    
    except Exception as e:
        print(f"❌ Demo 运行失败: {e}")
        print("请检查配置文件和依赖安装")


if __name__ == "__main__":
    asyncio.run(main())
