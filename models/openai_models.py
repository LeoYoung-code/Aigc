"""
OpenAI系列模型实现
"""
from core.openai_model import OpenAICompatibleModel
from core.registry import register_model
from config import openai_models_config


@register_model(
    key="j", 
    display_name="GPT-4o Mini大模型",
    openai_config=openai_models_config["gpt-4o-mini"]
)
class GPT4oMini(OpenAICompatibleModel):
    """GPT-4o Mini模型"""
    pass


@register_model(
    key="l", 
    display_name="DeepSeek-V3官方大模型",
    openai_config=openai_models_config["deepseek-chat"]
)
class DeepSeekV3(OpenAICompatibleModel):
    """DeepSeek Chat模型"""
    pass


@register_model(
    key="i", 
    display_name="DeepSeek官方大模型",
    openai_config=openai_models_config["deepseek-reasoner"]
)
class DeepSeekReasoner(OpenAICompatibleModel):
    """DeepSeek Reasoner模型"""
    pass


@register_model(
    key="e", 
    display_name="Moonshot-V1-32k大模型",
    openai_config=openai_models_config["moonshot-v1-32k"]
)
class Moonshot(OpenAICompatibleModel):
    """Moonshot模型"""
    pass


@register_model(
    key="h", 
    display_name="SiliconFlow大模型",
    openai_config=openai_models_config["deepseek-ai/DeepSeek-V2.5"]
)
class SiliconFlow(OpenAICompatibleModel):
    """SiliconFlow模型"""
    pass


@register_model(
    key="k", 
    display_name="阿里云百炼QwqPlus(128K)大模型",
    openai_config=openai_models_config["qwq-plus"]
)
class QwqPlus(OpenAICompatibleModel):
    """阿里云百炼QwqPlus模型"""
    pass


@register_model(
    key="b", 
    display_name="阿里云百炼DeepSeek大模型",
    openai_config=openai_models_config["deepseek-r1"]
)
class BaiLian(OpenAICompatibleModel):
    """阿里云百炼DeepSeek模型"""
    pass 


@register_model(
    key="a", 
    display_name="迪普达达模型",
    openai_config=openai_models_config["ark-dipu"]
)
class ArkDipu(OpenAICompatibleModel):
    """Ark-Dipu模型"""
    pass


@register_model(
    key="d", 
    display_name="深度求索Ark模型",
    openai_config=openai_models_config["ark-deepseek"]
)
class ArkDeepSeek(OpenAICompatibleModel):
    """Ark-DeepSeek模型"""
    pass


@register_model(
    key="c", 
    display_name="豆包256k模型",
    openai_config=openai_models_config["ark-doubao"]
)
class ArkDouBao(OpenAICompatibleModel):
    """Ark-DouBao模型"""
    pass 