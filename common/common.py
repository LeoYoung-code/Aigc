from rich.console import Console
from rich.markdown import Markdown
from class_interface import ClassInterface
from abc import ABC, abstractmethod
from typing import Type, Dict
import config


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

def print_stream(stream):
    resp_think = []
    resp_conclusion = []
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if not delta:
            continue
        if reason := delta.reasoning_content:
            print(reason, end="")
            resp_think.append(reason)

        if res := delta.content:
            print(res, end="")
            resp_conclusion.append(res)

    if resp_think:
        print_think_md(''.join(resp_think))
    if resp_conclusion:
        r = ''.join(resp_conclusion)
        print_conclusion_md(r)
        return r


def print_think_md(res):
    print("\n" * 3, end="")
    title = "# 🤔思考内容输出: \n"
    md = Markdown(title + res)
    _CONSOLE.print(md)


def print_conclusion_md(res):
    print("\n" * 3, end="")
    title = "# 📒结论输出: "
    md = Markdown(title + res)
    _CONSOLE.print(md)


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























