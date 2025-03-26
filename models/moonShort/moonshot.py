import os
from common import common
from class_interface import ClassInterface

class Moonshot(ClassInterface):
    def initialize(self):
        print("正在使用moonshot-v1-32k大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("moonshot-v1-32k", common.get_input(conclusion))