import os
from common import common
from class_interface import ClassInterface

class QwqPlus(ClassInterface):
    def initialize(self):
        print("正在使用阿里云百炼QwqPlus(128K)大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("qwq-plus", common.get_input(conclusion))
