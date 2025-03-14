import os
from common import common
import google.generativeai as genai
from class_interface import ClassInterface

# 模型初始化
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')


def get_all_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

def req(conclusion=None):
    content = common.get_input(conclusion)
    response = model.generate_content(content, stream=True)
    try:
        text = ""
        for chunk in response:
            common.markdown_stream(chunk.text)
            text += chunk.text
        return common.print_conclusion_md(text)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')

class Gemini(ClassInterface):
    def initialize(self):
        # get_all_model()
        print("正在使用GEMINI_1_5_PRO_LATEST大模型")

    def request(self, conclusion=None):
       return req(conclusion)
