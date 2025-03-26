import os
from common import common
from class_interface import ClassInterface

class DeepSeekV3(ClassInterface):
    def initialize(self):
        print("正在使用DeepSeek-V3官方大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("deepseek-chat", common.get_input(conclusion))
