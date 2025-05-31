"""
LangChain + 硅基流动 + Playwright 浏览器操作 Streamlit Web 应用
提供美观的 Web 界面进行AI驱动的浏览器操作
"""

import streamlit as st
import asyncio
import sys
import os
from utils.llm_wrapper import create_llm
from utils.browser_tools import create_browser_agent, PlaywrightToolkit


@st.cache_resource
def init_llm():
    """初始化 LLM（缓存）"""
    try:
        return create_llm()
    except Exception as e:
        st.error(f"LLM 初始化失败: {e}")
        st.stop()


def check_playwright_environment():
    """检查 Playwright 环境"""
    try:
        import playwright
        from playwright.async_api import async_playwright
        return True, "Playwright 环境正常"
    except ImportError:
        return False, "Playwright 未安装，请运行: pip install playwright && playwright install"
    except Exception as e:
        return False, f"Playwright 环境检查失败: {e}"


async def run_browser_task(task_description: str, headless: bool = True):
    """异步执行浏览器任务"""
    try:
        llm = init_llm()
        agent = create_browser_agent(llm, headless=headless)
        
        result = await agent.execute_task(task_description)
        await agent.close()
        
        return result
    except Exception as e:
        return f"❌ 任务执行失败: {e}"


async def run_page_extraction(url: str, extract_type: str, headless: bool = True):
    """异步执行页面内容提取"""
    try:
        llm = init_llm()
        agent = create_browser_agent(llm, headless=headless)
        
        result = await agent.navigate_and_extract(url, extract_type)
        await agent.close()
        
        return result
    except Exception as e:
        return f"❌ 页面提取失败: {e}"


async def run_browser_tools_demo(url: str, operations: list, headless: bool = True):
    """异步执行浏览器工具演示"""
    try:
        toolkit = PlaywrightToolkit(headless=headless)
        await toolkit.initialize()
        
        results = []
        
        # 导航到页面
        nav_result = await toolkit.navigate_to(url)
        results.append(f"📍 导航结果: {nav_result}")
        
        # 执行操作
        for operation in operations:
            if operation == "获取标题":
                title = await toolkit.get_page_title()
                results.append(f"📄 页面标题: {title}")
                
            elif operation == "获取URL":
                current_url = await toolkit.get_current_url()
                results.append(f"🔗 当前URL: {current_url}")
                
            elif operation == "提取文本":
                text = await toolkit.extract_text()
                text_preview = text[:500] + "..." if len(text) > 500 else text
                results.append(f"📝 页面文本:\n{text_preview}")
                
            elif operation == "提取链接":
                links = await toolkit.extract_links()
                links_info = f"🔗 页面链接 (共 {len(links)} 个):\n"
                for i, link in enumerate(links[:5]):  # 只显示前5个
                    links_info += f"{i+1}. {link['text'][:30]} -> {link['href']}\n"
                if len(links) > 5:
                    links_info += f"... 还有 {len(links) - 5} 个链接"
                results.append(links_info)
        
        await toolkit.close()
        return "\n\n".join(results)
        
    except Exception as e:
        return f"❌ 工具演示失败: {e}"


