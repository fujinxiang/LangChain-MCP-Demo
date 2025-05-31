"""
LangChain + 硅基流动 + Playwright 浏览器操作 Demo
演示如何使用 AI 进行智能网页操作
"""

import sys
import asyncio
from utils.llm_wrapper import create_llm
from utils.browser_tools import create_browser_agent


async def demo_browser_planning():
    """演示浏览器任务规划"""
    print("🌐 浏览器任务规划演示")
    print("-" * 40)
    
    try:
        # 创建 LLM 和浏览器代理
        llm = create_llm()
        agent = create_browser_agent(llm, headless=True)
        
        # 示例任务
        tasks = [
            "访问百度首页并搜索'人工智能'",
            "访问GitHub，搜索LangChain项目",
        ]
        
        print("🤖 AI 浏览器助手准备就绪\n")
        
        for i, task in enumerate(tasks, 1):
            print(f"📋 任务 {i}: {task}")
            
            try:
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
            ("https://example.com", "示例网站"),
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
    print("您可以描述想要执行的浏览器任务，AI 将为您规划执行步骤")
    print("输入 'quit' 或 'exit' 退出\n")
    
    try:
        llm = create_llm()
        agent = create_browser_agent(llm, headless=True)
        
        while True:
            try:
                user_task = input("👤 请描述您的浏览器任务: ").strip()
                
                if user_task.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break
                
                if not user_task:
                    continue
                
                print("🤖 AI 正在分析任务...")
                result = await agent.execute_task(user_task)
                print(result)
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
    
    tools_info = [
        ("navigate_browser", "导航到指定URL"),
        ("click", "点击页面元素"),
        ("extract_text", "提取页面文本内容"),
        ("extract_hyperlinks", "提取页面中的所有链接"),
        ("get_elements", "获取指定选择器的页面元素"),
        ("current_page", "获取当前页面信息")
    ]
    
    print("📋 可用工具:")
    for tool_name, description in tools_info:
        print(f"  • {tool_name}: {description}")
    
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
        await demo_browser_planning()
        
        # 简单导航演示
        await demo_simple_navigation()
        
        # 交互模式
        await interactive_browser_mode()
    
    except Exception as e:
        print(f"❌ Demo 运行失败: {e}")
        print("请检查配置文件和依赖安装")


if __name__ == "__main__":
    asyncio.run(main())
