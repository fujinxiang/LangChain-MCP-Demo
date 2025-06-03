# 硅基流动 + MCP Playwright 演示项目

基于硅基流动 LLM 和 MCP Playwright 的智能浏览器自动化项目。

## ✨ 功能特性

- 🤖 **硅基流动 LLM**: 集成硅基流动 API 的智能对话系统
- 🌐 **MCP Playwright**: 基于 MCP 协议的浏览器自动化操作
- 🔧 **自动化安装**: 一键安装所有依赖和配置

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd LangChainDemo

# 安装 Python 依赖
pip install -r requirements.txt

# 运行自动化安装脚本
python setup_mcp.py
```

### 2. 配置 API Key

创建 `.env` 文件并配置硅基流动 API：

```env
# 硅基流动 API 配置
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_API_KEY=your-api-key-here
```

### 3. 运行演示

```bash
# 运行 MCP Playwright 演示
python mcp_browser_demo.py
```

## 📁 项目结构

```
LangChainDemo/
├── utils/
│   ├── llm_wrapper.py          # 硅基流动 LLM 包装器
│   ├── mcp_browser_tools.py    # MCP Playwright 工具
│   └── __init__.py
├── mcp_browser_demo.py         # MCP Playwright 演示
├── setup_mcp.py               # 自动化安装脚本
├── config.py                  # 配置文件
├── requirements.txt           # Python 依赖
└── README.md                  # 项目说明
```

## 🔧 核心组件

### 硅基流动 LLM 包装器

`utils/llm_wrapper.py` 提供了硅基流动 API 的 LangChain 集成：

```python
from utils.llm_wrapper import SiliconFlowLLM

llm = SiliconFlowLLM()
response = llm.invoke("你好，请介绍一下硅基流动")
print(response)
```

### MCP Playwright 工具

`utils/mcp_browser_tools.py` 提供了基于 MCP 协议的浏览器自动化：

```python
from utils.mcp_browser_tools import MCPPlaywrightAgent

agent = MCPPlaywrightAgent()
await agent.navigate("https://www.baidu.com")
await agent.screenshot("baidu_homepage")
await agent.close()
```

## 🛠️ 安装说明

### 自动安装（推荐）

运行 `setup_mcp.py` 脚本会自动完成以下操作：

1. 检查 Node.js 环境
2. 安装 MCP Playwright 服务器
3. 安装 Playwright 浏览器
4. 验证安装结果

### 手动安装

如果自动安装失败，可以手动执行：

```bash
# 1. 安装 Node.js (如果未安装)
# 下载并安装 Node.js: https://nodejs.org/

# 2. 安装 MCP Playwright 服务器
npm install -g @executeautomation/playwright-mcp-server

# 3. 安装 Playwright 浏览器
playwright install
```

## 📖 使用示例

### 基础浏览器操作

```python
import asyncio
from utils.mcp_browser_tools import MCPPlaywrightAgent

async def demo():
    agent = MCPPlaywrightAgent()
    
    # 导航到网页
    await agent.navigate("https://www.example.com")
    
    # 截图
    await agent.screenshot("example_page")
    
    # 点击元素
    await agent.click("button#submit")
    
    # 填写表单
    await agent.fill("input[name='username']", "test_user")
    
    # 关闭浏览器
    await agent.close()

asyncio.run(demo())
```

### 智能浏览器代理

```python
from utils.mcp_browser_tools import create_mcp_browser_agent

# 创建智能浏览器代理
agent = create_mcp_browser_agent()

# 使用自然语言指令
result = await agent.execute_task("打开百度，搜索'人工智能'")
print(result)
```

## 🔗 相关链接

- [硅基流动 API](https://siliconflow.cn/)
- [MCP 协议](https://modelcontextprotocol.io/)
- [Playwright](https://playwright.dev/)
- [LangChain](https://langchain.com/)

## �� 许可证

MIT License
