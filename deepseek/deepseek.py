import os
from common import common
from openai import OpenAI
from class_interface import ClassInterface

client = OpenAI(
    base_url='https://api.deepseek.com',
    api_key=os.getenv('DEEP_SEEK_API_KEY')
)


def get_stream(content):
    return client.chat.completions.create(
        model="deepseek-reasoner",
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


class DeepSeek(ClassInterface):
    def initialize(self):
        print("正在使用DeepSeek官方大模型")

    def request(self, conclusion=None):
       return req(conclusion)
