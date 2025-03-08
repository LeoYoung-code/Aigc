import os
from common import common
from openai import OpenAI
from class_interface import ClassInterface

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def get_stream(content):
    return client.chat.completions.create(
        model="deepseek-r1",
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


class BaiLian(ClassInterface):
    def initialize(self):
        print("正在使用阿里云百炼DeepSeek大模型")

    def request(self, conclusion=None):
       return req(conclusion)
