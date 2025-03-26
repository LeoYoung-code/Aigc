from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.console import Group
from rich.panel import Panel
from class_interface import ClassInterface
from abc import ABC, abstractmethod
from typing import Type, Dict, Literal, Optional
import config
import shutil


_CONSOLE = Console()


# 定义接口
class ClassFactoryInterface(ABC):
    @abstractmethod
    def get_class(self, model_name: str) -> 'ClassInterface':
        pass


# 让 ClassFactory 实现接口
class ClassFactory(ClassFactoryInterface):
    def __init__(self):
        import config
        self._class_map: Dict[str, Type['ClassInterface']] = config.class_map_config

    def get_class(self, model_name: str) -> 'ClassInterface':
        cls = self._class_map.get(model_name)
        if cls is None:
            raise ValueError(f"Unknown class: {model_name}")
        return cls()


def markdown_chunk(chunk):
    """简易版的单块Markdown流式输出，用于替换print(chunk, end="")"""
    md = Markdown(chunk, code_theme="dracula")
    _CONSOLE.print(md, end="")
    return chunk


def print_parting_line(text = "这是一条分割线"):
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
    _CONSOLE.print(Text(output_text, style="yellow  bold"))




def print_think_md(res):
    markdown_print(res, header="🤔思考内容输出", header_color="yellow", end="\n")


def print_conclusion_md(res):
    print("\n" * 3, end="")
    markdown_print(res, header="📒结论输出", header_color="yellow", end="\n")
    return res

def get_input(conclusion):
    if conclusion:
        return conclusion + "\n 将上述内容转换成 markdown 格式的脑图文案."
    print("请输入您的问题👩‍⚕️（空行结束）:")
    lines = []
    while True:
        line = input()
        if not line:  # 检测到空行时终止                                                                                                                                                                                                                                                                                      
            break
        lines.append(line)
    print("\n" * 3 + "输入结束, ⌛️请等待回答...")
    return '\n'.join(lines)


def create_mindmap(conclusion):
    factory = ClassFactory()
    try:
        instance = factory.get_class(config.MODEL_GENERATE_MIND)
        instance.initialize()
        return instance.request(conclusion)
    except ValueError as e:
        print(e)


PrintType = Literal["ok", "warn", "info", "error", "sigint", "exit", "changelog"]
HeaderColor = Literal["green", "yellow", "blue", "red", "white", "cyan"]


def markdown_print(
        data: str, header: Optional[str] = None, end: Optional[str] = "", header_color: Optional[HeaderColor] = "blue"
) -> None:
    # Print the header if it exists
    if header:
        header_text = Text(f"╰─❯ {header}:", style=f"{header_color} underline bold")
        _CONSOLE.print(header_text, end=end)

    # Create a Markdown object
    markdown = Markdown(data, code_theme="dracula")

    # Print the Markdown content with word wrapping handled by Console
    _CONSOLE.print(markdown, width=_CONSOLE.width)


def markdown_stream(chunks):
    response = ""
    def render_content():
        """渲染内容，使用与 print_stream 类似的面板样式"""
        md = Markdown("**╰─❯ 📒 结论输出:**\n\n" + response, code_theme="dracula")
        panel = Panel(md, title="结论", border_style="blue")
        return panel 
    with Live(render_content(), refresh_per_second=4, auto_refresh=False, vertical_overflow="crop_above") as live:
        for chunk in chunks:
            if hasattr(chunk, 'text'):
                response += chunk.text
                live.update(render_content(), refresh=True)
    return response



def print_stream(stream):
    """
    该函数实时接收流式响应内容，将思考内容和结论输出分区显示，
    并且只有在思考内容全部输出完成后，才显示结论输出面板。
    通过 Group 和 Panel 组合实现清晰布局，使用 Live 组件自动刷新界面。
    """
    # 初始化两个区域的内容
    think_text = ""
    conclusion_text = ""
    # 跟踪是否思考已完成
    thinking_complete = False
    # 跟踪是否已收到任何结论内容
    has_conclusion = False
    # 存储最后一个chunk，用于检测思考内容是否已结束
    last_chunk_has_reasoning = False
    
    def render_content():
        """
        定义一个渲染函数，根据当前状态决定显示哪些面板
        """
        panels = []
        
        # 始终显示思考面板
        md_think = Markdown("**╰─❯ 🤔 思考内容输出:**\n\n" + think_text, code_theme="dracula")
        panel_think = Panel(md_think, title="思考内容", border_style="blue")
        panels.append(panel_think)
        
        # 只有当思考完成且有结论内容时才显示结论面板
        if thinking_complete and has_conclusion:
            md_conclusion = Markdown("**╰─❯ 📒 结论输出:**\n\n" + conclusion_text, code_theme="dracula")
            panel_conclusion = Panel(md_conclusion, title="结论", border_style="green")
            panels.append(panel_conclusion)
            
        # 用 Group 组合面板
        return Group(*panels)

    # 使用 Live 开启实时更新
    with Live(render_content(), refresh_per_second=4,auto_refresh=False, vertical_overflow="crop_above") as live:
        # 遍历流式响应的每个 chunk
        for chunk in stream:
            # 若 chunk 无效则跳过
            if not chunk.choices or len(chunk.choices) == 0:
                continue
                
            delta = getattr(chunk.choices[0], 'delta', None)
            if not delta:
                continue
                
            # 检查当前chunk中是否有思考内容
            current_has_reasoning = hasattr(delta, 'reasoning_content') and getattr(delta, 'reasoning_content') is not None
            
            # 累加思考内容（如果有）
            if reason := getattr(delta, 'reasoning_content', None):
                think_text += reason
                last_chunk_has_reasoning = True
            else:
                # 如果上一个chunk有思考内容，但当前chunk没有，说明思考内容已结束
                if last_chunk_has_reasoning and not current_has_reasoning:
                    thinking_complete = True
                last_chunk_has_reasoning = False
            
            # 累加结论输出（如果有）
            if res := getattr(delta, 'content', None):
                conclusion_text += res
                has_conclusion = True
                
                # 一旦出现结论内容，我们也可以认为思考已经结束
                thinking_complete = True
            
            # 每次有新内容则刷新展示
            live.update(render_content(), refresh=True)
            
    # 流结束后返回完整的结论文本
    return conclusion_text