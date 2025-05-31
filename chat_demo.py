"""
LangChain + 硅基流动聊天 Demo
简单的对话式问答应用
"""

import sys
from utils.llm_wrapper import create_llm
from langchain.prompts import PromptTemplate


def main():
    """主函数"""
    print("🚀 LangChain + 硅基流动聊天 Demo")
    print("=" * 50)
    
    try:
        # 创建 LLM 实例
        llm = create_llm()
        print("✅ LLM 初始化成功\n")
        
        # 创建提示模板
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="""你是一个有用的AI助手。请回答以下问题：

问题: {question}

回答:"""
        )
          # 创建链（使用新的 RunnableSequence 语法）
        chain = prompt_template | llm
        
        print("💬 开始聊天（输入 'quit' 或 'exit' 退出）\n")
        
        while True:
            try:
                # 获取用户输入
                user_input = input("👤 您: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 AI: ", end="", flush=True)
                  # 调用链获取回答
                response = chain.invoke({"question": user_input})
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                print()
    
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("请检查配置文件和 API Key 设置")
        sys.exit(1)


if __name__ == "__main__":
    main()
