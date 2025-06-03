"""
测试 LangChain MCP Adapters + Playwright MCP 集成
验证 MCP 环境是否正确配置
"""

import asyncio
import sys
import traceback


async def test_mcp_imports():
    """测试 MCP 相关模块导入"""
    print("🔧 测试 MCP 模块导入...")
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        print("✅ langchain-mcp-adapters 导入成功")
        return True
    except ImportError as e:
        print(f"❌ langchain-mcp-adapters 导入失败: {e}")
        print("💡 请安装: pip install langchain-mcp-adapters")
        return False


async def test_mcp_toolkit_creation():
    """测试 MCP 客户端创建"""
    print("\n🔧 测试 MCP 客户端创建...")
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        # 配置 MCP 服务器
        server_config = {
            "playwright": {
                "command": "npx",
                "args": ["-y", "@executeautomation/playwright-mcp-server"],
                "transport": "stdio"
            }
        }
        
        # 创建客户端（但不初始化，因为可能没有安装 MCP 服务器）
        client = MultiServerMCPClient(server_config)
        print("✅ MCP 客户端创建成功")
        return True
        
    except Exception as e:
        print(f"❌ MCP 客户端创建失败: {e}")
        return False


async def test_mcp_browser_tools():
    """测试自定义 MCP 浏览器工具"""
    print("\n🔧 测试自定义 MCP 浏览器工具...")
    
    try:
        from utils.mcp_browser_tools import MCPPlaywrightAgent, create_mcp_browser_agent
        
        # 创建代理（但不初始化）
        agent = MCPPlaywrightAgent()
        print("✅ MCPPlaywrightAgent 创建成功")
        
        # 测试配置
        config = agent._get_default_config()
        expected_keys = ["command", "args", "env"]
        if all(key in config for key in expected_keys):
            print("✅ MCP 配置格式正确")
        else:
            print("❌ MCP 配置格式不正确")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP 浏览器工具测试失败: {e}")
        traceback.print_exc()
        return False


async def test_llm_integration():
    """测试 LLM 集成"""
    print("\n🔧 测试 LLM 集成...")
    
    try:
        from utils.llm_wrapper import create_llm
        from utils.mcp_browser_tools import create_mcp_browser_agent
        
        # 创建 LLM
        llm = create_llm()
        print("✅ LLM 创建成功")
        
        # 创建智能代理（但不初始化）
        smart_agent = create_mcp_browser_agent(llm)
        print("✅ 智能 MCP 代理创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM 集成测试失败: {e}")
        return False


async def test_mcp_server_availability():
    """测试 MCP 服务器可用性"""
    print("\n🔧 测试 MCP 服务器可用性...")
    
    try:
        from utils.mcp_browser_tools import MCPPlaywrightAgent
        
        agent = MCPPlaywrightAgent()
        
        # 尝试初始化（这会实际连接 MCP 服务器）
        try:
            await agent.initialize()
            print("✅ MCP Playwright 服务器连接成功")
            
            # 获取可用工具
            tools = await agent.get_available_tools()
            print(f"✅ 获取到 {len(tools)} 个 MCP 工具")
            
            # 显示前5个工具
            for i, tool in enumerate(tools[:5]):
                print(f"  🔧 {tool}")
            
            if len(tools) > 5:
                print(f"  ... 和其他 {len(tools) - 5} 个工具")
            
            await agent.close()
            return True
            
        except Exception as e:
            print(f"❌ MCP 服务器连接失败: {e}")
            print("💡 请确保已安装: npm install -g @executeautomation/playwright-mcp-server")
            return False
            
    except Exception as e:
        print(f"❌ MCP 服务器可用性测试失败: {e}")
        return False


async def run_integration_tests():
    """运行所有集成测试"""
    print("🚀 LangChain MCP Adapters + Playwright MCP 集成测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_mcp_imports),
        ("工具包创建", test_mcp_toolkit_creation),
        ("浏览器工具", test_mcp_browser_tools),
        ("LLM 集成", test_llm_integration),
        ("MCP 服务器", test_mcp_server_availability),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 总体结果: {passed}/{len(results)} 测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！MCP 集成配置正确")
    elif passed >= len(results) - 1:  # 除了服务器连接外都通过
        print("⚡ 基础功能正常，MCP 服务器需要单独安装")
        print("💡 运行: npm install -g @executeautomation/playwright-mcp-server")
    else:
        print("⚠️ 存在配置问题，请检查依赖安装")
        print("💡 确保已安装: pip install langchain-mcp-adapters")


def show_setup_instructions():
    """显示完整的安装说明"""
    print("\n📋 完整安装说明:")
    print("=" * 40)
    
    print("1️⃣ 安装 Python 依赖:")
    print("   pip install langchain-mcp-adapters")
    
    print("\n2️⃣ 安装 Node.js 和 MCP Playwright 服务器:")
    print("   # 确保已安装 Node.js 和 npm")
    print("   npm install -g @executeautomation/playwright-mcp-server")
    
    print("\n3️⃣ 安装 Playwright 浏览器:")
    print("   playwright install")
    
    print("\n4️⃣ 验证安装:")
    print("   python test_mcp_integration.py")
    
    print("\n5️⃣ 运行演示:")
    print("   python mcp_browser_demo.py")
    print("   python browser_demo.py  # 选择 MCP 模式")


async def main():
    """主函数"""
    try:
        await run_integration_tests()
        show_setup_instructions()
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 