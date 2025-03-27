"""
控制台UI模块 - 提供终端界面相关功能
"""
from typing import Optional, Dict, Any, List, Union, Literal
import shutil
from rich.console import Console as RichConsole
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Group


# 类型定义
PrintType = Literal["ok", "warn", "info", "error", "sigint", "exit", "changelog"]
HeaderColor = Literal["green", "yellow", "blue", "red", "white", "cyan"]


class Console:
    """增强的控制台类，提供丰富的输出功能"""
    
    _instance = None  # 单例实例
    
    def __new__(cls):
        """实现单例模式"""
        if cls._instance is None:
            cls._instance = super(Console, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化实例"""
        if not getattr(self, "_initialized", False):
            self._console = RichConsole()
            self._initialized = True
    
    def print(self, text: str, style: Optional[str] = None, end: str = "\n"):
        """打印文本"""
        self._console.print(text, style=style, end=end)
    
    def print_markdown(self, text: str, code_theme: str = "dracula"):
        """打印Markdown格式文本"""
        md = Markdown(text, code_theme=code_theme)
        self._console.print(md)
    
    def print_header(self, text: str, style: str = "bold cyan"):
        """打印带样式的标题"""
        self._console.print(f"\n{text}", style=style)
    
    def print_divider(self, text: str = "这是一条分割线", style: str = "yellow bold"):
        """
        打印带文字的分割线
        
        Args:
            text: 分割线中的文字
            style: 文字样式
        """
        # 自动获取终端的列数
        terminal_width = shutil.get_terminal_size().columns

        # 计算左右两侧分割线的长度
        left_length = (terminal_width - len(text) - 2) // 2
        right_length = terminal_width - left_length - len(text) - 2

        # 生成左右两侧的分割线
        left_line = "=" * left_length
        right_line = "=" * (right_length -  len(text))

        # 组合分割线和文本
        output_text = f"{left_line} {text} {right_line}"

        # 打印输出
        self._console.print(Text(output_text, style))
    
    def create_progress(self, description: str = "处理中"):
        """创建进度条"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[bold]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self._console
        )
    
    def markdown_print(self, 
                       data: str, 
                       header: Optional[str] = None, 
                       end: Optional[str] = "", 
                       header_color: Optional[HeaderColor] = "blue") -> None:
        """
        打印Markdown格式文本
        
        Args:
            data: Markdown格式文本
            header: 标题
            end: 结束字符
            header_color: 标题颜色
        """
        # 打印标题
        if header:
            header_text = Text(f"╰─❯ {header}:", style=f"{header_color} underline bold")
            self._console.print(header_text, end=end)
        
        # 打印Markdown内容
        markdown = Markdown(data, code_theme="dracula")
        self._console.print(markdown, width=self._console.width)
    
    def print_conclusion(self, content: str) -> str:
        """
        打印结论
        
        Args:
            content: 结论内容
            
        Returns:
            结论内容
        """
        self.print("\n" * 2)
        self.markdown_print(content, header="📒结论输出", header_color="yellow", end="\n")
        return content
    
    def markdown_stream(self, chunks) -> str:
        """
        流式渲染Markdown内容
        
        Args:
            chunks: Markdown内容块
            
        Returns:
            完整内容
        """
        response = ""
        
        def render_content():
            """渲染内容"""
            md = Markdown("**╰─❯ 📒 结论输出:**\n\n" + response, code_theme="dracula")
            panel = Panel(md, title="结论", border_style="blue")
            return panel
        
        with Live(render_content(), refresh_per_second=4, auto_refresh=False, vertical_overflow="crop_above") as live:
            for chunk in chunks:
                if hasattr(chunk, 'text'):
                    response += chunk.text
                    live.update(render_content(), refresh=True)
        
        return response 
    
    def print_stream(self, stream) -> str:
        """
        实时打印流式响应内容，将思考内容和结论输出分区显示
        
        Args:
            stream: 流式响应
            
        Returns:
            完整响应内容
        """
        # 初始化内容
        think_text = ""
        conclusion_text = ""
        
        # 跟踪状态
        thinking_complete = False
        has_conclusion = False
        last_chunk_has_reasoning = False
        
        def render_content():
            """根据当前状态渲染内容"""
            panels = []
            
            # 思考面板
            md_think = Markdown("**╰─❯ 🤔 思考内容输出:**\n\n" + think_text, code_theme="dracula")
            panel_think = Panel(md_think, title="思考内容", border_style="blue")
            panels.append(panel_think)
            
            # 结论面板（只在适当时显示）
            if thinking_complete and has_conclusion:
                md_conclusion = Markdown("**╰─❯ 📒 结论输出:**\n\n" + conclusion_text, code_theme="dracula")
                panel_conclusion = Panel(md_conclusion, title="结论", border_style="green")
                panels.append(panel_conclusion)
            
            return Group(*panels)
        
        # 使用Live组件实时更新
        with Live(render_content(), refresh_per_second=4, auto_refresh=False, vertical_overflow="crop_above") as live:
            for chunk in stream:
                # 跳过无效chunk
                if not hasattr(chunk, 'choices') or not chunk.choices or len(chunk.choices) == 0:
                    continue
                
                delta = getattr(chunk.choices[0], 'delta', None)
                if not delta:
                    continue
                
                # 检查是否有思考内容
                current_has_reasoning = hasattr(delta, 'reasoning_content') and getattr(delta, 'reasoning_content') is not None
                
                # 累加思考内容
                if reason := getattr(delta, 'reasoning_content', None):
                    think_text += reason
                    last_chunk_has_reasoning = True
                else:
                    # 检测思考内容是否结束
                    if last_chunk_has_reasoning and not current_has_reasoning:
                        thinking_complete = True
                    last_chunk_has_reasoning = False
                
                # 累加结论输出
                if res := getattr(delta, 'content', None):
                    conclusion_text += res
                    has_conclusion = True
                    thinking_complete = True
                
                # 更新显示
                live.update(render_content(), refresh=True)
        
        # 返回结论
        return conclusion_text
    
    @property
    def width(self) -> int:
        """获取控制台宽度"""
        return self._console.width
    
    @property
    def height(self) -> int:
        """获取控制台高度"""
        return self._console.height


# 为了向后兼容，提供全局函数版本
def markdown_print(
    data: str, 
    header: Optional[str] = None, 
    end: Optional[str] = "", 
    header_color: Optional[HeaderColor] = "blue"
) -> None:
    """向后兼容: 打印Markdown格式文本"""
    Console().markdown_print(data, header, end, header_color)


def print_conclusion(content: str) -> str:
    """向后兼容: 打印结论"""
    return Console().print_conclusion(content)


def markdown_stream(chunks) -> str:
    """向后兼容: 流式渲染Markdown内容"""
    return Console().markdown_stream(chunks)


def print_stream(stream) -> str:
    """向后兼容: 实时打印流式响应内容"""
    return Console().print_stream(stream)
