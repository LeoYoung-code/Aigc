import argparse
import sys

from sympy import false

import config

# 自定义帮助信息（包含ANSI颜色和格式）
sHelp = """\033[1;36m
【模型选择指南】\033[0m

请通过以下格式指定要使用的模型：
  \033[1m使用方法:\033[0m python main.py 模型代号

\033[1;33m可用模型及对应类:\033[0m
{model_list}

\033[2m提示: 模型代号区分大小写，请严格按列表输入\033[0m
""".format(
    model_list='\n'.join([
        f"  \033[32m▶\033[0m \033[1m{k.ljust(6)}\033[0m : \033[3;34m{v.__name__}\033[0m"
        for k, v in config.class_map_config.items()
    ])
)


# 自定义解析器类
class CustomParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        # 覆盖原始方法直接打印彩色帮助
        if message.startswith("usage: "):
            return  # 跳过自动生成的usage行
        print(sHelp)

    def error(self, message):
        """参数错误时显示自定义帮助"""
        print(sHelp)
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
    metavar='\033[3;31m模型代号\033[0m',  # 给参数添加颜色
    help=argparse.SUPPRESS  # 隐藏参数说明
)


# 新增参数 -m 或 --is_mind
parser.add_argument(
    '-m', '--is_mind',
    action='store_true',
    default=False,
    help='\033[3m是否启用脑图模式\033[0m'  # 带格式的help描述
)

# 添加自定义help选项
parser.add_argument(
    '-h', '--help',
    action='store_true',
    help='\033[3m显示帮助信息\033[0m'  # 带格式的help描述
)

def get_params():
    # 解析参数
    try:
        args = parser.parse_args()
    except SystemExit:
        return None,false

    # 处理help选项
    if args.help:
        print(sHelp)
        return None,false

    # 验证参数有效性
    if args.model_name not in config.class_map_config:
        print(f"\033[31m错误：未知模型代号 '{args.model_name}'\033[0m")
        print(sHelp)
        sys.exit(1)

    # 正常执行流程
    print(f"已选择模型：\033[1;32m{args.model_name}\033[0m (\033[34m{config.class_map_config[args.model_name].__name__}\033[0m)")
    return args.model_name, args.is_mind
