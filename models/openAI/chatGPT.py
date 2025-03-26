from common import common
from class_interface import ClassInterface

def req(conclusion=None):
    try:
        content = common.get_input(conclusion)
        return common.call_openai_model("gpt-4o-mini", content)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


class OpenAI(ClassInterface):
    def initialize(self):
        print("正在使用GPT_4o_MINI大模型")

    def request(self, conclusion=None):
       return req(conclusion)