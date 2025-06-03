"""
使用 LangChain MCP Adapters 接入 Playwright MCP 服务器
提供基于 MCP 协议的浏览器自动化功能
"""

import asyncio
import json
from typing import Optional, Dict, Any, List, Union
from langchain_mcp_adapters.client import MultiServerMCPClient


class MCPPlaywrightAgent:
    """基于 MCP 的 Playwright 浏览器代理"""
    
    def __init__(self, mcp_server_config: Optional[Dict[str, Any]] = None):
        """
        初始化 MCP Playwright 代理
        
        Args:
            mcp_server_config: MCP 服务器配置，如果为 None 则使用默认配置
        """
        self.mcp_server_config = mcp_server_config or self._get_default_config()
        self.client: Optional[MultiServerMCPClient] = None
        self._initialized = False
        self.session_id: Optional[str] = None
        
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认的 MCP 服务器配置"""
        return {
            "playwright": {
                "command": "npx",
                "args": ["@executeautomation/playwright-mcp-server"],
                "transport": "stdio"
            }
        }
    
    async def initialize(self):
        """初始化 MCP 客户端"""
        if self._initialized:
            return
            
        try:
            # 创建 MCP 客户端
            self.client = MultiServerMCPClient(self.mcp_server_config)
            
            # 获取可用工具
            tools = await self.client.get_tools()
            print(f"✅ MCP Playwright 工具包初始化成功，可用工具: {len(tools)} 个")
            
            # 显示可用工具
            for tool in tools:
                print(f"  🔧 {tool.name}: {tool.description}")
            
            self._initialized = True
            
        except Exception as e:
            print(f"❌ MCP Playwright 初始化失败: {e}")
            print("💡 请确保已安装: npm install -g @executeautomation/playwright-mcp-server")
            raise
    
    async def _call_tool(self, tool_name: str, **kwargs) -> str:
        """调用指定的 MCP 工具"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # 获取所有工具
            tools = await self.client.get_tools()
            
            # 找到对应的工具
            target_tool = None
            for tool in tools:
                if tool.name == tool_name:
                    target_tool = tool
                    break
            
            if not target_tool:
                return f"❌ 工具 {tool_name} 未找到"
            
            # 调用工具
            result = await target_tool.ainvoke(kwargs)
            return str(result)
            
        except Exception as e:
            return f"❌ 调用工具 {tool_name} 失败: {e}"
    
    async def navigate_to(self, url: str, **kwargs) -> str:
        """导航到指定 URL"""
        try:
            result = await self._call_tool("playwright_navigate", url=url, **kwargs)
            return f"✅ 成功导航到: {url}\n{result}"
        except Exception as e:
            return f"❌ 导航失败: {e}"
    
    async def take_screenshot(self, name: str, **kwargs) -> str:
        """截取屏幕截图"""
        try:
            result = await self._call_tool("playwright_screenshot", name=name, **kwargs)
            return f"✅ 截图完成: {name}\n{result}"
        except Exception as e:
            return f"❌ 截图失败: {e}"
    
    async def click_element(self, selector: str) -> str:
        """点击页面元素"""
        try:
            result = await self._call_tool("playwright_click", selector=selector)
            return f"✅ 成功点击元素: {selector}\n{result}"
        except Exception as e:
            return f"❌ 点击失败: {e}"
    
    async def fill_input(self, selector: str, value: str) -> str:
        """填写输入框"""
        try:
            result = await self._call_tool("playwright_fill", selector=selector, value=value)
            return f"✅ 成功填写: {selector} = {value}\n{result}"
        except Exception as e:
            return f"❌ 填写失败: {e}"
    
    async def hover_element(self, selector: str) -> str:
        """悬停在页面元素上"""
        try:
            result = await self._call_tool("playwright_hover", selector=selector)
            return f"✅ 成功悬停: {selector}\n{result}"
        except Exception as e:
            return f"❌ 悬停失败: {e}"
    
    async def select_option(self, selector: str, value: str) -> str:
        """选择下拉框选项"""
        try:
            result = await self._call_tool("playwright_select", selector=selector, value=value)
            return f"✅ 成功选择: {selector} = {value}\n{result}"
        except Exception as e:
            return f"❌ 选择失败: {e}"
    
    async def execute_javascript(self, script: str) -> str:
        """执行 JavaScript 代码"""
        try:
            result = await self._call_tool("playwright_evaluate", script=script)
            return f"✅ JavaScript 执行成功:\n{result}"
        except Exception as e:
            return f"❌ JavaScript 执行失败: {e}"
    
    async def get_page_text(self) -> str:
        """获取页面可见文本"""
        try:
            result = await self._call_tool("playwright_get_visible_text", random_string="dummy")
            return result
        except Exception as e:
            return f"❌ 获取页面文本失败: {e}"
    
    async def get_page_html(self) -> str:
        """获取页面 HTML"""
        try:
            result = await self._call_tool("playwright_get_visible_html", random_string="dummy")
            return result
        except Exception as e:
            return f"❌ 获取页面 HTML 失败: {e}"
    
    async def go_back(self) -> str:
        """浏览器后退"""
        try:
            result = await self._call_tool("playwright_go_back", random_string="dummy")
            return f"✅ 后退成功\n{result}"
        except Exception as e:
            return f"❌ 后退失败: {e}"
    
    async def go_forward(self) -> str:
        """浏览器前进"""
        try:
            result = await self._call_tool("playwright_go_forward", random_string="dummy")
            return f"✅ 前进成功\n{result}"
        except Exception as e:
            return f"❌ 前进失败: {e}"
    
    async def press_key(self, key: str, selector: Optional[str] = None) -> str:
        """按键操作"""
        try:
            params = {"key": key}
            if selector:
                params["selector"] = selector
                
            result = await self._call_tool("playwright_press_key", **params)
            return f"✅ 按键成功: {key}\n{result}"
        except Exception as e:
            return f"❌ 按键失败: {e}"
    
    async def drag_and_drop(self, source_selector: str, target_selector: str) -> str:
        """拖拽操作"""
        try:
            result = await self._call_tool(
                "playwright_drag",
                sourceSelector=source_selector,
                targetSelector=target_selector
            )
            return f"✅ 拖拽成功: {source_selector} -> {target_selector}\n{result}"
        except Exception as e:
            return f"❌ 拖拽失败: {e}"
    
    async def save_as_pdf(self, output_path: str, filename: str = "page.pdf", **kwargs) -> str:
        """保存页面为 PDF"""
        try:
            result = await self._call_tool(
                "playwright_save_as_pdf",
                outputPath=output_path,
                filename=filename,
                **kwargs
            )
            return f"✅ PDF 保存成功: {filename}\n{result}"
        except Exception as e:
            return f"❌ PDF 保存失败: {e}"
    
    async def get_console_logs(self, log_type: str = "all", limit: Optional[int] = None) -> str:
        """获取控制台日志"""
        try:
            params = {"type": log_type}
            if limit:
                params["limit"] = limit
                
            result = await self._call_tool("playwright_console_logs", **params)
            return f"📋 控制台日志:\n{result}"
        except Exception as e:
            return f"❌ 获取控制台日志失败: {e}"
    
    async def start_codegen_session(self, output_path: str, test_name_prefix: str = "GeneratedTest") -> str:
        """开始代码生成会话"""
        try:
            result = await self._call_tool(
                "playwright_start_codegen_session",
                options={
                    "outputPath": output_path,
                    "testNamePrefix": test_name_prefix,
                    "includeComments": True
                }
            )
            
            # 从结果中提取会话 ID（如果可能）
            if isinstance(result, dict) and "sessionId" in result:
                self.session_id = result["sessionId"]
            
            return f"✅ 代码生成会话已开始\n{result}"
        except Exception as e:
            return f"❌ 开始代码生成会话失败: {e}"
    
    async def end_codegen_session(self) -> str:
        """结束代码生成会话"""
        if not self.session_id:
            return "❌ 没有活跃的代码生成会话"
        
        try:
            result = await self._call_tool("playwright_end_codegen_session", sessionId=self.session_id)
            self.session_id = None
            return f"✅ 代码生成会话已结束\n{result}"
        except Exception as e:
            return f"❌ 结束代码生成会话失败: {e}"
    
    async def get_available_tools(self) -> List[str]:
        """获取可用工具列表"""
        if not self._initialized:
            await self.initialize()
        
        try:
            tools = await self.client.get_tools()
            return [tool.name for tool in tools]
        except Exception as e:
            print(f"❌ 获取工具列表失败: {e}")
            return []
    
    async def close(self):
        """关闭 MCP 连接"""
        try:
            if self.client:
                await self._call_tool("playwright_close", random_string="dummy")
                print("✅ MCP Playwright 连接已关闭")
        except Exception as e:
            print(f"❌ 关闭 MCP 连接失败: {e}")


