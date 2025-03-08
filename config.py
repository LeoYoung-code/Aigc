from typing import Type, Dict
from class_interface import ClassInterface
from ark.dipuDada import DipuDada
from ark.deepseekModel import DeepSeekArk
from ark.doubao256kModel import DouBao256kModel
from google.gemini import Gemini
from moonShort.moonshot import Moonshot
from mistral.mistralLarge import Mistral
from openAI.chatGPT import OpenAI
from siliconFlow.siliconFlow import SiliconFlow
from deepseek.deepseek import DeepSeek
from dashscope.bailian import BaiLian
from dashscope.qwqPlus import QwqPlus

# 定义类映射配置
class_map_config: Dict[str, Type["ClassInterface"]] = {
    "a": DipuDada,
    "b": BaiLian,
    "c": DouBao256kModel,
    "d": DeepSeekArk,
    "e": Moonshot,
    "f": Mistral,
    "j": OpenAI,
    "h": SiliconFlow,
    "g": Gemini,
    "i": DeepSeek,
    "k": QwqPlus,
}


# 定义脑图生成模型
MODEL_GENERATE_MIND = "c"