import os
from common import common
from class_interface import ClassInterface

def req(conclusion=None):
    try:
        content = common.get_input(conclusion)
        return common.call_openai_model("deepseek-reasoner", content)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


class DeepSeek(ClassInterface):
    def initialize(self):
        print("正在使用DeepSeek官方大模型")

    def request(self, conclusion=None):
       return req(conclusion)
