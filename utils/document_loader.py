"""
文档加载和处理工具
"""

import os
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentLoader:
    """文档加载器"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """加载文本文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        return self.text_splitter.split_documents(documents)
    
    def load_text_content(self, content: str, source: str = "memory") -> List[Document]:
        """加载文本内容"""
        document = Document(page_content=content, metadata={"source": source})
        return self.text_splitter.split_documents([document])
    
    def load_multiple_files(self, file_paths: List[str]) -> List[Document]:
        """加载多个文件"""
        all_documents = []
        for file_path in file_paths:
            try:
                documents = self.load_text_file(file_path)
                all_documents.extend(documents)
                print(f"✅ 已加载文件: {file_path}")
            except Exception as e:
                print(f"❌ 加载文件失败 {file_path}: {e}")
        
        return all_documents


class SimpleVectorStore:
    """简单的向量存储（基于文本匹配）"""
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def add_documents(self, documents: List[Document]):
        """添加文档"""
        self.documents.extend(documents)
        print(f"✅ 已添加 {len(documents)} 个文档片段到向量存储")
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """基于关键词的相似度搜索（简化版）"""
        query_words = set(query.lower().split())
        
        # 计算文档与查询的相似度（基于关键词重叠）
        scored_docs = []
        for doc in self.documents:
            doc_words = set(doc.page_content.lower().split())
            similarity = len(query_words.intersection(doc_words)) / len(query_words.union(doc_words))
            scored_docs.append((similarity, doc))
        
        # 按相似度排序并返回前k个
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:k] if score > 0]
