import os
from common import common
from models.baidu.baiduQianfan import BaiduQianfan

def test_baidu_model():
    # 确保环境变量已设置
    if not os.getenv("BAIDU_API_KEY"):
        print("请先设置环境变量 BAIDU_API_KEY")
        return
    
    # 实例化百度文心一言模型
    model = BaiduQianfan()
    model.initialize()
    
    # 测试简单请求
    result = common.call_openai_model(
        "ernie-x1-32k-preview", 
        "你好，请用中文介绍一下自己是什么模型"
    )
    print("\n测试完成")

if __name__ == "__main__":
    test_baidu_model() 