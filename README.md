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

## 安装

1. 克隆项目：

```bash
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant
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

## 使用方法

### 基本用法

```bash
python main.py <模型代号>
```

例如：

```bash
python main.py demo  # 使用演示模型
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

- `demo`: 演示模型 (无需API密钥)
- `b`: 阿里云百炼DeepSeek大模型
- `e`: Moonshot-V1-32k大模型
- `h`: SiliconFlow大模型
- `i`: DeepSeek官方大模型
- `j`: GPT-4o Mini大模型
- `k`: 阿里云百炼QwqPlus(128K)大模型
- `l`: DeepSeek-V3官方大模型

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
