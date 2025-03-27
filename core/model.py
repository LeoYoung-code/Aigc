"""
模型基类和接口定义
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class ModelInterface(ABC):
    """模型接口，定义所有模型必须实现的方法"""
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化模型"""
        pass
    
    @abstractmethod
    async def request_async(self, content: str, **kwargs) -> str:
        """异步请求模型响应"""
        pass
    
    @abstractmethod
    def req_model(self, content: Optional[str] = None, **kwargs) -> str:
        """同步请求模型响应"""
        pass


class BaseModel(ModelInterface):
    """
    模型基类，提供基础功能实现
    
    子类需要实现:
    - _initialize()：模型初始化逻辑
    - _request_implementation()：实际的请求实现
    """
    
    # 模型元数据（由注册装饰器填充）
    _model_key: str = None
    _model_config: Dict[str, Any] = None
    
    def __init__(self):
        self.initialized = False
        self.history: List[Dict[str, str]] = []  # 聊天历史
    
    def initialize(self) -> None:
        """
        初始化模型
        """
        if not self.initialized:
            self._initialize()
            self.initialized = True
            # print(f"正在使用{self._model_config.get('display_name', '未知模型')}")
    
    def _initialize(self) -> None:
        """
        初始化模型实现
        子类应该重写此方法实现具体的初始化逻辑
        """
        pass
    
    async def request_async(self, content: str, **kwargs) -> str:
        """
        异步请求模型响应
        
        Args:
            content: 用户输入内容
            **kwargs: 其他参数
            
        Returns:
            模型响应
        """
        # 默认实现调用同步方法，子类可重写提供真正的异步实现
        return self.req_model(content, **kwargs)
    
    def req_model(self, content: Optional[str] = None, **kwargs) -> str:
        """
        请求模型响应
        
        Args:
            content: 用户输入内容，为None时从标准输入获取
            **kwargs: 其他参数
            
        Returns:
            模型响应
        """
        from core.utils import get_input
        
        # 如果没有传入内容，从标准输入获取
        if content is None:
            content = get_input(kwargs.get("conclusion"))
        
        # 添加到历史记录
        if content:
            self.history.append({"role": "user", "content": content})
        
        # 调用实际实现
        response = self._request_implementation(content, **kwargs)
        
        # 添加响应到历史
        if response:
            self.history.append({"role": "assistant", "content": response})
            
        return response
    
    def _request_implementation(self, content: str, **kwargs) -> str:
        """
        实际的请求实现
        子类应该重写此方法实现具体的请求逻辑
        
        Args:
            content: 用户输入内容
            **kwargs: 其他参数
            
        Returns:
            模型响应
        """
        raise NotImplementedError("子类必须实现_request_implementation方法")
    
    def clear_history(self) -> None:
        """清除聊天历史"""
        self.history = []
    
    @property
    def model_key(self) -> str:
        """获取模型标识符"""
        return self._model_key
    
    @property
    def model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return self._model_config 