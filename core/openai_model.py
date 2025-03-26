"""
OpenAI兼容模型基类
"""
import os
from typing import Dict, Any, Optional, Union, List
import asyncio

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from core.model import BaseModel
from core.utils import get_env_var
from ui.console import Console, print_stream, print_conclusion


class OpenAICompatibleModel(BaseModel):
    """
    OpenAI兼容模型基类，支持所有使用OpenAI API协议的模型
    
    子类可以通过两种方式设置OpenAI兼容参数:
    1. 设置类属性 openai_config
    2. 通过装饰器参数传递
    """
    
    # OpenAI配置，子类可以覆盖
    openai_config = None
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.async_client = None
    
    def _initialize(self) -> None:
        """初始化OpenAI客户端"""
        if not self._model_config or not self._model_config.get("openai_config"):
            raise ValueError("缺少OpenAI配置，请确保已通过装饰器设置")
        
        openai_config = self._model_config["openai_config"]
        
        # 创建客户端参数
        client_args = {}
        
        # 设置API基础URL
        if openai_config.get("base_url"):
            client_args["base_url"] = openai_config["base_url"]
        
        # 设置API密钥
        api_key_env = openai_config.get("api_key_env")
        if api_key_env:
            api_key = get_env_var(api_key_env)
            if not api_key:
                raise ValueError(f"环境变量 {api_key_env} 未设置，无法调用模型")
            client_args["api_key"] = api_key
        
        # 创建客户端
        self.client = OpenAI(**client_args)
        self.async_client = AsyncOpenAI(**client_args)
    
    def _get_request_params(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        获取请求参数
        
        Args:
            content: 用户输入内容
            **kwargs: 其他参数
            
        Returns:
            请求参数字典
        """
        openai_config = self._model_config["openai_config"]
        
        # 基本参数
        params = {
            "model": openai_config["model_id"],
            "messages": [
                {"role": "system", "content": openai_config.get("system_message", "")}
            ]
        }
        
        # 添加历史消息
        history_limit = kwargs.get("history_limit", 10)
        if history_limit > 0 and len(self.history) > 0:
            # 添加最近的历史记录（不超过限制）
            history_to_add = self.history[-history_limit*2:] if history_limit > 0 else []
            params["messages"].extend(history_to_add)
        
        # 添加当前消息
        params["messages"].append({"role": "user", "content": content})
        
        # 添加流式参数
        if kwargs.get("stream", openai_config.get("stream", True)):
            params["stream"] = True
        
        # 添加温度参数
        if "temperature" in kwargs:
            params["temperature"] = kwargs["temperature"]
        elif "temperature" in openai_config:
            params["temperature"] = openai_config["temperature"]
        
        # 添加其他参数
        for key in ["max_tokens", "presence_penalty", "frequency_penalty", "top_p"]:
            if key in kwargs:
                params[key] = kwargs[key]
            elif key in openai_config:
                params[key] = openai_config[key]
        
        return params
    
    def _request_implementation(self, content: str, **kwargs) -> str:
        """
        实现OpenAI API请求
        
        Args:
            content: 用户输入内容
            **kwargs: 其他参数
            
        Returns:
            模型响应
        """
        console = Console()
        
        try:
            # 获取请求参数
            params = self._get_request_params(content, **kwargs)
            is_stream = params.get("stream", True)
            
            # 发送请求
            if is_stream:
                # 流式请求
                stream = self.client.chat.completions.create(**params)
                return print_stream(stream)
            else:
                # 非流式请求
                response = self.client.chat.completions.create(**params)
                content = response.choices[0].message.content
                return print_conclusion(content)
                
        except Exception as e:
            error_message = f"模型调用失败: {type(e).__name__}: {e}"
            console.print(error_message, style="bold red")
            return f"模型 {self._model_config.get('display_name', '未知')} 调用出错: {str(e)}\n\n" \
                   f"请检查以下可能的问题：\n1. API密钥是否正确设置\n2. 网络连接是否正常\n3. 模型服务是否可用"
    
    async def request_async(self, content: str, **kwargs) -> str:
        """
        异步请求模型响应
        
        Args:
            content: 用户输入内容
            **kwargs: 其他参数
            
        Returns:
            模型响应
        """
        console = Console()
        
        try:
            # 添加到历史记录
            if content:
                self.history.append({"role": "user", "content": content})
            
            # 获取请求参数
            params = self._get_request_params(content, **kwargs)
            is_stream = params.get("stream", True)
            
            # 发送请求
            if is_stream:
                # 流式请求
                stream = await self.async_client.chat.completions.create(**params)
                response = await self._process_stream_async(stream)
            else:
                # 非流式请求
                response = await self.async_client.chat.completions.create(**params)
                response = response.choices[0].message.content
            
            # 添加响应到历史
            if response:
                self.history.append({"role": "assistant", "content": response})
                
            return response
                
        except Exception as e:
            error_message = f"模型调用失败: {type(e).__name__}: {e}"
            console.print(error_message, style="bold red")
            return f"模型 {self._model_config.get('display_name', '未知')} 调用出错: {str(e)}\n\n" \
                   f"请检查以下可能的问题：\n1. API密钥是否正确设置\n2. 网络连接是否正常\n3. 模型服务是否可用"
    
    async def _process_stream_async(self, stream) -> str:
        """
        异步处理流式响应
        
        Args:
            stream: 流式响应
            
        Returns:
            完整响应内容
        """
        # 这里可以实现异步流式输出，暂时简化为收集完整内容
        response = ""
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        
        return response 