class MCPSmartBrowserAgent:
    """智能的 MCP 浏览器代理，支持复杂任务"""
    
    def __init__(self, llm, mcp_server_config: Optional[Dict[str, Any]] = None):
        """
        初始化智能浏览器代理
        
        Args:
            llm: LangChain 语言模型实例
            mcp_server_config: MCP 服务器配置
        """
        self.llm = llm
        self.mcp_agent = MCPPlaywrightAgent(mcp_server_config)
        self._initialized = False
    
    async def initialize(self):
        """初始化代理"""
        if not self._initialized:
            await self.mcp_agent.initialize()
            self._initialized = True
    
    async def execute_smart_task(self, task_description: str) -> str:
        """执行智能任务"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # 使用 LLM 分析任务并生成执行计划
            prompt = f"""
作为一个浏览器自动化专家，请分析以下任务并提供详细的执行步骤：

任务: {task_description}

请提供 JSON 格式的执行计划，包含以下字段：
- steps: 执行步骤列表，每个步骤包含 action 和 params
- description: 任务描述

可用的操作包括:
- navigate_to: 导航到 URL
- click_element: 点击元素
- fill_input: 填写输入框
- take_screenshot: 截图
- execute_javascript: 执行 JS
- get_page_text: 获取页面文本
- wait: 等待指定时间（秒）

