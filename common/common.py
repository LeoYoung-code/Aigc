from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from class_interface import ClassInterface
from abc import ABC, abstractmethod
from typing import Type, Dict, Literal, Optional
from termcolor import colored
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


def print_stream(stream):
    resp_think = []
    resp_conclusion = []
    # _CONSOLE.print(Text("\n╰─❯ 大模型响应:", style="yellow underline bold"))
    print_parting_line("大模型响应")
    with Live(console=_CONSOLE, refresh_per_second=8, auto_refresh=True, vertical_overflow="visible") as live_content:
        think_text = ""
        conclusion_text = ""
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if not delta:
                continue

            if reason := delta.reasoning_content:
                # 累积内容并更新显示
                think_text += reason
                resp_think.append(reason)

                # 使用Markdown渲染累积的内容
                md = Markdown(think_text, code_theme="dracula")
                live_content.update(md)
            if res := delta.content:
                conclusion_text += res
                resp_conclusion.append(res)
                md = Markdown(conclusion_text, code_theme="dracula")
                live_content.update(md)
        # 渲染完成后清空Live内容
        empty_md = Markdown("")
        live_content.update(empty_md)

    if resp_think:
        print_think_md(''.join(resp_think))
    if resp_conclusion:
        r = ''.join(resp_conclusion)
        print_conclusion_md(r)
        return r



def print_think_md(res):
    markdown_print(res, header="🤔思考内容输出", header_color="yellow", end="\n")


def print_conclusion_md(res):
    print("\n" * 3, end="")
    markdown_print(res, header="📒结论输出", header_color="yellow", end="\n")


def get_input(conclusion):
    if conclusion:
        return conclusion + "\n 将上述内容转换成 markdown 格式的脑图文案."
    print("\n" * 3 + "请输入您的问题👩‍⚕️（空行结束）:")
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
    buffer = ""
    update_threshold = 3  # 每积累3个字符更新一次，可以根据需要调整
    
    with Live(
        console=_CONSOLE, 
        refresh_per_second=4,  # 降低刷新频率
        vertical_overflow="visible",  # 修改为visible以显示完整内容
        auto_refresh=False  # 手动控制刷新时机
    ) as live:
        for chunk in chunks:
            buffer += chunk
            response += chunk
            
            # 当缓冲区达到阈值或收到换行符时更新显示
            if len(buffer) >= update_threshold or '\n' in buffer:
                md = Markdown(response, code_theme="dracula")
                live.update(md)
                live.refresh()
                buffer = ""  # 清空缓冲区
                
        # 确保最后的内容也被显示
        if buffer:
            md = Markdown(response, code_theme="dracula")
            live.update(md)
    
    # 渲染完成后清空控制台
    _CONSOLE.clear()
    
    return response


def custom_print(
        ptype: PrintType,
        text: str,
        exit_code: Optional[int] = None,
        print_now: Optional[bool] = True,
        start: Optional[str] = "",
        end: Optional[str] = "",
) -> Optional[str]:
    """
    Custom STDOUT function which works soft of like logging
    It uses pre-defined prefixes (E.g. `[ERROR] <your_text>`)
    :param ptype: Print type (the mentioned prefix)
    :param text: the text you would like to print
    :param exit_code: custom exit status if you like to abort everything
    :param print_now: whether to print or return the content
    :param start: Add custom text before the prefix
    :param end: Add custom text after the text
    :return: The content if "print_now" is false
    """

    formats = {
        "ok": ("[OK] ", "green"),
        "warn": ("[WARN] ", "yellow"),
        "info": ("[INFO] ", "blue"),
        "error": ("[ERROR] ", "red"),
        "sigint": ("[SIGINT] ", "red"),
        "exit": ("[EXIT] ", "red"),
        "changelog": ("[CHANGELOG] ", "cyan"),
    }

    prefix, color = formats.get(ptype.lower(), ("[UNKNOWN] ", "white"))
    formatted_text = start + colored(prefix, color) + text + end

    if print_now:
        print(formatted_text)
        if exit_code is not None:
            exit(exit_code)
    else:
        if exit_code is not None:
            print(f"Cannot use exit_code when not printing immediately.")
            exit(1)

    return formatted_text if not print_now else None
