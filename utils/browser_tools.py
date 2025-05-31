"""
Playwright 浏览器工具包装器
提供网页操作功能，包括页面访问、元素交互、内容提取等
使用原生 Playwright API 实现
"""

import asyncio
from typing import Optional, Dict, Any, List
from playwright.async_api import async_playwright, Browser, Page, BrowserContext


class PlaywrightToolkit:
    """Playwright 浏览器工具包"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._initialized = False
    
    async def initialize(self):
        """异步初始化浏览器"""
        if self._initialized:
            return
        
        try:
            # 启动 Playwright
            self.playwright = await async_playwright().start()
            
            # 创建浏览器实例
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            
            # 创建浏览器上下文
            self.context = await self.browser.new_context()
            
            # 创建页面
            self.page = await self.context.new_page()
            
            self._initialized = True
            print("✅ Playwright 浏览器工具包初始化成功")
            
        except Exception as e:
            print(f"❌ Playwright 初始化失败: {e}")
            print("💡 请确保已安装 Playwright 浏览器: python -m playwright install")
            raise
    
    async def navigate_to(self, url: str) -> str:
        """导航到指定URL"""
        if not self._initialized:
            await self.initialize()
        
        try:
            await self.page.goto(url)
            return f"✅ 成功导航到: {url}"
        except Exception as e:
            return f"❌ 导航失败: {e}"
    
    async def extract_text(self) -> str:
        """提取页面文本内容"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            text = await self.page.inner_text('body')
            return text
        except Exception as e:
            return f"❌ 提取文本失败: {e}"
    
    async def extract_links(self) -> List[Dict[str, str]]:
        """提取页面中的所有链接"""
        if not self.page:
            return []
        
        try:
            links = await self.page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links.map(link => ({
                        text: link.textContent.trim(),
                        href: link.href,
                        title: link.title || ''
                    }));
                }
            """)
            return links
        except Exception as e:
            print(f"❌ 提取链接失败: {e}")
            return []
    
    async def click_element(self, selector: str) -> str:
        """点击页面元素"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            await self.page.click(selector)
            return f"✅ 成功点击元素: {selector}"
        except Exception as e:
            return f"❌ 点击失败: {e}"
    
    async def fill_input(self, selector: str, text: str) -> str:
        """填写输入框"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            await self.page.fill(selector, text)
            return f"✅ 成功填写: {selector} = {text}"
        except Exception as e:
            return f"❌ 填写失败: {e}"
    
    async def get_page_title(self) -> str:
        """获取页面标题"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            title = await self.page.title()
            return title
        except Exception as e:
            return f"❌ 获取标题失败: {e}"
    
    async def get_current_url(self) -> str:
        """获取当前页面URL"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            url = self.page.url
            return url
        except Exception as e:
            return f"❌ 获取URL失败: {e}"
    
    async def screenshot(self, path: str = None) -> str:
        """截图"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            if path:
                await self.page.screenshot(path=path)
                return f"✅ 截图保存到: {path}"
            else:
                screenshot_bytes = await self.page.screenshot()
                return f"✅ 截图完成，大小: {len(screenshot_bytes)} bytes"
        except Exception as e:
            return f"❌ 截图失败: {e}"
    
    async def wait_for_element(self, selector: str, timeout: int = 30000) -> str:
        """等待元素出现"""
        if not self.page:
            return "❌ 页面未初始化"
        
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return f"✅ 元素已出现: {selector}"
        except Exception as e:
            return f"❌ 等待元素失败: {e}"
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """获取工具描述"""
        return {
            "navigate_to": "导航到指定URL",
            "extract_text": "提取页面文本内容",
            "extract_links": "提取页面中的所有链接",
            "click_element": "点击页面元素",
            "fill_input": "填写输入框",
            "get_page_title": "获取页面标题",
            "get_current_url": "获取当前页面URL",
            "screenshot": "截图",
            "wait_for_element": "等待元素出现"
        }
    
    async def close(self):
        """关闭浏览器"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
            self._initialized = False
            print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️ 关闭浏览器时出错: {e}")


class SimpleBrowserAgent:
    """简单的浏览器代理，结合 LLM 和 Playwright 工具"""
    
    def __init__(self, llm, headless: bool = True):
        self.llm = llm
        self.toolkit = PlaywrightToolkit(headless=headless)
        self._initialized = False
    
    async def initialize(self):
        """初始化代理"""
        await self.toolkit.initialize()
        self._initialized = True
    
    async def execute_task(self, task_description: str) -> str:
        """执行浏览器任务"""
        if not self._initialized:
            await self.initialize()
        
        # 获取可用工具描述
        tool_descriptions = self.toolkit.get_tool_descriptions()
        
        # 构建工具描述文本
        tools_text = "\n".join([
            f"- {name}: {desc}" 
            for name, desc in tool_descriptions.items()
        ])
        
        # 创建任务规划提示
        planning_prompt = f"""
你是一个智能的浏览器自动化助手。用户给出了一个任务，你需要分析任务并规划执行步骤。

可用的浏览器操作工具:
{tools_text}

用户任务: {task_description}

请分析这个任务，并给出详细的执行步骤建议。每个步骤应该包含：
1. 要使用的工具名称
2. 工具的参数说明
3. 预期的结果
4. 可能的注意事项

请用中文回答，格式要清晰，具体可操作。
"""
        
        try:
            # 打印 planning_prompt 到控制台
            print("🔍 规划提示内容:")
            print("=" * 50)
            print(planning_prompt)
            print("=" * 50)
            
            # 使用 LLM 规划任务
            plan_response = self.llm.invoke(planning_prompt)
            
            return f"""
📋 任务分析完成

🎯 任务描述: {task_description}

📝 AI 执行建议:
{plan_response}

🛠️ 可用工具说明:
{chr(10).join([f'• {name}: {desc}' for name, desc in tool_descriptions.items()])}

💡 使用提示: 
- 这是一个任务规划建议，实际执行需要根据具体情况调整
- 可以通过 Python 代码调用相应的工具方法
- 建议先测试简单网站，再处理复杂任务
"""
        
        except Exception as e:
            return f"❌ 任务分析失败: {e}"
    
    async def navigate_and_extract(self, url: str, extract_type: str = "text") -> str:
        """导航到页面并提取内容"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # 导航到页面
            nav_result = await self.toolkit.navigate_to(url)
            
            if "❌" in nav_result:
                return nav_result
            
            # 获取页面基本信息
            title = await self.toolkit.get_page_title()
            current_url = await self.toolkit.get_current_url()
            
            result = f"🌐 页面访问成功\n"
            result += f"📄 标题: {title}\n"
            result += f"🔗 URL: {current_url}\n\n"
            
            # 提取内容
            if extract_type == "text":
                content = await self.toolkit.extract_text()
                result += f"📝 页面文本内容:\n{content[:1000]}{'...' if len(content) > 1000 else ''}"
                
            elif extract_type == "links":
                links = await self.toolkit.extract_links()
                result += f"🔗 页面链接 (共 {len(links)} 个):\n"
                for i, link in enumerate(links[:10]):  # 只显示前10个链接
                    result += f"{i+1}. {link['text'][:50]} -> {link['href']}\n"
                if len(links) > 10:
                    result += f"... 还有 {len(links) - 10} 个链接"
            
            return result
            
        except Exception as e:
            return f"❌ 页面操作失败: {e}"
    
    async def close(self):
        """关闭代理"""
        await self.toolkit.close()


def create_browser_agent(llm, headless: bool = True) -> SimpleBrowserAgent:
    """创建浏览器代理实例"""
    return SimpleBrowserAgent(llm, headless=headless)
