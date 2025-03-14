import httpx
from common import common
from volcenginesdkarkruntime import Ark
from class_interface import ClassInterface

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    timeout=httpx.Timeout(timeout=1800),
)

def get_stream(content):
    return client.chat.completions.create(
        model="doubao-1-5-pro-256k-250115",
        messages=[
            {"role": "system", "content": "你是迪普，是人工智能助手,用中文详细的回答每一个问题。"},
            {"role": "user", "content": content},
        ],
        stream=True
    )

class DouBao256kModel(ClassInterface):
    def initialize(self):
        print("正在使用Doubao-1.5-pro-256k 支持256k上下文窗口的推理")

    def request(self, conclusion=None):
        try:
            content = common.get_input(conclusion)
            stream = get_stream(content)
            return common.print_stream(stream)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')