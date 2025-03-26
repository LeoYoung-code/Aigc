import os
from common import common
from class_interface import ClassInterface

class SiliconFlow(ClassInterface):
    def initialize(self):
        print("正在使用SILICON_FLOW大模型")

    def request(self, conclusion=None):
        content = common.get_input(conclusion)
        return common.call_openai_model("deepseek-ai/DeepSeek-V2.5", content)
