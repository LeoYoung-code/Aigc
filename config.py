from typing import Type, Dict
from class_interface import ClassInterface
from models.ark.dipuDada import DipuDada
from models.ark.deepseekModel import DeepSeekArk
from models.ark.doubao256kModel import DouBao256kModel
from models.deepseek.deepseek_code import DeepSeekV3
from models.google.gemini import Gemini
from models.moonShort.moonshot import Moonshot
from models.mistral.mistralLarge import Mistral
from models.openAI.chatGPT import OpenAI
from models.siliconFlow.siliconFlow import SiliconFlow
from models.deepseek.deepseek_think import DeepSeek
from models.dashscope.bailian import BaiLian
from models.dashscope.qwqPlus import QwqPlus

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
    "l": DeepSeekV3,
}


# 定义脑图生成模型
MODEL_GENERATE_MIND = "c"