def browser_planning_page():
    """浏览器任务规划页面"""
    st.header("🤖 AI 浏览器任务规划")
    st.write("描述您想要执行的浏览器任务，AI 将为您分析并提供执行建议")
    
    # 环境检查
    is_ok, env_msg = check_playwright_environment()
    if is_ok:
        st.success(f"✅ {env_msg}")
    else:
        st.error(f"❌ {env_msg}")
        st.stop()
    
    # 任务输入
    task_description = st.text_area(
        "📋 描述您的浏览器任务:",
        height=100,
        placeholder="例如：访问百度首页并搜索'人工智能'，然后获取搜索结果..."
    )
    
    # 浏览器选项
    col1, col2 = st.columns(2)
    with col1:
        headless = st.checkbox("🖥️ 无界面模式 (headless)", value=True, 
                              help="启用后浏览器在后台运行，不显示界面")
    
    # 执行按钮
    if st.button("🚀 分析任务", disabled=not task_description.strip()):
        with st.spinner("🤖 AI 正在分析任务..."):
            try:
                # 在事件循环中运行异步任务
                result = asyncio.run(run_browser_task(task_description, headless))
                st.success("✅ 任务分析完成!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"❌ 分析失败: {e}")
    
    # 示例任务
    st.subheader("💡 示例任务")
    example_tasks = [
        "访问百度首页并搜索'LangChain'",
        "访问GitHub，搜索Python项目",
        "访问新闻网站，获取今日头条",
        "访问电商网站，搜索商品价格",
        "访问技术博客，提取文章标题"
    ]
    
    for task in example_tasks:
        if st.button(f"📌 {task}", key=f"example_{task}"):
            st.session_state.task_input = task
            st.rerun()


def page_extraction_page():
    """页面内容提取页面"""
    st.header("🔍 页面内容提取")
    st.write("输入网址，自动提取页面内容")
    
    # 环境检查
    is_ok, env_msg = check_playwright_environment()
    if is_ok:
        st.success(f"✅ {env_msg}")
    else:
        st.error(f"❌ {env_msg}")
        st.stop()
    
    # URL输入
    url = st.text_input(
        "🌐 输入网址:",
        placeholder="https://example.com",
        help="请输入完整的URL，包含http://或https://"
    )
    
    # 提取选项
    col1, col2, col3 = st.columns(3)
    with col1:
        extract_text = st.checkbox("📝 提取文本内容", value=True)
    with col2:
        extract_links = st.checkbox("🔗 提取页面链接", value=False)
    with col3:
        headless = st.checkbox("🖥️ 无界面模式", value=True)
    
    # 执行按钮
    if st.button("🔍 开始提取", disabled=not url.strip()):
        if not url.startswith(('http://', 'https://')):
            st.warning("⚠️ 请输入完整的URL，包含http://或https://")
            return
        
        # 执行文本提取
        if extract_text:
            with st.spinner("📝 正在提取页面文本..."):
                try:
                    result = asyncio.run(run_page_extraction(url, "text", headless))
                    st.subheader("📝 页面文本内容")
                    st.text_area("", value=result, height=300, disabled=True)
                except Exception as e:
                    st.error(f"❌ 文本提取失败: {e}")
        
        # 执行链接提取
        if extract_links:
            with st.spinner("🔗 正在提取页面链接..."):
                try:
                    result = asyncio.run(run_page_extraction(url, "links", headless))
                    st.subheader("🔗 页面链接")
                    st.text_area("", value=result, height=200, disabled=True)
                except Exception as e:
                    st.error(f"❌ 链接提取失败: {e}")
    
    # 预设网站
    st.subheader("🌟 快速测试网站")
    test_sites = [
        ("https://httpbin.org/html", "HTTPBin HTML测试页"),
        ("https://example.com", "Example.com 示例网站"),
        ("https://httpbin.org/json", "HTTPBin JSON测试页"),
        ("https://news.ycombinator.com", "Hacker News")
    ]
    
    cols = st.columns(2)
    for i, (site_url, site_name) in enumerate(test_sites):
        with cols[i % 2]:
            if st.button(f"🔗 {site_name}", key=f"site_{i}"):
                st.session_state.url_input = site_url
                st.rerun()


def browser_tools_page():
    """浏览器工具演示页面"""
    st.header("🛠️ 浏览器工具演示")
    st.write("演示各种浏览器操作工具的功能")
    
    # 环境检查
    is_ok, env_msg = check_playwright_environment()
    if is_ok:
        st.success(f"✅ {env_msg}")
    else:
        st.error(f"❌ {env_msg}")
        st.stop()
    
    # 工具说明
    st.subheader("📋 可用工具")
    tools_info = {
        "获取标题": "获取页面标题",
        "获取URL": "获取当前页面URL",
        "提取文本": "提取页面文本内容",
        "提取链接": "提取页面中的所有链接"
    }
    
    for tool_name, description in tools_info.items():
        st.write(f"• **{tool_name}**: {description}")
    
    # 输入区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input(
            "🌐 目标网址:",
            placeholder="https://example.com"
        )
    
    with col2:
        headless = st.checkbox("🖥️ 无界面模式", value=True)
    
    # 操作选择
    st.subheader("🔧 选择要执行的操作")
    operations = []
    
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("📄 获取标题"):
            operations.append("获取标题")
        if st.checkbox("🔗 获取URL"):
            operations.append("获取URL")
    
    with col2:
        if st.checkbox("📝 提取文本"):
            operations.append("提取文本")
        if st.checkbox("🔗 提取链接"):
            operations.append("提取链接")
    
    # 执行按钮
    if st.button("🚀 执行操作", disabled=not url.strip() or not operations):
        if not url.startswith(('http://', 'https://')):
            st.warning("⚠️ 请输入完整的URL，包含http://或https://")
            return
        
        with st.spinner("🤖 正在执行浏览器操作..."):
            try:
                result = asyncio.run(run_browser_tools_demo(url, operations, headless))
                st.success("✅ 操作执行完成!")
                st.text_area("📊 执行结果:", value=result, height=400, disabled=True)
                
            except Exception as e:
                st.error(f"❌ 操作执行失败: {e}")


def main():
    """主函数"""
    st.set_page_config(
        page_title="AI 浏览器助手",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏
    with st.sidebar:
        st.title("🌐 AI 浏览器助手")
        st.write("选择功能模式:")
        
        page = st.radio(
            "功能模式",
            ["🤖 任务规划", "🔍 内容提取", "🛠️ 工具演示"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.subheader("ℹ️ 关于")
        st.write("""
        这是一个基于 LangChain、硅基流动 API 和 Playwright 构建的智能浏览器助手。
        
        **功能特性:**
        - AI 任务规划分析
        - 自动化页面操作
        - 内容提取和分析
        - 智能浏览器工具
        
        **技术栈:**
        - LangChain
        - 硅基流动 API
        - Playwright
        - Streamlit
        """)
        
        st.markdown("---")
        st.subheader("⚠️ 使用须知")
        st.write("""
        - 请遵守网站的robots.txt和使用条款
        - 避免对网站造成过大负载
        - 尊重网站的访问频率限制
        - 确保已安装Playwright浏览器
        """)
        
        st.markdown("---")
        st.write("💡 **提示**: 确保已正确配置 API Key 和 Playwright 环境")
    
    # 主内容区域
    if page == "🤖 任务规划":
        browser_planning_page()
    elif page == "🔍 内容提取":
        page_extraction_page()
    elif page == "🛠️ 工具演示":
        browser_tools_page()


if __name__ == "__main__":
    main()
