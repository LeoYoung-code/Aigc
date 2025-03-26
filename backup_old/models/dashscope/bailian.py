import os
from common import common
from class_interface import ClassInterface

class BaiLian(ClassInterface):
    def initialize(self):
        print("正在使用阿里云百炼DeepSeek大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("deepseek-r1", common.get_input(conclusion))
