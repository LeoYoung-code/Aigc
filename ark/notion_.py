from class_interface import ClassInterface
import os
from common import common

# 确保设置了API基础URL
COZE_CN_BASE_URL = "https://api.coze.cn"

# 获取环境变量中的API令牌
coze_api_token = os.getenv("COZE_API_TOKEN")

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType

class CozeModel(ClassInterface):
    def __init__(self):
        self.coze = None
        self.bot_id = "7480850052634738727"  # 需要从Coze网站获取实际的bot ID
        self.user_id = "888"  # 可以使用业务ID或随机字符串
    
    def initialize(self):
        # 初始化Coze客户端
        self.coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)
        print("正在使用Coze API进行对话")
    
    def request(self, conclusion=None):
        try:
            content = common.get_input(conclusion)
            return self.chat_with_bot(content)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
    
    def chat_with_bot(self, content):
        result = ""
        # 使用流式调用与机器人对话
        for event in self.coze.chat.stream(
            bot_id=self.bot_id, 
            user_id=self.user_id, 
            additional_messages=[Message.build_user_question_text(content)]
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                message = event.message
                # 累积结果
                if message.role == "bot" and message.content:
                    result += message.content
                print(f"role={message.role}, content={message.content}")
        
        return result

# 如果直接运行此脚本
if __name__ == "__main__":
    model = CozeModel()
    model.initialize()
    model.request()