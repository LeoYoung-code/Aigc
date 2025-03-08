import param
from common import common
import common.markmap as markmap

def main():
    model_name, is_mind = param.get_params()
    if model_name is None:
        return
    factory = common.ClassFactory()
    try:
        instance = factory.get_class(model_name)
        instance.initialize()
        res = instance.request(None)
        if is_mind and res:
            r = common.create_mindmap(res)
            markmap.markdown_to_markmap(r)
    except KeyboardInterrupt:
        print("\n检测到用户终止操作，Bye😊！")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()