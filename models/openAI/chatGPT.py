from common import common
from class_interface import ClassInterface
from openai import OpenAI
client = OpenAI()



def get_stream(content):
    return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

def req(conclusion=None):
    try:
        content = common.get_input(conclusion)
        stream = get_stream(content)
        return common.print_stream(stream)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')



class OpenAI(ClassInterface):
    def initialize(self):
        # get_all_model()
        print("正在使用GPT_4o_MINI大模型")

    def request(self, conclusion=None):
       return req(conclusion)