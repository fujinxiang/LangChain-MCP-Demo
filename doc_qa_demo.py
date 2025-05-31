"""
LangChain + 硅基流动文档问答 Demo
基于文档内容的问答应用
"""

import sys
import os
from utils.llm_wrapper import create_llm
from utils.document_loader import DocumentLoader, SimpleVectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class DocumentQA:
    """文档问答系统"""
    
    def __init__(self):
        self.llm = create_llm()
        self.doc_loader = DocumentLoader()
        self.vector_store = SimpleVectorStore()
        
        # 创建问答提示模板
        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""基于以下上下文信息，回答用户的问题。如果上下文中没有相关信息，请说明无法从提供的文档中找到答案。

上下文信息:
{context}

用户问题: {question}

回答:"""
        )
        
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
    
    def load_documents(self, file_paths_or_content):
        """加载文档"""
        if isinstance(file_paths_or_content, str):
            if os.path.exists(file_paths_or_content):
                # 文件路径
                documents = self.doc_loader.load_text_file(file_paths_or_content)
            else:
                # 文本内容
                documents = self.doc_loader.load_text_content(file_paths_or_content)
        elif isinstance(file_paths_or_content, list):
            # 多个文件路径
            documents = self.doc_loader.load_multiple_files(file_paths_or_content)
        else:
            raise ValueError("不支持的输入类型")
        
        self.vector_store.add_documents(documents)
        return len(documents)
    
    def query(self, question: str) -> str:
        """查询文档"""
        # 搜索相关文档
        relevant_docs = self.vector_store.similarity_search(question, k=3)
        
        if not relevant_docs:
            return "抱歉，我在提供的文档中没有找到与您问题相关的信息。"
        
        # 构建上下文
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # 生成回答
        response = self.qa_chain.run(context=context, question=question)
        return response


def demo_with_sample_text():
    """使用示例文本进行演示"""
    print("📄 使用示例文档进行演示")
    print("-" * 30)
    
    # 示例文档内容
    sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。

机器学习是人工智能的一个子领域，它使计算机能够在没有明确编程的情况下学习。机器学习算法通过分析数据来识别模式，并使用这些模式来做出预测或决策。

深度学习是机器学习的一个子集，它使用多层神经网络来模拟人脑的工作方式。深度学习在图像识别、语音识别和自然语言处理等领域取得了重大突破。

自然语言处理（NLP）是人工智能的一个领域，专注于使计算机能够理解、解释和生成人类语言。NLP 技术广泛应用于聊天机器人、语音助手和机器翻译等应用中。

LangChain 是一个用于构建基于大语言模型的应用程序的框架。它提供了丰富的工具和组件，帮助开发者更容易地集成和使用各种 AI 模型。
"""
    
    qa_system = DocumentQA()
    doc_count = qa_system.load_documents(sample_text)
    print(f"✅ 已加载 {doc_count} 个文档片段\n")
    
    # 示例问题
    sample_questions = [
        "什么是人工智能？",
        "机器学习和深度学习的关系是什么？",
        "LangChain 是什么？",
        "NLP 有哪些应用？"
    ]
    
    print("🤖 示例问答:")
    for i, question in enumerate(sample_questions, 1):
        print(f"\n{i}. 问题: {question}")
        answer = qa_system.query(question)
        print(f"   回答: {answer}")
    
    return qa_system


def interactive_mode(qa_system):
    """交互模式"""
    print("\n" + "=" * 50)
    print("💬 进入交互问答模式")
    print("您可以询问关于已加载文档的任何问题")
    print("输入 'quit' 或 'exit' 退出\n")
    
    while True:
        try:
            user_question = input("👤 您的问题: ").strip()
            
            if user_question.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
            
            if not user_question:
                continue
            
            print("🤖 AI: ", end="", flush=True)
            answer = qa_system.query(user_question)
            print(answer)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            print()


def main():
    """主函数"""
    print("🚀 LangChain + 硅基流动文档问答 Demo")
    print("=" * 50)
    
    try:
        # 演示模式
        qa_system = demo_with_sample_text()
        
        # 交互模式
        interactive_mode(qa_system)
    
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("请检查配置文件和 API Key 设置")
        sys.exit(1)


if __name__ == "__main__":
    main()
