import os
from common import common
from class_interface import ClassInterface

class DeepSeek(ClassInterface):
    def initialize(self):
        print("正在使用DeepSeek官方大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("deepseek-reasoner", common.get_input(conclusion))
