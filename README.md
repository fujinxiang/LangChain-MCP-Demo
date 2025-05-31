# LangChain + 硅基流动 Demo

一个使用 LangChain 框架集成硅基流动大模型的简单示例应用。

## 功能特性

- 使用 LangChain 框架
- 集成硅基流动（SiliconFlow）API
- 支持对话式问答
- 支持文档问答
- 支持流式输出

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 到 `.env`
2. 在 `.env` 文件中设置您的硅基流动 API Key

```
SILICONFLOW_API_KEY=your_api_key_here
```

## 使用方法

### 基础聊天
```bash
python chat_demo.py
```

### 文档问答
```bash
python doc_qa_demo.py
```

### Web 应用界面
```bash
streamlit run streamlit_app.py
```

## 项目结构

```
LangChainDemo/
├── README.md
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
├── chat_demo.py          # 命令行聊天演示
├── doc_qa_demo.py        # 命令行文档问答演示
├── streamlit_app.py      # Web 界面应用
├── config.py             # 配置管理
└── utils/
    ├── __init__.py
    ├── llm_wrapper.py    # 硅基流动 LLM 包装器
    └── document_loader.py # 文档加载和处理工具
```

## 硅基流动支持的模型

- deepseek-chat
- Qwen/Qwen2.5-7B-Instruct
- meta-llama/Meta-Llama-3.1-8B-Instruct
- 等更多模型...

## 快速开始

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd LangChainDemo
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 API Key**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置您的硅基流动 API Key
   ```

4. **运行演示**
   ```bash
   # 命令行聊天
   python chat_demo.py
   
   # 文档问答
   python doc_qa_demo.py
   
   # Web 界面（推荐）
   streamlit run streamlit_app.py
   ```

## 注意事项

- 请确保您已获得硅基流动 API Key
- 首次运行可能需要下载相关依赖
- 网络连接需要稳定以访问 API 服务
- 建议使用 Python 3.8 或更高版本

## 许可证

MIT License
