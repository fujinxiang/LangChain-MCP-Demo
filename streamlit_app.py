"""
LangChain + 硅基流动 Streamlit Web 应用
提供美观的 Web 界面进行聊天和文档问答
"""

import streamlit as st
import sys
import os
from utils.llm_wrapper import create_llm
from utils.document_loader import DocumentLoader, SimpleVectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


@st.cache_resource
def init_llm():
    """初始化 LLM（缓存）"""
    try:
        return create_llm()
    except Exception as e:
        st.error(f"LLM 初始化失败: {e}")
        st.stop()


@st.cache_resource
def init_qa_system():
    """初始化文档问答系统（缓存）"""
    llm = init_llm()
    doc_loader = DocumentLoader()
    vector_store = SimpleVectorStore()
    
    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""基于以下上下文信息，回答用户的问题。如果上下文中没有相关信息，请说明无法从提供的文档中找到答案。

上下文信息:
{context}

用户问题: {question}

回答:"""
    )
    
    qa_chain = LLMChain(llm=llm, prompt=qa_prompt)
    
    return {
        'llm': llm,
        'doc_loader': doc_loader,
        'vector_store': vector_store,
        'qa_chain': qa_chain
    }


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
                    
                    chain = LLMChain(llm=llm, prompt=prompt_template)
                    response = chain.run(question=prompt)
                    
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


def doc_qa_page():
    """文档问答页面"""
    st.header("📄 文档问答系统")
    st.write("上传文档或输入文本，然后对文档内容进行问答！")
    
    qa_system = init_qa_system()
    
    # 初始化文档存储
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False
        st.session_state.doc_count = 0
    
    # 文档输入区域
    st.subheader("📝 文档输入")
    
    input_method = st.radio(
        "选择输入方式:",
        ["直接输入文本", "上传文本文件"],
        horizontal=True
    )
    
    documents_to_load = []
    
    if input_method == "直接输入文本":
        text_input = st.text_area(
            "请输入您的文档内容:",
            height=200,
            placeholder="在这里粘贴您的文档内容..."
        )
        if text_input.strip():
            documents_to_load.append(("直接输入", text_input))
    
    else:
        uploaded_files = st.file_uploader(
            "选择文本文件",
            type=['txt'],
            accept_multiple_files=True
        )
        
        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode('utf-8')
            documents_to_load.append((uploaded_file.name, content))
    
    # 加载文档按钮
    if st.button("📚 加载文档", disabled=len(documents_to_load) == 0):
        with st.spinner("正在加载文档..."):
            try:
                total_chunks = 0
                for source, content in documents_to_load:
                    documents = qa_system['doc_loader'].load_text_content(content, source)
                    qa_system['vector_store'].add_documents(documents)
                    total_chunks += len(documents)
                
                st.session_state.documents_loaded = True
                st.session_state.doc_count = total_chunks
                st.success(f"✅ 成功加载 {total_chunks} 个文档片段！")
                
            except Exception as e:
                st.error(f"❌ 文档加载失败: {e}")
    
    # 显示文档状态
    if st.session_state.documents_loaded:
        st.info(f"📊 当前已加载 {st.session_state.doc_count} 个文档片段")
    
    # 问答区域
    st.subheader("❓ 文档问答")
    
    if not st.session_state.documents_loaded:
        st.warning("请先加载文档后再进行问答")
    else:
        # 初始化问答历史
        if "qa_messages" not in st.session_state:
            st.session_state.qa_messages = []
        
        # 显示问答历史
        for message in st.session_state.qa_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 问答输入
        if question := st.chat_input("请针对文档内容提问..."):
            # 添加用户问题
            st.session_state.qa_messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            
            # 获取 AI 回答
            with st.chat_message("assistant"):
                with st.spinner("AI 正在分析文档..."):
                    try:
                        # 搜索相关文档
                        relevant_docs = qa_system['vector_store'].similarity_search(question, k=3)
                        
                        if not relevant_docs:
                            answer = "抱歉，我在提供的文档中没有找到与您问题相关的信息。"
                        else:
                            # 构建上下文
                            context = "\n\n".join([doc.page_content for doc in relevant_docs])
                            
                            # 生成回答
                            answer = qa_system['qa_chain'].run(context=context, question=question)
                        
                        st.markdown(answer)
                        
                        # 添加 AI 回答到历史
                        st.session_state.qa_messages.append({"role": "assistant", "content": answer})
                        
                    except Exception as e:
                        error_msg = f"抱歉，发生了错误: {e}"
                        st.error(error_msg)
                        st.session_state.qa_messages.append({"role": "assistant", "content": error_msg})
        
        # 清除问答历史按钮
        if st.button("🗑️ 清除问答历史"):
            st.session_state.qa_messages = []
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
        st.write("选择功能模式:")
        
        page = st.radio(
            "功能模式",
            ["💬 AI 聊天", "📄 文档问答"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.subheader("ℹ️ 关于")
        st.write("""
        这是一个基于 LangChain 框架和硅基流动 API 构建的演示应用。
        
        **功能特性:**
        - AI 智能对话
        - 文档内容问答
        - 流畅的 Web 界面
        
        **技术栈:**
        - LangChain
        - 硅基流动 API
        - Streamlit
        """)
        
        st.markdown("---")
        st.write("💡 **提示**: 确保已正确配置 API Key")
    
    # 主内容区域
    if page == "💬 AI 聊天":
        chat_page()
    elif page == "📄 文档问答":
        doc_qa_page()


if __name__ == "__main__":
    main()
