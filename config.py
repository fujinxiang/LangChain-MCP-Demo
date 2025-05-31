import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # 硅基流动 API 配置
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
    SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    
    # 模型配置
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.SILICONFLOW_API_KEY:
            raise ValueError("请设置 SILICONFLOW_API_KEY 环境变量")
        
        print(f"✅ 配置加载成功")
        print(f"API 基础 URL: {cls.SILICONFLOW_BASE_URL}")
        print(f"默认模型: {cls.DEFAULT_MODEL}")
        print(f"温度: {cls.TEMPERATURE}")
        print(f"最大令牌: {cls.MAX_TOKENS}")

# 创建配置实例
config = Config()
