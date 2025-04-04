#!/usr/bin/env python3
"""
智能对话助手 - 主入口

支持多种大语言模型，提供命令行交互界面
"""
import traceback
import asyncio
from typing import Any, Optional
from functools import wraps
import shutil

import config
from ui.console import Console
from core.args import ArgumentParser
from core.registry import ModelRegistry
from utils.markmap import markdown_to_markmap

# 导入所有模型，确保它们被注册
import models


# 创建全局Console单例，避免重复创建
console = Console()


def handle_exceptions(func):
    """
    异常处理装饰器，统一处理各类异常
    """
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]⚠️ 检测到用户终止操作，Bye😊！[/bold yellow]", style="on black")
        except ValueError as e:
            console.print(f"[bold red]❌ 输入错误:[/bold red] {e}", style="on black")
        except Exception as e:
            console.print(f"[bold red]🔥 系统错误:[/bold red] {e}", style="on black")
            if config.ADVANCED_SETTINGS.get("debug", False):
                console.print(f"[dim red]{'='*50}\n调试信息:[/dim red]", style="on black")
                console.print(traceback.format_exc(), style="dim red")
                console.print(f"[dim red]{'='*50}[/dim red]", style="on black")
        return None
    
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]⚠️ 检测到用户终止操作，Bye😊！[/bold yellow]", style="on black")
        except ValueError as e:
            console.print(f"[bold red]❌ 输入错误:[/bold red] {e}", style="on black")
        except Exception as e:
            console.print(f"[bold red]🔥 系统错误:[/bold red] {e}", style="on black")
            if config.ADVANCED_SETTINGS.get("debug", False):
                console.print(f"[dim red]{'='*50}\n调试信息:[/dim red]", style="on black")
                console.print(traceback.format_exc(), style="dim red")
                console.print(f"[dim red]{'='*50}[/dim red]", style="on black")
        return None
        
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def create_mind_map(response: str) -> None:
    """
    创建思维导图
    
    Args:
        response: 模型响应文本
    """
    if not response:
        return
    
    try:
        # 将原始响应发送给C模型（豆包256k）进行整理
        console.print("正在将内容整理为思维导图...", style="bold cyan")
        
        # 使用run_model方法调用C模型，并传入原始响应作为输入
        mind_map_content = run_model(config.MODEL_GENERATE_MIND, False, f"请将以下内容整理为一个结构化的思维导图内容:\n\n{response}")

        # 显示成功提示
        console.print("[bold green]✨ 思维导图生成完成！[/bold green]", style="on black")

        # 使用处理后的内容创建思维导图
        markdown_to_markmap(mind_map_content)
    except Exception as e:
        console.print(f"[bold red]🔥 创建思维导图失败:[/bold red] {e}", style="on black")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")


def initialize_model(model_key: str):
    """
    初始化模型实例
    
    Args:
        model_key: 模型标识符
        
    Returns:
        初始化后的模型实例
    """
    registry = ModelRegistry()
    instance = registry.create_instance(model_key)
    instance.initialize()
    return instance


@handle_exceptions
async def run_async_model(model_key: str, is_mind: bool) -> None:
    """
    异步运行模型
    
    Args:
        model_key: 模型标识符
        is_mind: 是否生成思维导图
    """
    # 初始化模型
    instance = initialize_model(model_key)
    
    # 异步请求模型响应
    with console.create_progress() as progress:
        task = progress.add_task("正在处理请求...", total=None)
        response = await instance.request_async(None)
        progress.update(task, completed=100, description="[bold green]✓ 思考完成！")
    
    # 如果启用了思维导图模式，创建思维导图
    if is_mind and response:
        create_mind_map(response)
        
    return response


@handle_exceptions
def run_model(model_key: str, is_mind: bool, content: str = None) -> Any | None:
    """
    同步运行模型

    Args:
        model_key: 模型标识符
        is_mind: 是否生成思维导图
        content: 模型输入内容，默认为None表示从标准输入获取
    """
    # 初始化模型
    instance = initialize_model(model_key)

    # 请求模型响应
    response = instance.req_model(content)
    
    # 如果启用了思维导图模式，创建思维导图
    if is_mind and response:
        create_mind_map(response)

    return response


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
    # 显示欢迎信息
    app_title = f"{config.APP_INFO['name']} v{config.APP_INFO['version']}"
    terminal_width = shutil.get_terminal_size().columns
    
    # 创建装饰性标题
    console.print("\n", style="bold")
    console._console.rule(f"[bold cyan]{app_title}[/bold cyan]", style="cyan")
    
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 程序已退出[/bold yellow]", style="on black")
    except Exception as e:
        console.print(f"[bold red]❌ 程序异常:[/bold red] {e}", style="on black")
        if config.ADVANCED_SETTINGS.get("debug", False):
            console.print(traceback.format_exc(), style="dim red")