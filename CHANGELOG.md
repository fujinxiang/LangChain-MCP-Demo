# 更新日志 (CHANGELOG)

## [1.1.0] - 2025-05-31

### 修复
- **重要**: 修复 LangChain 弃用警告
  - 将 `LLMChain` 替换为新的 `RunnableSequence` 语法 (`prompt | llm`)
  - 更新所有相关文件：`chat_demo.py`、`doc_qa_demo.py`、`streamlit_app.py`
  - 将 `chain.run()` 方法替换为 `chain.invoke()` 方法
  - 确保与 LangChain 0.3.x 版本兼容

### 新增
- 添加 `.gitignore` 文件，包含 Python 项目常见的忽略规则
- 添加系统测试脚本 `test_system.py`
- 添加功能演示脚本 `demo.py`
- 完善 README.md 文档

### 技术细节
- **弃用修复**: `LLMChain` 在 LangChain 0.1.17 中被弃用
- **新语法**: 使用 `prompt | llm` 创建链
- **新调用方式**: 使用 `chain.invoke({"key": "value"})` 替代 `chain.run(key="value")`

## [1.0.0] - 2025-05-31

### 初始版本
- 实现 LangChain + 硅基流动集成
- 支持基础聊天功能
- 支持文档问答功能
- 提供 Streamlit Web 界面
- 包含配置管理和工具模块
