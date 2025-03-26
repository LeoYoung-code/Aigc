from common import common
from class_interface import ClassInterface

class OpenAI(ClassInterface):
    def initialize(self):
        print("正在使用GPT_4o_MINI大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("gpt-4o-mini", common.get_input(conclusion))