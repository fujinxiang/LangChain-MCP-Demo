#!/usr/bin/env python3
"""
简单示例演示脚本
演示 LangChain + 硅基流动 的基本功能（不需要真实 API Key）
"""

def demo_llm_wrapper():
    """演示 LLM 包装器的结构"""
    print("🤖 LLM 包装器演示")
    print("-" * 30)
    
    try:
        from utils.llm_wrapper import SiliconFlowLLM
        from config import config
        
        print(f"✅ LLM 类型: SiliconFlowLLM")
        print(f"✅ 基础 URL: {config.SILICONFLOW_BASE_URL}")
        print(f"✅ 默认模型: {config.DEFAULT_MODEL}")
        print(f"✅ 温度设置: {config.TEMPERATURE}")
        
        # 创建 LLM 实例（不调用 API）
        llm = SiliconFlowLLM()
        print(f"✅ LLM 实例创建成功，类型: {llm._llm_type}")
        
    except Exception as e:
        print(f"❌ LLM 包装器演示失败: {e}")

def demo_document_loader():
    """演示文档加载器"""
    print("\n📄 文档加载器演示")
    print("-" * 30)
    
    try:
        from utils.document_loader import DocumentLoader, SimpleVectorStore
        
        # 创建文档加载器
        doc_loader = DocumentLoader(chunk_size=500, chunk_overlap=100)
        print("✅ 文档加载器创建成功")
        
        # 示例文本
        sample_text = """
        LangChain 是一个强大的框架，用于构建基于大语言模型的应用程序。
        它提供了丰富的工具和组件，帮助开发者更容易地集成和使用各种 AI 模型。
        
        硅基流动（SiliconFlow）是一个提供大模型 API 服务的平台。
        它支持多种流行的开源大模型，如 DeepSeek、Qwen、Llama 等。
        
        通过结合 LangChain 和硅基流动，开发者可以快速构建智能应用。
        """
        
        # 加载文档
        documents = doc_loader.load_text_content(sample_text, "示例文档")
        print(f"✅ 文档分割成功，共 {len(documents)} 个片段")
        
        # 创建向量存储
        vector_store = SimpleVectorStore()
        vector_store.add_documents(documents)
        print("✅ 文档已添加到向量存储")
        
        # 测试搜索
        query = "LangChain 是什么"
        results = vector_store.similarity_search(query, k=2)
        print(f"✅ 搜索查询 '{query}' 返回 {len(results)} 个结果")
        
        if results:
            print("📄 搜索结果预览:")
            for i, doc in enumerate(results, 1):
                preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                print(f"   {i}. {preview}")
        
    except Exception as e:
        print(f"❌ 文档加载器演示失败: {e}")

def demo_project_structure():
    """演示项目结构"""
    print("\n🏗️ 项目结构演示")
    print("-" * 30)
    
    import os
    
    def show_tree(path, prefix="", max_depth=2, current_depth=0):
        if current_depth >= max_depth:
            return
        
        items = []
        try:
            for item in sorted(os.listdir(path)):
                if not item.startswith('.') and item != '__pycache__':
                    items.append(item)
        except PermissionError:
            return
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            item_path = os.path.join(path, item)
            
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item}")
            
            if os.path.isdir(item_path) and current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_tree(item_path, next_prefix, max_depth, current_depth + 1)
    
    print("LangChainDemo/")
    show_tree(".", max_depth=3)

def main():
    """主演示函数"""
    print("🎯 LangChain + 硅基流动 Demo 功能演示")
    print("=" * 50)
    
    # 演示各个组件
    demo_llm_wrapper()
    demo_document_loader()
    demo_project_structure()
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print("\n💡 使用提示:")
    print("1. 在 .env 文件中设置真实的硅基流动 API Key")
    print("2. 运行 'python chat_demo.py' 进行聊天测试")
    print("3. 运行 'python doc_qa_demo.py' 进行文档问答测试")
    print("4. 运行 'streamlit run streamlit_app.py' 启动 Web 界面")

if __name__ == "__main__":
    main()
