"""
非 OpenAI 协议模型实现
"""
import os
from typing import Optional

# Google Gemini
import google.generativeai as genai

# Mistral
from mistralai import Mistral

from core.model import BaseModel
from core.registry import register_model
from core.utils import get_input, get_env_var
from ui.console import print_stream, print_conclusion, markdown_stream


@register_model(
    key="g", 
    display_name="Google Gemini模型",
    api_key_env="GOOGLE_API_KEY",
    model_id="gemini-2.5-pro-exp-03-25"
)
class Gemini(BaseModel):
    """Google Gemini模型实现"""
    
    def _initialize(self) -> None:
        """初始化Gemini模型"""
        api_key_env = self._model_config.get("api_key_env")
        api_key = get_env_var(api_key_env)
        
        if not api_key:
            raise ValueError(f"环境变量 {api_key_env} 未设置，无法调用Gemini模型")
        
        # 配置Gemini
        genai.configure(api_key=api_key)
        
        # 创建模型
        model_id = self._model_config.get("model_id", "gemini-pro")
        self.model = genai.GenerativeModel(model_id)
    
    def _request_implementation(self, content: str, **kwargs) -> str:
        """实现Gemini请求"""
        try:
            # 根据参数决定是否使用流式输出
            stream = kwargs.get("stream", True)
            
            if stream:
                response = self.model.generate_content(content, stream=True)
                return markdown_stream(response)
            else:
                response = self.model.generate_content(content)
                return print_conclusion(response.text)
                
        except Exception as e:
            error_message = f"Gemini模型调用失败: {str(e)}"
            print(error_message)
            return error_message


@register_model(
    key="m", 
    display_name="Mistral大模型",
    api_key_env="MISTRAL_API_KEY",
    model_id="mistral-large-latest"
)
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
            "你是迪普，是人工智能助手,用中文详细的回答每一个问题。"
        )
    
    def _request_implementation(self, content: str, **kwargs) -> str:
        """实现Mistral请求"""
        try:
            # 准备消息
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            # 添加历史消息
            history_limit = kwargs.get("history_limit", 10)
            if history_limit > 0 and len(self.history) > 0:
                # 添加最近的历史记录（不超过限制）
                history_to_add = self.history[-history_limit*2:] if history_limit > 0 else []
                for msg in history_to_add:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            # 添加当前消息
            messages.append({"role": "user", "content": content})
            
            # 设置参数
            model_id = self._model_config.get("model_id", "mistral-large-latest")
            stream = kwargs.get("stream", False)
            
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