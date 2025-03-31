"""
非 OpenAI 协议模型实现
"""
import os
from typing import Optional, Dict, Any

# Google Gemini
import google.generativeai as genai

# Mistral
from mistralai import Mistral

from core.model import BaseModel
from core.registry import register_model
from core.utils import get_input, get_env_var
from ui.console import print_stream, print_conclusion, markdown_stream
from config import non_openai_models_config


# 使用配置自动注册装饰器
def model_config_register(model_key: str):
    """根据配置文件自动注册模型的装饰器"""
    config = non_openai_models_config[model_key]
    return register_model(
        key=config["key"],
        display_name=config["display_name"],
        api_key_env=config["api_key_env"],
        model_id=config["model_id"]
    )


def get_model_config(model_name: str, key: str, default=None):
    """从模型配置中获取参数，如果不存在则从默认配置获取"""
    if key in non_openai_models_config[model_name]:
        return non_openai_models_config[model_name][key]
    elif key in non_openai_models_config["default"]:
        return non_openai_models_config["default"][key]
    return default


# @model_config_register("gemini")
# class Gemini(BaseModel):
#     """Google Gemini模型实现"""
    
#     def _initialize(self) -> None:
#         """初始化Gemini模型"""
#         api_key_env = self._model_config.get("api_key_env")
#         api_key = get_env_var(api_key_env)
        
#         if not api_key:
#             raise ValueError(f"环境变量 {api_key_env} 未设置，无法调用Gemini模型")
        
#         # 配置Gemini
#         genai.configure(api_key=api_key)
        
#         # 创建模型
#         model_id = self._model_config.get("model_id", get_model_config("gemini", "model_id"))
#         self.model = genai.GenerativeModel(model_id)
    
#     def _request_implementation(self, content: str, **kwargs) -> str:
#         """实现Gemini请求"""
#         try:
#             # 根据参数决定是否使用流式输出
#             stream = kwargs.get("stream", get_model_config("gemini", "stream"))
            
#             if stream:
#                 response = self.model.generate_content(content, stream=True)
#                 return markdown_stream(response)
#             else:
#                 response = self.model.generate_content(content)
#                 return print_conclusion(response.text)
                
#         except Exception as e:
#             error_message = f"Gemini模型调用失败: {str(e)}"
#             print(error_message)
#             return error_message


@model_config_register("mistral")
class MistralModel(BaseModel):
    """Mistral模型实现"""
    
    def _initialize(self) -> None:
        """初始化Mistral模型"""
        api_key_env = self._model_config.get("api_key_env")
        api_key = get_env_var(api_key_env)
        
        if not api_key:
            raise ValueError(f"环境变量 {api_key_env} 未设置，无法调用Mistral模型")
        
        # 创建Mistral客户端
        self.client = Mistral(api_key=api_key)
        
        # 设置系统消息
        self.system_message = self._model_config.get(
            "system_message", 
            get_model_config("mistral", "system_message")
        )
    
    def _request_implementation(self, content: str, **kwargs) -> str:
        """实现Mistral请求"""
        try:
            # 准备消息
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            # 添加历史消息
            history_limit = kwargs.get("history_limit", get_model_config("mistral", "history_limit", 10))
            if history_limit > 0 and len(self.history) > 0:
                # 添加最近的历史记录（不超过限制）
                history_to_add = self.history[-history_limit*2:] if history_limit > 0 else []
                for msg in history_to_add:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            # 添加当前消息
            messages.append({"role": "user", "content": content})
            
            # 设置参数
            model_id = self._model_config.get("model_id", get_model_config("mistral", "model_id"))
            stream = kwargs.get("stream", get_model_config("mistral", "stream"))
            
            if stream:
                # 流式请求
                response_stream = self.client.chat_stream(
                    model=model_id,
                    messages=messages
                )
                return print_stream(response_stream)
            else:
                # 非流式请求
                response = self.client.chat.complete(
                    model=model_id,
                    messages=messages
                )
                content = response.choices[0].message.content
                return print_conclusion(content)
                
        except Exception as e:
            error_message = f"Mistral模型调用失败: {str(e)}"
            print(error_message)
            return error_message 