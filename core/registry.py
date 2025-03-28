"""
模型注册中心 - 提供模型注册和管理功能
"""
from typing import Dict, Type, Any, Optional, Callable, ClassVar
import inspect
import os
from functools import wraps


class ModelRegistry:
    """模型注册中心类，管理所有已注册的模型"""
    
    _instance = None  # 单例实例
    _models: Dict[str, Type] = {}  # 模型类映射
    _configs: Dict[str, Dict[str, Any]] = {}  # 模型配置映射
    
    def __new__(cls):
        """实现单例模式"""
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, key: str, display_name: str, **config) -> Callable:
        """
        注册模型装饰器
        
        Args:
            key: 模型的唯一标识符
            display_name: 模型显示名称
            **config: 模型配置参数
            
        Returns:
            装饰器函数
        """
        def decorator(model_cls):
            if key in cls._models:
                raise ValueError(f"模型标识符 '{key}' 已被注册")
                
            # 添加模型类
            cls._models[key] = model_cls
            
            # 存储基本配置
            model_config = {
                "display_name": display_name
            }
            
            # 添加OpenAI兼容配置（如果有）
            openai_config = {}
            if hasattr(model_cls, "openai_config"):
                openai_config = getattr(model_cls, "openai_config")
            elif "openai_config" in config:
                openai_config = config.pop("openai_config")
                
            if openai_config:
                model_config["openai_compatible"] = True
                model_config["openai_config"] = openai_config
            
            # 合并其他配置参数
            model_config.update(config)
            
            # 存储配置
            cls._configs[key] = model_config
            
            # 记录元数据到类中（方便访问）
            setattr(model_cls, "_model_key", key)
            setattr(model_cls, "_model_config", model_config)
            
            return model_cls
        
        return decorator
    
    @classmethod
    def get_model_class(cls, key: str) -> Optional[Type]:
        """获取模型类"""
        return cls._models.get(key)
    
    @classmethod
    def get_model_config(cls, key: str) -> Optional[Dict[str, Any]]:
        """获取模型配置"""
        return cls._configs.get(key)
    
    @classmethod
    def create_instance(cls, key: str) -> Any:
        """创建模型实例"""
        model_cls = cls.get_model_class(key)
        if not model_cls:
            raise ValueError(f"未知模型: {key}")
        return model_cls()
    
    @classmethod
    def list_models(cls) -> Dict[str, Dict[str, Any]]:
        """列出所有已注册模型及其配置"""
        return {k: {"class": v.__name__, "config": cls._configs.get(k, {})} 
                for k, v in cls._models.items()}
    
    @classmethod
    def get_openai_compatible_models(cls) -> Dict[str, Dict[str, Any]]:
        """获取所有支持OpenAI协议的模型配置"""
        return {k: cfg["openai_config"] 
                for k, cfg in cls._configs.items() 
                if cfg.get("openai_compatible", False)}


# 简化的注册装饰器
def register_model(key: str, display_name: str, **kwargs):
    """
    注册模型装饰器（简化版）
    
    Args:
        key: 模型标识符
        display_name: 显示名称
        **kwargs: 其他配置参数
    """
    return ModelRegistry.register(key, display_name, **kwargs) 