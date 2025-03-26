"""
命令行参数解析模块
"""
import argparse
import sys
from typing import Tuple, Optional
from core.registry import ModelRegistry


# 自定义帮助信息模板
HELP_TEMPLATE = """\033[1;36m
【模型选择指南】\033[0m

请通过以下格式指定要使用的模型：
  \033[1m使用方法:\033[0m python main.py 模型代号 [选项]

\033[1;33m可用模型列表:\033[0m
{model_list}

\033[2m提示: 模型代号区分大小写，请严格按列表输入\033[0m
"""


class ArgumentParser:
    """命令行参数解析器"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """创建命令行解析器"""
        # 自定义解析器类
        class CustomParser(argparse.ArgumentParser):
            def _print_message(self, message, file=None):
                # 覆盖原始方法直接打印彩色帮助
                if message.startswith("usage: "):
                    return  # 跳过自动生成的usage行
                
                # 获取模型列表
                registry = ModelRegistry()
                model_list = "\n".join([
                    f"  \033[32m▶\033[0m \033[1m{k.ljust(6)}\033[0m : \033[3;34m{registry.get_model_config(k)['display_name']}\033[0m"
                    for k in sorted(registry._models.keys())
                ])
                
                # 打印帮助信息
                print(HELP_TEMPLATE.format(model_list=model_list))
            
            def error(self, message):
                """参数错误时显示自定义帮助"""
                self._print_message(message)
                sys.exit(2)
        
        # 初始化解析器
        parser = CustomParser(
            add_help=False,  # 禁用默认的-h/--help
            usage=argparse.SUPPRESS  # 隐藏自动生成的usage
        )
        
        # 定义必须参数
        parser.add_argument(
            'model_name',
            type=str,
            nargs='?',  # 使参数可选
            metavar='\033[3;31m模型代号\033[0m',
            help=argparse.SUPPRESS  # 隐藏参数说明
        )
        
        # 新增参数 -m 或 --mindmap
        parser.add_argument(
            '-m', '--mindmap',
            action='store_true',
            default=False,
            help='\033[3m是否启用脑图模式\033[0m'
        )
        
        # 添加-a或--async参数
        parser.add_argument(
            '-a', '--async',
            action='store_true',
            default=False,
            dest='use_async',
            help='\033[3m使用异步模式\033[0m'
        )
        
        # 添加自定义help选项
        parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='\033[3m显示帮助信息\033[0m'
        )
        
        return parser
    
    def parse_args(self) -> Tuple[Optional[str], bool, bool]:
        """
        解析命令行参数
        
        Returns:
            Tuple[Optional[str], bool, bool]: (模型标识符, 是否生成脑图, 是否使用异步模式)
        """
        from ui.console import Console
        console = Console()
        
        # 解析参数
        try:
            args = self.parser.parse_args()
        except SystemExit:
            return None, False, False
        
        # 处理help选项
        if args.help:
            self.parser._print_message("")
            return None, False, False
        
        # 检查是否提供了模型名称
        if not args.model_name:
            self.parser._print_message("")
            return None, False, False
        
        # 验证模型是否存在
        registry = ModelRegistry()
        if args.model_name not in registry._models:
            console.print(f"错误：未知模型代号 '{args.model_name}'", style="bold red")
            self.parser._print_message("")
            return None, False, False
        
        # 打印选择信息
        console.print(f"已选择模型：[bold green]{args.model_name}[/] "
                      f"([blue]{registry.get_model_config(args.model_name)['display_name']}[/])")
        
        if args.mindmap:
            console.print("已启用脑图模式", style="bold yellow")
        
        if args.use_async:
            console.print("已启用异步模式", style="bold cyan")
        
        return args.model_name, args.mindmap, args.use_async 