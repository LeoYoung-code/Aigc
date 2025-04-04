"""
工具函数模块 - 提供通用工具函数
"""
import os
import sys
import asyncio
from typing import Optional, List, Dict, Any, Callable


def get_input(conclusion: Optional[str] = None) -> str:
    """
    从用户获取输入或使用结论
    
    Args:
        conclusion: 如果提供了结论，则将结论转换为脑图文案
        
    Returns:
        用户输入或转换后的结论
    """
    if conclusion:
        return conclusion + "\n 将上述内容转换成 markdown 格式的脑图文案."
    
    from ui.console import Console
    console = Console()
    
    console.print("请输入您的问题👩‍⚕️（空行结束）:", style="bold cyan")
    lines = []
    
    while True:
            line = input()
            if not line:  # 检测到空行时终止                                                                                                                                                                                                                                                                                      
                break
            lines.append(line)
    console.print("\n" * 1 + "输入结束, ⌛️请等待回答...", style="italic cyan")
    return '\n'.join(lines)


def get_env_var(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    安全地获取环境变量
    
    Args:
        name: 环境变量名称
        default: 默认值（如果环境变量不存在）
        required: 是否必须存在（如果为True且环境变量不存在则抛出异常）
        
    Returns:
        环境变量值或默认值
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise EnvironmentError(f"必须设置环境变量: {name}")
    return value


def run_async(func: Callable, *args, **kwargs) -> Any:
    """
    运行异步函数
    
    Args:
        func: 异步函数
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        异步函数的结果
    """
    if not asyncio.iscoroutinefunction(func):
        return func(*args, **kwargs)
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(func(*args, **kwargs))


def create_chunks(text: str, max_size: int = 2000) -> List[str]:
    """
    将文本分割成更小的块
    
    Args:
        text: 要分割的文本
        max_size: 每个块的最大大小
        
    Returns:
        文本块列表
    """
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 > max_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += '\n'
            current_chunk += line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks 