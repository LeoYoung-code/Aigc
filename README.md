
# 智能对话助手

一个支持多种大语言模型的命令行交互界面，提供丰富的功能和美观的界面。

## 主要特性

- 🌈 **多模型支持**：整合多种大语言模型，一个界面调用所有
- 🚀 **统一接口**：所有模型共享一致的调用方式
- 💫 **自动注册**：通过装饰器自动注册模型
- 📊 **思维导图**：支持将模型输出转换为思维导图
- 🔄 **异步支持**：提供同步和异步两种调用方式
- 🎨 **精美界面**：基于Rich库实现精美的终端界面
- 🏷️ **历史记录**：支持聊天历史记录管理
- 💾 **缓存支持**：支持响应缓存，提高使用效率

## 安装

1. 克隆项目：

```bash
    git clone https://github.com/LeoYoung-code/Aigc.git
    cd Aigc
```

2. 安装依赖：

```bash
    pip install -r requirements.txt
```

3. 安装思维导图生成工具（可选）：

```bash
    npm install -g markmap-cli
```

## 环境变量配置

根据你想使用的模型，设置相应的API密钥环境变量：

- OpenAI: `OPENAI_API_KEY`
- DeepSeek: `DEEP_SEEK_API_KEY`
- Moonshot: `MOONSHOT_API_KEY`
- 阿里云百炼: `DASHSCOPE_API_KEY`
- SiliconFlow: `SILICON_FLOW_API_KEY`
- Google: `GOOGLE_API_KEY`
- Ark: `ARK_API_KEY`
- Mistral: `MISTRAL_API_KEY`

## 使用方法

### 基本用法

```bash
    python main.py <模型代号>
```

例如：

```bash
    python main.py j     # 使用GPT-4o Mini
```

### 生成思维导图

```bash
    python main.py <模型代号> -m
```

### 使用异步模式

```bash
    python main.py <模型代号> -a
```

### 查看帮助信息

```bash
    python main.py -h
```

## 支持的模型

### OpenAI 协议模型

- `j`: GPT-4o Mini大模型

### DeepSeek 系列

- `i`: DeepSeek官方大模型 (deepseek-reasoner)
- `l`: DeepSeek-V3官方大模型 (deepseek-chat)

### 阿里云百炼 系列

- `b`: 阿里云百炼DeepSeek大模型 (deepseek-r1)
- `k`: 阿里云百炼QwqPlus(128K)大模型 (qwq-plus)

### Moonshot 系列

- `e`: Moonshot-V1-32k大模型

### Google 系列

- `g`: Google Gemini模型 (gemini-2.5-pro-exp-03-25)

### SiliconFlow 系列

- `h`: SiliconFlow大模型 (deepseek-ai/DeepSeek-V2.5)

### Ark 系列

- `a`: DeepSeek联网模型
- `c`: 豆包256k模型 (doubao-1-5-pro-256k-250115)
- `d`: 深度求索Ark-R1模型
- `f`: 深度求索Ark-V3模型 (deepseek-v3-250324)

### 其他模型

- `m`: Mistral大模型 (mistral-large-latest)
- `demo`: 演示模型 (无需API密钥)

## 添加新模型

要添加新模型，只需创建一个新的模型类并使用`@register_model`装饰器注册：

```python
from core.model import BaseModel
from core.registry import register_model

@register_model(
    key="x",  # 模型标识符
    display_name="新模型",  # 显示名称
    # 其他配置
)
class NewModel(BaseModel):
    def _initialize(self) -> None:
        # 初始化代码
        pass
        
    def _request_implementation(self, content: str, **kwargs) -> str:
        # 请求实现
        return "响应内容"
```

对于支持OpenAI API协议的模型，可以继承`OpenAICompatibleModel`：

```python
from core.openai_model import OpenAICompatibleModel
from core.registry import register_model

@register_model(
    key="y",
    display_name="OpenAI兼容模型",
    openai_config={
        "model_id": "model-id",
        "base_url": "https://api.example.com",
        "api_key_env": "API_KEY_ENV_NAME",
        "system_message": "系统提示信息",
        "stream": True
    }
)
class OpenAICompatibleModelExample(OpenAICompatibleModel):
    pass  # 不需要额外代码，基类已提供所有实现
```

## 高级设置

在`config.py`中可以自定义以下高级设置：

```python
ADVANCED_SETTINGS = {
    "cache_enabled": True,  # 启用缓存
    "cache_dir": "cache",  # 缓存目录
    "max_history": 20,  # 最大历史记录数
    "timeout": 60,  # 请求超时时间（秒）
    "retry_count": 3,  # 重试次数
    "auto_open_mindmap": True,  # 自动打开思维导图
}
```

## UI配置

支持自定义UI主题和代码高亮风格：

```python
UI_CONFIG = {
    "theme": "dark",  # 主题: dark, light
    "code_theme": "dracula",  # 代码主题: dracula, monokai, github等
    "compact_mode": False,  # 紧凑模式
    "refresh_rate": 4,  # 刷新率
}
```

## 项目结构

```
.
├── core/              # 核心功能模块
│   ├── args.py        # 命令行参数解析
│   ├── model.py       # 模型基类和接口
│   ├── openai_model.py # OpenAI兼容模型基类
│   ├── registry.py    # 模型注册中心
│   └── utils.py       # 核心工具函数
├── models/            # 模型实现
│   ├── demo_model.py  # 演示模型
│   └── openai_models.py # OpenAI系列模型
├── ui/                # 用户界面
│   └── console.py     # 控制台UI
├── utils/             # 工具模块
│   └── markmap.py     # 思维导图生成
├── config.py          # 配置文件
├── main.py            # 程序入口
└── requirements.txt   # 依赖文件
```

## 许可证

本项目采用 MIT 许可证。