例如:
{{
  "description": "访问百度并搜索人工智能",
  "steps": [
    {{"action": "navigate_to", "params": {{"url": "https://www.baidu.com"}}}},
    {{"action": "fill_input", "params": {{"selector": "#kw", "value": "人工智能"}}}},
    {{"action": "click_element", "params": {{"selector": "#su"}}}},
    {{"action": "wait", "params": {{"seconds": 3}}}},
    {{"action": "take_screenshot", "params": {{"name": "search_result"}}}}
  ]
}}
"""
            
            response = await self.llm.ainvoke(prompt)
            
            # 解析响应 - 修复：直接使用response而不是response.content
            try:
                import re
                # 处理response，可能是字符串或者对象
                if hasattr(response, 'content'):
                    response_text = response.content
                else:
                    response_text = str(response)
                
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                else:
                    raise ValueError("未找到有效的 JSON 响应")
            except (json.JSONDecodeError, ValueError) as e:
                return f"❌ 任务规划解析失败: {e}\n原始响应: {response_text if 'response_text' in locals() else str(response)}"
            
            # 执行计划
            results = []
            results.append(f"🎯 任务: {plan.get('description', task_description)}")
            results.append("=" * 50)
            
            for i, step in enumerate(plan.get('steps', []), 1):
                action = step.get('action')
                params = step.get('params', {})
                
                results.append(f"📋 步骤 {i}: {action}")
                
                try:
                    if action == "navigate_to":
                        result = await self.mcp_agent.navigate_to(**params)
                    elif action == "click_element":
                        result = await self.mcp_agent.click_element(**params)
                    elif action == "fill_input":
                        result = await self.mcp_agent.fill_input(**params)
                    elif action == "take_screenshot":
                        result = await self.mcp_agent.take_screenshot(**params)
                    elif action == "execute_javascript":
                        result = await self.mcp_agent.execute_javascript(**params)
                    elif action == "get_page_text":
                        result = await self.mcp_agent.get_page_text()
                    elif action == "wait":
                        seconds = params.get('seconds', 1)
                        await asyncio.sleep(seconds)
                        result = f"✅ 等待 {seconds} 秒"
                    else:
                        result = f"❌ 未知操作: {action}"
                    
                    results.append(result)
                    
                except Exception as e:
                    error_msg = f"❌ 步骤 {i} 执行失败: {e}"
                    results.append(error_msg)
                
                results.append("-" * 30)
            
            return "\n".join(results)
            
        except Exception as e:
            return f"❌ 智能任务执行失败: {e}"
    
    async def close(self):
        """关闭代理"""
        await self.mcp_agent.close()


def create_mcp_browser_agent(llm=None, mcp_server_config: Optional[Dict[str, Any]] = None):
    """
    创建 MCP 浏览器代理
    
    Args:
        llm: LangChain 语言模型实例（可选，如果提供则返回智能代理）
        mcp_server_config: MCP 服务器配置
    
    Returns:
        MCPPlaywrightAgent 或 MCPSmartBrowserAgent 实例
    """
    if llm:
        return MCPSmartBrowserAgent(llm, mcp_server_config)
    else:
        return MCPPlaywrightAgent(mcp_server_config) 