#!/usr/bin/env python3
"""
智能对话助手 - 主入口

支持多种大语言模型，提供命令行交互界面
"""
import sys
import traceback
import asyncio

import config
from ui.console import Console
from core.args import ArgumentParser
from core.registry import ModelRegistry
from core.utils import run_async
from utils.markmap import markdown_to_markmap

# 导入所有模型，确保它们被注册
import models.openai_models


def create_mind_map(response: str) -> None:
    """
    创建思维导图
    
    Args:
        response: 模型响应文本
    """
    if not response:
        return
    
    try:
        markdown_to_markmap(response)
    except Exception as e:
        console = Console()
        console.print(f"创建思维导图失败: {e}", style="bold red")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")


async def run_async_model(model_key: str, is_mind: bool) -> None:
    """
    异步运行模型
    
    Args:
        model_key: 模型标识符
        is_mind: 是否生成思维导图
    """
    console = Console()
    registry = ModelRegistry()
    
    try:
        # 创建模型实例
        instance = registry.create_instance(model_key)
        
        # 初始化模型
        instance.initialize()
        
        # 异步请求模型响应
        with console.create_progress() as progress:
            task = progress.add_task("正在处理请求...", total=None)
            response = await instance.request_async(None)
            progress.update(task, completed=100)
        
        # 如果启用了思维导图模式，创建思维导图
        if is_mind and response:
            create_mind_map(response)
            
    except KeyboardInterrupt:
        console.print("\n检测到用户终止操作，Bye😊！", style="bold yellow")
    except ValueError as e:
        console.print(f"错误: {e}", style="bold red")
    except Exception as e:
        console.print(f"发生错误: {e}", style="bold red")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")


def run_model(model_key: str, is_mind: bool) -> None:
    """
    同步运行模型
    
    Args:
        model_key: 模型标识符
        is_mind: 是否生成思维导图
    """
    console = Console()
    registry = ModelRegistry()
    
    try:
        # 创建模型实例
        instance = registry.create_instance(model_key)
        
        # 初始化模型
        instance.initialize()
        
        # 请求模型响应
        response = instance.request(None)
        
        # 如果启用了思维导图模式，创建思维导图
        if is_mind and response:
            create_mind_map(response)
            
    except KeyboardInterrupt:
        console.print("\n检测到用户终止操作，Bye😊！", style="bold yellow")
    except ValueError as e:
        console.print(f"错误: {e}", style="bold red")
    except Exception as e:
        console.print(f"发生错误: {e}", style="bold red")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")


def main() -> None:
    """程序主入口"""
    # 解析命令行参数
    parser = ArgumentParser()
    model_key, is_mind, use_async = parser.parse_args()
    
    if model_key is None:
        return
    
    # 根据不同模式运行
    if use_async:
        asyncio.run(run_async_model(model_key, is_mind))
    else:
        run_model(model_key, is_mind)


if __name__ == "__main__":
    console = Console()
    # 显示欢迎信息
    console.print_divider(f"{config.APP_INFO['name']} v{config.APP_INFO['version']}")
    
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n程序已退出", style="bold yellow")
    except Exception as e:
        console.print(f"程序异常: {e}", style="bold red")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")