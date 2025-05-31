#!/usr/bin/env python3
"""
测试 Streamlit 应用的浏览器功能
"""

import sys
import os
import asyncio

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_streamlit_imports():
    """测试 Streamlit 应用的导入"""
    print("🧪 测试 Streamlit 应用导入...")
    
    try:
        import streamlit_app
        print("✅ streamlit_app 导入成功")
        
        # 测试关键函数是否存在
        required_functions = [
            'chat_page',
            'doc_qa_page', 
            'browser_page',
            'task_planning_section',
            'page_navigation_section',
            'intelligent_analysis_section',
            'main'
        ]
        
        for func_name in required_functions:
            if hasattr(streamlit_app, func_name):
                print(f"✅ {func_name} 函数存在")
            else:
                print(f"❌ {func_name} 函数不存在")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_browser_functions():
    """测试浏览器相关函数"""
    print("\n🌐 测试浏览器函数...")
    
    try:
        from streamlit_app import plan_browser_task, navigate_and_extract_page
        
        print("✅ 浏览器函数导入成功")
        
        # 测试是否为异步函数
        if asyncio.iscoroutinefunction(plan_browser_task):
            print("✅ plan_browser_task 是异步函数")
        else:
            print("❌ plan_browser_task 不是异步函数")
            return False
            
        if asyncio.iscoroutinefunction(navigate_and_extract_page):
            print("✅ navigate_and_extract_page 是异步函数")
        else:
            print("❌ navigate_and_extract_page 不是异步函数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 浏览器函数测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("\n📦 测试依赖包...")
    
    dependencies = [
        ('streamlit', 'Streamlit'),
        ('asyncio', 'Asyncio'),
        ('playwright.async_api', 'Playwright'),
        ('utils.browser_tools', '浏览器工具'),
        ('utils.llm_wrapper', 'LLM包装器')
    ]
    
    all_good = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} 可用")
        except ImportError as e:
            print(f"❌ {name} 不可用: {e}")
            all_good = False
    
    return all_good

def show_feature_summary():
    """显示功能总结"""
    print("\n🎯 新增功能总结")
    print("=" * 50)
    print("""
📱 **Streamlit 应用新增功能:**

🌐 **浏览器助手页面**
   - 📋 任务规划：AI 分析浏览器任务并制定执行计划
   - 🔍 页面导航：自动访问网页并提取内容
   - 🤖 智能分析：AI 分析网页内容并生成报告

🛠️ **支持的操作:**
   - 网页导航和内容提取
   - 页面文本和链接提取
   - 智能任务规划和分析
   - 支持多种分析类型

💡 **使用方式:**
   1. 运行: streamlit run streamlit_app.py
   2. 在侧边栏选择 "🌐 浏览器助手"
   3. 选择相应的功能模式
   4. 输入任务或URL进行操作

⚠️ **注意事项:**
   - 需要安装 Playwright: pip install playwright
   - 需要下载浏览器: playwright install
   - 确保网络连接正常
   - 遵守网站使用条款
""")

def main():
    """主测试函数"""
    print("🚀 Streamlit 浏览器功能测试")
    print("=" * 50)
    
    tests = [
        ("Streamlit 导入", test_streamlit_imports),
        ("浏览器函数", test_browser_functions), 
        ("依赖包", test_dependencies)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        if test_func():
            passed += 1
            print(f"✅ {test_name}测试通过")
        else:
            print(f"❌ {test_name}测试失败")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！浏览器功能已成功集成到 Streamlit 应用中。")
        show_feature_summary()
        
        print("\n🚀 启动命令:")
        print("streamlit run streamlit_app.py")
        
    else:
        print("⚠️ 部分测试失败，请检查配置和依赖")

if __name__ == "__main__":
    main()
