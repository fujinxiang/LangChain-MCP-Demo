"""
Playwright 浏览器工具包装器
提供网页操作功能，包括页面访问、元素交互、内容提取等
使用原生 Playwright API 实现
"""

import asyncio
import re
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
    
    async def get_elements(self, selector: str) -> List[Dict[str, str]]:
        """获取页面元素"""
        if not self.page:
            return []
        
        try:
            elements = await self.page.evaluate(f"""
                () => {{
                    const elements = Array.from(document.querySelectorAll('{selector}'));
                    return elements.map(element => ({{
                        text: element.textContent ? element.textContent.trim() : '',
                        href: element.href || '',
                        title: element.title || '',
                        tag: element.tagName.toLowerCase(),
                        id: element.id || '',
                        className: element.className || ''
                    }}));
                }}
            """)
            return elements
        except Exception as e:
            print(f"❌ 获取元素失败: {e}")
            return []
    
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
            "wait_for_element": "等待元素出现",
            "get_elements": "获取指定选择器的页面元素"
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
        """执行浏览器任务（仅规划）"""
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
    
    async def execute_task_with_actions(self, task_description: str) -> str:
        """真正执行浏览器任务"""
        if not self._initialized:
            await self.initialize()
        
        result = f"🚀 开始执行任务: {task_description}\n"
        result += "=" * 50 + "\n\n"
        
        try:
            # 根据任务描述判断要执行的操作
            task_lower = task_description.lower()
            
            # 处理百度搜索任务
            if "百度" in task_description and "搜索" in task_description:
                return await self._execute_baidu_search(task_description)
            
            # 处理GitHub搜索任务
            elif "github" in task_lower and "搜索" in task_description:
                return await self._execute_github_search(task_description)
            
            # 处理访问网页任务
            elif "访问" in task_description:
                return await self._execute_visit_website(task_description)
            
            # 处理截图任务
            elif "截图" in task_description:
                return await self._execute_screenshot(task_description)
            
            # 通用网页操作
            else:
                return await self._execute_general_task(task_description)
                
        except Exception as e:
            return f"❌ 任务执行失败: {e}"
    
    async def _execute_baidu_search(self, task_description: str) -> str:
        """执行百度搜索"""
        result = "🔍 执行百度搜索任务\n\n"
        
        try:
            # 提取搜索关键词
            import re
            search_match = re.search(r"搜索['\"]?([^'\"]+)['\"]?", task_description)
            if search_match:
                search_term = search_match.group(1)
            else:
                search_term = "人工智能"  # 默认搜索词
            
            # 1. 访问百度首页
            result += "1️⃣ 访问百度首页...\n"
            nav_result = await self.toolkit.navigate_to("https://www.baidu.com")
            result += f"   {nav_result}\n\n"
            
            # 2. 截图
            result += "2️⃣ 截图百度首页...\n"
            screenshot_result = await self.toolkit.screenshot()
            result += f"   {screenshot_result}\n\n"
            
            # 3. 填写搜索框
            result += f"3️⃣ 填写搜索框: {search_term}...\n"
            fill_result = await self.toolkit.fill_input("#kw", search_term)
            result += f"   {fill_result}\n\n"
            
            # 4. 点击搜索按钮
            result += "4️⃣ 点击搜索按钮...\n"
            click_result = await self.toolkit.click_element("#su")
            result += f"   {click_result}\n\n"
            
            # 5. 等待搜索结果加载
            result += "5️⃣ 等待搜索结果...\n"
            await asyncio.sleep(2)  # 等待页面加载
            
            # 6. 获取页面信息
            title = await self.toolkit.get_page_title()
            url = await self.toolkit.get_current_url()
            result += f"   页面标题: {title}\n"
            result += f"   当前URL: {url}\n\n"
            
            # 7. 提取搜索结果
            result += "6️⃣ 提取搜索结果...\n"
            text_content = await self.toolkit.extract_text()
            # 只显示前500个字符
            result += f"   搜索结果预览:\n   {text_content[:500]}...\n\n"            # 8. 点击第一个搜索结果
            result += "7️⃣ 点击第一个搜索结果...\n"
            try:
                # 尝试多种可能的搜索结果选择器
                selectors = [
                    ".result.c-container h3 a",
                    ".result h3 a", 
                    "[data-click] h3 a",
                    ".c-container h3 a",
                    "h3 a[href*='www.']"  # 更通用的选择器
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        first_result = await self.toolkit.get_elements(selector)
                        if first_result and len(first_result) > 0:
                            first_result_url = first_result[0].get('href', '')
                            if first_result_url and 'http' in first_result_url:
                                await self.toolkit.navigate_to(first_result_url)
                                result += f"   成功访问第一个结果: {first_result_url}\n"
                                clicked = True
                                break
                    except Exception as e:
                        continue
                
                if not clicked:
                    result += "   ⚠️ 未找到可点击的搜索结果，跳过此步骤\n"
                        
            except Exception as e:
                result += f"   ❌ 点击搜索结果失败: {e}\n"
            
            # 9. 最终截图
            result += "8️⃣ 最终截图...\n"
            final_screenshot = await self.toolkit.screenshot('baidu-final.png')
            result += f"   {final_screenshot}\n\n"
            
            result += "✅ 百度搜索任务执行完成！"
            
        except Exception as e:
            result += f"❌ 百度搜索执行失败: {e}"
        
        return result
    
    async def _execute_github_search(self, task_description: str) -> str:
        """执行GitHub搜索"""
        result = "🔍 执行GitHub搜索任务\n\n"
        
        try:
            # 提取搜索关键词
            import re
            search_match = re.search(r"搜索['\"]?([^'\"]+)['\"]?", task_description)
            if search_match:
                search_term = search_match.group(1)
            else:
                search_term = "langchain"  # 默认搜索词
            
            # 1. 访问GitHub
            result += "1️⃣ 访问GitHub首页...\n"
            nav_result = await self.toolkit.navigate_to("https://github.com")
            result += f"   {nav_result}\n\n"
            
            # 2. 截图
            result += "2️⃣ 截图GitHub首页...\n"
            screenshot_result = await self.toolkit.screenshot()
            result += f"   {screenshot_result}\n\n"
            
            # 3. 填写搜索框
            result += f"3️⃣ 填写搜索框: {search_term}...\n"
            fill_result = await self.toolkit.fill_input("input[placeholder*='Search']", search_term)
            result += f"   {fill_result}\n\n"
            
            # 4. 提交搜索（按回车）
            result += "4️⃣ 提交搜索...\n"
            await self.toolkit.page.keyboard.press("Enter")
            result += "   ✅ 已提交搜索\n\n"
            
            # 5. 等待搜索结果
            result += "5️⃣ 等待搜索结果...\n"
            await asyncio.sleep(3)
            
            # 6. 获取页面信息
            title = await self.toolkit.get_page_title()
            url = await self.toolkit.get_current_url()
            result += f"   页面标题: {title}\n"
            result += f"   当前URL: {url}\n\n"
            
            # 7. 提取搜索结果
            result += "6️⃣ 提取搜索结果...\n"
            text_content = await self.toolkit.extract_text()
            result += f"   搜索结果预览:\n   {text_content[:500]}...\n\n"
            
            # 8. 最终截图
            result += "7️⃣ 最终截图...\n"
            final_screenshot = await self.toolkit.screenshot()
            result += f"   {final_screenshot}\n\n"
            
            result += "✅ GitHub搜索任务执行完成！"
            
        except Exception as e:
            result += f"❌ GitHub搜索执行失败: {e}"
        
        return result
    
    async def _execute_visit_website(self, task_description: str) -> str:
        """执行访问网站任务"""
        result = "🌐 执行网站访问任务\n\n"
        
        try:
            # 提取URL
            import re
            url_match = re.search(r"https?://[^\s]+", task_description)
            if url_match:
                url = url_match.group(0)
            else:
                # 默认URL
                url = "https://httpbin.org/html"
            
            # 1. 访问网站
            result += f"1️⃣ 访问网站: {url}...\n"
            nav_result = await self.toolkit.navigate_to(url)
            result += f"   {nav_result}\n\n"
            
            # 2. 获取页面信息
            result += "2️⃣ 获取页面信息...\n"
            title = await self.toolkit.get_page_title()
            current_url = await self.toolkit.get_current_url()
            result += f"   页面标题: {title}\n"
            result += f"   当前URL: {current_url}\n\n"
            
            # 3. 截图
            result += "3️⃣ 页面截图...\n"
            screenshot_result = await self.toolkit.screenshot('langchain-screenshot.png')
            result += f"   {screenshot_result}\n\n"
            
            # 4. 提取页面内容
            result += "4️⃣ 提取页面内容...\n"
            text_content = await self.toolkit.extract_text()
            result += f"   页面文本:\n   {text_content[:500]}...\n\n"
            
            # 5. 提取链接
            result += "5️⃣ 提取页面链接...\n"
            links = await self.toolkit.extract_links()
            result += f"   找到 {len(links)} 个链接\n"
            if links:
                for i, link in enumerate(links[:5]):  # 显示前5个链接
                    result += f"   {i+1}. {link.get('text', 'N/A')[:30]} -> {link.get('href', 'N/A')}\n"
            result += "\n"
            
            result += "✅ 网站访问任务执行完成！"
            
        except Exception as e:
            result += f"❌ 网站访问执行失败: {e}"
        
        return result
    
    async def _execute_screenshot(self, task_description: str) -> str:
        """执行截图任务"""
        result = "📷 执行截图任务\n\n"
        
        try:
            # 获取当前页面信息
            title = await self.toolkit.get_page_title()
            url = await self.toolkit.get_current_url()
            
            result += f"当前页面: {title}\n"
            result += f"当前URL: {url}\n\n"
            
            # 截图
            screenshot_result = await self.toolkit.screenshot()
            result += f"截图结果: {screenshot_result}\n\n"
            
            result += "✅ 截图任务执行完成！"
            
        except Exception as e:
            result += f"❌ 截图执行失败: {e}"
        
        return result
    
    async def _execute_general_task(self, task_description: str) -> str:
        """执行通用任务"""
        result = f"🔧 执行通用任务: {task_description}\n\n"
        
        try:
            # 访问一个测试页面
            result += "1️⃣ 访问测试页面...\n"
            nav_result = await self.toolkit.navigate_to("https://httpbin.org/html")
            result += f"   {nav_result}\n\n"
            
            # 获取页面信息
            result += "2️⃣ 获取页面信息...\n"
            title = await self.toolkit.get_page_title()
            url = await self.toolkit.get_current_url()
            result += f"   页面标题: {title}\n"
            result += f"   当前URL: {url}\n\n"
            
            # 截图
            result += "3️⃣ 截图...\n"
            screenshot_result = await self.toolkit.screenshot()
            result += f"   {screenshot_result}\n\n"
            
            result += "✅ 通用任务执行完成！"
            
        except Exception as e:
            result += f"❌ 通用任务执行失败: {e}"
        
        return result
    
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
