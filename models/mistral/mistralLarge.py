import os
from common import common
from mistralai import Mistral
from class_interface import ClassInterface

client = Mistral(api_key= os.getenv("MISTRAL_API_KEY"))

def req(conclusion=None):
    content = common.get_input(conclusion)
    chat_response = client.chat.complete(
        model = "mistral-large-latest", 
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ]
    )
    response = chat_response.choices[0].message.content
    return common.print_conclusion_md(response)
  


class Mistral(ClassInterface):
    def initialize(self):
        print("正在使用MistralLargeLatest大模型")

    def request(self, conclusion=None):
       return req(conclusion)
