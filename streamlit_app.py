"""
LangChain + 硅基流动 Streamlit Web 应用
提供美观的 Web 界面进行AI聊天
"""

import streamlit as st
import sys
import os
from utils.llm_wrapper import create_llm
from langchain.prompts import PromptTemplate


@st.cache_resource
def init_llm():
    """初始化 LLM（缓存）"""
    try:
        return create_llm()
    except Exception as e:
        st.error(f"LLM 初始化失败: {e}")
        st.stop()



def chat_page():
    """聊天页面"""
    st.header("💬 AI 聊天助手")
    st.write("与 AI 助手进行对话，体验 LangChain + 硅基流动的强大功能！")
    
    # 初始化聊天历史
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # 显示聊天历史
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 聊天输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 获取 AI 回复
        with st.chat_message("assistant"):
            with st.spinner("AI 正在思考..."):
                try:
                    llm = init_llm()
                    
                    # 创建提示模板
                    prompt_template = PromptTemplate(
                        input_variables=["question"],
                        template="""你是一个有用的AI助手。请回答以下问题：

问题: {question}

回答:"""
                    )                    
                    chain = prompt_template | llm
                    response = chain.invoke({"question": prompt})
                    
                    st.markdown(response)
                    
                    # 添加 AI 回复到历史
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"抱歉，发生了错误: {e}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    
    # 清除聊天历史按钮
    if st.button("🗑️ 清除聊天历史"):
        st.session_state.chat_messages = []
        st.rerun()




def main():
    """主函数"""
    st.set_page_config(
        page_title="LangChain + 硅基流动 Demo",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏
    with st.sidebar:
        st.title("🤖 LangChain + 硅基流动")
        
        st.markdown("---")
        st.subheader("ℹ️ 关于")
        st.write("""
        这是一个基于 LangChain 框架和硅基流动 API 构建的演示应用。
        
        **功能特性:**
        - AI 智能对话
        - 流畅的 Web 界面
        
        **技术栈:**
        - LangChain
        - 硅基流动 API
        - Streamlit
        """)
        
        st.markdown("---")
        st.write("💡 **提示**: 确保已正确配置 API Key")
    
    # 主内容区域 - 直接显示聊天页面
    chat_page()


if __name__ == "__main__":
    main()
