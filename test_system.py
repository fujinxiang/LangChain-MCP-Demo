#!/usr/bin/env python3
"""
系统测试脚本
验证 LangChain + 硅基流动 Demo 项目的基本功能
"""

import sys
import os

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试模块导入...")
    
    try:
        import langchain
        print(f"✅ LangChain: {langchain.__version__}")
    except ImportError as e:
        print(f"❌ LangChain 导入失败: {e}")
        return False
    
    try:
        import requests
        print(f"✅ Requests: {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests 导入失败: {e}")
        return False
    
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit 导入失败: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv: 导入成功")
    except ImportError as e:
        print(f"❌ Python-dotenv 导入失败: {e}")
        return False
    
    return True

def test_project_structure():
    """测试项目结构"""
    print("\n🏗️ 测试项目结构...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'config.py',
        'chat_demo.py',
        'doc_qa_demo.py',
        'streamlit_app.py',
        'utils/__init__.py',
        'utils/llm_wrapper.py',
        'utils/document_loader.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_config():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    
    try:
        from config import config
        print("✅ 配置模块导入成功")
        
        # 检查环境变量（不验证 API Key，因为可能还未设置）
        print(f"✅ 基础 URL: {config.SILICONFLOW_BASE_URL}")
        print(f"✅ 默认模型: {config.DEFAULT_MODEL}")
        print(f"✅ 温度: {config.TEMPERATURE}")
        print(f"✅ 最大令牌: {config.MAX_TOKENS}")
        
        if not config.SILICONFLOW_API_KEY:
            print("⚠️ API Key 未设置（需要在 .env 文件中配置）")
        else:
            print("✅ API Key 已设置")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_utils():
    """测试工具模块"""
    print("\n🛠️ 测试工具模块...")
    
    try:
        from utils.llm_wrapper import SiliconFlowLLM
        print("✅ LLM 包装器导入成功")
    except Exception as e:
        print(f"❌ LLM 包装器导入失败: {e}")
        return False
    
    try:
        from utils.document_loader import DocumentLoader, SimpleVectorStore
        print("✅ 文档加载器导入成功")
    except Exception as e:
        print(f"❌ 文档加载器导入失败: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 LangChain + 硅基流动 Demo 系统测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("项目结构", test_project_structure),
        ("配置", test_config),
        ("工具模块", test_utils)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} 测试失败")
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目设置正确。")
        print("\n📝 下一步:")
        print("1. 在 .env 文件中设置您的硅基流动 API Key")
        print("2. 运行 'python chat_demo.py' 测试基础聊天")
        print("3. 运行 'streamlit run streamlit_app.py' 启动 Web 界面")
    else:
        print("⚠️ 部分测试失败，请检查项目配置")
        sys.exit(1)

if __name__ == "__main__":
    main()
