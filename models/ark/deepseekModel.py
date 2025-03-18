import httpx
from common import common
from volcenginesdkarkruntime import Ark
from class_interface import ClassInterface

client = Ark(
    timeout=httpx.Timeout(timeout=1800),
)


def get_stream(content):
    return client.chat.completions.create(
        model="ep-20250208175039-r6lmf",
        messages=[
            {"role": "system", "content": "你是迪普，是人工智能助手,用中文详细的回答每一个问题。"},
            {"role": "user", "content": content},
        ],
        stream=True
    )

def req(conclusion=None):
    try:
        content = common.get_input(conclusion)
        stream = get_stream(content)
        return common.print_stream(stream)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


class DeepSeekArk(ClassInterface):

    def initialize(self):
        print("正在使用DeepSeek-R1 基于MoE架构（总参数量671B，激活37B）")

    def request(self, conclusion=None):
       return req(conclusion)