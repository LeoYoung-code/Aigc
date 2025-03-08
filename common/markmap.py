import os
import time
import subprocess
import shutil

def save_markdown_to_file(markdown_text, prefix="模型总结"):
    """
    将markdown文本保存到指定路径的文件中
    
    Args:
        markdown_text (str): 要保存的markdown文本内容
        prefix (str, optional): 文件名前缀，默认为"模型总结"
    
    Returns:
        str: 创建的文件路径
    """
    # 确保目标目录存在
    target_dir = "resource/md_cache"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 生成毫秒级时间戳
    timestamp = int(time.time() * 1000)
    
    # 构建文件名和完整路径
    filename = f"{prefix}_{timestamp}.md"
    file_path = os.path.join(target_dir, filename)
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    return file_path

def generate_markmap(file_path):
    """
    使用markmap-cli将Markdown文件转换为思维导图
    
    Args:
        file_path (str): Markdown文件的路径
    
    Returns:
        tuple: (生成的思维导图HTML文件路径, 命令执行状态码, 命令输出信息)
    """
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
                return output_file, result.returncode, result.stdout
            else:
                return None, result.returncode, "命令执行成功但未找到输出文件"
        else:
            return None, result.returncode, result.stderr
    
    except subprocess.SubprocessError as e:
        return None, -1, str(e)


def markdown_to_markmap(markdown_text, prefix="模型总结"):
    """
    将Markdown文本直接转换为思维导图
    
    Args:
        markdown_text (str): 要转换的Markdown文本内容
        prefix (str, optional): 文件名前缀，默认为"模型总结"
    
    Returns:
        tuple: (生成的思维导图HTML文件路径, 命令执行状态码, 命令输出信息)
    """
    # 先保存Markdown文件
    md_file_path = save_markdown_to_file(markdown_text, prefix)
    
    # 然后生成思维导图
    return generate_markmap(md_file_path)
