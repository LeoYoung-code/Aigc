import os
from common import common
import google.generativeai as genai
from class_interface import ClassInterface

# 模型初始化
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')


def get_all_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

class Gemini(ClassInterface):
    def initialize(self):
        # get_all_model()
        print("正在使用gemini_2.0_flash大模型")

    def request(self, conclusion=None):
        content = common.get_input(conclusion)
        if not content:
            print("\n" * 3 + "输入为空，请重新输入")
            content = common.get_input(conclusion)
        response = model.generate_content(content, stream=True)
        return  common.markdown_stream(response)
        
