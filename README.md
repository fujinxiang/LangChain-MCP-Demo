# LangChain Demo Project

基于 LangChain 的人工智能应用演示项目，集成了硅基流动 LLM 和多种 AI 功能。

## ✨ 新功能：MCP 集成

现在支持 **Model Context Protocol (MCP)** 模式的浏览器自动化！

### 🔗 MCP 模式优势

- ⚡ 更高效的工具执行性能
- 🛠️ 更丰富的 Playwright 操作支持  
- 📊 更好的错误处理和日志
- 🔄 支持实时代码生成
- 🤖 标准化的工具调用协议

### 🚀 MCP 快速开始

```bash
# 1. 安装 Python 依赖
pip install langchain-mcp-adapters

# 2. 安装 MCP Playwright 服务器
npm install -g @executeautomation/playwright-mcp-server

# 3. 验证 MCP 集成
python test_mcp_integration.py

# 4. 运行 MCP 演示
python mcp_browser_demo.py
```

## 📋 功能特性

### 传统功能
- 🤖 **LLM 对话**: 基于硅基流动的智能对话系统
- 📄 **文档问答**: PDF/TXT 文档智能问答
- 🌐 **网页操作**: Playwright 浏览器自动化
- 🎨 **Streamlit UI**: 友好的 Web 界面

### MCP 新增功能
- 🔧 **JavaScript 执行**: 在浏览器中执行自定义 JS 代码
- 📋 **控制台日志**: 获取浏览器控制台日志
- ⌨️ **键盘操作**: 支持各种键盘按键和快捷键
- 🖱️ **拖拽操作**: 元素拖拽和拖放
- 📄 **PDF 保存**: 将页面保存为 PDF 文件
- 🎬 **代码生成**: 实时记录操作并生成 Playwright 测试代码
- 🎯 **元素悬停**: 鼠标悬停操作
- ⬅️➡️ **导航控制**: 浏览器前进、后退操作

## 🛠️ 安装和配置

### 基础环境
```bash
# 克隆项目
git clone [repository-url]
cd LangChainDemo

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### MCP 环境 (新)
```bash
# 安装 MCP 适配器
pip install langchain-mcp-adapters

# 安装 Node.js (如果未安装)
# 下载并安装: https://nodejs.org/

# 安装 MCP Playwright 服务器
npm install -g @executeautomation/playwright-mcp-server
```

### 配置文件
创建 `config.py` 文件：
```python
# 硅基流动 API 配置
SILICONCLOUD_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONCLOUD_API_KEY = "your-api-key-here"

# 默认模型
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V2.5"
```

## 🎮 使用方式

### 1. 基础对话演示
```bash
python chat_demo.py
```

### 2. 文档问答演示
```bash
python doc_qa_demo.py
```

### 3. 浏览器操作演示

#### 传统模式
```bash
python browser_demo.py
# 选择 "1. 传统 Playwright 模式"
```

#### MCP 模式 (推荐)
```bash
python browser_demo.py
# 选择 "2. MCP Playwright 模式"

# 或直接运行 MCP 专用演示
python mcp_browser_demo.py
```

### 4. Web UI 界面
```bash
streamlit run streamlit_app.py
```

## 🔧 MCP 使用示例

### 基础操作
```python
from utils.mcp_browser_tools import MCPPlaywrightAgent

agent = MCPPlaywrightAgent()
await agent.initialize()

# 导航
await agent.navigate_to("https://www.baidu.com")

# 截图
await agent.take_screenshot("homepage", savePng=True)

# 执行 JavaScript
result = await agent.execute_javascript("document.title")

await agent.close()
```

### 智能任务
```python
from utils.llm_wrapper import create_llm
from utils.mcp_browser_tools import create_mcp_browser_agent

llm = create_llm()
agent = create_mcp_browser_agent(llm)

# AI 自动执行复杂任务
result = await agent.execute_smart_task("访问百度并搜索人工智能，然后截图")

await agent.close()
```

## 📊 项目结构

```
LangChainDemo/
├── utils/
│   ├── llm_wrapper.py          # LLM 封装
│   ├── browser_tools.py        # 传统 Playwright 工具
│   ├── mcp_browser_tools.py    # MCP Playwright 工具 (新)
│   └── document_loader.py      # 文档加载器
├── browser_demo.py             # 浏览器演示 (支持双模式)
├── mcp_browser_demo.py         # MCP 专用演示 (新)
├── test_mcp_integration.py     # MCP 集成测试 (新)
├── chat_demo.py                # 对话演示
├── doc_qa_demo.py              # 文档问答演示
├── streamlit_app.py            # Web UI
├── config.py                   # 配置文件
└── requirements.txt            # 依赖列表
```

## 🧪 测试

### 基础功能测试
```bash
python test_llm_simple.py
python test_browser.py
```

### MCP 集成测试
```bash
python test_mcp_integration.py
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### MCP 相关贡献
如果您想为 MCP 功能做贡献，请关注：
- 新的 Playwright 操作支持
- MCP 服务器性能优化  
- 智能任务模板扩展
- 错误处理改进

## 📄 许可证

MIT License

## 🔗 相关链接

- [LangChain 文档](https://python.langchain.com/)
- [硅基流动 API](https://siliconflow.cn/)
- [Playwright 文档](https://playwright.dev/)
- [MCP 规范](https://modelcontextprotocol.io/)
- [langchain-mcp-adapters](https://github.com/peterdeep/langchain-mcp-adapters)
