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
        self.session = None  # 保存复用的会话
        self.tools = None  # 缓存工具列表
        self._session_context = None  # 保存会话上下文管理器
        
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
        """初始化 MCP 客户端和会话"""
        if self._initialized:
            return
            
        try:            # 创建 MCP 客户端
            self.client = MultiServerMCPClient(self.mcp_server_config)
            
            # 使用正确的异步上下文管理器方式创建会话
            self._session_context = self.client.session("playwright")
            self.session = await self._session_context.__aenter__()
            
            # 加载工具
            from langchain_mcp_adapters.tools import load_mcp_tools
            self.tools = await load_mcp_tools(self.session)
            
            print(f"✅ MCP Playwright 工具包初始化成功，可用工具: {len(self.tools)} 个")
            
            # 显示可用工具
            for tool in self.tools:
                print(f"  🔧 {tool.name}: {tool.description}")
            
            self._initialized = True
            
        except Exception as e:
            print(f"❌ MCP Playwright 初始化失败: {e}")
            print("💡 请确保已安装: npm install -g @executeautomation/playwright-mcp-server")
            raise
    
    async def call_tool(self, tool_name: str, **kwargs) -> str:
        """调用指定的 MCP 工具"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # 找到对应的工具
            target_tool = None
            for tool in self.tools:
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
        """关闭 MCP 会话和连接"""
        try:
            # 关闭浏览器
            if self._initialized and self.tools:
                await self.call_tool("playwright_close", random_string="dummy")
              # 关闭会话
            if self._session_context and self.session:
                await self._session_context.__aexit__(None, None, None)
                self.session = None
                self._session_context = None
              # 重置状态
            self._initialized = False
            self.tools = None
            self.session_id = None
            self._session_context = None
            
            print("✅ MCP Playwright 连接已关闭")
            
        except Exception as e:
            print(f"❌ 关闭 MCP 连接时出错: {e}")


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
            # 动态获取可用工具列表
            available_tools = []
            if self.mcp_agent.tools:
                for tool in self.mcp_agent.tools:
                    # 获取工具的参数信息
                    tool_info = f"- {tool.name}: {tool.description}"
                    if hasattr(tool, 'args') and tool.args:
                        # 如果有参数信息，添加参数说明
                        params = []
                        for param_name, param_info in tool.args.items():
                            param_desc = f"{param_name}"
                            if hasattr(param_info, 'description') and param_info.description:
                                param_desc += f" ({param_info.description})"
                            params.append(param_desc)
                        if params:
                            tool_info += f" (参数: {', '.join(params)})"
                    available_tools.append(tool_info)
            
            tools_list = "\n".join(available_tools) if available_tools else "- 无可用工具"
            
            # 使用 LLM 分析任务并生成执行计划
            prompt = f"""
作为一个浏览器自动化专家，请分析以下任务并提供详细的执行步骤：

任务: {task_description}

请提供 JSON 格式的执行计划，包含以下字段：
- steps: 执行步骤列表，每个步骤包含 action 和 params
- description: 任务描述

可用的操作包括（action请直接使用这些工具名称）:
{tools_list}
- wait: 等待指定时间（秒，特殊操作）

例如:
{{
  "description": "访问百度并搜索人工智能",
  "steps": [
    {{"action": "playwright_navigate", "params": {{"url": "https://www.baidu.com"}}}},
    {{"action": "playwright_fill", "params": {{"selector": "#kw", "value": "人工智能"}}}},
    {{"action": "playwright_click", "params": {{"selector": "#su"}}}},
    {{"action": "wait", "params": {{"seconds": 3}}}},
    {{"action": "playwright_screenshot", "params": {{"name": "search_result"}}}}
  ]
}}
"""
            print(f"🔍 请求 prompt: {prompt}")
            response = await self.llm.ainvoke(prompt)
            
            # 解析响应
            try:
                import re
                # 处理response，可能是字符串或者对象
                if hasattr(response, 'content'):
                    response_text = response.content
                else:
                    response_text = str(response)
                
                print(f"🔍 LLM 响应: {response_text}")

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
                    if action == "wait":
                        # 特殊处理等待操作
                        seconds = params.get('seconds', 1)
                        await asyncio.sleep(seconds)
                        result = f"✅ 等待 {seconds} 秒"
                    else:
                        # 直接调用对应的 MCP 工具
                        result = await self.mcp_agent.call_tool(action, **params)
                    
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