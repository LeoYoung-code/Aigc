import os
from common import common
from volcenginesdkarkruntime import Ark
from class_interface import ClassInterface


client = Ark(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

def get_stream(content):
    return client.bot_chat.completions.create(
        model="bot-20250217100631-l4csl",
        messages = [
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

class DipuDada(ClassInterface):
    def initialize(self):
        print("正在使用DeepSeek-🌍联网🛜大模型")

    def request(self, conclusion=None):
        return req(conclusion)
