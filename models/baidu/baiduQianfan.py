from common import common
from class_interface import ClassInterface

class BaiduQianfan(ClassInterface):
    def initialize(self):
        print("正在使用百度文心一言大模型")

    def request(self, conclusion=None):
        return common.call_openai_model("ernie-x1-32k-preview", common.get_input(conclusion)) 