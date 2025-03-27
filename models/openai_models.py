"""
OpenAI系列模型实现
"""
from core.openai_model import OpenAICompatibleModel
from core.registry import register_model
from config import openai_models_config


# 使用配置自动注册装饰器
def model_config_register(model_key: str):
    """根据配置文件自动注册OpenAI兼容模型的装饰器"""
    config = openai_models_config[model_key]
    return register_model(
        key=config["key"],
        display_name=config.get("display_name", f"{model_key}大模型"),
        openai_config=config
    )


@model_config_register("gpt-4o-mini")
class GPT4oMini(OpenAICompatibleModel):
    """GPT-4o Mini模型"""
    pass


@model_config_register("deepseek-chat")
class DeepSeekV3(OpenAICompatibleModel):
    """DeepSeek Chat模型"""
    pass


@model_config_register("deepseek-reasoner")
class DeepSeekReasoner(OpenAICompatibleModel):
    """DeepSeek Reasoner模型"""
    pass


@model_config_register("moonshot-v1-32k")
class Moonshot(OpenAICompatibleModel):
    """Moonshot模型"""
    pass


@model_config_register("deepseek-ai/DeepSeek-V2.5")
class SiliconFlow(OpenAICompatibleModel):
    """SiliconFlow模型"""
    pass


@model_config_register("qwq-plus")
class QwqPlus(OpenAICompatibleModel):
    """阿里云百炼QwqPlus模型"""
    pass


@model_config_register("deepseek-r1")
class BaiLian(OpenAICompatibleModel):
    """阿里云百炼DeepSeek模型"""
    pass 


@model_config_register("ark-dipu")
class ArkDipu(OpenAICompatibleModel):
    """Ark-Dipu模型"""
    pass


@model_config_register("ark-deepseek")
class ArkDeepSeek(OpenAICompatibleModel):
    """Ark-DeepSeek模型"""
    pass


@model_config_register("ark-doubao")
class ArkDouBao(OpenAICompatibleModel):
    """Ark-DouBao模型"""
    pass 