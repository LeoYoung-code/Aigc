import os
from common import common
from openai import OpenAI
from class_interface import ClassInterface

client = OpenAI(
    base_url='https://api.siliconflow.cn/v1',
    api_key=os.getenv('SILICON_FLOW_API_KEY')
)


def get_stream(content):
    return client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V2.5",
        messages=[
            {"role": "system", "content": "你是迪普，是人工智能助手,用中文详细的回答每一个问题。"},
            {"role": "user", "content": content},
        ],
        stream=True
    )

class SiliconFlow(ClassInterface):
    def initialize(self):
        print("正在使用SILICON_FLOW大模型")

    def request(self, conclusion=None):
        content = common.get_input(conclusion)
        stream = get_stream(content)
        return common.print_stream(stream)
