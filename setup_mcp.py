#!/usr/bin/env python3
"""
LangChain MCP Adapters + Playwright MCP 自动化安装脚本
帮助用户快速设置 MCP 环境
"""

import subprocess
import sys
import os
import platform
import asyncio


def check_python_version():
    """检查 Python 版本"""
    print("🐍 检查 Python 版本...")
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python 版本太低: {version.major}.{version.minor}")
        print("💡 请升级到 Python 3.8 或更高版本")
        return False
    print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_node_installed():
    """检查 Node.js 是否已安装"""
    print("\n📦 检查 Node.js 安装...")
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, check=True)
        node_version = result.stdout.strip()
        print(f"✅ Node.js 版本: {node_version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js 未安装")
        return False


def install_python_dependencies():
    """安装 Python 依赖"""
    print("\n📦 安装 Python 依赖...")
    
    dependencies = [
        "langchain-mcp-adapters",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10", 
        "playwright>=1.40.0"
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {dep} 安装失败: {e}")
            return False
    
    return True


def install_mcp_server():
    """安装 MCP Playwright 服务器"""
    print("\n🔧 安装 MCP Playwright 服务器...")
    
    try:
        # 检查 npm 是否可用
        subprocess.run(['npm', '--version'], 
                      capture_output=True, text=True, check=True)
        
        # 安装 MCP 服务器
        print("正在安装 @executeautomation/playwright-mcp-server...")
        subprocess.run(['npm', 'install', '-g', '@executeautomation/playwright-mcp-server'], 
                      check=True)
        print("✅ MCP Playwright 服务器安装成功")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ MCP 服务器安装失败: {e}")
        print("💡 请确保 Node.js 和 npm 已正确安装")
        return False


def install_playwright_browsers():
    """安装 Playwright 浏览器"""
    print("\n🌐 安装 Playwright 浏览器...")
    
    try:
        subprocess.run([sys.executable, '-m', 'playwright', 'install'], 
                      check=True)
        print("✅ Playwright 浏览器安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Playwright 浏览器安装失败: {e}")
        return False


async def test_mcp_integration():
    """测试 MCP 集成"""
    print("\n🧪 测试 MCP 集成...")
    
    try:
        # 导入测试
        from langchain_mcp_adapters import MultiServerMCPClient
        print("✅ langchain-mcp-adapters 导入成功")
        
        # 创建基础工具包配置
        server_config = {
            "command": "npx",
            "args": ["@executeautomation/playwright-mcp-server"],
            "env": None
        }
        
        toolkit = MultiServerMCPClient(server_params=server_config)
        print("✅ MCP 工具包创建成功")
        
        # 尝试初始化（这会测试 MCP 服务器连接）
        try:
            await toolkit.ainit()
            tools = await toolkit.get_available_tools()
            print(f"✅ MCP 服务器连接成功，获取到 {len(tools)} 个工具")
            await toolkit.aclose()
            return True
        except Exception as e:
            print(f"⚠️ MCP 服务器连接测试失败: {e}")
            print("💡 基础环境已安装，但 MCP 服务器可能需要手动启动")
            return False
            
    except Exception as e:
        print(f"❌ MCP 集成测试失败: {e}")
        return False


def show_nodejs_install_instructions():
    """显示 Node.js 安装说明"""
    print("\n📋 Node.js 安装说明:")
    print("=" * 40)
    
    system = platform.system().lower()
    
    if system == "windows":
        print("Windows 用户:")
        print("  1. 访问 https://nodejs.org/")
        print("  2. 下载 LTS 版本")
        print("  3. 运行安装程序")
        print("  4. 重启命令行工具")
    elif system == "darwin":  # macOS
        print("macOS 用户:")
        print("  方法1 - 官网下载:")
        print("    1. 访问 https://nodejs.org/")
        print("    2. 下载 LTS 版本")
        print("  方法2 - 使用 Homebrew:")
        print("    brew install node")
    else:  # Linux
        print("Linux 用户:")
        print("  Ubuntu/Debian:")
        print("    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -")
        print("    sudo apt-get install -y nodejs")
        print("  CentOS/RHEL:")
        print("    curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -")
        print("    sudo yum install -y nodejs")


def show_next_steps():
    """显示后续步骤"""
    print("\n🎯 后续步骤:")
    print("=" * 30)
    print("1️⃣ 验证安装:")
    print("   python test_mcp_integration.py")
    print("\n2️⃣ 运行演示:")
    print("   python mcp_browser_demo.py")
    print("   python browser_demo.py  # 选择 MCP 模式")
    print("\n3️⃣ 配置 API:")
    print("   编辑 config.py 文件，设置硅基流动 API Key")
    print("\n4️⃣ 开始使用:")
    print("   从 utils.mcp_browser_tools 导入 MCPPlaywrightAgent")


async def main():
    """主安装流程"""
    print("🚀 LangChain MCP Adapters + Playwright MCP 自动化安装")
    print("=" * 60)
    
    # 检查基础环境
    if not check_python_version():
        return
    
    node_available = check_node_installed()
    
    # 安装 Python 依赖
    if not install_python_dependencies():
        print("❌ Python 依赖安装失败，请手动安装")
        return
    
    # 安装 Playwright 浏览器
    if not install_playwright_browsers():
        print("❌ Playwright 浏览器安装失败")
        return
    
    # 安装 MCP 服务器（如果 Node.js 可用）
    mcp_server_installed = False
    if node_available:
        mcp_server_installed = install_mcp_server()
    else:
        print("\n⚠️ Node.js 未安装，跳过 MCP 服务器安装")
        show_nodejs_install_instructions()
    
    # 测试集成
    if mcp_server_installed:
        integration_ok = await test_mcp_integration()
    else:
        integration_ok = False
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 安装结果总结:")
    
    results = [
        ("Python 环境", True),
        ("Python 依赖", True),
        ("Playwright 浏览器", True),
        ("Node.js", node_available),
        ("MCP 服务器", mcp_server_installed),
        ("MCP 集成测试", integration_ok)
    ]
    
    for item, status in results:
        status_icon = "✅" if status else "❌"
        print(f"  {item}: {status_icon}")
    
    if all(status for _, status in results):
        print("\n🎉 完美！所有组件安装成功")
    elif mcp_server_installed:
        print("\n⚡ 基本环境就绪，MCP 服务器可能需要额外配置")
    else:
        print("\n⚠️ 部分组件安装失败，请按照说明手动安装")
    
    show_next_steps()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 安装被用户中断")
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")
        import traceback
        traceback.print_exc() 