"""
脑图生成工具模块 - 提供Markdown转思维导图功能
"""
import os
import time
import subprocess
import shutil
from typing import Optional, Tuple, Union
from pathlib import Path
import functools

# 缓存Console单例
_console = None

def get_console():
    """获取Console单例实例"""
    global _console
    if _console is None:
        from ui.console import Console
        _console = Console()
    return _console


@functools.lru_cache()
def get_project_root() -> Path:
    """
    获取项目根目录的绝对路径
    
    Returns:
        项目根目录的绝对路径
    """
    return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save_markdown_to_file(markdown_text: str, prefix: str = "模型总结") -> str:
    """
    将markdown文本保存到指定路径的文件中
    
    Args:
        markdown_text: 要保存的markdown文本内容
        prefix: 文件名前缀，默认为"模型总结"
    
    Returns:
        创建的文件路径
    """
    if not markdown_text or markdown_text.strip() == "":
        raise ValueError("Markdown文本内容不能为空")
        
    # 获取项目根目录
    project_root = get_project_root()
    
    # 确保目标目录存在
    target_dir = project_root / "resource" / "md_cache"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成毫秒级时间戳
    timestamp = int(time.time() * 1000)
    
    # 构建文件名和完整路径
    filename = f"{prefix}_{timestamp}.md"
    file_path = target_dir / filename
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    return str(file_path)


def open_file(file_path: str) -> bool:
    """
    根据操作系统打开文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        是否成功打开
    """
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS or Linux
            if 'darwin' in os.uname().sysname.lower():  # macOS
                subprocess.run(['open', file_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', file_path], check=True)
        return True
    except Exception:
        return False


def generate_markmap(file_path: str) -> Tuple[Optional[str], int, str]:
    """
    使用markmap-cli将Markdown文件转换为思维导图
    
    Args:
        file_path: Markdown文件的路径
    
    Returns:
        (生成的思维导图HTML文件路径, 命令执行状态码, 命令输出信息)
    """
    console = get_console()
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Markdown文件不存在: {file_path}")
    
    # 检查npx是否可用
    if not shutil.which("npx"):
        raise EnvironmentError("未找到npx命令，请确保已安装Node.js和npm")
    
    # 确定输出文件路径（默认情况下markmap-cli会生成同名的.html文件）
    output_file = os.path.splitext(file_path)[0] + ".html"
    
    try:
        # 执行npx markmap-cli命令
        result = subprocess.run(
            ["npx", "markmap-cli", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        # 检查命令是否成功执行
        if result.returncode == 0:
            # 检查输出文件是否生成
            if os.path.exists(output_file):
                console.print(f"思维导图已生成: {output_file}", style="bold green")
                return output_file, result.returncode, result.stdout
            else:
                return None, result.returncode, "命令执行成功但未找到输出文件"
        else:
            return None, result.returncode, result.stderr
    
    except subprocess.SubprocessError as e:
        return None, -1, str(e)


def markdown_to_markmap(markdown_text: str, prefix: str = "模型总结") -> Tuple[Optional[str], int, str]:
    """
    将Markdown文本直接转换为思维导图
    
    Args:
        markdown_text: 要转换的Markdown文本内容
        prefix: 文件名前缀，默认为"模型总结"
    
    Returns:
        (生成的思维导图HTML文件路径, 命令执行状态码, 命令输出信息)
    """
    console = get_console()
    
    # 打印等待信息
    console.print("正在生成思维导图...", style="bold cyan")
    
    try:
        # 先保存Markdown文件
        md_file_path = save_markdown_to_file(markdown_text, prefix)
        
        # 然后生成思维导图
        result = generate_markmap(md_file_path)
        
        if result[0]:
            console.print("思维导图生成成功！", style="bold green")
            # # 尝试自动打开文件
            # if open_file(result[0]):
            #     console.print("已自动打开思维导图", style="italic cyan")
            # else:
            #     console.print(f"无法自动打开，请手动打开文件: {result[0]}", style="italic yellow")
        else:
            console.print(f"思维导图生成失败: {result[2]}", style="bold red")
        
        return result
    except Exception as e:
        console.print(f"生成思维导图时发生错误: {e}", style="bold red")
        return None, -1, str(e) 