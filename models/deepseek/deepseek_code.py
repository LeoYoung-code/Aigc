import os
from common import common
from class_interface import ClassInterface

def req(conclusion=None):
    try:
        content = common.get_input(conclusion)
        return common.call_openai_model("deepseek-chat", content)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


class DeepSeekV3(ClassInterface):
    def initialize(self):
        # print(client.models.list())
        print("正在使用DeepSeek-V3官方大模型")

    def request(self, conclusion=None):
       return req(conclusion)
